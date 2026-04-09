"""
themes.py - Gestion des thèmes et palettes de couleurs
"""
import random
import colorsys

THEMES = {
    "dark_purple": {
        "bg":          "#0d1117",
        "bg2":         "#1a0f2e",
        "blob1":       "#4c1d8f",
        "blob2":       "#0f4d6e",
        "accent1":     "#c084fc",   # violet
        "accent2":     "#22d3ee",   # cyan
        "accent3":     "#f472b6",   # rose
        "text":        "#ffffff",
        "text_muted":  "#9ca3af",
        "badge_bg":    "#131325",
        "rule":        "linear-gradient(90deg, #22d3ee, #c084fc)",
        "terminal_bg": "#1e1e2e",
        "terminal_border": "rgba(192,132,252,.3)",
    },
    "dark_blue": {
        "bg":          "#0a0f1e",
        "bg2":         "#0f1f3d",
        "blob1":       "#1e3a8a",
        "blob2":       "#0c4a6e",
        "accent1":     "#60a5fa",
        "accent2":     "#34d399",
        "accent3":     "#fb923c",
        "text":        "#ffffff",
        "text_muted":  "#94a3b8",
        "badge_bg":    "#0f1f3d",
        "rule":        "linear-gradient(90deg, #34d399, #60a5fa)",
        "terminal_bg": "#0f172a",
        "terminal_border": "rgba(96,165,250,.3)",
    },
    "dark_green": {
        "bg":          "#0a0f0a",
        "bg2":         "#0d2010",
        "blob1":       "#14532d",
        "blob2":       "#052e16",
        "accent1":     "#4ade80",
        "accent2":     "#86efac",
        "accent3":     "#fbbf24",
        "text":        "#ffffff",
        "text_muted":  "#86efac",
        "badge_bg":    "#0d1f0e",
        "rule":        "linear-gradient(90deg, #4ade80, #86efac)",
        "terminal_bg": "#052e16",
        "terminal_border": "rgba(74,222,128,.3)",
    },
    "dark_red": {
        "bg":          "#0f0a0a",
        "bg2":         "#2d0f0f",
        "blob1":       "#7f1d1d",
        "blob2":       "#450a0a",
        "accent1":     "#f87171",
        "accent2":     "#fbbf24",
        "accent3":     "#c084fc",
        "text":        "#ffffff",
        "text_muted":  "#fca5a5",
        "badge_bg":    "#1f0d0d",
        "rule":        "linear-gradient(90deg, #f87171, #fbbf24)",
        "terminal_bg": "#1c0505",
        "terminal_border": "rgba(248,113,113,.3)",
    },
    "dark_orange": {
        "bg":          "#0f0c08",
        "bg2":         "#2d1a08",
        "blob1":       "#78350f",
        "blob2":       "#431407",
        "accent1":     "#fb923c",
        "accent2":     "#fbbf24",
        "accent3":     "#34d399",
        "text":        "#ffffff",
        "text_muted":  "#fdba74",
        "badge_bg":    "#1f1008",
        "rule":        "linear-gradient(90deg, #fb923c, #fbbf24)",
        "terminal_bg": "#1c1008",
        "terminal_border": "rgba(251,146,60,.3)",
    },
}

def hsl_to_hex(h, s, l):
    """Convertit HSL (0-1 chacun) en hex."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

def random_theme():
    """Génère un thème dark aléatoire harmonieux."""
    hue = random.random()
    hue2 = (hue + 0.55 + random.uniform(-0.05, 0.05)) % 1.0
    hue3 = (hue + 0.33 + random.uniform(-0.05, 0.05)) % 1.0

    bg_base = hsl_to_hex(hue, 0.5, 0.07)
    bg2     = hsl_to_hex(hue, 0.6, 0.12)
    blob1   = hsl_to_hex(hue, 0.7, 0.25)
    blob2   = hsl_to_hex(hue2, 0.6, 0.20)

    accent1 = hsl_to_hex(hue, 0.85, 0.68)
    accent2 = hsl_to_hex(hue2, 0.80, 0.60)
    accent3 = hsl_to_hex(hue3, 0.80, 0.65)

    text_muted = hsl_to_hex(hue, 0.20, 0.62)
    badge_bg   = hsl_to_hex(hue, 0.55, 0.10)
    term_bg    = hsl_to_hex(hue, 0.60, 0.08)

    r, g, b = tuple(int(hsl_to_hex(hue, 0.85, 0.68)[i:i+2], 16) for i in (1,3,5))
    term_border = f"rgba({r},{g},{b},.3)"

    return {
        "bg": bg_base,
        "bg2": bg2,
        "blob1": blob1,
        "blob2": blob2,
        "accent1": accent1,
        "accent2": accent2,
        "accent3": accent3,
        "text": "#ffffff",
        "text_muted": text_muted,
        "badge_bg": badge_bg,
        "rule": f"linear-gradient(90deg, {accent2}, {accent1})",
        "terminal_bg": term_bg,
        "terminal_border": term_border,
    }

def get_theme(name: str) -> dict:
    if name == "random":
        return random_theme()
    if name not in THEMES:
        raise ValueError(f"Thème inconnu: {name}. Disponibles: {list(THEMES.keys())} + 'random'")
    return THEMES[name]
