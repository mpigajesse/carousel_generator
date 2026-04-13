"""
download_fonts.py - Telecharge toutes les fonts en local et genere fonts.css.
Usage: python download_fonts.py

Cree dans static/fonts/:
  clash-display/      -> ClashDisplay-{weight}.woff2 (fichiers complets)
  manrope/            -> Manrope-{hash}.woff2 (subsets latin + latin-ext par weight)
  jetbrains-mono/     -> JetBrainsMono-{hash}.woff2 (subsets latin + latin-ext)
  fonts.css           -> CSS complet avec @font-face et chemins relatifs
"""

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("requests non installe. Lancez: pip install requests")
    sys.exit(1)

FONTS_DIR = Path(__file__).parent / "static" / "fonts"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Sources
SOURCES = {
    "clash-display": {
        "url": "https://api.fontshare.com/v2/css?f[]=clash-display@500,600,700&display=swap",
        "subdir": "clash-display",
    },
    "manrope": {
        "url": "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap",
        "subdir": "manrope",
    },
    "jetbrains-mono": {
        "url": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap",
        "subdir": "jetbrains-mono",
    },
}

# Subsets a conserver (les autres sont ignorees)
# Pour le texte francais/anglais, latin + latin-ext suffisent.
# None = conserver tous les subsets (pour Fontshare qui n'a pas de subset)
KEEP_SUBSETS = {
    "clash-display": None,  # pas de subset splitting -> garder tout
    "manrope": {"latin", "latin-ext"},
    "jetbrains-mono": {"latin", "latin-ext"},
}

# Correspondance unicode-range -> nom de subset
SUBSET_NAMES = [
    ("cyrillic-ext",  r"U\+0460"),
    ("cyrillic",      r"U\+0301.*U\+0400"),
    ("greek-ext",     r"U\+1F00"),
    ("greek",         r"U\+0370"),
    ("vietnamese",    r"U\+0102"),
    ("latin-ext",     r"U\+0100"),
    ("latin",         r"U\+0000"),
]


def identify_subset(unicode_range: str) -> str:
    for name, pattern in SUBSET_NAMES:
        if re.search(pattern, unicode_range):
            return name
    return "other"


def fetch_css(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse_font_faces(css: str) -> list[dict]:
    """
    Parse les blocs @font-face.
    Retourne une liste de dicts avec:
      family, weight, style, display, urls, unicode_range, subset_name
    """
    blocks = re.findall(r"@font-face\s*\{([^}]+)\}", css, re.DOTALL)
    result = []
    for block in blocks:
        family_m = re.search(r"font-family:\s*['\"]?([^'\";\n]+)['\"]?", block)
        weight_m = re.search(r"font-weight:\s*(\d+)", block)
        style_m  = re.search(r"font-style:\s*(\w+)", block)
        display_m = re.search(r"font-display:\s*(\w+)", block)
        range_m  = re.search(r"unicode-range:\s*([^\n;]+)", block)

        # Extraire TOUTES les paires (url, format)
        urls = []
        for url_m in re.finditer(
            r"url\(['\"]?((?:https?:)?//[^'\")\s]+)['\"]?\)\s*format\(['\"]?([^'\")\s]+)['\"]?\)",
            block,
        ):
            raw_url = url_m.group(1)
            fmt     = url_m.group(2)
            if raw_url.startswith("//"):
                raw_url = "https:" + raw_url
            urls.append({"url": raw_url, "format": fmt})

        if not urls:
            continue

        unicode_range = range_m.group(1).strip() if range_m else ""
        subset = identify_subset(unicode_range) if unicode_range else "full"

        result.append({
            "family":        family_m.group(1).strip() if family_m else "Unknown",
            "weight":        int(weight_m.group(1)) if weight_m else 400,
            "style":         style_m.group(1) if style_m else "normal",
            "display":       display_m.group(1) if display_m else "swap",
            "urls":          urls,
            "unicode_range": unicode_range,
            "subset":        subset,
        })
    return result


def pick_best_url(urls: list[dict]) -> dict | None:
    priority = {"woff2": 0, "woff": 1, "truetype": 2, "opentype": 3, "ttf": 4}
    return min(urls, key=lambda u: priority.get(u["format"], 99), default=None)


def ext_for_format(fmt: str) -> str:
    return {"woff2": "woff2", "woff": "woff", "truetype": "ttf", "ttf": "ttf"}.get(fmt, fmt)


def url_to_filename(url: str, fmt: str) -> str:
    name = url.split("?")[0].split("/")[-1]
    ext  = ext_for_format(fmt)
    if not name.endswith(f".{ext}"):
        name = name.split(".")[0] + f".{ext}"
    return name


def download_file(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 100:
        print(f"  OK (cache) {dest.name}")
        return True
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        print(f"  DL {dest.name}  ({len(resp.content)//1024} KB)")
        return True
    except Exception as e:
        print(f"  ERR {dest.name}: {e}")
        return False


def process_family(key: str, config: dict) -> list[str]:
    """
    Telecharge les fonts d'une famille et retourne les blocs CSS locaux.
    """
    print(f"\n[{key}]")
    subdir  = FONTS_DIR / config["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    keep    = KEEP_SUBSETS.get(key)  # None = garder tout

    css     = fetch_css(config["url"])
    faces   = parse_font_faces(css)

    css_blocks = []
    seen_files = set()

    for face in faces:
        subset = face["subset"]
        # Filtrer les subsets non desires
        if keep is not None and subset not in keep:
            continue

        best = pick_best_url(face["urls"])
        if not best:
            continue

        local_name = url_to_filename(best["url"], best["format"])
        dest       = subdir / local_name

        if local_name not in seen_files:
            download_file(best["url"], dest)
            seen_files.add(local_name)

        # Construire le bloc CSS local
        local_rel = f"{config['subdir']}/{local_name}"
        fmt       = best["format"]
        block_lines = [
            "@font-face {",
            f"  font-family: '{face['family']}';",
            f"  font-style: {face['style']};",
            f"  font-weight: {face['weight']};",
            f"  font-display: block;",  # block = attend le chargement complet (pas de FOUT)
            f"  src: url('{local_rel}') format('{fmt}');",
        ]
        if face["unicode_range"]:
            block_lines.append(f"  unicode-range: {face['unicode_range']};")
        block_lines.append("}")
        css_blocks.append("\n".join(block_lines))

    return css_blocks


def main():
    print(f"Cible: {FONTS_DIR}")
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    all_css_blocks = [
        "/* Fonts locales generees par download_fonts.py */",
        "/* Chemin: static/fonts/fonts.css */",
        "",
    ]

    for key, config in SOURCES.items():
        try:
            blocks = process_family(key, config)
            if blocks:
                all_css_blocks.append(f"/* ── {key} ── */")
                all_css_blocks.extend(blocks)
                all_css_blocks.append("")
        except Exception as e:
            print(f"  ERR {key}: {e}")

    # Ecrire fonts.css
    fonts_css = FONTS_DIR / "fonts.css"
    fonts_css.write_text("\n".join(all_css_blocks), encoding="utf-8")
    print(f"\nfonts.css genere: {fonts_css}")
    print(f"Total blocs: {sum(1 for b in all_css_blocks if b.startswith('@font-face'))}")
    print("\nDone!")


if __name__ == "__main__":
    main()
