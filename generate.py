"""
generate.py - Générateur de carousel Instagram
Usage: python generate.py --config carousel.yaml --theme dark_purple --output output/
       python generate.py --config carousel.yaml --theme random
"""

import argparse
import os
import sys
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from themes import get_theme


# Filtre Jinja2 pour convertir hex en rgb (pour rgba())
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r},{g},{b}"


def _calculate_text_size(slide: dict) -> dict:
    """
    Calcule automatiquement la taille optimale du texte pour chaque slide.
    S'assure que le contenu tient dans les 936px disponibles (1080 - 2*72 padding).
    """
    body = slide.get("body", "")
    if slide.get("type") == "compare" and "columns" in slide:
        for col in slide["columns"]:
            body += " " + col.get("body", "")

    if not body:
        slide["text_size"] = 42
        slide["is_compact"] = False
        return slide

    # Compter le nombre approximatif de caractères visibles (sans HTML tags)
    import re
    text_only = re.sub(r'<[^>]+>', '', body)
    char_count = len(text_only)

    if slide.get("type") == "compare":
        char_count = int(char_count * 1.5)  # Les colonnes divisent l'espace horizontal

    # Logique de scaling ajustée pour utiliser l'espace
    if char_count < 150:
        text_size = 46  # Très court = occupation maximale
    elif char_count < 300:
        text_size = 40  # Court
    elif char_count < 500:
        text_size = 34  # Normal
    elif char_count < 750:
        text_size = 28  # Moyen
    elif char_count < 1000:
        text_size = 24  # Long
    else:
        text_size = 21  # Très long

    slide["text_size"] = text_size
    slide["is_compact"] = char_count >= 750
    return slide


def _extract_module_title(slides: list, footer: dict) -> str:
    """
    Extrait un titre significatif pour le fichier PDF final.
    Priorité: footer.series > premier slide title > fallback générique.
    """
    import re
    
    # 1. Utiliser footer.series si disponible et significatif
    series = footer.get("series", "").strip()
    if series and series.lower() not in ("series", "my series", "ai series"):
        return _sanitize_filename(series)
    
    # 2. Utiliser le titre de la première slide (cover)
    if slides:
        first_title = slides[0].get("title", "").strip()
        if first_title:
            # Nettoyer le titre des numéros de module "01 / 06 - "
            clean_title = re.sub(r'^\d+\s*/\s*\d+\s*[-–—:]\s*', '', first_title)
            return _sanitize_filename(clean_title)
    
    # 3. Fallback
    return _sanitize_filename("carousel")


def _sanitize_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier pour qu'il soit valide sur tous les OS.
    Supprime les caractères interdits et normalise.
    """
    import re
    # Remplacer les caractères interdits par des underscores
    forbidden = r'[<>:"/\\|?*]'
    clean = re.sub(forbidden, '_', filename)
    # Supprimer les espaces multiples et underscores doubles
    clean = re.sub(r'[\s_]+', '_', clean)
    # Nettoyer les underscores en début/fin
    clean = clean.strip('_')
    # Limiter la longueur à 80 caractères
    if len(clean) > 80:
        clean = clean[:80]
    return clean


def generate_carousel(
    config_path: str, theme_name: str, output_dir: str, format: str = "png"
):
    # Charger la config
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Récupérer le thème
    theme = get_theme(theme_name)
    print(f"🎨 Thème : {theme_name}")
    if theme_name == "random":
        print(f"   Accent1: {theme['accent1']} | Accent2: {theme['accent2']}")

    # Setup Jinja2 - use the script's directory (not config_path) to find templates
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    env.filters["hex_to_rgb"] = hex_to_rgb
    template = env.get_template("slide.html.j2")

    # Créer dossier de sortie
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    slides = config.get("slides", [])
    footer = config.get("footer", {"series": "Series", "author": "author"})

    # Extraire le titre du module pour le nom du PDF
    module_title = _extract_module_title(slides, footer)

    # Générer le HTML de chaque slide
    html_files = []
    for i, slide in enumerate(slides):
        # Calculer la taille du texte en fonction de la longueur du contenu
        slide = _calculate_text_size(slide)
        html = template.render(slide=slide, theme=theme, footer=footer)
        html_path = os.path.join(output_dir, f"slide_{i + 1:02d}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        html_files.append(html_path)

    print(f"📄 {len(html_files)} slides HTML générées")

    # Convertir en images avec Playwright
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "❌ Playwright non installé. Lancez: pip install playwright && playwright install chromium"
        )
        sys.exit(1)

    output_pngs = []
    output_pdfs = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, html_path in enumerate(html_files):
            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.emulate_media(media="screen")
            page.goto(f"file://{os.path.abspath(html_path)}")
            page.wait_for_timeout(800)  # Attendre les fonts Google

            png_path = os.path.join(output_dir, f"slide_{i + 1:02d}.png")
            page.screenshot(path=png_path, full_page=False)

            if format == "png":
                print(f"  ✅ slide_{i + 1:02d}.png")
                output_pngs.append(png_path)
            elif format == "pdf":
                # Transformer le PNG généré en un PDF parfait via Chromium
                pdf_path = os.path.join(output_dir, f"slide_{i + 1:02d}.pdf")
                abs_png_path = os.path.abspath(png_path).replace("\\", "/")
                
                img_html = f'''
                <!DOCTYPE html>
                <html><head><style>
                @page {{ size: 1080px 1080px; margin: 0; }}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ width: 1080px; height: 1080px; overflow: hidden; background: #000; }}
                img {{ width: 1080px; height: 1080px; display: block; }}
                </style></head>
                <body><img src="file:///{abs_png_path}" /></body>
                </html>
                '''
                page.set_content(img_html)
                # Attendre un instant pour s'assurer que l'image locale est chargée
                page.wait_for_timeout(200)
                page.pdf(
                    path=pdf_path,
                    width="1080px",
                    height="1080px",
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
                )
                print(f"  ✅ slide_{i + 1:02d}.pdf")
                output_pdfs.append(pdf_path)
                output_pngs.append(png_path) # Garder une référence pour nettoyage
            
            page.close()

        browser.close()

    if format == "pdf":
        final_pdf_name = f"{module_title}.pdf"
        final_pdf_path = os.path.join(output_dir, final_pdf_name)
        
        # Fusionner avec pypdf
        merge_pdfs(output_pdfs, final_pdf_path)
        
        # Nettoyage
        for f in output_pngs + output_pdfs + html_files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        print(f"📦 PDF parfait généré via fusion : {final_pdf_path}")
        return [final_pdf_path]

    # Mode PNG : nettoyer les html temporaires
    for f in html_files:
        if os.path.exists(f):
            os.remove(f)
            
    print(f"\n🚀 Terminé ! Fichiers dans: {output_dir}")
    return output_pngs


def merge_pdfs(pdf_files: list, output_path: str):
    """Fusionne plusieurs PDFs en un seul carousel."""
    try:
        from pypdf import PdfWriter

        writer = PdfWriter()
        for pdf in pdf_files:
            writer.append(pdf)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"📦 PDF fusionné : {output_path}")
    except ImportError:
        print("⚠️  Pour fusionner les PDFs, installez: pip install pypdf")


def main():
    parser = argparse.ArgumentParser(description="Générateur de carousel Instagram")
    parser.add_argument(
        "--config", default="carousel.yaml", help="Fichier de configuration YAML"
    )
    parser.add_argument(
        "--theme",
        default="dark_purple",
        help="Thème: dark_purple, dark_blue, dark_green, dark_red, dark_orange, random",
    )
    parser.add_argument("--output", default="output", help="Dossier de sortie")
    parser.add_argument(
        "--format", default="png", choices=["png", "pdf"], help="Format de sortie"
    )
    parser.add_argument(
        "--variants",
        type=int,
        default=1,
        help="Nombre de variantes de couleur à générer",
    )
    args = parser.parse_args()

    if args.variants > 1:
        # Générer plusieurs variantes de couleur
        for v in range(args.variants):
            out = os.path.join(args.output, f"variant_{v + 1:02d}")
            theme = "random" if args.theme == "random" else args.theme
            generate_carousel(args.config, "random", out, args.format)
            print(f"--- Variante {v + 1}/{args.variants} ---\n")
    else:
        generate_carousel(args.config, args.theme, args.output, args.format)


if __name__ == "__main__":
    main()
