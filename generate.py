"""
generate.py - Générateur de carousel Instagram
Usage: python generate.py --config carousel.yaml --theme dark_purple --output output/
       python generate.py --config carousel.yaml --theme random
"""

import argparse
import os
import re
import sys
import yaml
import asyncio
import platform
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from themes import get_theme

# Fix Windows asyncio event loop for Playwright
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


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
    # Remplacer les caractères interdits
    clean = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remplacer les espaces multiples par un seul underscore
    clean = re.sub(r'\s+', '_', clean)
    # Tronquer si trop long (max 80 caracteres pour le nom)
    if len(clean) > 80:
        clean = clean[:80]
    # Supprimer les underscores en début/fin
    clean = clean.strip('_')
    return clean.lower() if clean else "slide"


def _build_slide_filename(index: int, title: str, ext: str) -> str:
    """
    Construit un nom de fichier professionnel pour une slide.
    Format: 01_-_titre_nettoye.png (ou .pdf)
    """
    if title:
        # Nettoyer le titre : enlever les numéros, symboles, etc.
        clean = re.sub(r'^\d+\s*[-–—:/]\s*', '', title)  # Enlever "01 - ", "1:", etc.
        clean = re.sub(r'[<>:"/\\|?*]', '', clean)  # Caracteres interdits
        clean = re.sub(r'\s+', '_', clean)  # Espaces -> underscores
        # Tronquer a 50 caracteres
        if len(clean) > 50:
            clean = clean[:50]
            # Couper au dernier mot complet
            clean = clean[:clean.rfind('_')] if '_' in clean else clean[:50]
        clean = clean.strip('_')
        return f"{index:02d}_{clean}.{ext}"
    return f"{index:02d}.{ext}"


def generate_carousel(
    config_path: str, theme_name: str, output_dir: str, format: str = "png",
    platform: str = "linkedin"
):
    # Charger la config
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Récupérer le thème
    theme = get_theme(theme_name)
    print(f"Theme : {theme_name} | Platform : {platform}")
    if theme_name == "random":
        print(f"  Accent1: {theme['accent1']} | Accent2: {theme['accent2']}")

    # Dimensions selon la plateforme
    # LinkedIn : 1080x1080 (1:1), Instagram : 1080x1350 (4:5 portrait)
    PLATFORM_DIMS = {
        "linkedin":  (1080, 1080),
        "instagram": (1080, 1080),
    }
    slide_w, slide_h = PLATFORM_DIMS.get(platform, (1080, 1080))

    # Setup Jinja2 - use the script's directory (not config_path) to find templates
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    env.filters["hex_to_rgb"] = hex_to_rgb

    template_name = "slide_instagram.html.j2" if platform == "instagram" else "slide.html.j2"
    template = env.get_template(template_name)

    # Résoudre le chemin absolu vers fonts.css local (pour Playwright file://)
    fonts_css_path = template_dir / "static" / "fonts" / "fonts.css"
    if fonts_css_path.exists():
        # Playwright file:// needs forward slashes even on Windows
        fonts_css_url = "file:///" + fonts_css_path.resolve().as_posix()
    else:
        # Fallback CDN si fonts.css absent (lancer download_fonts.py pour corriger)
        fonts_css_url = None

    # Créer dossier de sortie
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    slides = config.get("slides", [])
    footer = config.get("footer", {"series": "Series", "author": "@Sohaib Baroud"})
    total_slides = len(slides)

    # Pour LinkedIn : convertir les types Instagram-only en types compatibles
    # (cta → content, quote → content, stat → content)
    if platform == "linkedin":
        _LI_TYPE_FALLBACK = {"cta": "content", "quote": "content", "stat": "content"}
        slides = [
            {**s, "type": _LI_TYPE_FALLBACK.get(s.get("type", "content"), s.get("type", "content"))}
            for s in slides
        ]

    # Extraire le titre du module pour le nom du PDF
    module_title = _extract_module_title(slides, footer)

    # Générer le HTML de chaque slide
    html_files = []
    png_files_info = []  # (num, title, path)
    for i, slide in enumerate(slides):
        # Calculer la taille du texte en fonction de la longueur du contenu
        slide = _calculate_text_size(slide)
        html = template.render(
            slide=slide, theme=theme, footer=footer,
            fonts_css_url=fonts_css_url,
            slide_index=i + 1, slide_total=total_slides,
        )
        html_path = os.path.join(output_dir, f"_tmp_slide_{i + 1:02d}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        html_files.append(html_path)

    print(f"{len(html_files)} slides HTML generees")

    # Convertir en images avec Playwright
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright non installe. Lancez: pip install playwright && playwright install chromium"
        )
        sys.exit(1)

    output_pngs = []
    output_pdfs = []

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, html_path in enumerate(html_files):
            page = browser.new_page(viewport={"width": slide_w, "height": slide_h})
            page.emulate_media(media="screen")
            page.goto(f"file://{os.path.abspath(html_path)}")
            # Fonts locales = pas de requête réseau. 400ms suffisent pour le rendu JS.
            # Si fonts CDN (fallback), augmenter à 1500ms.
            wait_ms = 400 if fonts_css_url else 1500
            page.wait_for_timeout(wait_ms)

            # Nom de fichier professionnel basé sur le titre de la slide
            slide_title = slides[i].get("title", "").strip() if i < len(slides) else ""
            # Toujours utiliser .png pour le screenshot initial (Playwright ne supporte que les images)
            temp_filename = _build_slide_filename(i + 1, slide_title, "png")
            temp_path = os.path.join(output_dir, temp_filename)
            page.screenshot(path=temp_path, full_page=False)

            if format == "png":
                print(f"  {temp_filename}")
                output_pngs.append(temp_path)
            elif format == "pdf":
                # Transformer le PNG généré en un PDF parfait via Chromium
                pdf_filename = _build_slide_filename(i + 1, slide_title, "pdf")
                pdf_path = os.path.join(output_dir, pdf_filename)
                abs_png_path = os.path.abspath(temp_path).replace("\\", "/")

                img_html = f'''
                <!DOCTYPE html>
                <html><head><style>
                @page {{ size: {slide_w}px {slide_h}px; margin: 0; }}
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ width: {slide_w}px; height: {slide_h}px; overflow: hidden; background: #000; }}
                img {{ width: {slide_w}px; height: {slide_h}px; display: block; }}
                </style></head>
                <body><img src="file:///{abs_png_path}" /></body>
                </html>
                '''
                page.set_content(img_html)
                # Attendre un instant pour s'assurer que l'image locale est chargée
                page.wait_for_timeout(200)
                page.pdf(
                    path=pdf_path,
                    width=f"{slide_w}px",
                    height=f"{slide_h}px",
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
                )
                print(f"  {pdf_filename}")
                output_pdfs.append(pdf_path)
                output_pngs.append(temp_path) # Garder une reference pour nettoyage
            
            page.close()

        browser.close()

    if format == "pdf":
        final_pdf_name = f"{module_title}.pdf"
        final_pdf_path = os.path.join(output_dir, final_pdf_name)

        # Sauvegarder le 1er PNG comme miniature de bibliothèque avant nettoyage
        import shutil as _shutil
        if output_pngs:
            thumb_dst = os.path.join(output_dir, "cover_thumb.png")
            _shutil.copy2(output_pngs[0], thumb_dst)

        # Fusionner avec pypdf
        merge_pdfs(output_pdfs, final_pdf_path)

        # Nettoyage des intermédiaires (cover_thumb.png conservé)
        for f in output_pngs + output_pdfs + html_files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        print(f"PDF parfait genere via fusion : {final_pdf_path}")
        return [final_pdf_path]

    # Mode PNG : nettoyer les html temporaires
    for f in html_files:
        if os.path.exists(f):
            os.remove(f)

    print(f"\nTermine ! Fichiers dans: {output_dir}")
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
        print(f"PDF fusionne : {output_path}")
    except ImportError:
        print("Pour fusionner les PDFs, installez: pip install pypdf")


def main():
    parser = argparse.ArgumentParser(description="Générateur de carousel Instagram / LinkedIn")
    parser.add_argument(
        "--config", default="carousel.yaml", help="Fichier de configuration YAML"
    )
    parser.add_argument(
        "--theme",
        default="dark_purple",
        help="Thème: dark_purple, ig_aurora_dark, ig_sunset_vibes, ig_minimal_white, ... random",
    )
    parser.add_argument("--output", default="output", help="Dossier de sortie")
    parser.add_argument(
        "--format", default="png", choices=["png", "pdf"], help="Format de sortie"
    )
    parser.add_argument(
        "--platform",
        default="linkedin",
        choices=["linkedin", "instagram"],
        help="Plateforme cible: linkedin (1080x1080) ou instagram (1080x1350)",
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
            generate_carousel(args.config, "random", out, args.format, args.platform)
            print(f"--- Variante {v + 1}/{args.variants} ---\n")
    else:
        generate_carousel(args.config, args.theme, args.output, args.format, args.platform)


if __name__ == "__main__":
    main()
