"""
generate_planning_pdf.py - Génère le planning de publication ACT en PDF
charté (couleurs, typographies, logo, losange) prêt à diffuser à l'équipe.

Usage:
    python generate_planning_pdf.py

Sortie:
    articles/PLANNING_PUBLICATION.pdf (A4 portrait)
"""
import asyncio
import base64
import platform
from pathlib import Path

from playwright.async_api import async_playwright

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

ROOT = Path(__file__).parent
LOGO_PNG = ROOT / "static" / "logo" / "logo1.png"  # version optimisee 216 KB
LOGO_DATA_URI = f"data:image/png;base64,{base64.b64encode(LOGO_PNG.read_bytes()).decode('ascii')}"
OUTPUT_PDF = ROOT / "articles" / "PLANNING_PUBLICATION.pdf"

HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Planning de publication ACT</title>
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
    line-height: 1.6;
    font-size: 11pt;
  }
  body { padding: 0; }
  @page { size: A4; margin: 18mm 16mm 18mm 16mm; }

  .page-break { page-break-before: always; }
  .no-break { page-break-inside: avoid; }

  /* — Header Cover — */
  .cover {
    min-height: 250mm;
    background: linear-gradient(160deg, var(--dark) 0%, var(--green) 60%, var(--dark-deep) 100%);
    color: var(--cream);
    padding: 24mm 16mm;
    position: relative;
    overflow: hidden;
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
    padding: 18px 26px;
    border-radius: 8px;
    margin-bottom: 56px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
  }
  .cover .logo img { width: 220px; height: auto; display: block; }
  .cover .eyebrow {
    font-family: 'Poppins', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: var(--orange);
    letter-spacing: 0.24em;
    text-transform: uppercase;
    margin-bottom: 16px;
    position: relative;
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
    font-size: 64px;
    line-height: 1.0;
    letter-spacing: -0.025em;
    margin-bottom: 24px;
    text-wrap: balance;
  }
  .cover h1 em { color: var(--orange); font-style: italic; }
  .cover .subtitle {
    font-family: 'Lora', serif;
    font-size: 22px;
    font-weight: 400;
    color: var(--cream);
    opacity: 0.85;
    max-width: 540px;
    margin-bottom: 60px;
    line-height: 1.4;
  }
  .cover .meta {
    border-top: 1px solid rgba(252,249,242,0.18);
    padding-top: 24px;
    font-size: 12px;
    color: var(--cream);
    opacity: 0.78;
    line-height: 1.9;
  }
  .cover .meta strong { color: var(--gold); font-weight: 500; }
  .cover .anchor {
    position: absolute;
    bottom: 24mm;
    left: 16mm;
    right: 16mm;
    font-family: 'Poppins', sans-serif;
    font-size: 11px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--cream);
    opacity: 0.6;
    border-top: 1px solid rgba(252,249,242,0.15);
    padding-top: 16px;
  }

  /* — Sections — */
  section { padding: 14mm 0 6mm; }
  h2 {
    font-family: 'Lora', serif;
    font-weight: 500;
    font-size: 30px;
    line-height: 1.1;
    color: var(--ink);
    margin-bottom: 6px;
    letter-spacing: -0.02em;
    text-wrap: balance;
  }
  h2 em { color: var(--orange); font-style: italic; }
  h2::before {
    content: '';
    display: inline-block;
    width: 14px; height: 14px;
    background: var(--orange);
    transform: rotate(-43.264deg);
    margin-right: 14px;
    vertical-align: middle;
  }
  h3 {
    font-family: 'Lora', serif;
    font-weight: 500;
    font-size: 20px;
    color: var(--ink);
    margin: 18px 0 8px;
  }
  h4 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 13px;
    color: var(--orange);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin: 14px 0 6px;
  }
  p { margin: 8px 0; color: var(--ink-soft); }
  strong { color: var(--ink); font-weight: 600; }
  em { font-style: italic; }

  ul.ds {
    list-style: none;
    margin: 8px 0;
    padding: 0;
  }
  ul.ds li {
    position: relative;
    padding-left: 20px;
    margin: 6px 0;
    color: var(--ink-soft);
  }
  ul.ds li::before {
    content: '';
    position: absolute;
    left: 0; top: 9px;
    width: 8px; height: 8px;
    background: var(--orange);
    transform: rotate(-43.264deg);
  }

  /* — Tables — */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 10pt;
  }
  thead th {
    background: var(--dark);
    color: var(--cream);
    text-align: left;
    padding: 10px 12px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 9pt;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  thead th:first-child { border-top-left-radius: 4px; }
  thead th:last-child { border-top-right-radius: 4px; }
  tbody td {
    padding: 9px 12px;
    border-bottom: 1px solid var(--line);
    vertical-align: top;
  }
  tbody tr:nth-child(even) { background: var(--cream-deep); }
  tbody tr:hover { background: rgba(211,84,0,0.04); }
  td strong { color: var(--orange); }

  /* — Cards — */
  .card {
    background: var(--cream);
    border: 1px solid var(--line);
    border-left: 4px solid var(--orange);
    padding: 18px 22px;
    margin: 14px 0;
    page-break-inside: avoid;
  }
  .card.dark {
    background: var(--dark);
    color: var(--cream);
    border-color: var(--orange);
  }
  .card.dark p, .card.dark li { color: var(--cream); opacity: 0.92; }
  .card.dark strong { color: var(--gold); }
  .card.dark h3 { color: var(--cream); }

  .quote-block {
    border-left: 3px solid var(--gold);
    padding: 12px 18px;
    margin: 14px 0;
    background: rgba(243,156,18,0.06);
    font-family: 'Lora', serif;
    font-style: italic;
    color: var(--ink);
  }

  pre, code.block {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 9pt;
    background: var(--dark);
    color: var(--cream);
    padding: 14px 18px;
    border-radius: 4px;
    overflow: hidden;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
  }
  pre .accent { color: var(--orange); }

  .stars { color: var(--gold); letter-spacing: 0.05em; }
  .badge {
    display: inline-block;
    padding: 2px 10px;
    background: var(--orange);
    color: var(--cream);
    font-family: 'Poppins', sans-serif;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 2px;
    margin-right: 6px;
  }
  .badge.gold { background: var(--gold); color: var(--dark); }
  .badge.green { background: var(--green); color: var(--cream); }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin: 14px 0;
  }

  /* — Footer — */
  .doc-footer {
    margin-top: 30mm;
    padding: 14mm 0 0;
    border-top: 2px solid var(--orange);
    color: var(--muted);
    font-size: 9pt;
    text-align: center;
    line-height: 1.8;
  }
  .doc-footer .signature {
    font-family: 'Lora', serif;
    font-size: 14px;
    color: var(--ink);
    font-weight: 500;
  }
  .doc-footer .signature em { color: var(--orange); font-style: italic; }
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════ COVER ═══════════════════════════════════════════ -->
<div class="cover">
  <div class="logo"><img src="__LOGO_URI__" alt="ACT — Africa Centred Technology"></div>

  <div class="eyebrow">Document interne · Stratégie éditoriale</div>
  <h1>Planning de <em>publication</em><br>Mai 2026</h1>
  <p class="subtitle">5 carrousels, 5 semaines, 1 cadence stratégique pour porter la voix d'ACT au-delà du Maroc.</p>

  <div class="meta">
    <strong>Auteur</strong> · Dr. Sohaib Baroud — Fondateur ACT<br>
    <strong>Lancement</strong> · <span style="color:var(--gold)">Vendredi 1er mai 2026 · 14h00</span><br>
    <strong>Période</strong> · 1er mai → 27 mai 2026 · 1 publication majeure par semaine<br>
    <strong>Plateformes</strong> · LinkedIn (primaire) · Instagram (secondaire) · Newsletter (relais)<br>
    <strong>Diffusion</strong> · Équipe ACT · Confidentiel
  </div>

  <div class="anchor">Casablanca · Rabat · Dakar — L'IA opérationnelle. Vraiment.</div>
</div>

<!-- ═══════════════════════════════════════════ PAGE 2 — INVENTAIRE ═══════════════════════════════════════════ -->
<div class="page-break"></div>
<section>
  <h2>L'<em>inventaire</em> · 5 carrousels prêts</h2>
  <p>Cinq productions ACT déjà structurées et prêtes à imprimer. Le sixième — <em>vibe_coding</em> — est volontairement écarté de ce planning, réservé pour un usage ultérieur.</p>

  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Slug</th>
        <th>Catégorie</th>
        <th>Audience</th>
        <th>Viralité</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1</strong></td>
        <td><code>chatgpt-gemini-claude-explication</code></td>
        <td>Data &amp; IA · LLM</td>
        <td><strong>Universelle</strong></td>
        <td><span class="stars">★★★★★</span></td>
      </tr>
      <tr>
        <td><strong>2</strong></td>
        <td><code>ia-generative-80-pourcent-sans-impact</code></td>
        <td>Data &amp; IA · GenAI</td>
        <td>DSI, dirigeants, consultants</td>
        <td><span class="stars">★★★★</span></td>
      </tr>
      <tr>
        <td><strong>3</strong></td>
        <td><code>cybersecurite-2026-instabilite-permanente</code></td>
        <td>Cybersecurity</td>
        <td>CISO, IT, dirigeants</td>
        <td><span class="stars">★★★</span></td>
      </tr>
      <tr>
        <td><strong>4</strong></td>
        <td><code>maroc-hub-numerique-afrique-data-centers</code></td>
        <td>Africa Focus</td>
        <td>Tech Afrique, MENA, investisseurs</td>
        <td><span class="stars">★★★</span></td>
      </tr>
      <tr>
        <td><strong>5</strong></td>
        <td><code>carousel-instagram-digital-morocco-2030</code></td>
        <td>Strategy · Maroc</td>
        <td>Décideurs Maroc, écosystème</td>
        <td><span class="stars">★★★</span></td>
      </tr>
    </tbody>
  </table>
</section>

<!-- ═══════════════════════════════════════════ CALENDRIER ═══════════════════════════════════════════ -->
<section>
  <h2>Le <em>calendrier</em> · 5 semaines</h2>
  <table>
    <thead>
      <tr>
        <th>Sem.</th>
        <th>Article</th>
        <th>Jour</th>
        <th>Heure</th>
        <th>Plateformes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="badge">S1</span></td>
        <td><strong>chatgpt-gemini-claude-explication</strong><br><em style="color:var(--orange)">Lancement viral · AUJOURD'HUI</em></td>
        <td><strong style="color:var(--orange)">Vendredi 1er mai 2026</strong></td>
        <td><strong style="color:var(--orange)">14h</strong></td>
        <td>LinkedIn + Instagram + Story</td>
      </tr>
      <tr>
        <td><span class="badge gold">S2</span></td>
        <td>ia-generative-80-pourcent-sans-impact</td>
        <td>Mercredi 6 mai</td>
        <td>8h–10h</td>
        <td>LinkedIn primaire</td>
      </tr>
      <tr>
        <td><span class="badge green">S3</span></td>
        <td>cybersecurite-2026-instabilite-permanente</td>
        <td>Jeudi 14 mai</td>
        <td>9h–11h</td>
        <td>LinkedIn + Newsletter</td>
      </tr>
      <tr>
        <td><span class="badge">S4</span></td>
        <td>maroc-hub-numerique-afrique-data-centers</td>
        <td>Mardi 19 mai</td>
        <td>10h–12h</td>
        <td>LinkedIn FR + Instagram</td>
      </tr>
      <tr>
        <td><span class="badge gold">S5</span></td>
        <td>carousel-instagram-digital-morocco-2030</td>
        <td>Mercredi 27 mai</td>
        <td>9h–11h</td>
        <td>LinkedIn + Instagram</td>
      </tr>
    </tbody>
  </table>

  <div class="card">
    <h4>Règles ACT — non négociables</h4>
    <ul class="ds">
      <li>Jamais de publication majeure le <strong>lundi</strong> (feed saturé week-end), <strong>vendredi</strong> (engagement -40%) ou <strong>dimanche</strong>.</li>
      <li>Cadence stricte : <strong>1 carrousel majeur / semaine</strong> pour préserver l'attention.</li>
      <li>Pas de double publication la même semaine.</li>
    </ul>
  </div>

  <div class="card dark">
    <h4 style="color:var(--gold)">Dérogation S1</h4>
    <p>La règle « pas de publication majeure le vendredi » est <strong>levée</strong> pour S1. Le 1er mai (fête du travail) libère du temps de scroll côté audience, ce qui peut compenser la baisse vendredi habituelle.</p>
    <p style="margin-top:8px"><em style="color:var(--orange)">À surveiller en KPIs sur les 24 premières heures.</em></p>
  </div>
</section>

<!-- ═══════════════════════════════════════════ POURQUOI #1 ═══════════════════════════════════════════ -->
<div class="page-break"></div>
<section>
  <h2>Pourquoi <em>cet article</em> en premier</h2>
  <p><code>chatgpt-gemini-claude-explication</code> est le seul des cinq à cocher les <strong>4 critères de viralité mondiale</strong>.</p>

  <div class="grid-2">
    <div class="card">
      <h3>1. Universalité</h3>
      <p>Tout le monde utilise ChatGPT, Gemini, Claude. <strong>Aucune barrière</strong> sectorielle, géographique ou linguistique.</p>
    </div>
    <div class="card">
      <h3>2. Mystère résolu</h3>
      <p>Hook chiffré (<strong>78M$</strong>) + promesse explicite : comprendre sans coder, sans équation.</p>
    </div>
    <div class="card">
      <h3>3. Utilité immédiate</h3>
      <p><strong>4 actions concrètes</strong> pour mieux prompter dès demain matin.</p>
    </div>
    <div class="card">
      <h3>4. Pédagogie sans condescendance</h3>
      <p>Accessible aux débutants. <strong>Respectable pour les experts.</strong></p>
    </div>
  </div>

  <div class="card dark">
    <h3 style="color:var(--gold)">Pourquoi pas un autre ?</h3>
    <p>Cybersecurity cible les CISO. GenAI cible les dirigeants. Maroc cible la MENA. Excellents — mais ciblés.</p>
    <p style="margin-top:8px">Le <strong>premier carrousel</strong> doit ouvrir le maximum de portes pour que les suivants atterrissent dans des feeds <em style="color:var(--orange)">déjà chauds</em>.</p>
  </div>
</section>

<!-- ═══════════════════════════════════════════ SETUP ═══════════════════════════════════════════ -->
<section>
  <h2>Le <em>setup</em> · à faire une fois</h2>

<pre><span class="accent">cd</span> D:\Generator\carousel_generator
<span class="accent">python</span> app.py
<span style="color:var(--muted)">→ http://localhost:5000 → Importer un fichier MD</span></pre>

  <table>
    <thead>
      <tr>
        <th>Fichier</th>
        <th>Thème LinkedIn</th>
        <th>Thème Instagram</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>chatgpt-gemini-claude-explication.md</code></td><td><strong>act_brand</strong> ou dark_blue</td><td><strong>ig_act_brand</strong> ou ig_ocean_deep</td></tr>
      <tr><td><code>ia-generative-80-pourcent-sans-impact.md</code></td><td><strong>act_brand</strong> ou dark_blue</td><td><strong>ig_act_brand</strong> ou ig_aurora_dark</td></tr>
      <tr><td><code>cybersecurite-2026-instabilite-permanente.md</code></td><td>dark_red ou crimson_tide</td><td>ig_aurora_dark</td></tr>
      <tr><td><code>maroc-hub-numerique-afrique-data-centers.md</code></td><td>kente_tech ou <strong>act_brand</strong></td><td>ig_sunset_vibes ou <strong>ig_act_brand</strong></td></tr>
      <tr><td><code>carousel-instagram-digital-morocco-2030.md</code></td><td><strong>act_brand</strong> ou dark_orange</td><td><strong>ig_act_brand</strong> ou ig_midnight_gold</td></tr>
    </tbody>
  </table>
  <p style="font-size:9.5pt;color:var(--muted)">Générer 2 versions par article (carré LinkedIn + vertical Instagram). Archiver les ZIP/PDF dans un dossier dédié.</p>
</section>

<!-- ═══════════════════════════════════════════ LANCEMENT VIRAL ═══════════════════════════════════════════ -->
<div class="page-break"></div>
<section>
  <h2>Lancement <em>viral</em> · Article #1</h2>
  <p><strong style="color:var(--orange)">AUJOURD'HUI vendredi 1er mai 2026 · publication à 14h00 précis.</strong> Plan en 5 vagues compressées sur 72h.</p>

  <h3>Vague 1 — Pré-publication <span style="color:var(--muted);font-size:11pt">(aujourd'hui 12h–13h45)</span></h3>
  <ul class="ds">
    <li><strong>12h</strong> · Story Instagram : extrait slide cover + sticker question <em>"Tu sais comment fonctionne ChatGPT ?"</em></li>
    <li><strong>13h</strong> · LinkedIn texte court sans visuel : <em>"Dans 1 heure, je publie ce que personne ne vous a expliqué simplement sur ChatGPT et Claude."</em></li>
    <li><strong>13h45</strong> · Story IG compte à rebours : sticker timer pour 14h00.</li>
  </ul>

  <h3>Vague 2 — Publication <span style="color:var(--muted);font-size:11pt">(aujourd'hui 14h00 PRÉCIS)</span></h3>
  <ul class="ds">
    <li><strong>LinkedIn</strong> · post + carrousel PDF, accroche en 3 lignes max + question ouverte.</li>
    <li><strong>Instagram feed</strong> · carrousel PNG (16 slides 1080×1350, thème <code>ig_act_brand</code>).</li>
    <li><strong>Instagram Story</strong> · 3 stories enchaînées (teaser → swipe vers feed → CTA blog).</li>
  </ul>

  <h3>Vague 3 — Amplification <span style="color:var(--muted);font-size:11pt">(aujourd'hui 14h30–22h)</span></h3>
  <ul class="ds">
    <li><strong>14h30</strong> · WhatsApp / Slack ACT : partage interne, booster les 90 premières minutes.</li>
    <li><strong>15h–17h</strong> · DM ciblés à 15–20 comptes max qui partagent réellement ce type de contenu.</li>
    <li><strong>14h–22h</strong> · Réponse à chaque commentaire dans les 30 min — l'algo LinkedIn pénalise le silence.</li>
    <li><strong>18h</strong> · Story IG : screenshots des premiers commentaires forts.</li>
  </ul>

  <h3>Vague 4 — Relance <span style="color:var(--muted);font-size:11pt">(samedi 2 mai + dimanche 3 mai)</span></h3>
  <ul class="ds">
    <li><strong>Samedi 9h</strong> · repost LinkedIn en thread, citer le post initial + ajouter une idée précise non couverte.</li>
    <li><strong>Samedi 12h</strong> · thread X / Twitter de 8 tweets reprenant les slides clés.</li>
    <li><strong>Dimanche 11h</strong> · story IG « les meilleurs commentaires de ce week-end ».</li>
  </ul>

  <h3>Vague 5 — Cross-canal <span style="color:var(--muted);font-size:11pt">(lundi 4 → mercredi 6 mai)</span></h3>
  <ul class="ds">
    <li><strong>Lundi 4 mai</strong> · Newsletter ACT, version longue avec lien blog.</li>
    <li><strong>Mardi 5 mai</strong> · Article LinkedIn (différent du post), version texte 1500 mots.</li>
    <li><strong>Mercredi 6 mai</strong> · enchaîner sur S2 — <code>ia-generative-80-pourcent-sans-impact</code>.</li>
    <li><em>Optionnel</em> · YouTube Short 60s — <em>"Pourquoi ChatGPT compte mal les R de strawberry"</em>.</li>
  </ul>
</section>

<!-- ═══════════════════════════════════════════ CAPTIONS ═══════════════════════════════════════════ -->
<div class="page-break"></div>
<section>
  <h2>Caption <em>LinkedIn</em> · Article #1</h2>
  <p style="color:var(--muted);font-size:10pt">Prête à publier. Copier-coller tel quel.</p>

<div class="card dark" style="font-family:'Poppins',sans-serif;font-size:10pt;line-height:1.7">
<p><strong style="color:var(--gold)">78 millions de dollars.</strong></p>
<p style="margin-top:10px">C'est ce qu'a coûté l'entraînement de GPT-4 — pour apprendre à faire UNE seule chose.</p>
<p style="margin-top:10px"><em style="color:var(--orange)">Prédire le mot suivant.</em></p>
<p style="margin-top:10px">Pas de base de données. Pas de règles écrites par des linguistes. Pas d'encyclopédie cachée.</p>
<p style="margin-top:10px">Juste une machine qui a lu une quantité obscène de texte et qui a appris quels mots se suivent.</p>
<p style="margin-top:10px">Et pourtant — ça rédige vos emails, débogue votre code, explique vos bilans.</p>
<p style="margin-top:10px">J'ai décortiqué les <strong style="color:var(--gold)">3 mécanismes</strong> que personne ne vous explique simplement :</p>
<p style="margin-top:6px">↓ Tokenisation<br>↓ Transformer<br>↓ Génération probabiliste</p>
<p style="margin-top:10px">Aucune équation. Aucune ligne de code. Juste les mécanismes.</p>
<p style="margin-top:10px">Quand vous comprenez ça, vous arrêtez d'être surpris par les hallucinations. Vous arrêtez d'attendre qu'une "prochaine version" les corrige. Vous promptez mieux. Vous architecturez vos workflows autour de la fenêtre de contexte.</p>
<p style="margin-top:10px">Bref — vous utilisez ces outils comme ils méritent de l'être.</p>
<p style="margin-top:10px">→ Carrousel complet ci-dessous.</p>
<p style="margin-top:14px;border-top:1px solid rgba(252,249,242,0.18);padding-top:10px"><em style="color:var(--orange)">Dr. Sohaib Baroud</em><br>Fondateur @ACT — Africa Centred Technology<br><span style="opacity:0.7">L'IA opérationnelle. Vraiment.</span></p>
<p style="margin-top:10px;font-size:9pt;opacity:0.6">#IA #ChatGPT #Claude #Gemini #LLM #IAgenerative</p>
</div>
</section>

<section>
  <h2>Caption <em>Instagram</em> · Article #1</h2>
<div class="card dark" style="font-family:'Poppins',sans-serif;font-size:10pt;line-height:1.7">
<p><strong style="color:var(--gold)">78 millions de dollars</strong> pour apprendre à prédire le mot suivant.</p>
<p style="margin-top:10px">C'est tout ce que GPT-4 sait faire.</p>
<p style="margin-top:10px">Et pourtant ça rédige vos emails, débogue votre code, explique vos bilans.</p>
<p style="margin-top:10px"><em style="color:var(--orange)">Comment ?</em></p>
<p style="margin-top:10px">→ Swipe pour comprendre les 3 mécanismes que personne ne vous explique simplement.</p>
<p style="margin-top:10px">Aucune équation. Aucune ligne de code. Juste les bases pour arrêter d'être surpris par ces outils.</p>
<p style="margin-top:10px">Sauvegardez ce post pour plus tard.</p>
<p style="margin-top:14px;border-top:1px solid rgba(252,249,242,0.18);padding-top:10px"><em style="color:var(--orange)">@sohaib.baroud</em> · Fondateur @act_africa<br><span style="opacity:0.7">L'IA opérationnelle. Vraiment.</span></p>
<p style="margin-top:10px;font-size:9pt;opacity:0.6">#IA #ChatGPT #Claude #Gemini #LLM #IAgenerative #TechAfrica #AI #PromptEngineering</p>
</div>
</section>

<!-- ═══════════════════════════════════════════ KPIs ═══════════════════════════════════════════ -->
<div class="page-break"></div>
<section>
  <h2>Les <em>KPIs</em> · Article #1</h2>
  <table>
    <thead>
      <tr>
        <th>Métrique</th>
        <th>Seuil minimum (24h)</th>
        <th>Seuil viral (72h)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>LinkedIn impressions</td><td>5 000</td><td><strong>50 000+</strong></td></tr>
      <tr><td>LinkedIn reactions</td><td>100</td><td><strong>1 000+</strong></td></tr>
      <tr><td>LinkedIn shares</td><td>10</td><td><strong>100+</strong></td></tr>
      <tr><td>LinkedIn comments</td><td>25</td><td><strong>250+</strong></td></tr>
      <tr><td>Instagram saves</td><td>50</td><td><strong>500+</strong></td></tr>
      <tr><td>Instagram shares</td><td>30</td><td><strong>300+</strong></td></tr>
      <tr><td>Tags spontanés</td><td>—</td><td>Indicateur de viralité organique</td></tr>
    </tbody>
  </table>

  <div class="card">
    <h4>Décision à 24h</h4>
    <ul class="ds">
      <li><strong>Seuil minimum atteint</strong> · continuer le calendrier S2 normalement.</li>
      <li><strong>Seuil minimum NON atteint</strong> · analyser le hook (3 premières lignes), envisager republication mardi S2 avec accroche différente, décaler les autres d'une semaine.</li>
    </ul>
  </div>
</section>

<!-- ═══════════════════════════════════════════ HOOKS S2-S5 ═══════════════════════════════════════════ -->
<section>
  <h2>Les <em>accroches</em> · S2 → S5</h2>
  <p>Hooks à adapter au moment de la rédaction des captions.</p>

  <div class="card">
    <h4>S2 — IA générative 80% sans impact</h4>
    <div class="quote-block">88% des entreprises utilisent l'IA. 80% n'en voient aucun impact mesurable. Voici ce que font les 20% qui réussissent.</div>
  </div>

  <div class="card">
    <h4>S3 — Cybersécurité 2026</h4>
    <div class="quote-block">+67% de surface d'attaque depuis 2022. La cybersécurité n'a plus de période de calme. Voici comment les meilleures équipes s'organisent.</div>
  </div>

  <div class="card">
    <h4>S4 — Maroc Hub Numérique</h4>
    <div class="quote-block">500 MW. Datacenter renouvelable. Dakhla. Le Maroc ne parle plus de transformation digitale — il la construit physiquement.</div>
  </div>

  <div class="card">
    <h4>S5 — Digital Morocco 2030</h4>
    <div class="quote-block">100 milliards de PIB grâce au numérique ? La 4e stratégie digitale du Maroc en 15 ans, décryptée sans complaisance.</div>
  </div>
</section>

<!-- ═══════════════════════════════════════════ WORKFLOW ═══════════════════════════════════════════ -->
<div class="page-break"></div>
<section>
  <h2>Le <em>workflow</em> récurrent · chaque semaine</h2>

  <table>
    <thead>
      <tr>
        <th>Quand</th>
        <th>Action</th>
        <th>Responsable</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>J-2</strong> dimanche soir</td><td>Générer le carrousel via <code>app.py</code>, archiver</td><td>Production</td></tr>
      <tr><td><strong>J-1</strong> lundi 21h</td><td>Story Instagram + post LinkedIn teaser</td><td>Social media</td></tr>
      <tr><td><strong>Jour J</strong> mardi/mercredi 9h</td><td>Publication LinkedIn + Instagram simultanée</td><td>Sohaib + Social media</td></tr>
      <tr><td><strong>J</strong> 12h–19h</td><td>Amplification (DM, réponses, relais interne)</td><td>Équipe complète</td></tr>
      <tr><td><strong>J+1</strong> 8h</td><td>Relance LinkedIn (thread) + X / Twitter</td><td>Sohaib</td></tr>
      <tr><td><strong>J+3</strong></td><td>Newsletter ACT + Article LinkedIn long-format</td><td>Production</td></tr>
      <tr><td><strong>J+5</strong></td><td>Bilan KPIs · ajustement S+1 si nécessaire</td><td>Sohaib + Production</td></tr>
    </tbody>
  </table>

  <div class="card dark">
    <h4 style="color:var(--gold)">Spécificité S1 — vendredi 1er mai 14h</h4>
    <p>Le workflow récurrent ci-dessus s'applique <strong>à partir de S2</strong>. Pour S1, le cycle est compressé sur la journée :</p>
    <ul class="ds" style="margin-top:8px">
      <li><strong>12h–13h45</strong> · pré-publication (story IG, teaser LinkedIn, compte à rebours)</li>
      <li><strong>14h00</strong> · publication LinkedIn + Instagram simultanée</li>
      <li><strong>14h30–22h</strong> · amplification & réponses commentaires</li>
      <li><strong>Sam–Dim</strong> · vague 4 (relances thread + X/Twitter)</li>
      <li><strong>Lun 4 → Mer 6 mai</strong> · vague 5 cross-canal puis enchaîner S2</li>
    </ul>
  </div>

</section>

<!-- ═══════════════════════════════════════════ COMMANDE ═══════════════════════════════════════════ -->
<section>
  <h2>Commande de <em>génération</em> immédiate</h2>

<pre><span class="accent">cd</span> D:\Generator\carousel_generator
<span class="accent">python</span> app.py
<span style="color:var(--muted)"># http://localhost:5000 → Importer un fichier MD</span>
<span style="color:var(--muted)"># Fichier : articles/chatgpt-gemini-claude-explication.md</span>
<span style="color:var(--muted)"># Thème : act_brand (LinkedIn) puis ig_act_brand (Instagram)</span>
<span style="color:var(--muted)"># → Générer</span></pre>

  <div class="card dark">
    <h3 style="color:var(--gold)">Et après ?</h3>
    <p>Une fois les KPIs S1 dans le vert, le calendrier S2–S5 enchaîne en pilote automatique. La cadence hebdomadaire installe la signature ACT dans les feeds qui comptent.</p>
    <p style="margin-top:10px"><em style="color:var(--orange)">L'IA opérationnelle. Vraiment.</em></p>
  </div>

  <div class="doc-footer">
    <img src="__LOGO_URI__" alt="ACT" style="width:140px;height:auto;margin-bottom:14px">
    <p class="signature">Dr. Sohaib Baroud — Fondateur <em>ACT</em></p>
    <p>Africa Centred Technology · Casablanca · Rabat · Dakar</p>
    <p style="margin-top:8px;font-size:8pt">Document interne · Diffusion équipe ACT · Confidentiel</p>
  </div>
</section>

</body>
</html>
"""


async def render_pdf():
    html_filled = HTML.replace("__LOGO_URI__", LOGO_DATA_URI)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_filled, wait_until="networkidle")
        # Laisser le temps aux Google Fonts de charger
        await page.wait_for_timeout(1500)
        OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
        # Ecrire dans un fichier temporaire puis remplacer (evite PermissionError si PDF ouvert dans un viewer)
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
        # PDF cible verrouille (ouvert dans un viewer). Garder le tmp et avertir.
        print(f"!! PDF cible verrouille (ferme-le dans le viewer). Version generee : {tmp}")
        return tmp
    return OUTPUT_PDF


def main():
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"-> Generation du PDF : {OUTPUT_PDF}")
    final = asyncio.run(render_pdf())
    size_kb = final.stat().st_size // 1024
    print(f"OK PDF genere ({size_kb} KB) : {final}")


if __name__ == "__main__":
    main()
