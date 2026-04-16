"""
generate.py - Générateur de carousel Instagram
Usage: python generate.py --config carousel.yaml --theme dark_purple --output output/
       python generate.py --config carousel.yaml --theme random
"""

import argparse
import asyncio
import base64
import os
import platform
import re
from pathlib import Path

import yaml
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


def _run_async(coro):
    """Exécute une coroutine asyncio depuis un contexte synchrone (thread-safe).
    Crée un nouvel event loop par appel pour éviter les conflits entre threads."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)


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

    text_only = re.sub(r'<[^>]+>', '', body)
    char_count = len(text_only)

    if slide.get("type") == "compare":
        char_count = int(char_count * 1.5)

    if char_count < 150:
        text_size = 46
    elif char_count < 300:
        text_size = 40
    elif char_count < 500:
        text_size = 34
    elif char_count < 750:
        text_size = 28
    elif char_count < 1000:
        text_size = 24
    else:
        text_size = 21

    slide["text_size"] = text_size
    slide["is_compact"] = char_count >= 750
    return slide


def _prefetch_images_as_base64(html: str) -> str:
    """Télécharge les images externes (<img src="https?://...">) et les remplace
    par des data URLs base64 pour garantir le rendu offline dans Playwright.
    En cas d'échec réseau, conserve l'URL originale (fallback silencieux).
    Ne touche pas aux src qui sont déjà des data: URLs (ex: logo).
    Limite : 5 Mo par image.
    Formats acceptés : tous les types image/* + fallback sur l'extension de l'URL
    pour les CDNs qui servent avec application/octet-stream.
    """
    import urllib.request
    from urllib.parse import urlparse
    from pathlib import PurePosixPath

    MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 Mo

    # Extension → MIME type pour les CDNs à content-type générique
    _EXT_MIME: dict[str, str] = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".gif":  "image/gif",
        ".webp": "image/webp",
        ".avif": "image/avif",
        ".svg":  "image/svg+xml",
        ".bmp":  "image/bmp",
        ".ico":  "image/x-icon",
        ".tiff": "image/tiff",
        ".tif":  "image/tiff",
    }

    def _resolve_mime(content_type: str, url: str) -> str | None:
        """Retourne le MIME type si la réponse est une image, None sinon."""
        if content_type.startswith("image/"):
            return content_type
        # CDNs qui envoient application/octet-stream ou binary/octet-stream :
        # détection par l'extension de l'URL (avant ?query)
        path = PurePosixPath(urlparse(url).path)
        return _EXT_MIME.get(path.suffix.lower())

    def _replace(m: re.Match) -> str:
        full_tag_prefix = m.group(1)   # tout ce qui précède src= dans la balise <img>
        url = m.group(2)
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 carousel-generator/1.0"}
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw_ct = resp.headers.get_content_type() or ""
                mime = _resolve_mime(raw_ct, url)
                if mime is None:
                    return m.group(0)   # Pas une image — garder l'URL
                # Rejeter les images trop volumineuses
                content_length = int(resp.headers.get("Content-Length") or 0)
                if content_length > MAX_IMAGE_BYTES:
                    return m.group(0)
                raw = resp.read(MAX_IMAGE_BYTES + 1)
                if len(raw) > MAX_IMAGE_BYTES:
                    return m.group(0)
            b64 = base64.b64encode(raw).decode("ascii")
            return f'{full_tag_prefix}src="data:{mime};base64,{b64}"'
        except Exception:
            return m.group(0)   # Fallback : garder l'URL originale

    # Regex scopée aux balises <img> uniquement — évite de capturer
    # les src de <script>, <link>, <audio>, <video>, etc.
    return re.sub(r'(<img\b[^>]*?\s)src="(https?://[^"]+)"', _replace, html)


def _extract_module_title(slides: list, footer: dict) -> str:
    """
    Extrait un titre significatif pour le fichier PDF final.
    Priorité: footer.series > premier slide title > fallback générique.
    """
    series = footer.get("series", "").strip()
    if series and series.lower() not in ("series", "my series", "ai series"):
        return _sanitize_filename(series)

    if slides:
        first_title = slides[0].get("title", "").strip()
        if first_title:
            clean_title = re.sub(r'^\d+\s*/\s*\d+\s*[-–—:]\s*', '', first_title)
            return _sanitize_filename(clean_title)

    return _sanitize_filename("carousel")


def _sanitize_filename(filename: str) -> str:
    """Nettoie un nom de fichier pour qu'il soit valide sur tous les OS."""
    clean = re.sub(r'[<>:"/\\|?*]', '', filename)
    clean = re.sub(r'\s+', '_', clean)
    if len(clean) > 80:
        clean = clean[:80]
    clean = clean.strip('_')
    return clean.lower() if clean else "slide"


def _build_slide_filename(index: int, title: str, ext: str) -> str:
    """Construit un nom de fichier professionnel pour une slide.
    Format: 01_titre_nettoye.png (ou .pdf)
    """
    if title:
        clean = re.sub(r'^\d+\s*[-–—:/]\s*', '', title)
        clean = re.sub(r'[<>:"/\\|?*]', '', clean)
        clean = re.sub(r'\s+', '_', clean)
        if len(clean) > 50:
            clean = clean[:50]
            clean = clean[:clean.rfind('_')] if '_' in clean else clean[:50]
        clean = clean.strip('_')
        return f"{index:02d}_{clean}.{ext}"
    return f"{index:02d}.{ext}"


# ─────────────────────────────────────────
#  MOTEUR PLAYWRIGHT PARALLÈLE (async)
# ─────────────────────────────────────────

async def _capture_slides_async(
    html_files, slides, slide_w, slide_h, output_dir, fonts_css_url, progress_cb=None
):
    """Capture toutes les slides en parallèle par batches via Playwright async.

    Stratégie : BATCH_SIZE pages sont ouvertes simultanément, naviguent en
    parallèle et prennent leurs screenshots en même temps.
    Gain typique : ~5x plus rapide qu'une exécution séquentielle.
    """
    from playwright.async_api import async_playwright

    BATCH_SIZE = 5                           # Pages simultanées max (équilibre RAM/vitesse)
    wait_ms = 150 if fonts_css_url else 900  # 150ms fonts locales vs 900ms CDN fallback
    total = len(html_files)

    async def _one(browser, idx):
        page = await browser.new_page(viewport={"width": slide_w, "height": slide_h})
        await page.emulate_media(media="screen")
        abs_path = os.path.abspath(html_files[idx]).replace("\\", "/")
        await page.goto(f"file:///{abs_path}")
        await page.wait_for_timeout(wait_ms)
        slide_title = slides[idx].get("title", "").strip() if idx < len(slides) else ""
        filename = _build_slide_filename(idx + 1, slide_title, "png")
        path = os.path.join(output_dir, filename)
        await page.screenshot(path=path, full_page=False)
        await page.close()
        if progress_cb:
            progress_cb(idx + 1, total)
        return idx, path, slide_title

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        collected = {}

        for batch_start in range(0, total, BATCH_SIZE):
            idxs = range(batch_start, min(batch_start + BATCH_SIZE, total))
            batch = await asyncio.gather(*[_one(browser, i) for i in idxs])
            for idx, path, title in batch:
                collected[idx] = (path, title)

        await browser.close()

    return [(collected[i][0], collected[i][1]) for i in range(total)]


async def _convert_to_pdfs_async(png_results, slide_w, slide_h, output_dir):
    """Convertit tous les PNGs capturés en PDFs en parallèle via Chromium."""
    from playwright.async_api import async_playwright

    BATCH_SIZE = 5

    async def _one_pdf(browser, idx, temp_path, slide_title):
        pdf_filename = _build_slide_filename(idx + 1, slide_title, "pdf")
        pdf_path = os.path.join(output_dir, pdf_filename)
        abs_png = os.path.abspath(temp_path).replace("\\", "/")
        img_html = (
            f"<!DOCTYPE html><html><head><style>"
            f"@page{{size:{slide_w}px {slide_h}px;margin:0}}"
            f"*{{margin:0;padding:0;box-sizing:border-box}}"
            f"body{{width:{slide_w}px;height:{slide_h}px;overflow:hidden}}"
            f"img{{width:100%;height:100%;display:block}}"
            f'</style></head><body><img src="file:///{abs_png}"/></body></html>'
        )
        page = await browser.new_page(viewport={"width": slide_w, "height": slide_h})
        await page.set_content(img_html)
        await page.wait_for_timeout(200)
        await page.pdf(
            path=pdf_path,
            width=f"{slide_w}px",
            height=f"{slide_h}px",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await page.close()
        return idx, pdf_path

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        collected = {}

        for batch_start in range(0, len(png_results), BATCH_SIZE):
            batch_slice = png_results[batch_start:batch_start + BATCH_SIZE]
            tasks = [
                _one_pdf(browser, batch_start + i, path, title)
                for i, (path, title) in enumerate(batch_slice)
            ]
            batch = await asyncio.gather(*tasks)
            for idx, pdf_path in batch:
                collected[idx] = pdf_path

        await browser.close()

    return [collected[i] for i in range(len(png_results))]


# ─────────────────────────────────────────
#  POINT D'ENTRÉE PRINCIPAL
# ─────────────────────────────────────────

def generate_carousel(
    config_path, theme_name: str, output_dir: str, format: str = "png",
    platform: str = "linkedin", config_dict: dict | None = None, progress_cb=None
):
    """Génère un carousel complet.

    Args:
        config_path: chemin vers un fichier YAML (ignoré si config_dict fourni)
        theme_name:  nom du thème ou 'random'
        output_dir:  dossier de sortie
        format:      'png' ou 'pdf'
        platform:    'linkedin' ou 'instagram'
        config_dict: dict de configuration Python direct (évite le fichier YAML)
        progress_cb: callable(current_slide, total_slides) appelé après chaque capture
    """
    # Charger la config (dict direct ou fichier YAML)
    if config_dict is not None:
        config = config_dict
    else:
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

    theme = get_theme(theme_name)
    print(f"Theme : {theme_name} | Platform : {platform}")
    if theme_name == "random":
        print(f"  Accent1: {theme['accent1']} | Accent2: {theme['accent2']}")

    PLATFORM_DIMS = {
        "linkedin":  (1080, 1080),
        "instagram": (1080, 1080),
    }
    slide_w, slide_h = PLATFORM_DIMS.get(platform, (1080, 1080))

    # Setup Jinja2 - use the script's directory (not config_path) to find templates
    template_dir = Path(__file__).parent
    # nosec B701 — autoescape intentionally disabled: templates render to PNG/PDF via
    # Playwright headless (never served to a browser), so XSS via Jinja2 is not applicable.
    env = Environment(loader=FileSystemLoader(str(template_dir)))  # nosec B701
    env.filters["hex_to_rgb"] = hex_to_rgb

    template_name = "slide_instagram.html.j2" if platform == "instagram" else "slide.html.j2"
    template = env.get_template(template_name)

    fonts_css_path = template_dir / "static" / "fonts" / "fonts.css"
    if fonts_css_path.exists():
        fonts_css_url = "file:///" + fonts_css_path.resolve().as_posix()
    else:
        fonts_css_url = None

    logo_path = template_dir / "static" / "logo" / "logo.png"
    if logo_path.exists():
        logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        logo_url = f"data:image/png;base64,{logo_b64}"
    else:
        logo_url = None

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    slides = config.get("slides", [])
    footer = config.get("footer", {"series": "Series", "author": "@Sohaib Baroud"})
    total_slides = len(slides)

    if platform == "linkedin":
        _LI_TYPE_FALLBACK = {"cta": "content", "quote": "content", "stat": "content"}
        slides = [
            {**s, "type": _LI_TYPE_FALLBACK.get(s.get("type", "content"), s.get("type", "content"))}
            for s in slides
        ]

    module_title = _extract_module_title(slides, footer)

    # Génération HTML (rapide — Jinja2 pur Python)
    html_files = []
    for i, slide in enumerate(slides):
        # Valider image_url : accepter uniquement http/https pour éviter
        # l'injection de schemes dangereux dans le DOM Playwright
        if slide.get('image_url'):
            from urllib.parse import urlparse as _urlparse
            _url = slide['image_url'].strip()
            _scheme = _urlparse(_url).scheme.lower()
            # Accepter http/https (URLs externes) et data:image/ (images locales base64)
            _allowed = (
                _scheme in ('http', 'https')
                or (_scheme == 'data' and _url.startswith('data:image/'))
            )
            if not _allowed:
                slide = {**slide, 'image_url': ''}
        slide = _calculate_text_size(slide)
        html = template.render(
            slide=slide, theme=theme, footer=footer,
            fonts_css_url=fonts_css_url,
            logo_url=logo_url,
            slide_index=i + 1, slide_total=total_slides,
        )
        html = _prefetch_images_as_base64(html)   # ← AJOUT : embed images avant capture
        html_path = os.path.join(output_dir, f"_tmp_slide_{i + 1:02d}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        html_files.append(html_path)

    print(f"{len(html_files)} slides HTML prêtes — capture parallèle…")

    # Capture parallèle via Playwright async (5x plus rapide que séquentiel)
    png_results = _run_async(_capture_slides_async(
        html_files, slides, slide_w, slide_h, output_dir, fonts_css_url, progress_cb
    ))
    output_pngs = [r[0] for r in png_results]
    print(f"  ✓ {len(output_pngs)} slides capturées")

    if format == "pdf":
        # Conversion parallèle PNG → PDF puis merge
        output_pdfs = _run_async(_convert_to_pdfs_async(png_results, slide_w, slide_h, output_dir))

        final_pdf_name = f"{module_title}.pdf"
        final_pdf_path = os.path.join(output_dir, final_pdf_name)

        import shutil as _shutil
        if output_pngs:
            _shutil.copy2(output_pngs[0], os.path.join(output_dir, "cover_thumb.png"))

        merge_pdfs(output_pdfs, final_pdf_path)

        for f in output_pngs + output_pdfs + html_files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError as e:
                    print(f"Avertissement : impossible de supprimer {f} : {e}")

        print(f"PDF généré : {final_pdf_path}")
        return [final_pdf_path]

    # Mode PNG : nettoyer les html temporaires
    for f in html_files:
        if os.path.exists(f):
            os.remove(f)

    print(f"\nTerminé ! Fichiers dans: {output_dir}")
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
        print(f"PDF fusionné : {output_path}")
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
        for v in range(args.variants):
            out = os.path.join(args.output, f"variant_{v + 1:02d}")
            generate_carousel(args.config, "random", out, args.format, args.platform)
            print(f"--- Variante {v + 1}/{args.variants} ---\n")
    else:
        generate_carousel(args.config, args.theme, args.output, args.format, args.platform)


if __name__ == "__main__":
    main()
