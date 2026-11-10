# ACT — Docx recipes

Patterns Python prêts à copier pour produire des documents Word (et PDF par conversion) conformes
à la charte ACT, avec la bibliothèque `python-docx`.

**Avant d'utiliser ce fichier**, lire aussi `/mnt/skills/public/docx/SKILL.md` qui couvre les bases
techniques de la création de fichier docx.

**Note importante** : les polices Lora et JetBrains Mono ne sont pas installées par défaut sur Windows
ni sur Office 365. Pour les documents Word destinés à être édités par les équipes :
- **Titres** : utiliser **Georgia** (substitut système de Lora, présent partout)
- **Body** : utiliser **Calibri** (substitut système de Poppins, présent partout)
- **Mono** : utiliser **Consolas** (substitut système de JetBrains Mono)

Les couleurs ACT, le losange et l'italique orange restent identiques.

---

## 1. Helpers réutilisables (à copier en haut du script)

```python
from docx import Document
from docx.shared import Pt, RGBColor, Mm, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# === COULEURS ACT ===
ACT_ORANGE     = RGBColor(0xD3, 0x54, 0x00)
ACT_ORANGE_HOT = RGBColor(0xFF, 0x6B, 0x00)
ACT_GOLD       = RGBColor(0xF3, 0x9C, 0x12)
ACT_DARK       = RGBColor(0x0A, 0x14, 0x10)
ACT_GREEN      = RGBColor(0x1B, 0x30, 0x22)
ACT_CREAM      = RGBColor(0xFC, 0xF9, 0xF2)
ACT_INK_SOFT   = RGBColor(0x3A, 0x45, 0x40)
ACT_MUTED      = RGBColor(0x6B, 0x7A, 0x72)
ACT_LINE       = RGBColor(0xD5, 0xCF, 0xBE)

# === POLICES (substituts système Office) ===
FONT_DISPLAY = "Georgia"        # substitut de Lora
FONT_BODY    = "Calibri"        # substitut de Poppins
FONT_MONO    = "Consolas"       # substitut de JetBrains Mono

def set_cell_shading(cell, hex_color):
    """Applique un fond de couleur à une cellule de tableau."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)

def add_h1(doc, text, accent_words=None):
    """Titre H1 — Georgia 36pt, italique orange sur accent_words."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(16)
    p.paragraph_format.line_spacing = 1.05

    if accent_words:
        # Découpe et applique italique orange aux mots accentués
        words = text.split()
        for i, w in enumerate(words):
            run = p.add_run(w + (' ' if i < len(words)-1 else ''))
            run.font.name = FONT_DISPLAY
            run.font.size = Pt(36)
            run.font.color.rgb = ACT_DARK
            if w.strip('.,;:!?') in accent_words:
                run.font.italic = True
                run.font.color.rgb = ACT_ORANGE
    else:
        run = p.add_run(text)
        run.font.name = FONT_DISPLAY
        run.font.size = Pt(36)
        run.font.color.rgb = ACT_DARK
    return p

def add_h2(doc, text, accent_words=None):
    """Titre H2 — Georgia 24pt."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    if accent_words:
        for i, w in enumerate(text.split()):
            run = p.add_run(w + ' ')
            run.font.name = FONT_DISPLAY
            run.font.size = Pt(24)
            run.font.color.rgb = ACT_DARK
            if w.strip('.,;:!?') in accent_words:
                run.font.italic = True
                run.font.color.rgb = ACT_ORANGE
    else:
        run = p.add_run(text)
        run.font.name = FONT_DISPLAY
        run.font.size = Pt(24)
        run.font.color.rgb = ACT_DARK
    return p

def add_eyebrow(doc, text):
    """Surtitre — losange + Calibri 10pt capitales orange."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run_diamond = p.add_run('◆  ')
    run_diamond.font.name = FONT_BODY
    run_diamond.font.size = Pt(11)
    run_diamond.font.color.rgb = ACT_ORANGE
    run_diamond.font.bold = True

    run = p.add_run(text.upper())
    run.font.name = FONT_BODY
    run.font.size = Pt(9)
    run.font.color.rgb = ACT_ORANGE
    run.font.bold = True
    # Letter-spacing approché par espacement de caractères
    rPr = run._element.get_or_add_rPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:val'), '40')
    rPr.append(spacing)
    return p

def add_body(doc, text):
    """Paragraphe de corps — Calibri 11pt, ink-soft, line-height 1.5."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = FONT_BODY
    run.font.size = Pt(11)
    run.font.color.rgb = ACT_INK_SOFT
    return p

def add_bullet(doc, text):
    """Bullet point losange — utilise le losange Unicode (◆) au lieu de la puce native."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)

    run_d = p.add_run('◆  ')
    run_d.font.name = FONT_BODY
    run_d.font.size = Pt(8)
    run_d.font.color.rgb = ACT_ORANGE
    run_d.font.bold = True

    run = p.add_run(text)
    run.font.name = FONT_BODY
    run.font.size = Pt(11)
    run.font.color.rgb = ACT_INK_SOFT
    return p

def add_quote(doc, text):
    """Citation pull-quote — Georgia italique 14pt, indenté."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(16)
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.line_spacing = 1.4
    run = p.add_run(text)
    run.font.name = FONT_DISPLAY
    run.font.size = Pt(14)
    run.font.italic = True
    run.font.color.rgb = ACT_DARK
    return p
```

---

## 2. Mise en page A4 standard

```python
doc = Document()

# Marges A4 : 25mm haut/bas, 20mm gauche/droite
for section in doc.sections:
    section.top_margin = Mm(25)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(20)
    section.right_margin = Mm(20)
    section.page_height = Mm(297)
    section.page_width = Mm(210)
```

---

## 3. En-tête + pied de page ACT

```python
def add_act_header_footer(doc, doc_title="Document"):
    """En-tête avec losange + titre, pied avec mention + pagination."""
    section = doc.sections[0]

    # ─── EN-TÊTE ──────────────────────
    header = section.header
    h_para = header.paragraphs[0]
    h_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    run_d = h_para.add_run('◆  ')
    run_d.font.name = FONT_BODY
    run_d.font.size = Pt(10)
    run_d.font.color.rgb = ACT_ORANGE
    run_d.font.bold = True

    run = h_para.add_run(f'ACT  ·  {doc_title.upper()}')
    run.font.name = FONT_BODY
    run.font.size = Pt(8)
    run.font.color.rgb = ACT_MUTED
    run.font.bold = True

    # Filet orange sous l'en-tête
    p_fmt = h_para.paragraph_format
    pPr = h_para._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:color'), 'D35400')
    bottom.set(qn('w:space'), '4')
    pBdr.append(bottom)
    pPr.append(pBdr)

    # ─── PIED DE PAGE ──────────────────
    footer = section.footer
    f_para = footer.paragraphs[0]
    f_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = f_para.add_run('Africa Centred Technology  ·  Page ')
    run.font.name = FONT_DISPLAY
    run.font.size = Pt(9)
    run.font.color.rgb = ACT_MUTED
    run.font.italic = True

    # Numéro de page (champ Word)
    run_pg = f_para.add_run()
    fld_char1 = OxmlElement('w:fldChar')
    fld_char1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.text = 'PAGE'
    fld_char2 = OxmlElement('w:fldChar')
    fld_char2.set(qn('w:fldCharType'), 'end')
    run_pg._element.append(fld_char1)
    run_pg._element.append(instr)
    run_pg._element.append(fld_char2)
    run_pg.font.name = FONT_MONO
    run_pg.font.size = Pt(9)
    run_pg.font.color.rgb = ACT_ORANGE
    run_pg.font.bold = True
```

---

## 4. Couverture de document

```python
def add_act_cover(doc, eyebrow, title_main, title_accent, subtitle, date_str):
    """Page de couverture ACT."""
    # Espace haut
    for _ in range(3):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)

    # Losange grand
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run('◆')
    run.font.name = FONT_BODY
    run.font.size = Pt(72)
    run.font.color.rgb = ACT_ORANGE
    run.font.bold = True

    # Eyebrow
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(24)
    run = p.add_run(eyebrow.upper())
    run.font.name = FONT_BODY
    run.font.size = Pt(10)
    run.font.color.rgb = ACT_ORANGE
    run.font.bold = True
    rPr = run._element.get_or_add_rPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:val'), '60')
    rPr.append(spacing)

    # Titre — partie main + partie accent en italique orange
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.line_spacing = 1.0

    run_main = p.add_run(title_main + ' ')
    run_main.font.name = FONT_DISPLAY
    run_main.font.size = Pt(60)
    run_main.font.color.rgb = ACT_DARK

    run_acc = p.add_run(title_accent)
    run_acc.font.name = FONT_DISPLAY
    run_acc.font.size = Pt(60)
    run_acc.font.color.rgb = ACT_ORANGE
    run_acc.font.italic = True

    # Sous-titre
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    run = p.add_run(subtitle)
    run.font.name = FONT_DISPLAY
    run.font.size = Pt(16)
    run.font.color.rgb = ACT_MUTED
    run.font.italic = True

    # Filet orange + date
    for _ in range(8):
        doc.add_paragraph()

    p = doc.add_paragraph()
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '12')
    top.set(qn('w:color'), 'D35400')
    top.set(qn('w:space'), '12')
    pBdr.append(top)
    pPr.append(pBdr)

    p = doc.add_paragraph()
    run = p.add_run(date_str.upper())
    run.font.name = FONT_BODY
    run.font.size = Pt(9)
    run.font.color.rgb = ACT_MUTED
    run.font.bold = True

    p = doc.add_paragraph()
    run = p.add_run('Casablanca  ·  Rabat  ·  Dakar')
    run.font.name = FONT_DISPLAY
    run.font.size = Pt(11)
    run.font.color.rgb = ACT_ORANGE
    run.font.italic = True

    doc.add_page_break()
```

Usage type :
```python
add_act_cover(
    doc,
    eyebrow="Proposition commerciale",
    title_main="Cadrage IA",
    title_accent="opérationnel.",
    subtitle="Diagnostic + roadmap 90 jours pour la direction innovation de [Client]",
    date_str="Avril 2026"
)
```

---

## 5. Tableau ACT (en-tête sombre, lignes alternées)

```python
def add_act_table(doc, headers, rows):
    """Tableau ACT : en-tête fond Dark + texte Cream, body Calibri 10pt."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # En-tête
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_shading(cell, '0A1410')  # Dark
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        run = p.add_run(h.upper())
        run.font.name = FONT_BODY
        run.font.size = Pt(9)
        run.font.color.rgb = ACT_ORANGE
        run.font.bold = True

    # Lignes
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        for c_idx, value in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            run = p.add_run(str(value))
            run.font.name = FONT_BODY
            run.font.size = Pt(10)
            run.font.color.rgb = ACT_INK_SOFT

    return table
```

Usage :
```python
add_act_table(
    doc,
    ["Phase", "Durée", "Livrable"],
    [
        ["Cadrage", "2 semaines", "Note d'opportunité + roadmap"],
        ["POC", "6 semaines", "Démo fonctionnelle + retour ROI"],
        ["Industrialisation", "12 semaines", "Solution en production"]
    ]
)
```

---

## 6. Style global du document (à appliquer en fin de script)

```python
# Définition du style "Normal" par défaut
styles = doc.styles
normal = styles['Normal']
normal.font.name = FONT_BODY
normal.font.size = Pt(11)
normal.paragraph_format.line_spacing = 1.5
```

---

## 7. Conversion PDF (depuis le docx)

Pour produire un PDF à partir du docx, deux options :

**Option A — LibreOffice CLI (Linux/Mac/Windows)** :
```bash
soffice --headless --convert-to pdf document.docx
```

**Option B — Script python via le helper du skill docx** :
```python
import subprocess
subprocess.run([
    'soffice', '--headless', '--convert-to', 'pdf',
    '--outdir', '/mnt/user-data/outputs/',
    'document.docx'
], check=True)
```

---

## 8. Validation finale

Avant de livrer un document Word ACT :

- [ ] La couverture comporte le losange + eyebrow + titre avec italique orange + ancrage géographique
- [ ] L'en-tête contient `◆ ACT · [TITRE]` aligné à droite avec filet orange
- [ ] Le pied de page numérote en `Consolas Orange` au format `Page X`
- [ ] Les bullets utilisent le losange `◆` orange (pas de puces classiques `•`)
- [ ] Les couleurs respectent : fond cream, texte ink-soft, accents Orange/Gold
- [ ] Aucun titre n'utilise de typo autre que Georgia (= Lora substitut)
- [ ] Le nom du fichier suit la nomenclature `ACT_DOC_..._YYYYMMDD_vXX.docx`
- [ ] Si conversion PDF prévue : tester l'export pour vérifier que les couleurs et caractères spéciaux passent (◆ notamment)
