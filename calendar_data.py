"""
calendar_data.py - Donnees partagees du planning de couleurs ACT 2026.
Utilise par :
  - app.py (route /calendar) pour afficher le planning dans l'application web
  - generate_color_calendar_pdf.py pour generer le PDF imprimable
"""

# ─── Calendrier mois par mois ────────────────────────────────────────────

MONTHS = [
    {
        "name": "Mai 2026",
        "mood": "Lancement",
        "subtitle": "ACT brand omnipresent · 5 publications",
        "rows": [
            ["Vendredi 1er mai · 14h (derogation)", "LLM expliques (chatgpt-gemini-claude)", "act_brand", "ig_act_brand"],
            ["Mercredi 6 mai · 8h-10h", "GenAI 80% sans impact", "dark_blue", "ig_ocean_deep"],
            ["Jeudi 14 mai · 9h-11h", "Cybersecurite 2026", "dark_red", "ig_aurora_dark"],
            ["Mardi 19 mai · 10h-12h", "Maroc data centers", "kente_tech", "ig_sunset_vibes"],
            ["Mercredi 27 mai · 9h-11h", "Digital Morocco 2030", "act_brand", "ig_act_brand"],
        ],
    },
    {
        "name": "Juin 2026",
        "mood": "Ouverture ete",
        "subtitle": "Couleurs vives, attention en hausse",
        "rows": [
            ["S1 (1-7) Mer 9h", "Tendances ete tech", "tropical_breeze", "ig_coral_burst"],
            ["S2 (8-14) Mar 10h", "Pratique outils IA", "sunset_glow", "ig_coral_burst"],
            ["S3 (15-21) Mer 9h", "Cas client Africa Focus", "dark_orange", "ig_sunset_vibes"],
            ["S4 (22-28) Jeu 9h", "Cloud / Infra", "emerald_city", "ig_sage_earth"],
            ["S5 (29-30) Mar 10h", "Bilan mi-annee", "act_brand", "ig_act_brand"],
        ],
    },
    {
        "name": "Juillet 2026",
        "mood": "Luxe lifestyle",
        "subtitle": "Cream/gold, lecture detendue",
        "rows": [
            ["S1 (1-5) Mer 10h", "Premium content", "golden_aura", "ig_midnight_gold"],
            ["S2 (6-12) Mar 11h", "Article fond ete", "neutral_warm", "ig_cream_luxury"],
            ["S3 (13-19) PAUSE Aid/trone", "Story IG seulement", "—", "—"],
            ["S4 (20-26) Mer 9h", "Carriere / Skills", "lavender_dream", "ig_rose_pop"],
            ["S5 (27-31) Mar 10h", "Africa Focus", "dark_orange", "ig_act_brand"],
        ],
    },
    {
        "name": "Aout 2026",
        "mood": "Pause editoriale neutres",
        "subtitle": "Articles de fond, ton sobre",
        "rows": [
            ["S1 (3-9) Mer 10h", "Etude / livre blanc", "neutral_paper", "ig_neutral_paper"],
            ["S2 (10-16) PAUSE Rev. Roi-Peuple", "Story IG seulement", "—", "—"],
            ["S3 (17-23) Mar 10h", "Article editorial", "neutral_linen", "ig_neutral_linen"],
            ["S4 (24-30) Mer 9h", "Tech profonde / R&D", "neutral_carbon", "ig_neutral_carbon"],
        ],
    },
    {
        "name": "Septembre 2026",
        "mood": "Rentree signature",
        "subtitle": "ACT brand fort + categorielles",
        "rows": [
            ["S1 (1-6) Mar 9h", "Manifeste rentree", "act_brand", "ig_act_brand"],
            ["S2 (7-13) Mer 9h", "DSI / GenAI bilan", "dark_blue", "ig_ocean_deep"],
            ["S3 (14-20) Jeu 9h", "Cybersecurity rentree", "dark_red", "ig_aurora_dark"],
            ["S4 (21-27) Mar 10h", "Africa Focus", "kente_tech", "ig_sunset_vibes"],
            ["S5 (28-30) Mer 9h", "Annonce produit/service", "act_brand", "ig_act_brand"],
        ],
    },
    {
        "name": "Octobre 2026",
        "mood": "Peak engagement",
        "subtitle": "Couleurs categorielles fortes",
        "rows": [
            ["S1 (28sept-4oct) Mar 9h", "Cybersecurity peak", "crimson_tide", "ig_aurora_dark"],
            ["S2 (5-11) Mer 9h", "Data & IA", "dark_blue", "ig_ocean_deep"],
            ["S3 (12-18) Jeu 9h", "Digital Strategy", "dark_orange", "ig_sunset_vibes"],
            ["S4 (19-25) Mar 10h", "Cloud / Infra", "forest_night", "ig_sage_earth"],
            ["S5 (26-31) Mer 9h", "Africa Focus", "kente_tech", "ig_act_brand"],
        ],
    },
    {
        "name": "Novembre 2026",
        "mood": "Editorial premium",
        "subtitle": "Papier de luxe, articles de fond",
        "rows": [
            ["S1 (2-8) Mar 9h", "Livre blanc IA Maroc", "neutral_paper", "ig_neutral_paper"],
            ["S2 (9-15) Mer 9h", "Etude sectorielle", "neutral_linen", "ig_neutral_linen"],
            ["S3 (16-22) PAUSE Indep. 18 nov", "Hommage / heritage", "neutral_stone", "ig_neutral_stone"],
            ["S4 (23-29) Mer 9h", "Architecture tech", "neutral_fog", "ig_neutral_fog"],
            ["S5 (30) Mar 10h", "R&D profonde", "neutral_carbon", "ig_neutral_carbon"],
        ],
    },
    {
        "name": "Decembre 2026",
        "mood": "Bilan & previsions",
        "subtitle": "Signature annee",
        "rows": [
            ["S1 (1-6) Mar 9h", "Bilan annee ACT", "golden_aura", "ig_midnight_gold"],
            ["S2 (7-13) Mer 9h", "Manifeste 2027", "act_brand", "ig_act_brand"],
            ["S3 (14-20) Jeu 9h", "Previsions tech 2027", "cosmic_void", "ig_aurora_dark"],
            ["S4 (21-27) PAUSE fetes", "Story IG / vœux", "neutral_obsidian", "ig_neutral_obsidian"],
            ["S5 (28-31) Mer 10h", "Lancement 2027", "act_brand", "ig_act_brand"],
        ],
    },
]

# ─── Couleurs hex (bg, accent1) pour les swatchs ─────────────────────────

THEME_HEX = {
    "act_brand":           ("#0A1410", "#D35400"),
    "ig_act_brand":        ("#0A1410", "#D35400"),
    "dark_blue":           ("#0c2461", "#5dade2"),
    "ig_ocean_deep":       ("#020c1a", "#06b6d4"),
    "dark_red":            ("#7a1f1f", "#ff6b6b"),
    "ig_aurora_dark":      ("#0d0520", "#a855f7"),
    "kente_tech":          ("#0a0a0a", "#f5c518"),
    "ig_sunset_vibes":     ("#1a0808", "#f97316"),
    "tropical_breeze":     ("#0a1f1c", "#5eead4"),
    "ig_coral_burst":      ("#0f0a06", "#ff6b35"),
    "sunset_glow":         ("#1a0808", "#f97316"),
    "dark_orange":         ("#0f0c08", "#fb923c"),
    "emerald_city":        ("#0a1f1a", "#10b981"),
    "ig_sage_earth":       ("#f4f1ea", "#7a8471"),
    "golden_aura":         ("#0f0a06", "#fbbf24"),
    "ig_midnight_gold":    ("#080604", "#d4a843"),
    "neutral_warm":        ("#1A1614", "#D4B896"),
    "ig_cream_luxury":     ("#f5e6d3", "#d4a574"),
    "lavender_dream":      ("#0a0612", "#a78bfa"),
    "ig_rose_pop":         ("#0f0510", "#ec4899"),
    "neutral_paper":       ("#FAF7F0", "#1F1E1B"),
    "ig_neutral_paper":    ("#FAF7F0", "#1F1E1B"),
    "neutral_linen":       ("#F8F4ED", "#1C1A16"),
    "ig_neutral_linen":    ("#F8F4ED", "#1C1A16"),
    "neutral_carbon":      ("#0C0C0E", "#B89968"),
    "ig_neutral_carbon":   ("#0C0C0E", "#B89968"),
    "crimson_tide":        ("#1a0505", "#dc143c"),
    "midnight_ocean":      ("#020617", "#38bdf8"),
    "forest_night":        ("#0a1a0d", "#16a34a"),
    "neutral_stone":       ("#F4EFE7", "#5C4A36"),
    "ig_neutral_stone":    ("#F4EFE7", "#5C4A36"),
    "neutral_fog":         ("#EEF1F4", "#1A1F26"),
    "ig_neutral_fog":      ("#EEF1F4", "#1A1F26"),
    "cosmic_void":         ("#000000", "#a855f7"),
    "neutral_obsidian":    ("#0A0E0C", "#8FA888"),
    "ig_neutral_obsidian": ("#0A0E0C", "#8FA888"),
    "neutral_charcoal":    ("#0F0F10", "#C9B89A"),
    "ig_neutral_charcoal": ("#0F0F10", "#C9B89A"),
    "neutral_slate":       ("#0E1216", "#A8B2BD"),
    "ig_neutral_slate":    ("#0E1216", "#A8B2BD"),
    "neutral_clay":        ("#F0E6DC", "#2D241D"),
    "ig_neutral_clay":     ("#F0E6DC", "#2D241D"),
    "neutral_mono":        ("#FFFFFF", "#000000"),
    "ig_neutral_mono":     ("#FFFFFF", "#000000"),
    "—":                   ("#E0E0E0", "#9E9E9E"),
}

# ─── Legende ─────────────────────────────────────────────────────────────

LEGEND_COLOR = [
    ("act_brand",       "Charte ACT — signature obligatoire"),
    ("dark_blue",       "Data & IA, Cloud"),
    ("dark_red",        "Cybersecurity"),
    ("dark_orange",     "Digital Strategy"),
    ("kente_tech",      "Africa Focus"),
    ("crimson_tide",    "Cyber peak"),
    ("midnight_ocean",  "Cloud profond"),
    ("forest_night",    "Infra naturelle"),
    ("cosmic_void",     "Previsions tech"),
    ("golden_aura",     "Bilan / premium"),
    ("lavender_dream",  "Carriere / Skills"),
    ("tropical_breeze", "Tendances ete"),
    ("sunset_glow",     "Pratique chaude"),
    ("emerald_city",    "Cloud / Infra"),
]

LEGEND_NEUTRAL = [
    ("neutral_charcoal",  "Annonce premium dark"),
    ("neutral_carbon",    "Tech profonde / R&D"),
    ("neutral_obsidian",  "Naturel / wellness"),
    ("neutral_slate",     "Corporate B2B"),
    ("neutral_warm",      "Magazine lifestyle"),
    ("neutral_paper",     "Livre blanc / editorial"),
    ("neutral_linen",     "Edition haut de gamme"),
    ("neutral_stone",     "Hommage / sobre"),
    ("neutral_fog",       "Architecture / minimal"),
    ("neutral_clay",      "Crafted / artisanal"),
    ("neutral_mono",      "Communique presse"),
]

# ─── Logique mensuelle (mood + strategie) ────────────────────────────────

LOGIC = [
    {"period": "Mai", "mood": "Lancement", "strategy": "Rotation `act_brand` + couleurs categorielles + 1 neutre"},
    {"period": "Juin", "mood": "Ouverture ete", "strategy": "Couleurs vives (`tropical_breeze`, `sunset_glow`, `aurora_borealis`)"},
    {"period": "Juillet", "mood": "Luxe lifestyle", "strategy": "Cream/gold (`golden_aura`, `ig_cream_luxury`, `neutral_warm`)"},
    {"period": "Aout", "mood": "Pause editoriale", "strategy": "Neutres (papier, lin, carbone) — articles de fond"},
    {"period": "Septembre", "mood": "Rentree signature", "strategy": "`act_brand` + categorielles fortes"},
    {"period": "Octobre", "mood": "Peak engagement", "strategy": "Couleurs categorielles (`dark_red`, `kente_tech`, `dark_blue`)"},
    {"period": "Novembre", "mood": "Editorial premium", "strategy": "Neutres papier (`neutral_paper`, `neutral_linen`)"},
    {"period": "Decembre", "mood": "Bilan & previsions", "strategy": "`golden_aura` + neutres + `act_brand` (cloture)"},
]


def get_swatch(theme: str) -> dict:
    """Retourne {bg, accent} pour un theme."""
    bg, accent = THEME_HEX.get(theme, ("#cccccc", "#666666"))
    return {"bg": bg, "accent": accent, "is_dash": theme == "—"}
