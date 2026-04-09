"""
themes.py - Gestion des thèmes et palettes de couleurs
15 thèmes prédéfinis premium + générateur aléatoire avancé
"""
import random
import colorsys
import math

THEMES = {
    # ═══════════════════════════════════════════
    # THÈMES AFRO-TECH (Afrofuturisme & Afrique)
    # ═══════════════════════════════════════════
    "kente_tech": {
        "bg":          "#0a0505",
        "bg2":         "#140a0a",
        "blob1":       "#5e1111",
        "blob2":       "#1f4214",
        "accent1":     "#f59e0b",   # gold
        "accent2":     "#dc2626",   # red
        "accent3":     "#16a34a",   # green
        "text":        "#fffbeb",
        "text_muted":  "#f3f4f6",
        "badge_bg":    "#1f0c0c",
        "rule":        "linear-gradient(90deg, #dc2626, #f59e0b, #16a34a)",
        "terminal_bg": "#120505",
        "terminal_border": "rgba(245,158,11,.4)",
    },
    "savanna_gold": {
        "bg":          "#110a05",
        "bg2":         "#1c110a",
        "blob1":       "#632c0c",
        "blob2":       "#78350f",
        "accent1":     "#eab308",   # bright yellow
        "accent2":     "#f97316",   # vibrant orange
        "accent3":     "#ef4444",   # warm red
        "text":        "#fff8f0",
        "text_muted":  "#fed7aa",
        "badge_bg":    "#24140b",
        "rule":        "linear-gradient(90deg, #f97316, #eab308)",
        "terminal_bg": "#170c06",
        "terminal_border": "rgba(234,179,8,.4)",
    },
    "jungle_emerald": {
        "bg":          "#021008",
        "bg2":         "#061b10",
        "blob1":       "#0f3d23",
        "blob2":       "#134e2c",
        "accent1":     "#22c55e",   # neon green
        "accent2":     "#10b981",   # emerald
        "accent3":     "#eab308",   # jungle gold
        "text":        "#ecfdf5",
        "text_muted":  "#a7f3d0",
        "badge_bg":    "#0a2818",
        "rule":        "linear-gradient(90deg, #10b981, #22c55e, #eab308)",
        "terminal_bg": "#04150b",
        "terminal_border": "rgba(34,197,94,.4)",
    },
    "sahara_dune": {
        "bg":          "#110e0c",
        "bg2":         "#1d1612",
        "blob1":       "#8b5a2b",
        "blob2":       "#6b4423",
        "accent1":     "#f59e0b",   # amber/sand
        "accent2":     "#38bdf8",   # oasis blue
        "accent3":     "#d97706",   # deep sand
        "text":        "#fffcf5",
        "text_muted":  "#fde68a",
        "badge_bg":    "#241a14",
        "rule":        "linear-gradient(90deg, #38bdf8, #f59e0b)",
        "terminal_bg": "#14100e",
        "terminal_border": "rgba(245,158,11,.4)",
    },
    "afro_futurism": {
        "bg":          "#050511",
        "bg2":         "#0a0a20",
        "blob1":       "#3730a3",
        "blob2":       "#1e1b4b",
        "accent1":     "#22d3ee",   # cyber cyan
        "accent2":     "#d946ef",   # fuchsia
        "accent3":     "#f59e0b",   # tech gold
        "text":        "#f8fafc",
        "text_muted":  "#cbd5e1",
        "badge_bg":    "#0f0f2e",
        "rule":        "linear-gradient(90deg, #22d3ee, #d946ef, #f59e0b)",
        "terminal_bg": "#070716",
        "terminal_border": "rgba(217,70,239,.4)",
    },
    "terracotta_sunset": {
        "bg":          "#170705",
        "bg2":         "#260e0a",
        "blob1":       "#7c2d12",
        "blob2":       "#431407",
        "accent1":     "#f87171",   # soft red
        "accent2":     "#fb923c",   # vivid orange
        "accent3":     "#eab308",   # sunset yellow
        "text":        "#fff5f5",
        "text_muted":  "#fecaca",
        "badge_bg":    "#33140e",
        "rule":        "linear-gradient(90deg, #f87171, #fb923c)",
        "terminal_bg": "#1f0907",
        "terminal_border": "rgba(248,113,113,.4)",
    }
}

def hsl_to_hex(h, s, l):
    """Convertit HSL (0-1 chacun) en hex."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

def hex_to_rgb(hex_color):
    """Convertit hex en tuple RGB."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c*2 for c in hex_color)
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

def rgb_to_hex(r, g, b):
    """Convertit RGB en hex."""
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def complementary_hue(h):
    """Retourne la teinte complémentaire."""
    return (h + 0.5) % 1.0

def triadic_hues(h):
    """Retourne 3 teintes triadiques."""
    return [h, (h + 0.33) % 1.0, (h + 0.66) % 1.0]

def analogous_hues(h):
    """Retourne 3 teintes analogues."""
    return [(h - 0.08) % 1.0, h, (h + 0.08) % 1.0]

def split_complementary_hues(h):
    """Retourne 3 teintes split-complementary."""
    return [(h + 0.42) % 1.0, h, (h + 0.58) % 1.0]

def generate_palette(base_hue, scheme="complementary"):
    """Génère une palette de couleurs selon un schéma donné."""
    if scheme == "complementary":
        hues = [base_hue, complementary_hue(base_hue), base_hue]
    elif scheme == "triadic":
        hues = triadic_hues(base_hue)
    elif scheme == "analogous":
        hues = analogous_hues(base_hue)
    elif scheme == "split_complementary":
        hues = split_complementary_hues(base_hue)
    else:
        hues = [base_hue, (base_hue + 0.5) % 1.0, (base_hue + 0.33) % 1.0]
    
    return hues

def random_theme():
    """
    Génère un thème dark aléatoire harmonieux et impactant.
    Utilise la théorie des couleurs pour des palettes captivantes.
    """
    # Teinte de base aléatoire
    base_hue = random.random()
    
    # Choix aléatoire du schéma de couleurs
    schemes = ["complementary", "triadic", "analogous", "split_complementary"]
    scheme = random.choice(schemes)
    
    # Générer les teintes
    hues = generate_palette(base_hue, scheme)
    hue1, hue2, hue3 = hues[0], hues[1], hues[2]
    
    # Variation aléatoire de la saturation et luminosité pour plus de diversité
    sat_range = (0.75, 0.95)  # Saturation élevée pour des couleurs vives
    light_range = (0.55, 0.75)  # Luminosité moyenne-haute pour lisibilité
    
    sat1 = random.uniform(*sat_range)
    sat2 = random.uniform(*sat_range) * 0.9
    sat3 = random.uniform(*sat_range) * 0.85
    
    light1 = random.uniform(*light_range)
    light2 = random.uniform(*light_range)
    light3 = random.uniform(*light_range) * 0.95
    
    # Accents principaux
    accent1 = hsl_to_hex(hue1, sat1, light1)
    accent2 = hsl_to_hex(hue2, sat2, light2)
    accent3 = hsl_to_hex(hue3, sat3, light3)
    
    # Arrière-plans sombres profonds
    bg_light = random.uniform(0.04, 0.08)
    bg2_light = random.uniform(0.08, 0.14)
    bg_sat = random.uniform(0.4, 0.7)
    
    bg = hsl_to_hex(hue1, bg_sat * 0.7, bg_light)
    bg2 = hsl_to_hex(hue1, bg_sat, bg2_light)
    
    # Blobs décoratifs
    blob1 = hsl_to_hex(hue1, 0.7, 0.25)
    blob2 = hsl_to_hex(hue2, 0.6, 0.20)
    
    # Texte
    text = "#ffffff"
    text_muted = hsl_to_hex(hue1, 0.15, 0.60 + random.uniform(0, 0.1))
    
    # Éléments UI
    badge_bg = hsl_to_hex(hue1, 0.5, 0.08 + random.uniform(0, 0.04))
    terminal_bg = hsl_to_hex(hue1, 0.5, 0.06 + random.uniform(0, 0.03))
    
    # Bordure terminal avec la couleur accent1
    r, g, b = hex_to_rgb(accent1)
    terminal_border = f"rgba({r},{g},{b},.3)"
    
    # Dégradé avec les 3 accents
    rule = f"linear-gradient(90deg, {accent1}, {accent2}, {accent3})"
    
    return {
        "bg": bg,
        "bg2": bg2,
        "blob1": blob1,
        "blob2": blob2,
        "accent1": accent1,
        "accent2": accent2,
        "accent3": accent3,
        "text": text,
        "text_muted": text_muted,
        "badge_bg": badge_bg,
        "rule": rule,
        "terminal_bg": terminal_bg,
        "terminal_border": terminal_border,
    }

def get_theme(name: str) -> dict:
    """Récupère un thème par son nom ou génère un thème aléatoire."""
    if name == "random":
        return random_theme()
    if name not in THEMES:
        raise ValueError(f"Thème inconnu: {name}. Disponibles: {list(THEMES.keys())} + 'random'")
    return THEMES[name]

def get_theme_preview(name: str) -> str:
    """Retourne un emoji et description pour l'aperçu du thème."""
    previews = {
        "kente_tech": ("🔴", "Kente Tech - Couleurs traditionnelles vibrantes"),
        "savanna_gold": ("🦁", "Or de la Savane - Chaleur et éclat africain"),
        "jungle_emerald": ("🌴", "Émeraude de la Jungle - Luxuriance naturelle"),
        "sahara_dune": ("🐪", "Dunes du Sahara - Sables dorés et oasis"),
        "afro_futurism": ("🛸", "Afrofuturisme - Le futur ancré dans la racine"),
        "terracotta_sunset": ("🌅", "Coucher Terracotta - Argile et soleil vibrant"),
    }
    return previews.get(name, ("🎨", "Thème personnalisé"))