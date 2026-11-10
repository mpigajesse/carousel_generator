"""
themes.py - Gestion des thèmes et palettes de couleurs
15 thèmes prédéfinis premium + générateur aléatoire avancé
"""
import colorsys
import random

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
    # ═══════════════════════════════════════════
    # THÈME PERSONNALISÉ
    # ═══════════════════════════════════════════
    "kente_tech": {
        "bg":          "#0a0a0a",
        "bg2":         "#141414",
        "blob1":       "#1a5c00",
        "blob2":       "#8b0000",
        "accent1":     "#f5c518",   # gold (Kente jaune)
        "accent2":     "#22c55e",   # vert (Kente vert)
        "accent3":     "#ef4444",   # rouge (Kente rouge)
        "text":        "#ffffff",
        "text_muted":  "#a3a3a3",
        "badge_bg":    "#141414",
        "rule":        "linear-gradient(90deg, #f5c518, #22c55e, #ef4444)",
        "terminal_bg": "#0f0f0f",
        "terminal_border": "rgba(245,197,24,.3)",
    },
    # ═══════════════════════════════════════════
    # NEUTRES — Palettes sobres pour communications formelles,
    # partenariats, annonces corporate, éditorial premium.
    # Aucune couleur vive : que des gris colorés, ivoires, bruns chauds.
    # ═══════════════════════════════════════════
    "neutral_charcoal": {
        # Charbon premium — fond très sombre, accents gris-doré subtils
        "bg":          "#0F0F10",
        "bg2":         "#1A1A1C",
        "blob1":       "#26262A",
        "blob2":       "#2E2E33",
        "accent1":     "#C9B89A",   # gris-doré chaud (pas or vif)
        "accent2":     "#9E9486",   # taupe clair
        "accent3":     "#7A7368",   # taupe moyen
        "text":        "#F5F2EC",
        "text_muted":  "#A8A39A",
        "badge_bg":    "#1A1A1C",
        "rule":        "linear-gradient(90deg, #C9B89A, #7A7368)",
        "terminal_bg": "#0F0F10",
        "terminal_border": "rgba(201,184,154,.25)",
    },
    "neutral_stone": {
        # Pierre/sable — fond très clair, accents bruns chauds
        "bg":          "#F4EFE7",
        "bg2":         "#EBE4D6",
        "blob1":       "#D9CFBC",
        "blob2":       "#C4B89F",
        "accent1":     "#5C4A36",   # brun terre
        "accent2":     "#8A6F4E",   # ocre brun
        "accent3":     "#3A2F22",   # brun très foncé
        "text":        "#2A2520",
        "text_muted":  "#6B5F4F",
        "badge_bg":    "#E5DCC8",
        "rule":        "linear-gradient(90deg, #5C4A36, #8A6F4E)",
        "terminal_bg": "#EBE4D6",
        "terminal_border": "rgba(92,74,54,.25)",
    },
    "neutral_paper": {
        # Papier ivoire — éditorial premium, lecture longue
        "bg":          "#FAF7F0",
        "bg2":         "#F2EDE0",
        "blob1":       "#E8E0CD",
        "blob2":       "#D8CEB7",
        "accent1":     "#1F1E1B",   # encre noire
        "accent2":     "#6B5F4F",   # gris-brun
        "accent3":     "#A09483",   # gris chaud clair
        "text":        "#1F1E1B",
        "text_muted":  "#6B5F4F",
        "badge_bg":    "#EFE9D9",
        "rule":        "linear-gradient(90deg, #1F1E1B, #6B5F4F)",
        "terminal_bg": "#F2EDE0",
        "terminal_border": "rgba(31,30,27,.20)",
    },
    "neutral_slate": {
        # Ardoise bleu-gris — corporate sobre, B2B sérieux
        "bg":          "#0E1216",
        "bg2":         "#181D23",
        "blob1":       "#222A33",
        "blob2":       "#2C3640",
        "accent1":     "#A8B2BD",   # gris bleuté clair
        "accent2":     "#7B8590",   # gris bleuté moyen
        "accent3":     "#5A636E",   # gris bleuté foncé
        "text":        "#E8EAEC",
        "text_muted":  "#9BA1A8",
        "badge_bg":    "#181D23",
        "rule":        "linear-gradient(90deg, #A8B2BD, #5A636E)",
        "terminal_bg": "#0E1216",
        "terminal_border": "rgba(168,178,189,.25)",
    },
    "neutral_warm": {
        # Beige chaud — magazine luxe, communication mode/lifestyle
        "bg":          "#1A1614",
        "bg2":         "#241E1A",
        "blob1":       "#2E2722",
        "blob2":       "#3A312A",
        "accent1":     "#D4B896",   # beige doré chaud
        "accent2":     "#A89074",   # beige moyen
        "accent3":     "#7A6650",   # beige foncé
        "text":        "#F5EFE5",
        "text_muted":  "#B8A993",
        "badge_bg":    "#241E1A",
        "rule":        "linear-gradient(90deg, #D4B896, #7A6650)",
        "terminal_bg": "#1A1614",
        "terminal_border": "rgba(212,184,150,.25)",
    },
    "neutral_mono": {
        # Monochrome pur — noir + blanc + gris uniquement, journalistique
        "bg":          "#FFFFFF",
        "bg2":         "#F5F5F5",
        "blob1":       "#E8E8E8",
        "blob2":       "#D4D4D4",
        "accent1":     "#000000",
        "accent2":     "#404040",
        "accent3":     "#7A7A7A",
        "text":        "#000000",
        "text_muted":  "#5C5C5C",
        "badge_bg":    "#EEEEEE",
        "rule":        "linear-gradient(90deg, #000000, #7A7A7A)",
        "terminal_bg": "#F5F5F5",
        "terminal_border": "rgba(0,0,0,.18)",
    },
    "neutral_linen": {
        # Lin chaud — texture papier de luxe, contraste AAA (15:1)
        "bg":          "#F8F4ED",
        "bg2":         "#EFE8DA",
        "blob1":       "#E0D6C2",
        "blob2":       "#CCBFA5",
        "accent1":     "#1C1A16",   # noir-brun -> ratio 15.4:1 sur bg
        "accent2":     "#5C4534",   # brun chaud -> 9.1:1
        "accent3":     "#8A7560",   # taupe sable -> 5.0:1
        "text":        "#1C1A16",
        "text_muted":  "#5C4534",
        "badge_bg":    "#EBE3D2",
        "rule":        "linear-gradient(90deg, #1C1A16, #5C4534)",
        "terminal_bg": "#EFE8DA",
        "terminal_border": "rgba(28,26,22,.20)",
    },
    "neutral_carbon": {
        # Carbone profond — accent cuivré bronze, contraste AAA (17:1)
        "bg":          "#0C0C0E",
        "bg2":         "#16161A",
        "blob1":       "#22232A",
        "blob2":       "#2C2D34",
        "accent1":     "#B89968",   # cuivre bronze -> 7.4:1 sur bg
        "accent2":     "#8E7858",   # bronze foncé -> 4.6:1
        "accent3":     "#D4C19B",   # cuivre clair -> 10.8:1
        "text":        "#F0EDE6",
        "text_muted":  "#B0A998",
        "badge_bg":    "#16161A",
        "rule":        "linear-gradient(90deg, #B89968, #D4C19B)",
        "terminal_bg": "#0C0C0E",
        "terminal_border": "rgba(184,153,104,.28)",
    },
    "neutral_fog": {
        # Brouillard gris-bleu froid — minimaliste tech, contraste AAA (15:1)
        "bg":          "#EEF1F4",
        "bg2":         "#E2E7ED",
        "blob1":       "#D0D7E0",
        "blob2":       "#B8C2CD",
        "accent1":     "#1A1F26",   # anthracite bleuté -> 15.1:1 sur bg
        "accent2":     "#4A5560",   # gris bleu moyen -> 7.6:1
        "accent3":     "#7A8693",   # gris bleu clair -> 4.5:1
        "text":        "#1A1F26",
        "text_muted":  "#4A5560",
        "badge_bg":    "#E2E7ED",
        "rule":        "linear-gradient(90deg, #1A1F26, #4A5560)",
        "terminal_bg": "#E2E7ED",
        "terminal_border": "rgba(26,31,38,.20)",
    },
    "neutral_clay": {
        # Argile/terracotta désaturée — chaleur sourde, contraste AAA (13:1)
        "bg":          "#F0E6DC",
        "bg2":         "#E5D7C8",
        "blob1":       "#D2BFA8",
        "blob2":       "#B89E84",
        "accent1":     "#2D241D",   # brun très foncé -> 13.0:1 sur bg
        "accent2":     "#8B5A3C",   # terracotta sourde -> 5.2:1
        "accent3":     "#5C4233",   # brun moyen -> 8.6:1
        "text":        "#2D241D",
        "text_muted":  "#5C4233",
        "badge_bg":    "#E5D7C8",
        "rule":        "linear-gradient(90deg, #2D241D, #8B5A3C)",
        "terminal_bg": "#E5D7C8",
        "terminal_border": "rgba(45,36,29,.22)",
    },
    "neutral_obsidian": {
        # Obsidienne noir-vert — minéral profond, contraste AAA (17:1)
        "bg":          "#0A0E0C",
        "bg2":         "#131816",
        "blob1":       "#1F2622",
        "blob2":       "#2A332E",
        "accent1":     "#8FA888",   # vert sauge clair -> 8.2:1 sur bg
        "accent2":     "#6B8466",   # vert sauge moyen -> 5.0:1
        "accent3":     "#B5C9AE",   # vert sauge très clair -> 12.0:1
        "text":        "#E8E6DD",
        "text_muted":  "#A8B0A2",
        "badge_bg":    "#131816",
        "rule":        "linear-gradient(90deg, #8FA888, #B5C9AE)",
        "terminal_bg": "#0A0E0C",
        "terminal_border": "rgba(143,168,136,.28)",
    },

    # ═══════════════════════════════════════════
    # ACT BRAND — Charte officielle Africa Centred Technology
    # Ratio 60/30/10 : Dark dominante / Green secondaire / Orange + Gold accent
    # ═══════════════════════════════════════════
    "act_brand": {
        "bg":          "#0A1410",   # ACT Dark
        "bg2":         "#070E1C",   # ACT Dark Deep
        "blob1":       "#1B3022",   # ACT Green
        "blob2":       "#2C4A35",   # ACT Green Mid
        "accent1":     "#D35400",   # ACT Orange primaire
        "accent2":     "#F39C12",   # ACT Gold
        "accent3":     "#FF6B00",   # ACT Orange Hot
        "text":        "#FCF9F2",   # ACT Cream
        "text_muted":  "#D5CFBE",   # ACT Line
        "badge_bg":    "#1B3022",   # ACT Green
        "rule":        "linear-gradient(90deg, #D35400, #F39C12)",
        "terminal_bg": "#070E1C",
        "terminal_border": "rgba(211,84,0,.3)",
    },
}

IG_THEMES = {
    # ═══════════════════════════════════════════
    # INSTAGRAM-OPTIMIZED THEMES
    # ═══════════════════════════════════════════

    # 1. Dark purple/blue/pink gradient — viral aesthetic
    "ig_aurora_dark": {
        "bg":               "#0d0520",
        "bg2":              "#1a0a38",
        "bg_gradient":      "linear-gradient(145deg, #0d0520 0%, #1a0a38 40%, #0a1a40 100%)",
        "blob1":            "#3b1060",
        "blob2":            "#0a2060",
        "accent1":          "#c084fc",
        "accent2":          "#f472b6",
        "accent3":          "#38bdf8",
        "text":             "#ffffff",
        "text_muted":       "#c4b5fd",
        "badge_bg":         "#200a40",
        "rule":             "linear-gradient(90deg, #c084fc, #f472b6)",
        "terminal_bg":      "#0d0520",
        "terminal_border":  "rgba(192,132,252,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # 2. Warm coral/orange/pink gradient — lifestyle/wellness
    "ig_sunset_vibes": {
        "bg":               "#1a0a0a",
        "bg2":              "#2d0a1a",
        "bg_gradient":      "linear-gradient(145deg, #2d0a1a 0%, #3d1a00 50%, #1a0a14 100%)",
        "blob1":            "#5c1a10",
        "blob2":            "#3d1500",
        "accent1":          "#fb7185",
        "accent2":          "#f97316",
        "accent3":          "#fbbf24",
        "text":             "#fff7f0",
        "text_muted":       "#fda4af",
        "badge_bg":         "#3d0a14",
        "rule":             "linear-gradient(90deg, #fb7185, #f97316)",
        "terminal_bg":      "#1a0a0a",
        "terminal_border":  "rgba(251,113,133,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # 3. Clean white/light — pro minimal aesthetic
    "ig_minimal_white": {
        "bg":               "#ffffff",
        "bg2":              "#f5f5f5",
        "bg_gradient":      None,
        "blob1":            "#e0e0f0",
        "blob2":            "#f0e0e8",
        "accent1":          "#1a1a2e",
        "accent2":          "#6366f1",
        "accent3":          "#f43f5e",
        "text":             "#0f0f1a",
        "text_muted":       "#6b7280",
        "badge_bg":         "#ebebeb",
        "rule":             "linear-gradient(90deg, #1a1a2e, #6366f1)",
        "terminal_bg":      "#f8f8f8",
        "terminal_border":  "rgba(26,26,46,.3)",
        "surface":          "rgba(0,0,0,0.06)",
        "surface2":         "rgba(0,0,0,0.10)",
        "is_light":         True,
    },

    # 4. Warm cream/beige — luxury/fashion aesthetic
    "ig_cream_luxury": {
        "bg":               "#faf6f0",
        "bg2":              "#f5ede0",
        "bg_gradient":      "linear-gradient(145deg, #faf6f0 0%, #f5ede0 100%)",
        "blob1":            "#e8d8c0",
        "blob2":            "#dcc8b0",
        "accent1":          "#1c1410",
        "accent2":          "#b5873e",
        "accent3":          "#8b6355",
        "text":             "#1c1410",
        "text_muted":       "#6b5c4e",
        "badge_bg":         "#ede5d8",
        "rule":             "linear-gradient(90deg, #1c1410, #b5873e)",
        "terminal_bg":      "#f0ebe2",
        "terminal_border":  "rgba(28,20,16,.3)",
        "surface":          "rgba(0,0,0,0.06)",
        "surface2":         "rgba(0,0,0,0.10)",
        "is_light":         True,
    },

    # 5. Electric neon on deep black — Gen-Z aesthetic
    "ig_neon_pulse": {
        "bg":               "#050505",
        "bg2":              "#0d0014",
        "bg_gradient":      "linear-gradient(145deg, #050505 0%, #0d0014 50%, #000d14 100%)",
        "blob1":            "#003320",
        "blob2":            "#001a33",
        "accent1":          "#00ff88",
        "accent2":          "#ff0080",
        "accent3":          "#0088ff",
        "text":             "#ffffff",
        "text_muted":       "#88ffcc",
        "badge_bg":         "#0a0014",
        "rule":             "linear-gradient(90deg, #00ff88, #ff0080)",
        "terminal_bg":      "#050505",
        "terminal_border":  "rgba(0,255,136,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # 6. Deep ocean teal/blue — calm/premium
    "ig_ocean_deep": {
        "bg":               "#041520",
        "bg2":              "#062030",
        "bg_gradient":      "linear-gradient(145deg, #041520 0%, #062030 50%, #041830 100%)",
        "blob1":            "#073a50",
        "blob2":            "#053248",
        "accent1":          "#22d3ee",
        "accent2":          "#2dd4bf",
        "accent3":          "#818cf8",
        "text":             "#f0fdff",
        "text_muted":       "#7dd3fc",
        "badge_bg":         "#062838",
        "rule":             "linear-gradient(90deg, #22d3ee, #2dd4bf)",
        "terminal_bg":      "#041520",
        "terminal_border":  "rgba(34,211,238,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # 7. Bold rose/pink — beauty/fashion
    "ig_rose_pop": {
        "bg":               "#1a0510",
        "bg2":              "#2d0a1e",
        "bg_gradient":      "linear-gradient(145deg, #1a0510 0%, #2d0a1e 60%, #1a0520 100%)",
        "blob1":            "#500a28",
        "blob2":            "#3d0a30",
        "accent1":          "#f9a8d4",
        "accent2":          "#fb7185",
        "accent3":          "#fbbf24",
        "text":             "#fff0f5",
        "text_muted":       "#fda4af",
        "badge_bg":         "#350820",
        "rule":             "linear-gradient(90deg, #f9a8d4, #fb7185)",
        "terminal_bg":      "#1a0510",
        "terminal_border":  "rgba(249,168,212,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # 8. Earthy green/terracotta — wellness/nature
    "ig_sage_earth": {
        "bg":               "#f7f4ef",
        "bg2":              "#ede8df",
        "bg_gradient":      "linear-gradient(145deg, #f7f4ef 0%, #ede8df 100%)",
        "blob1":            "#d8e8d0",
        "blob2":            "#e8d4c0",
        "accent1":          "#4a7c59",
        "accent2":          "#c2714f",
        "accent3":          "#8b9d6a",
        "text":             "#2c2420",
        "text_muted":       "#6b6055",
        "badge_bg":         "#e5e0d8",
        "rule":             "linear-gradient(90deg, #4a7c59, #c2714f)",
        "terminal_bg":      "#f0ede8",
        "terminal_border":  "rgba(74,124,89,.3)",
        "surface":          "rgba(0,0,0,0.06)",
        "surface2":         "rgba(0,0,0,0.10)",
        "is_light":         True,
    },

    # 9. Black with gold accents — luxury brand aesthetic
    "ig_midnight_gold": {
        "bg":               "#080604",
        "bg2":              "#100d05",
        "bg_gradient":      "linear-gradient(145deg, #080604 0%, #100d05 50%, #08060a 100%)",
        "blob1":            "#241a02",
        "blob2":            "#180e04",
        "accent1":          "#d4a843",
        "accent2":          "#c9a227",
        "accent3":          "#e8c87a",
        "text":             "#fefce8",
        "text_muted":       "#d4a843",
        "badge_bg":         "#120e04",
        "rule":             "linear-gradient(90deg, #d4a843, #c9a227)",
        "terminal_bg":      "#080604",
        "terminal_border":  "rgba(212,168,67,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # 10. Bright coral/tangerine — energetic/youth
    "ig_coral_burst": {
        "bg":               "#0f0a06",
        "bg2":              "#1e0e08",
        "bg_gradient":      "linear-gradient(145deg, #0f0a06 0%, #1e0e08 60%, #0a0f0a 100%)",
        "blob1":            "#3d1a08",
        "blob2":            "#1a1a08",
        "accent1":          "#ff6b35",
        "accent2":          "#ffd700",
        "accent3":          "#ff3366",
        "text":             "#fff8f0",
        "text_muted":       "#ffaa80",
        "badge_bg":         "#200e06",
        "rule":             "linear-gradient(90deg, #ff6b35, #ffd700)",
        "terminal_bg":      "#0f0a06",
        "terminal_border":  "rgba(255,107,53,.3)",
        "surface":          "rgba(255,255,255,0.06)",
        "surface2":         "rgba(255,255,255,0.10)",
        "is_light":         False,
    },

    # ═══════════════════════════════════════════
    # NEUTRES (IG) — Palettes sobres format 1080×1350
    # Communications formelles, partenariats, éditorial premium.
    # ═══════════════════════════════════════════
    "ig_neutral_charcoal": {
        # Charbon premium IG
        "bg":               "#0F0F10",
        "bg2":              "#1A1A1C",
        "bg_gradient":      "linear-gradient(145deg, #0F0F10 0%, #1A1A1C 55%, #26262A 100%)",
        "blob1":            "#26262A",
        "blob2":            "#2E2E33",
        "accent1":          "#C9B89A",
        "accent2":          "#9E9486",
        "accent3":          "#7A7368",
        "text":             "#F5F2EC",
        "text_muted":       "#A8A39A",
        "badge_bg":         "#1A1A1C",
        "rule":             "linear-gradient(90deg, #C9B89A, #7A7368)",
        "terminal_bg":      "#0F0F10",
        "terminal_border":  "rgba(201,184,154,.25)",
        "surface":          "rgba(245,242,236,0.06)",
        "surface2":         "rgba(245,242,236,0.10)",
        "is_light":         False,
    },
    "ig_neutral_paper": {
        # Papier ivoire IG — éditorial light
        "bg":               "#FAF7F0",
        "bg2":              "#F2EDE0",
        "bg_gradient":      "linear-gradient(145deg, #FAF7F0 0%, #F2EDE0 60%, #E8E0CD 100%)",
        "blob1":            "#E8E0CD",
        "blob2":            "#D8CEB7",
        "accent1":          "#1F1E1B",
        "accent2":          "#6B5F4F",
        "accent3":          "#A09483",
        "text":             "#1F1E1B",
        "text_muted":       "#6B5F4F",
        "badge_bg":         "#EFE9D9",
        "rule":             "linear-gradient(90deg, #1F1E1B, #6B5F4F)",
        "terminal_bg":      "#F2EDE0",
        "terminal_border":  "rgba(31,30,27,.20)",
        "surface":          "rgba(31,30,27,0.04)",
        "surface2":         "rgba(31,30,27,0.08)",
        "is_light":         True,
    },
    "ig_neutral_stone": {
        # Pierre/sable IG — light minimaliste
        "bg":               "#F4EFE7",
        "bg2":              "#EBE4D6",
        "bg_gradient":      "linear-gradient(145deg, #F4EFE7 0%, #EBE4D6 60%, #D9CFBC 100%)",
        "blob1":            "#D9CFBC",
        "blob2":            "#C4B89F",
        "accent1":          "#5C4A36",
        "accent2":          "#8A6F4E",
        "accent3":          "#3A2F22",
        "text":             "#2A2520",
        "text_muted":       "#6B5F4F",
        "badge_bg":         "#E5DCC8",
        "rule":             "linear-gradient(90deg, #5C4A36, #8A6F4E)",
        "terminal_bg":      "#EBE4D6",
        "terminal_border":  "rgba(92,74,54,.25)",
        "surface":          "rgba(42,37,32,0.04)",
        "surface2":         "rgba(42,37,32,0.08)",
        "is_light":         True,
    },
    "ig_neutral_slate": {
        # Ardoise bleu-gris IG — corporate dark
        "bg":               "#0E1216",
        "bg2":              "#181D23",
        "bg_gradient":      "linear-gradient(145deg, #0E1216 0%, #181D23 55%, #222A33 100%)",
        "blob1":            "#222A33",
        "blob2":            "#2C3640",
        "accent1":          "#A8B2BD",
        "accent2":          "#7B8590",
        "accent3":          "#5A636E",
        "text":             "#E8EAEC",
        "text_muted":       "#9BA1A8",
        "badge_bg":         "#181D23",
        "rule":             "linear-gradient(90deg, #A8B2BD, #5A636E)",
        "terminal_bg":      "#0E1216",
        "terminal_border":  "rgba(168,178,189,.25)",
        "surface":          "rgba(232,234,236,0.06)",
        "surface2":         "rgba(232,234,236,0.10)",
        "is_light":         False,
    },
    "ig_neutral_warm": {
        # Beige chaud IG — magazine lifestyle
        "bg":               "#1A1614",
        "bg2":              "#241E1A",
        "bg_gradient":      "linear-gradient(145deg, #1A1614 0%, #241E1A 55%, #2E2722 100%)",
        "blob1":            "#2E2722",
        "blob2":            "#3A312A",
        "accent1":          "#D4B896",
        "accent2":          "#A89074",
        "accent3":          "#7A6650",
        "text":             "#F5EFE5",
        "text_muted":       "#B8A993",
        "badge_bg":         "#241E1A",
        "rule":             "linear-gradient(90deg, #D4B896, #7A6650)",
        "terminal_bg":      "#1A1614",
        "terminal_border":  "rgba(212,184,150,.25)",
        "surface":          "rgba(245,239,229,0.06)",
        "surface2":         "rgba(245,239,229,0.10)",
        "is_light":         False,
    },
    "ig_neutral_mono": {
        # Monochrome pur IG — noir/blanc/gris journalistique
        "bg":               "#FFFFFF",
        "bg2":              "#F5F5F5",
        "bg_gradient":      "linear-gradient(145deg, #FFFFFF 0%, #F5F5F5 60%, #E8E8E8 100%)",
        "blob1":            "#E8E8E8",
        "blob2":            "#D4D4D4",
        "accent1":          "#000000",
        "accent2":          "#404040",
        "accent3":          "#7A7A7A",
        "text":             "#000000",
        "text_muted":       "#5C5C5C",
        "badge_bg":         "#EEEEEE",
        "rule":             "linear-gradient(90deg, #000000, #7A7A7A)",
        "terminal_bg":      "#F5F5F5",
        "terminal_border":  "rgba(0,0,0,.18)",
        "surface":          "rgba(0,0,0,0.04)",
        "surface2":         "rgba(0,0,0,0.08)",
        "is_light":         True,
    },
    "ig_neutral_linen": {
        # Lin chaud IG — papier de luxe, contraste AAA
        "bg":               "#F8F4ED",
        "bg2":              "#EFE8DA",
        "bg_gradient":      "linear-gradient(145deg, #F8F4ED 0%, #EFE8DA 60%, #E0D6C2 100%)",
        "blob1":            "#E0D6C2",
        "blob2":            "#CCBFA5",
        "accent1":          "#1C1A16",
        "accent2":          "#5C4534",
        "accent3":          "#8A7560",
        "text":             "#1C1A16",
        "text_muted":       "#5C4534",
        "badge_bg":         "#EBE3D2",
        "rule":             "linear-gradient(90deg, #1C1A16, #5C4534)",
        "terminal_bg":      "#EFE8DA",
        "terminal_border":  "rgba(28,26,22,.20)",
        "surface":          "rgba(28,26,22,0.04)",
        "surface2":         "rgba(28,26,22,0.08)",
        "is_light":         True,
    },
    "ig_neutral_carbon": {
        # Carbone profond IG — accent cuivré bronze
        "bg":               "#0C0C0E",
        "bg2":              "#16161A",
        "bg_gradient":      "linear-gradient(145deg, #0C0C0E 0%, #16161A 55%, #22232A 100%)",
        "blob1":            "#22232A",
        "blob2":            "#2C2D34",
        "accent1":          "#B89968",
        "accent2":          "#8E7858",
        "accent3":          "#D4C19B",
        "text":             "#F0EDE6",
        "text_muted":       "#B0A998",
        "badge_bg":         "#16161A",
        "rule":             "linear-gradient(90deg, #B89968, #D4C19B)",
        "terminal_bg":      "#0C0C0E",
        "terminal_border":  "rgba(184,153,104,.28)",
        "surface":          "rgba(240,237,230,0.06)",
        "surface2":         "rgba(240,237,230,0.10)",
        "is_light":         False,
    },
    "ig_neutral_fog": {
        # Brouillard gris-bleu IG — minimaliste tech
        "bg":               "#EEF1F4",
        "bg2":              "#E2E7ED",
        "bg_gradient":      "linear-gradient(145deg, #EEF1F4 0%, #E2E7ED 60%, #D0D7E0 100%)",
        "blob1":            "#D0D7E0",
        "blob2":            "#B8C2CD",
        "accent1":          "#1A1F26",
        "accent2":          "#4A5560",
        "accent3":          "#7A8693",
        "text":             "#1A1F26",
        "text_muted":       "#4A5560",
        "badge_bg":         "#E2E7ED",
        "rule":             "linear-gradient(90deg, #1A1F26, #4A5560)",
        "terminal_bg":      "#E2E7ED",
        "terminal_border":  "rgba(26,31,38,.20)",
        "surface":          "rgba(26,31,38,0.04)",
        "surface2":         "rgba(26,31,38,0.08)",
        "is_light":         True,
    },
    "ig_neutral_clay": {
        # Argile/terracotta désaturée IG
        "bg":               "#F0E6DC",
        "bg2":              "#E5D7C8",
        "bg_gradient":      "linear-gradient(145deg, #F0E6DC 0%, #E5D7C8 60%, #D2BFA8 100%)",
        "blob1":            "#D2BFA8",
        "blob2":            "#B89E84",
        "accent1":          "#2D241D",
        "accent2":          "#8B5A3C",
        "accent3":          "#5C4233",
        "text":             "#2D241D",
        "text_muted":       "#5C4233",
        "badge_bg":         "#E5D7C8",
        "rule":             "linear-gradient(90deg, #2D241D, #8B5A3C)",
        "terminal_bg":      "#E5D7C8",
        "terminal_border":  "rgba(45,36,29,.22)",
        "surface":          "rgba(45,36,29,0.04)",
        "surface2":         "rgba(45,36,29,0.08)",
        "is_light":         True,
    },
    "ig_neutral_obsidian": {
        # Obsidienne noir-vert IG — minéral profond
        "bg":               "#0A0E0C",
        "bg2":              "#131816",
        "bg_gradient":      "linear-gradient(145deg, #0A0E0C 0%, #131816 55%, #1F2622 100%)",
        "blob1":            "#1F2622",
        "blob2":            "#2A332E",
        "accent1":          "#8FA888",
        "accent2":          "#6B8466",
        "accent3":          "#B5C9AE",
        "text":             "#E8E6DD",
        "text_muted":       "#A8B0A2",
        "badge_bg":         "#131816",
        "rule":             "linear-gradient(90deg, #8FA888, #B5C9AE)",
        "terminal_bg":      "#0A0E0C",
        "terminal_border":  "rgba(143,168,136,.28)",
        "surface":          "rgba(232,230,221,0.06)",
        "surface2":         "rgba(232,230,221,0.10)",
        "is_light":         False,
    },

    # ═══════════════════════════════════════════
    # ACT BRAND (IG) — Charte officielle Africa Centred Technology
    # Format Instagram 1080×1350 — Dark dominante, Orange ACT accent
    # ═══════════════════════════════════════════
    "ig_act_brand": {
        "bg":               "#0A1410",   # ACT Dark
        "bg2":              "#070E1C",   # ACT Dark Deep
        "bg_gradient":      "linear-gradient(145deg, #0A1410 0%, #1B3022 55%, #070E1C 100%)",
        "blob1":            "#1B3022",   # ACT Green
        "blob2":            "#2C4A35",   # ACT Green Mid
        "accent1":          "#D35400",   # ACT Orange primaire
        "accent2":          "#F39C12",   # ACT Gold
        "accent3":          "#FF6B00",   # ACT Orange Hot
        "text":             "#FCF9F2",   # ACT Cream
        "text_muted":       "#D5CFBE",   # ACT Line
        "badge_bg":         "#1B3022",
        "rule":             "linear-gradient(90deg, #D35400, #F39C12)",
        "terminal_bg":      "#070E1C",
        "terminal_border":  "rgba(211,84,0,.3)",
        "surface":          "rgba(252,249,242,0.06)",
        "surface2":         "rgba(252,249,242,0.10)",
        "is_light":         False,
    },
}


def hsl_to_hex(h, s, lightness):
    """Convertit HSL (0-1 chacun) en hex."""
    r, g, b = colorsys.hls_to_rgb(h, lightness, s)
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
    """Récupère un thème par son nom ou génère un thème aléatoire.

    Checks IG_THEMES first when the name starts with 'ig_', then falls back
    to THEMES.  Returns a random theme when name is 'random'.
    """
    if name == "random":
        return random_theme()
    if name.startswith("ig_"):
        if name in IG_THEMES:
            return IG_THEMES[name]
        raise ValueError(
            f"Thème Instagram inconnu: {name}. "
            f"Disponibles: {list(IG_THEMES.keys())}"
        )
    if name not in THEMES:
        all_names = list(THEMES.keys()) + list(IG_THEMES.keys())
        raise ValueError(
            f"Thème inconnu: {name}. Disponibles: {all_names} + 'random'"
        )
    return THEMES[name]


def get_ig_theme(name: str) -> dict:
    """Récupère un thème Instagram par son nom.

    Looks in IG_THEMES first, then falls back to THEMES.
    """
    if name in IG_THEMES:
        return IG_THEMES[name]
    if name in THEMES:
        return THEMES[name]
    all_names = list(IG_THEMES.keys()) + list(THEMES.keys())
    raise ValueError(
        f"Thème inconnu: {name}. Disponibles: {all_names}"
    )

def get_theme_preview(name: str) -> str:
    """Retourne la description du thème."""
    previews = {
        # Standard themes
        "dark_purple": "Violet/Cyan - Classique elegant",
        "dark_blue": "Bleu/Vert - Calme professionnel",
        "dark_green": "Vert/Or - Nature et fraicheur",
        "dark_red": "Rouge/Or - Passion et energie",
        "dark_orange": "Orange/Or - Chaleur et dynamisme",
        "midnight_ocean": "Bleu ocean - Profondeur marine",
        "sunset_glow": "Coucher de soleil - Chaleur doree",
        "neon_tokyo": "Neon cyberpunk - Futuriste vibrant",
        "emerald_city": "Emeraude - Luxe et sophistication",
        "cyber_punk": "Cyberpunk - Energie electrique",
        "arctic_frost": "Glace arctique - Fraicheur cristalline",
        "golden_aura": "Aura doree - Prestige et lumiere",
        "lavender_dream": "Reve lavande - Douceur onirique",
        "forest_night": "Foret nocturne - Mystere naturel",
        "crimson_tide": "Maree cramoisie - Intensite dramatique",
        "cosmic_void": "Vide cosmique - Espace infini",
        "tropical_breeze": "Brise tropicale - Exotisme apaisant",
        "volcanic_fire": "Feu volcanique - Puissance brute",
        "aurora_borealis": "Aurore boreale - Magie celeste",
        "kente_tech": "Kente Tech - Heritage africain vibrant",
        # Neutres
        "neutral_charcoal": "Neutral Charcoal - Charbon premium gris-dore (dark)",
        "neutral_stone": "Neutral Stone - Pierre/sable bruns chauds (light)",
        "neutral_paper": "Neutral Paper - Ivoire editorial premium (light)",
        "neutral_slate": "Neutral Slate - Ardoise bleu-gris corporate (dark)",
        "neutral_warm": "Neutral Warm - Beige chaud magazine luxe (dark)",
        "neutral_mono": "Neutral Mono - Monochrome noir/blanc journalistique (light)",
        "neutral_linen": "Neutral Linen - Lin chaud papier de luxe AAA (light)",
        "neutral_carbon": "Neutral Carbon - Carbone bronze cuivre AAA (dark)",
        "neutral_fog": "Neutral Fog - Brouillard gris-bleu tech AAA (light)",
        "neutral_clay": "Neutral Clay - Argile/terracotta sourde AAA (light)",
        "neutral_obsidian": "Neutral Obsidian - Obsidienne sauge minerale AAA (dark)",
        "act_brand": "ACT Brand - Charte officielle Africa Centred Technology",
        # Instagram-optimized themes
        "ig_aurora_dark": "IG Aurora Dark - Violet/Bleu/Rose viral (dark)",
        "ig_sunset_vibes": "IG Sunset Vibes - Corail/Orange/Rose lifestyle (dark)",
        "ig_minimal_white": "IG Minimal White - Blanc epure professionnel (light)",
        "ig_cream_luxury": "IG Cream Luxury - Creme/Beige luxe et mode (light)",
        "ig_neon_pulse": "IG Neon Pulse - Neon electrique Gen-Z (dark)",
        "ig_ocean_deep": "IG Ocean Deep - Bleu/Sarcelle ocean premium (dark)",
        "ig_rose_pop": "IG Rose Pop - Rose/Fuchsia beaute et mode (dark)",
        "ig_sage_earth": "IG Sage Earth - Vert sauge/Terre nature bien-etre (light)",
        "ig_midnight_gold": "IG Midnight Gold - Noir/Or luxe de marque (dark)",
        "ig_coral_burst": "IG Coral Burst - Corail/Tangerine energie jeunesse (dark)",
        # Neutres IG
        "ig_neutral_charcoal": "IG Neutral Charcoal - Charbon premium IG (dark)",
        "ig_neutral_paper": "IG Neutral Paper - Ivoire editorial IG (light)",
        "ig_neutral_stone": "IG Neutral Stone - Pierre minimaliste IG (light)",
        "ig_neutral_slate": "IG Neutral Slate - Ardoise corporate IG (dark)",
        "ig_neutral_warm": "IG Neutral Warm - Beige chaud lifestyle IG (dark)",
        "ig_neutral_mono": "IG Neutral Mono - Monochrome journalistique IG (light)",
        "ig_neutral_linen": "IG Neutral Linen - Lin chaud IG AAA (light)",
        "ig_neutral_carbon": "IG Neutral Carbon - Carbone bronze IG AAA (dark)",
        "ig_neutral_fog": "IG Neutral Fog - Brouillard tech IG AAA (light)",
        "ig_neutral_clay": "IG Neutral Clay - Argile sourde IG AAA (light)",
        "ig_neutral_obsidian": "IG Neutral Obsidian - Obsidienne sauge IG AAA (dark)",
        "ig_act_brand": "IG ACT Brand - Charte officielle ACT format Instagram (dark)",
    }
    return previews.get(name, "Theme personnalise")


# ═══════════════════════════════════════════════════════════════════════════
# AUDIT WCAG — fonctions utilitaires pour valider la lisibilité des thèmes.
# Tout thème ajouté doit passer "audit_theme(name)" sans avertissement.
# Ratios cibles (WCAG 2.1) :
#   - text/bg          ≥ 4.5:1 (AA), idéal ≥ 7:1 (AAA)
#   - accent1/bg       ≥ 3.0:1 (AA large text), idéal ≥ 4.5:1
#   - accent2/bg       ≥ 3.0:1
# ═══════════════════════════════════════════════════════════════════════════

def _hex_to_linear_rgb(hex_color: str) -> tuple:
    """Convertit hex -> tuple (r, g, b) lineaire pour calcul de luminance WCAG."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def _lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(_lin(c) for c in rgb)


def _relative_luminance(hex_color: str) -> float:
    """Luminance relative WCAG 2.1."""
    r, g, b = _hex_to_linear_rgb(hex_color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    """Ratio de contraste WCAG 2.1 entre deux couleurs hex (1.0 a 21.0)."""
    la = _relative_luminance(hex_a)
    lb = _relative_luminance(hex_b)
    lighter, darker = (la, lb) if la > lb else (lb, la)
    return (lighter + 0.05) / (darker + 0.05)


def audit_theme(name: str) -> dict:
    """Audit WCAG d'un theme : retourne un rapport avec ratios texte/accents sur fond.

    Critere "intelligent" :
      - text/bg >= 4.5:1 OBLIGATOIRE (AA)
      - text/bg >= 7.0:1 RECOMMANDE (AAA)
      - accent1/bg >= 3.0:1 OBLIGATOIRE (AA large)
      - accent1/bg >= 4.5:1 RECOMMANDE

    Args:
        name: nom du theme (LinkedIn ou Instagram).

    Returns:
        dict avec champs : theme, ratios (text, accent1/2/3, text_muted),
        warnings (liste), level (AAA/AA/FAIL).
    """
    theme = THEMES.get(name) or IG_THEMES.get(name)
    if not theme:
        raise ValueError(f"Theme inconnu: {name}")

    bg = theme["bg"]
    ratios = {
        "text/bg":        round(contrast_ratio(theme["text"], bg), 2),
        "text_muted/bg":  round(contrast_ratio(theme["text_muted"], bg), 2),
        "accent1/bg":     round(contrast_ratio(theme["accent1"], bg), 2),
        "accent2/bg":     round(contrast_ratio(theme["accent2"], bg), 2),
        "accent3/bg":     round(contrast_ratio(theme["accent3"], bg), 2),
    }
    warnings = []
    if ratios["text/bg"] < 4.5:
        warnings.append(f"FAIL text/bg = {ratios['text/bg']}:1 (< 4.5 AA)")
    if ratios["text_muted/bg"] < 4.5:
        warnings.append(f"WARN text_muted/bg = {ratios['text_muted/bg']}:1 (< 4.5 AA)")
    if ratios["accent1/bg"] < 3.0:
        warnings.append(f"FAIL accent1/bg = {ratios['accent1/bg']}:1 (< 3.0 AA large)")
    if ratios["accent2/bg"] < 3.0:
        warnings.append(f"WARN accent2/bg = {ratios['accent2/bg']}:1 (< 3.0)")

    if any(w.startswith("FAIL") for w in warnings):
        level = "FAIL"
    elif ratios["text/bg"] >= 7.0 and ratios["accent1/bg"] >= 4.5:
        level = "AAA"
    else:
        level = "AA"

    return {
        "theme": name,
        "ratios": ratios,
        "warnings": warnings,
        "level": level,
    }


def audit_all_themes() -> list:
    """Audit complet de tous les themes (LinkedIn + Instagram). Retourne la liste des rapports."""
    reports = []
    for name in list(THEMES.keys()) + list(IG_THEMES.keys()):
        try:
            reports.append(audit_theme(name))
        except (KeyError, ValueError) as e:
            reports.append({"theme": name, "error": str(e), "level": "ERROR"})
    return reports


if __name__ == "__main__":
    # Lancer "python themes.py" pour afficher l'audit WCAG complet.
    print(f"{'Theme':<28} {'Level':<6} {'text/bg':<10} {'accent1/bg':<12} Warnings")
    print("-" * 100)
    for r in audit_all_themes():
        if "error" in r:
            print(f"{r['theme']:<28} ERROR  {r['error']}")
            continue
        warns = "; ".join(r["warnings"]) if r["warnings"] else "OK"
        print(f"{r['theme']:<28} {r['level']:<6} {r['ratios']['text/bg']:<10} {r['ratios']['accent1/bg']:<12} {warns}")
