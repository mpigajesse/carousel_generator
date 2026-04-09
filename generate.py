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

    output_files = []
    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, html_path in enumerate(html_files):
            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.goto(f"file://{os.path.abspath(html_path)}")
            page.wait_for_timeout(800)  # Attendre les fonts Google

            if format == "png":
                out_path = os.path.join(output_dir, f"slide_{i + 1:02d}.png")
                page.screenshot(path=out_path, full_page=False)
            elif format == "pdf":
                out_path = os.path.join(output_dir, f"slide_{i + 1:02d}.pdf")
                page.pdf(
                    path=out_path,
                    width="1080px",
                    height="1080px",
                    print_background=True,
                )

            print(f"  ✅ slide_{i + 1:02d}.{format}")
            output_files.append(out_path)
            page.close()

        browser.close()

    # Si PDF : fusionner toutes les slides en un seul fichier
    if format == "pdf":
        merge_pdfs(output_files, os.path.join(output_dir, "carousel_final.pdf"))

    print(f"\n🚀 Terminé ! Fichiers dans: {output_dir}")
    return output_files


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
