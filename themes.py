"""
themes.py - Gestion des thèmes et palettes de couleurs
15 thèmes prédéfinis premium + générateur aléatoire avancé
"""
import random
import colorsys
import math

THEMES = {
    # ═══════════════════════════════════════════
    # THÈMES CLASSIQUES
    # ═══════════════════════════════════════════
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
    # ═══════════════════════════════════════════
    # THÈMES PREMIUM
    # ═══════════════════════════════════════════
    "midnight_ocean": {
        "bg":          "#020617",
        "bg2":         "#0c1929",
        "blob1":       "#082f49",
        "blob2":       "#0c4a6e",
        "accent1":     "#38bdf8",   # sky blue
        "accent2":     "#2dd4bf",   # teal
        "accent3":     "#818cf8",   # indigo
        "text":        "#f0f9ff",
        "text_muted":  "#94a3b8",
        "badge_bg":    "#0c1929",
        "rule":        "linear-gradient(90deg, #38bdf8, #2dd4bf, #818cf8)",
        "terminal_bg": "#081421",
        "terminal_border": "rgba(56,189,248,.3)",
    },
    "sunset_glow": {
        "bg":          "#1c0a0a",
        "bg2":         "#2d1215",
        "blob1":       "#7f1d1d",
        "blob2":       "#92400e",
        "accent1":     "#fb7185",   # rose
        "accent2":     "#f59e0b",   # amber
        "accent3":     "#c084fc",   # violet
        "text":        "#fff1f2",
        "text_muted":  "#fda4af",
        "badge_bg":    "#2d1215",
        "rule":        "linear-gradient(90deg, #fb7185, #f59e0b)",
        "terminal_bg": "#1f0f12",
        "terminal_border": "rgba(251,113,133,.3)",
    },
    "neon_tokyo": {
        "bg":          "#0a0a0f",
        "bg2":         "#13131f",
        "blob1":       "#7c3aed",
        "blob2":       "#db2777",
        "accent1":     "#a78bfa",   # light purple
        "accent2":     "#f0abfc",   # pink
        "accent3":     "#22d3ee",   # cyan
        "text":        "#faf5ff",
        "text_muted":  "#c4b5fd",
        "badge_bg":    "#13131f",
        "rule":        "linear-gradient(90deg, #a78bfa, #f0abfc, #22d3ee)",
        "terminal_bg": "#0f0f17",
        "terminal_border": "rgba(167,139,250,.3)",
    },
    "emerald_city": {
        "bg":          "#052e16",
        "bg2":         "#064e3b",
        "blob1":       "#047857",
        "blob2":       "#065f46",
        "accent1":     "#34d399",   # emerald
        "accent2":     "#6ee7b7",   # light green
        "accent3":     "#fbbf24",   # amber
        "text":        "#ecfdf5",
        "text_muted":  "#6ee7b7",
        "badge_bg":    "#064e3b",
        "rule":        "linear-gradient(90deg, #34d399, #6ee7b7)",
        "terminal_bg": "#042f2e",
        "terminal_border": "rgba(52,211,153,.3)",
    },
    "cyber_punk": {
        "bg":          "#0a0a14",
        "bg2":         "#14142a",
        "blob1":       "#2563eb",
        "blob2":       "#dc2626",
        "accent1":     "#60a5fa",   # blue
        "accent2":     "#f472b6",   # pink
        "accent3":     "#facc15",   # yellow
        "text":        "#f8fafc",
        "text_muted":  "#93c5fd",
        "badge_bg":    "#14142a",
        "rule":        "linear-gradient(90deg, #60a5fa, #f472b6)",
        "terminal_bg": "#0f172a",
        "terminal_border": "rgba(96,165,250,.3)",
    },
    "arctic_frost": {
        "bg":          "#0c1222",
        "bg2":         "#162032",
        "blob1":       "#1e40af",
        "blob2":       "#0891b2",
        "accent1":     "#93c5fd",   # light blue
        "accent2":     "#67e8f9",   # cyan
        "accent3":     "#e0e7ff",   # lavender
        "text":        "#f0f9ff",
        "text_muted":  "#93c5fd",
        "badge_bg":    "#162032",
        "rule":        "linear-gradient(90deg, #93c5fd, #67e8f9)",
        "terminal_bg": "#0f172a",
        "terminal_border": "rgba(147,197,253,.3)",
    },
    "golden_aura": {
        "bg":          "#1c1308",
        "bg2":         "#291d0c",
        "blob1":       "#92400e",
        "blob2":       "#78350f",
        "accent1":     "#fbbf24",   # amber
        "accent2":     "#f59e0b",   # gold
        "accent3":     "#fb923c",   # orange
        "text":        "#fffbeb",
        "text_muted":  "#fcd34d",
        "badge_bg":    "#291d0c",
        "rule":        "linear-gradient(90deg, #fbbf24, #f59e0b)",
        "terminal_bg": "#1f150a",
        "terminal_border": "rgba(251,191,36,.3)",
    },
    "lavender_dream": {
        "bg":          "#130a1f",
        "bg2":         "#1e1133",
        "blob1":       "#6d28d9",
        "blob2":       "#7c3aed",
        "accent1":     "#c4b5fd",   # lavender
        "accent2":     "#a78bfa",   # purple
        "accent3":     "#f0abfc",   # pink
        "text":        "#faf5ff",
        "text_muted":  "#c4b5fd",
        "badge_bg":    "#1e1133",
        "rule":        "linear-gradient(90deg, #c4b5fd, #a78bfa)",
        "terminal_bg": "#160d26",
        "terminal_border": "rgba(196,181,253,.3)",
    },
    "forest_night": {
        "bg":          "#05140e",
        "bg2":         "#0a2e1d",
        "blob1":       "#065f46",
        "blob2":       "#047857",
        "accent1":     "#6ee7b7",   # mint
        "accent2":     "#34d399",   # emerald
        "accent3":     "#a7f3d0",   # light green
        "text":        "#ecfdf5",
        "text_muted":  "#6ee7b7",
        "badge_bg":    "#0a2e1d",
        "rule":        "linear-gradient(90deg, #6ee7b7, #34d399)",
        "terminal_bg": "#052e16",
        "terminal_border": "rgba(110,231,183,.3)",
    },
    "crimson_tide": {
        "bg":          "#1a0505",
        "bg2":         "#2d0a0a",
        "blob1":       "#991b1b",
        "blob2":       "#b91c1c",
        "accent1":     "#f87171",   # red
        "accent2":     "#fca5a5",   # light red
        "accent3":     "#fbbf24",   # amber
        "text":        "#fef2f2",
        "text_muted":  "#fca5a5",
        "badge_bg":    "#2d0a0a",
        "rule":        "linear-gradient(90deg, #f87171, #fca5a5)",
        "terminal_bg": "#1f0505",
        "terminal_border": "rgba(248,113,113,.3)",
    },
    "cosmic_void": {
        "bg":          "#0a0a14",
        "bg2":         "#111128",
        "blob1":       "#4338ca",
        "blob2":       "#6366f1",
        "accent1":     "#818cf8",   # indigo
        "accent2":     "#c084fc",   # purple
        "accent3":     "#22d3ee",   # cyan
        "text":        "#eef2ff",
        "text_muted":  "#a5b4fc",
        "badge_bg":    "#111128",
        "rule":        "linear-gradient(90deg, #818cf8, #c084fc, #22d3ee)",
        "terminal_bg": "#0f0f1f",
        "terminal_border": "rgba(129,140,248,.3)",
    },
    "tropical_breeze": {
        "bg":          "#042f2e",
        "bg2":         "#064e3b",
        "blob1":       "#0891b2",
        "blob2":       "#0d9488",
        "accent1":     "#22d3ee",   # cyan
        "accent2":     "#2dd4bf",   # teal
        "accent3":     "#fbbf24",   # amber
        "text":        "#f0fdfa",
        "text_muted":  "#5eead4",
        "badge_bg":    "#064e3b",
        "rule":        "linear-gradient(90deg, #22d3ee, #2dd4bf)",
        "terminal_bg": "#042f2e",
        "terminal_border": "rgba(34,211,238,.3)",
    },
    "volcanic_fire": {
        "bg":          "#1a0a00",
        "bg2":         "#2d1200",
        "blob1":       "#b91c1c",
        "blob2":       "#ea580c",
        "accent1":     "#fb923c",   # orange
        "accent2":     "#fbbf24",   # yellow
        "accent3":     "#f87171",   # red
        "text":        "#fff7ed",
        "text_muted":  "#fdba74",
        "badge_bg":    "#2d1200",
        "rule":        "linear-gradient(90deg, #fb923c, #fbbf24)",
        "terminal_bg": "#1f0f00",
        "terminal_border": "rgba(251,146,60,.3)",
    },
    "aurora_borealis": {
        "bg":          "#0a1628",
        "bg2":         "#0f2744",
        "blob1":       "#0891b2",
        "blob2":       "#7c3aed",
        "accent1":     "#34d399",   # green
        "accent2":     "#22d3ee",   # cyan
        "accent3":     "#a78bfa",   # purple
        "text":        "#f0f9ff",
        "text_muted":  "#7dd3fc",
        "badge_bg":    "#0f2744",
        "rule":        "linear-gradient(90deg, #34d399, #22d3ee, #a78bfa)",
        "terminal_bg": "#0c1a30",
        "terminal_border": "rgba(52,211,153,.3)",
    },
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
        "dark_purple": ("💜", "Violet/Cyan - Classique élégant"),
        "dark_blue": ("💙", "Bleu/Vert - Calme professionnel"),
        "dark_green": ("💚", "Vert/Or - Nature et fraîcheur"),
        "dark_red": ("❤️", "Rouge/Or - Passion et énergie"),
        "dark_orange": ("🧡", "Orange/Or - Chaleur et dynamisme"),
        "midnight_ocean": ("🌊", "Bleu océan - Profondeur marine"),
        "sunset_glow": ("🌅", "Coucher de soleil - Chaleur dorée"),
        "neon_tokyo": ("🌃", "Néon cyberpunk - Futuriste vibrant"),
        "emerald_city": ("💎", "Émeraude - Luxe et sophistication"),
        "cyber_punk": ("⚡", "Cyberpunk - Énergie électrique"),
        "arctic_frost": ("❄️", "Glace arctique - Fraîcheur cristalline"),
        "golden_aura": ("✨", "Aura dorée - Prestige et lumière"),
        "lavender_dream": ("💜", "Rêve lavande - Douceur onirique"),
        "forest_night": ("🌲", "Forêt nocturne - Mystère naturel"),
        "crimson_tide": ("🩸", "Marée cramoisie - Intensité dramatique"),
        "cosmic_void": ("🌌", "Vide cosmique - Espace infini"),
        "tropical_breeze": ("🌴", "Brise tropicale - Exotisme apaisant"),
        "volcanic_fire": ("🌋", "Feu volcanique - Puissance brute"),
        "aurora_borealis": ("🌈", "Aurore boréale - Magie céleste"),
    }
    return previews.get(name, ("🎨", "Thème personnalisé"))