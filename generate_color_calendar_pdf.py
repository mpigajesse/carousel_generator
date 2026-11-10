"""
generate_color_calendar_pdf.py - Genere le PDF du planning de couleurs ACT
mai-decembre 2026 avec swatchs hex visuels, charte ACT.

Usage:
    python generate_color_calendar_pdf.py

Sortie:
    articles/PLANNING_COULEURS_2026.pdf
"""
import asyncio
import base64
import platform
from pathlib import Path

from playwright.async_api import async_playwright

# Note : les donnees du calendrier (MONTHS, THEME_HEX, LEGEND_*) sont egalement
# definies dans calendar_data.py qui sert la route /calendar de l'app web.
# Toute modification doit etre repercutee dans les deux fichiers.

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

ROOT = Path(__file__).parent
LOGO_PNG = ROOT / "static" / "logo" / "logo1.png"
LOGO_DATA_URI = f"data:image/png;base64,{base64.b64encode(LOGO_PNG.read_bytes()).decode('ascii')}"
OUTPUT_PDF = ROOT / "articles" / "PLANNING_COULEURS_2026.pdf"

# Note : les definitions locales ci-dessous existent en doublon dans calendar_data.py.
# La version partagee (importee plus haut) est la source de verite pour app.py.
# Si vous modifiez les donnees, faites-le dans calendar_data.py et resynchronisez ici.

MONTHS = [
    {
        "name": "Mai 2026",
        "mood": "Lancement",
        "subtitle": "ACT brand omnipresent · 5 publications",
        "rows": [
            ["Vendredi 1er mai · 14h *(derogation)*", "LLM expliques (chatgpt-gemini-claude)", "act_brand", "ig_act_brand"],
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

# Couleurs hex de chaque theme (bg, accent1) pour les swatchs
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


def swatch(theme_name: str) -> str:
    """Genere le HTML d'un swatch (rectangle colore avec bg + accent + nom + hex)."""
    bg, accent = THEME_HEX.get(theme_name, ("#cccccc", "#666666"))
    is_dash = theme_name == "—"
    if is_dash:
        return f'<span class="swatch-dash">—</span>'
    return f"""<span class="swatch">
  <span class="swatch-chip" style="background:{bg};border-color:{accent}">
    <span class="swatch-accent" style="background:{accent}"></span>
  </span>
  <span class="swatch-meta">
    <span class="swatch-name">{theme_name}</span>
    <span class="swatch-hex">{bg} · {accent}</span>
  </span>
</span>"""


def render_month(m: dict) -> str:
    rows_html = ""
    for date_label, article, lk, ig in m["rows"]:
        rows_html += f"""
        <tr>
          <td class="cell-date">{date_label}</td>
          <td class="cell-article">{article}</td>
          <td class="cell-swatch">{swatch(lk)}</td>
          <td class="cell-swatch">{swatch(ig)}</td>
        </tr>"""
    return f"""
    <section class="month no-break">
      <div class="month-header">
        <span class="month-eyebrow">◆ {m['mood']}</span>
        <h2>{m['name']}</h2>
        <p class="month-subtitle">{m['subtitle']}</p>
      </div>
      <table class="month-table">
        <thead>
          <tr>
            <th style="width:23%">Date</th>
            <th style="width:30%">Article / sujet</th>
            <th style="width:23%">LinkedIn 1080×1080</th>
            <th style="width:24%">Instagram 1080×1350</th>
          </tr>
        </thead>
        <tbody>{rows_html}
        </tbody>
      </table>
    </section>
    """


HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Planning des couleurs ACT — Mai → Décembre 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --orange: #D35400;
    --orange-hot: #FF6B00;
    --gold: #F39C12;
    --dark: #0A1410;
    --dark-deep: #070E1C;
    --green: #1B3022;
    --green-mid: #2C4A35;
    --cream: #FCF9F2;
    --cream-deep: #F4EFE4;
    --ink: #0A1410;
    --ink-soft: #3A4540;
    --muted: #6B7A72;
    --line: #D5CFBE;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    background: var(--cream);
    color: var(--ink);
    font-family: 'Poppins', system-ui, sans-serif;
    font-weight: 400;
    line-height: 1.55;
    font-size: 9.5pt;
  }
  @page { size: A4; margin: 14mm 12mm 14mm 12mm; }

  .page-break { page-break-before: always; }
  .no-break { page-break-inside: avoid; }

  /* — COVER — */
  .cover {
    min-height: 260mm;
    background: linear-gradient(160deg, var(--dark) 0%, var(--green) 60%, var(--dark-deep) 100%);
    color: var(--cream);
    padding: 22mm 14mm;
    position: relative;
    overflow: hidden;
    margin: -14mm -12mm 0;
  }
  .cover::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 360px; height: 360px;
    background: var(--orange);
    transform: rotate(-43.264deg);
    opacity: 0.10;
  }
  .cover::after {
    content: '';
    position: absolute;
    bottom: -120px; left: -100px;
    width: 280px; height: 280px;
    background: var(--gold);
    transform: rotate(-43.264deg);
    opacity: 0.07;
  }
  .cover .logo {
    position: relative;
    display: inline-block;
    background: var(--cream);
    padding: 16px 22px;
    border-radius: 8px;
    margin-bottom: 50px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
  }
  .cover .logo img { width: 200px; height: auto; display: block; }
  .cover .eyebrow {
    font-family: 'Poppins', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: var(--orange);
    letter-spacing: 0.24em;
    text-transform: uppercase;
    margin-bottom: 16px;
  }
  .cover .eyebrow::before {
    content: '';
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--orange);
    transform: rotate(-43.264deg);
    margin-right: 12px;
    vertical-align: middle;
  }
  .cover h1 {
    font-family: 'Lora', Georgia, serif;
    font-weight: 500;
    font-size: 56px;
    line-height: 1.0;
    letter-spacing: -0.025em;
    margin-bottom: 22px;
    text-wrap: balance;
  }
  .cover h1 em { color: var(--orange); font-style: italic; }
  .cover .subtitle {
    font-family: 'Lora', serif;
    font-size: 20px;
    font-weight: 400;
    color: var(--cream);
    opacity: 0.85;
    max-width: 520px;
    margin-bottom: 50px;
    line-height: 1.4;
  }
  .cover .meta {
    border-top: 1px solid rgba(252,249,242,0.18);
    padding-top: 20px;
    font-size: 11px;
    color: var(--cream);
    opacity: 0.78;
    line-height: 1.9;
  }
  .cover .meta strong { color: var(--gold); font-weight: 500; }
  .cover .anchor {
    position: absolute;
    bottom: 22mm;
    left: 14mm;
    right: 14mm;
    font-family: 'Poppins', sans-serif;
    font-size: 10px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--cream);
    opacity: 0.6;
    border-top: 1px solid rgba(252,249,242,0.15);
    padding-top: 14px;
  }

  /* — SECTIONS — */
  section { padding: 8mm 0 4mm; }
  h2 {
    font-family: 'Lora', serif;
    font-weight: 500;
    font-size: 26px;
    line-height: 1.1;
    color: var(--ink);
    margin-bottom: 4px;
    letter-spacing: -0.02em;
  }
  h2 em { color: var(--orange); font-style: italic; }
  .month-eyebrow {
    display: inline-block;
    font-family: 'Poppins', sans-serif;
    font-size: 9.5pt;
    font-weight: 600;
    color: var(--orange);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .month-subtitle {
    font-family: 'Lora', serif;
    font-style: italic;
    color: var(--ink-soft);
    margin-bottom: 10px;
    font-size: 11pt;
  }
  .month-header { margin-bottom: 8px; }

  /* — TABLE MOIS — */
  table.month-table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 9pt;
  }
  table.month-table thead th {
    background: var(--dark);
    color: var(--cream);
    text-align: left;
    padding: 8px 10px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 8pt;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  table.month-table tbody td {
    padding: 8px 10px;
    border-bottom: 1px solid var(--line);
    vertical-align: middle;
  }
  table.month-table tbody tr:nth-child(even) { background: var(--cream-deep); }
  .cell-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    color: var(--ink);
    font-weight: 500;
  }
  .cell-article { color: var(--ink-soft); font-size: 9pt; }
  .cell-swatch { padding: 6px 10px !important; }

  /* — SWATCH — */
  .swatch {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .swatch-chip {
    display: inline-block;
    width: 30px; height: 22px;
    border-radius: 4px;
    border: 1.5px solid;
    flex-shrink: 0;
    position: relative;
    overflow: hidden;
  }
  .swatch-accent {
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 40%;
  }
  .swatch-meta {
    display: flex;
    flex-direction: column;
    line-height: 1.25;
  }
  .swatch-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    color: var(--ink);
    font-weight: 500;
  }
  .swatch-hex {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    color: var(--muted);
  }
  .swatch-dash {
    font-family: 'Lora', serif;
    color: var(--muted);
    font-style: italic;
    font-size: 11pt;
  }

  /* — LEGENDE / WORKFLOW — */
  .card {
    background: var(--cream);
    border: 1px solid var(--line);
    border-left: 4px solid var(--orange);
    padding: 14px 18px;
    margin: 12px 0;
    page-break-inside: avoid;
    font-size: 9.5pt;
  }
  .card.dark {
    background: var(--dark);
    color: var(--cream);
    border-color: var(--orange);
  }
  .card.dark p, .card.dark li { color: var(--cream); opacity: 0.92; }
  .card.dark strong { color: var(--gold); }
  .card.dark h3 { color: var(--cream); }
  .card h4 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 11pt;
    color: var(--orange);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  ul.ds {
    list-style: none;
    margin: 6px 0;
    padding: 0;
  }
  ul.ds li {
    position: relative;
    padding-left: 18px;
    margin: 4px 0;
    color: var(--ink-soft);
    font-size: 9.5pt;
  }
  ul.ds li::before {
    content: '';
    position: absolute;
    left: 0; top: 8px;
    width: 7px; height: 7px;
    background: var(--orange);
    transform: rotate(-43.264deg);
  }

  pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: var(--dark);
    color: var(--cream);
    padding: 12px 14px;
    border-radius: 4px;
    line-height: 1.5;
  }

  /* — Legende grid — */
  .legend-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px 14px;
    margin: 10px 0;
  }
  .legend-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 8.5pt;
    border-bottom: 1px dotted var(--line);
    padding: 4px 0;
  }
  .legend-row .swatch-chip { width: 28px; height: 18px; }
  .legend-row .legend-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    flex-shrink: 0;
    min-width: 130px;
  }
  .legend-row .legend-use {
    color: var(--muted);
    font-size: 8pt;
    flex-grow: 1;
  }

  .doc-footer {
    margin-top: 16mm;
    padding: 10mm 0 0;
    border-top: 2px solid var(--orange);
    color: var(--muted);
    font-size: 9pt;
    text-align: center;
  }
  .doc-footer .signature {
    font-family: 'Lora', serif;
    font-size: 13px;
    color: var(--ink);
    font-weight: 500;
  }
  .doc-footer .signature em { color: var(--orange); font-style: italic; }
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
  <div class="logo"><img src="__LOGO_URI__" alt="ACT"></div>
  <div class="eyebrow">Référence interne · Charte couleurs annuelle</div>
  <h1>Planning des <em>couleurs</em><br>Mai → Décembre 2026</h1>
  <p class="subtitle">À consulter avant chaque génération de carrousel. Une chronologie, un thème par créneau, une lisibilité garantie WCAG AAA.</p>
  <div class="meta">
    <strong>Auteur</strong> · Dr. Sohaib Baroud — Fondateur ACT<br>
    <strong>Période</strong> · 8 mois · 32+ créneaux de publication<br>
    <strong>Rotation</strong> · Aucun thème consécutif identique<br>
    <strong>Lisibilité</strong> · 53/54 thèmes en WCAG AAA · 1 en AA<br>
    <strong>Audit</strong> · <code>python themes.py</code>
  </div>
  <div class="anchor">Casablanca · Rabat · Dakar — L'IA opérationnelle. Vraiment.</div>
</div>

<!-- LOGIQUE -->
<div class="page-break"></div>
<section>
  <h2>La <em>logique</em> du calendrier</h2>
  <p style="color:var(--ink-soft);margin-bottom:8px">8 moods successifs sur l'année — chacun guide les choix de couleurs.</p>
  <table class="month-table">
    <thead>
      <tr><th style="width:14%">Période</th><th style="width:22%">Mood</th><th>Stratégie de couleurs</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Mai</strong></td><td>Lancement</td><td>Rotation <code>act_brand</code> + couleurs catégorielles + 1 neutre</td></tr>
      <tr><td><strong>Juin</strong></td><td>Ouverture été</td><td>Couleurs vives (<code>tropical_breeze</code>, <code>sunset_glow</code>, <code>aurora_borealis</code>)</td></tr>
      <tr><td><strong>Juillet</strong></td><td>Luxe lifestyle</td><td>Cream/gold (<code>golden_aura</code>, <code>ig_cream_luxury</code>, <code>neutral_warm</code>)</td></tr>
      <tr><td><strong>Août</strong></td><td>Pause éditoriale</td><td>Neutres (papier, lin, carbone) — articles de fond</td></tr>
      <tr><td><strong>Septembre</strong></td><td>Rentrée signature</td><td><code>act_brand</code> + catégorielles fortes</td></tr>
      <tr><td><strong>Octobre</strong></td><td>Peak engagement</td><td>Couleurs catégorielles (<code>dark_red</code>, <code>kente_tech</code>, <code>dark_blue</code>)</td></tr>
      <tr><td><strong>Novembre</strong></td><td>Éditorial premium</td><td>Neutres papier (<code>neutral_paper</code>, <code>neutral_linen</code>)</td></tr>
      <tr><td><strong>Décembre</strong></td><td>Bilan & prévisions</td><td><code>golden_aura</code> + neutres + <code>act_brand</code> (clôture)</td></tr>
    </tbody>
  </table>
  <div class="card dark">
    <h4 style="color:var(--gold)">Règle de rotation</h4>
    <p>Jamais 2 publications consécutives avec le même thème. <code>act_brand</code> / <code>ig_act_brand</code> max 1 fois / mois — sinon perd sa charge symbolique.</p>
  </div>
</section>

<!-- CALENDRIER MOIS PAR MOIS -->
__MONTHS__

<!-- LEGENDE -->
<div class="page-break"></div>
<section>
  <h2>Légende des <em>thèmes</em></h2>
  <p style="color:var(--ink-soft);margin-bottom:6px">32 thèmes LinkedIn + 22 thèmes Instagram. Voici les principaux du planning.</p>

  <h3 style="font-family:'Lora',serif;font-size:14pt;margin:10px 0 4px;color:var(--orange);font-style:italic">Couleurs catégorielles</h3>
  <div class="legend-grid">__LEGEND_COLOR__</div>

  <h3 style="font-family:'Lora',serif;font-size:14pt;margin:14px 0 4px;color:var(--orange);font-style:italic">Neutres</h3>
  <div class="legend-grid">__LEGEND_NEUTRAL__</div>
</section>

<!-- WORKFLOW -->
<section>
  <h2>Workflow <em>pré-génération</em></h2>
  <ul class="ds">
    <li><strong>1.</strong> Ouvrir ce PDF (ou <code>PLANNING_COULEURS_2026.md</code>).</li>
    <li><strong>2.</strong> Localiser la date dans le mois en cours.</li>
    <li><strong>3.</strong> Lire le thème principal. Si l'article ne colle pas au mood, prendre l'alternative.</li>
    <li><strong>4.</strong> Vérifier WCAG : <code>python themes.py | findstr &lt;nom_theme&gt;</code> → AAA recommandé.</li>
    <li><strong>5.</strong> Lancer <code>app.py</code> et choisir le thème dans la liste.</li>
    <li><strong>6.</strong> Générer LinkedIn (1080×1080) puis Instagram (1080×1350) avec le pendant <code>ig_*</code>.</li>
  </ul>

  <div class="card">
    <h4>Règles d'or — non négociables</h4>
    <ul class="ds">
      <li>Pas 2 fois le même thème consécutif (rotation obligatoire).</li>
      <li><code>act_brand</code> / <code>ig_act_brand</code> réservés aux moments forts (lancement, signature, manifeste, annonces majeures).</li>
      <li>Neutres clairs (light) sur articles ≥ 200 chars de body — meilleure lisibilité longue.</li>
      <li>Couleurs vives (<code>cyber_punk</code>, <code>neon_tokyo</code>, <code>ig_neon_pulse</code>) : 1-2 fois / trimestre max.</li>
      <li>Toujours auditer avant validation : <code>python themes.py</code>.</li>
    </ul>
  </div>

  <div class="doc-footer">
    <img src="__LOGO_URI__" alt="ACT" style="width:130px;height:auto;margin-bottom:12px">
    <p class="signature">Dr. Sohaib Baroud — Fondateur <em>ACT</em></p>
    <p>Africa Centred Technology · Casablanca · Rabat · Dakar</p>
    <p style="margin-top:6px;font-size:8pt">Référence interne · Document évolutif · Mis à jour à chaque ajout de thème</p>
  </div>
</section>

</body>
</html>
"""

# Legendes — couleurs categorielles principales
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


def render_legend_row(name: str, use: str) -> str:
    bg, accent = THEME_HEX.get(name, ("#cccccc", "#666666"))
    return f"""<div class="legend-row">
      <span class="swatch-chip" style="background:{bg};border-color:{accent}"><span class="swatch-accent" style="background:{accent}"></span></span>
      <span class="legend-name">{name}</span>
      <span class="legend-use">{use}</span>
    </div>"""


async def render_pdf():
    months_html = "\n".join(render_month(m) for m in MONTHS)
    legend_color = "\n".join(render_legend_row(n, u) for n, u in LEGEND_COLOR)
    legend_neutral = "\n".join(render_legend_row(n, u) for n, u in LEGEND_NEUTRAL)

    html = (
        HTML
        .replace("__LOGO_URI__", LOGO_DATA_URI)
        .replace("__MONTHS__", months_html)
        .replace("__LEGEND_COLOR__", legend_color)
        .replace("__LEGEND_NEUTRAL__", legend_neutral)
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_PDF.with_suffix(".tmp.pdf")
        await page.pdf(
            path=str(tmp),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()
    try:
        tmp.replace(OUTPUT_PDF)
    except PermissionError:
        print(f"!! PDF cible verrouille : {OUTPUT_PDF}. Version generee : {tmp}")
        return tmp
    return OUTPUT_PDF


def main():
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"-> Generation : {OUTPUT_PDF}")
    final = asyncio.run(render_pdf())
    size_kb = final.stat().st_size // 1024
    print(f"OK PDF genere ({size_kb} KB) : {final}")


if __name__ == "__main__":
    main()
