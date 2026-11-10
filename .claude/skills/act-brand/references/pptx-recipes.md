# ACT — Pptx recipes

Patterns Python prêts à copier pour produire des présentations PowerPoint conformes à la charte ACT,
avec la bibliothèque `python-pptx`.

**Avant d'utiliser ce fichier**, lire aussi `/mnt/skills/public/pptx/SKILL.md` qui couvre les bases
techniques de la création de fichier pptx.

---

## 1. Helpers réutilisables

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# === COULEURS ACT ===
ACT_ORANGE = RGBColor(0xD3, 0x54, 0x00)
ACT_GOLD   = RGBColor(0xF3, 0x9C, 0x12)
ACT_DARK   = RGBColor(0x0A, 0x14, 0x10)
ACT_GREEN  = RGBColor(0x1B, 0x30, 0x22)
ACT_CREAM  = RGBColor(0xFC, 0xF9, 0xF2)
ACT_MUTED  = RGBColor(0x6B, 0x7A, 0x72)
ACT_INK_S  = RGBColor(0x3A, 0x45, 0x40)

# === POLICES ===
# Substitution système : Lora→Georgia, Poppins→Calibri, JetBrains Mono→Consolas
FONT_DISPLAY = "Georgia"
FONT_BODY    = "Calibri"
FONT_MONO    = "Consolas"

# === DIMENSIONS 16:9 ===
SLIDE_W = Inches(13.333)   # 1920 px à 144 dpi
SLIDE_H = Inches(7.5)      # 1080 px à 144 dpi

def setup_presentation():
    """Initialise une présentation 16:9 ACT."""
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs

def set_slide_bg(slide, rgb_color):
    """Applique une couleur de fond pleine au slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = rgb_color

def add_diamond(slide, x, y, size, color=ACT_ORANGE):
    """Ajoute un losange (carré pivoté de -43.264°) à la position (x, y)."""
    sq = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Emu(size), Emu(size))
    sq.fill.solid()
    sq.fill.fore_color.rgb = color
    sq.line.fill.background()  # pas de contour
    sq.rotation = -43.264
    return sq

def add_text(slide, x, y, w, h, text, font=FONT_BODY, size=14, color=ACT_INK_S,
             bold=False, italic=False, align=PP_ALIGN.LEFT):
    """Ajoute une zone de texte avec mise en forme ACT."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)

    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    return tb

def add_text_with_accent(slide, x, y, w, h, text_main, text_accent, text_after="",
                         font=FONT_DISPLAY, size=44, base_color=ACT_CREAM,
                         accent_color=ACT_ORANGE, align=PP_ALIGN.LEFT):
    """Ajoute un texte multi-runs : partie normale + partie accent (italique orange)."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align

    if text_main:
        r1 = p.add_run()
        r1.text = text_main
        r1.font.name = font
        r1.font.size = Pt(size)
        r1.font.color.rgb = base_color

    r2 = p.add_run()
    r2.text = text_accent
    r2.font.name = font
    r2.font.size = Pt(size)
    r2.font.color.rgb = accent_color
    r2.font.italic = True

    if text_after:
        r3 = p.add_run()
        r3.text = text_after
        r3.font.name = font
        r3.font.size = Pt(size)
        r3.font.color.rgb = base_color

    return tb
```

---

## 2. Slide de couverture

Fond Dark, losange grand format, eyebrow Orange capitales, titre Lora avec mot-clé italique Orange,
sous-titre Poppins Light, logo ACT bas-droite.

```python
def add_cover_slide(prs, eyebrow, title_main, title_accent, subtitle, date_str):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    set_slide_bg(slide, ACT_DARK)

    # Losange grand
    add_diamond(slide, Inches(0.7), Inches(0.7), Emu(914400 * 0.7), ACT_ORANGE)

    # Eyebrow
    add_text(slide, Inches(0.7), Inches(2.5), Inches(8), Inches(0.4),
             text=eyebrow.upper(), font=FONT_BODY, size=12,
             color=ACT_ORANGE, bold=True)

    # Titre — main + accent en italique orange
    add_text_with_accent(slide,
        Inches(0.7), Inches(3.0), Inches(11), Inches(2.5),
        text_main=title_main + " ", text_accent=title_accent,
        font=FONT_DISPLAY, size=72, base_color=ACT_CREAM, accent_color=ACT_ORANGE)

    # Sous-titre
    add_text(slide, Inches(0.7), Inches(5.6), Inches(10), Inches(0.6),
             text=subtitle, font=FONT_BODY, size=18,
             color=ACT_CREAM, italic=False)

    # Pied : date à gauche, logo compact à droite
    add_text(slide, Inches(0.7), Inches(6.8), Inches(5), Inches(0.4),
             text=date_str.upper(), font=FONT_BODY, size=10,
             color=ACT_MUTED, bold=True)

    add_text(slide, Inches(8), Inches(6.8), Inches(5), Inches(0.4),
             text="ACT  ·  Africa Centred Technology",
             font=FONT_DISPLAY, size=11, color=ACT_MUTED, italic=True,
             align=PP_ALIGN.RIGHT)

    return slide
```

---

## 3. Slide de contenu (fond Cream)

```python
def add_content_slide(prs, eyebrow, title_main, title_accent, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, ACT_CREAM)

    # Eyebrow + losange
    add_diamond(slide, Inches(0.7), Inches(0.78), Emu(914400 * 0.12), ACT_ORANGE)
    add_text(slide, Inches(0.95), Inches(0.7), Inches(10), Inches(0.4),
             text=eyebrow.upper(), font=FONT_BODY, size=11,
             color=ACT_ORANGE, bold=True)

    # Titre
    add_text_with_accent(slide,
        Inches(0.7), Inches(1.2), Inches(11), Inches(1.2),
        text_main=title_main + " ", text_accent=title_accent,
        font=FONT_DISPLAY, size=40, base_color=ACT_DARK, accent_color=ACT_ORANGE)

    # Bullets
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(2.8), Inches(11), Inches(4))
    tf = tb.text_frame
    tf.word_wrap = True

    for i, item in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.space_after = Pt(12)

        # Diamant en début de ligne
        r_d = p.add_run()
        r_d.text = "◆  "
        r_d.font.name = FONT_BODY
        r_d.font.size = Pt(13)
        r_d.font.color.rgb = ACT_ORANGE
        r_d.font.bold = True

        # Texte
        r_t = p.add_run()
        r_t.text = item
        r_t.font.name = FONT_BODY
        r_t.font.size = Pt(18)
        r_t.font.color.rgb = ACT_INK_S

    return slide
```

---

## 4. Slide de transition (fond Green)

```python
def add_transition_slide(prs, chapter_num, chapter_title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, ACT_GREEN)

    # Numéro de chapitre énorme en italique gold
    add_text(slide, Inches(0.7), Inches(1.5), Inches(12), Inches(3),
             text=f"0{chapter_num}", font=FONT_DISPLAY, size=200,
             color=ACT_GOLD, italic=True)

    # Titre du chapitre
    add_text(slide, Inches(0.7), Inches(5.0), Inches(12), Inches(1.2),
             text=chapter_title, font=FONT_DISPLAY, size=44,
             color=ACT_CREAM)

    # Filet orange + ancrage géographique
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(0.7), Inches(6.4), Inches(2), Emu(914400 * 0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = ACT_ORANGE
    line.line.fill.background()

    add_text(slide, Inches(0.7), Inches(6.65), Inches(8), Inches(0.4),
             text="Casablanca  ·  Rabat  ·  Dakar",
             font=FONT_BODY, size=10, color=ACT_GOLD, bold=True)

    return slide
```

---

## 5. Slide chiffre-clé (impact)

Un seul chiffre, énorme, en Lora Italic Gold. Sous-titre en Poppins Light.

```python
def add_kpi_slide(prs, eyebrow, big_number, unit, description):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, ACT_DARK)

    # Eyebrow centré en haut
    add_text(slide, Inches(0.7), Inches(1), Inches(12), Inches(0.5),
             text=eyebrow.upper(), font=FONT_BODY, size=12,
             color=ACT_ORANGE, bold=True, align=PP_ALIGN.CENTER)

    # Chiffre énorme
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(2.2), Inches(12), Inches(3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER

    r_num = p.add_run()
    r_num.text = big_number
    r_num.font.name = FONT_DISPLAY
    r_num.font.size = Pt(220)
    r_num.font.color.rgb = ACT_GOLD
    r_num.font.italic = True

    r_unit = p.add_run()
    r_unit.text = unit
    r_unit.font.name = FONT_DISPLAY
    r_unit.font.size = Pt(80)
    r_unit.font.color.rgb = ACT_ORANGE
    r_unit.font.italic = True

    # Description
    add_text(slide, Inches(2), Inches(5.8), Inches(9), Inches(1),
             text=description, font=FONT_BODY, size=20,
             color=ACT_CREAM, align=PP_ALIGN.CENTER)

    return slide
```

---

## 6. Slide à 3 colonnes (comparatif, étapes, valeurs)

```python
def add_three_col_slide(prs, eyebrow, title_main, title_accent, columns):
    """columns = [{'title': str, 'desc': str}, x3]"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, ACT_CREAM)

    # En-tête
    add_diamond(slide, Inches(0.7), Inches(0.78), Emu(914400 * 0.12), ACT_ORANGE)
    add_text(slide, Inches(0.95), Inches(0.7), Inches(10), Inches(0.4),
             text=eyebrow.upper(), font=FONT_BODY, size=11,
             color=ACT_ORANGE, bold=True)

    add_text_with_accent(slide,
        Inches(0.7), Inches(1.2), Inches(11), Inches(1.2),
        text_main=title_main + " ", text_accent=title_accent,
        font=FONT_DISPLAY, size=36, base_color=ACT_DARK, accent_color=ACT_ORANGE)

    # 3 colonnes
    col_width = Inches(3.8)
    col_y = Inches(3.2)
    col_h = Inches(3.5)
    gap = Inches(0.3)

    for i, col in enumerate(columns[:3]):
        x = Inches(0.7) + (col_width + gap) * i

        # Numéro en grand italique gold
        add_text(slide, x, col_y, col_width, Inches(0.8),
                 text=f"0{i+1}", font=FONT_DISPLAY, size=44,
                 color=ACT_GOLD, italic=True)

        # Titre colonne
        add_text(slide, x, col_y + Inches(0.9), col_width, Inches(0.5),
                 text=col['title'], font=FONT_DISPLAY, size=20,
                 color=ACT_DARK, bold=False)

        # Description
        add_text(slide, x, col_y + Inches(1.5), col_width, Inches(2),
                 text=col['desc'], font=FONT_BODY, size=12,
                 color=ACT_INK_S)

    return slide
```

---

## 7. Exemple complet de présentation

```python
prs = setup_presentation()

# Couverture
add_cover_slide(prs,
    eyebrow="Proposition commerciale · 04/2026",
    title_main="Cadrage IA",
    title_accent="opérationnel.",
    subtitle="Diagnostic + roadmap 90 jours pour [Client]",
    date_str="Avril 2026")

# Sommaire / agenda
add_content_slide(prs,
    eyebrow="Agenda",
    title_main="Au programme,",
    title_accent="cinq temps.",
    bullets=[
        "Le contexte : pourquoi maintenant",
        "Notre diagnostic en 5 points",
        "La méthode ACT, en 3 phases",
        "Les livrables concrets",
        "Échéance, budget, équipe"
    ])

# Transition
add_transition_slide(prs, 1, "Le contexte")

# Chiffre clé
add_kpi_slide(prs,
    eyebrow="Le marché en un chiffre",
    big_number="38",
    unit="%",
    description="des grandes entreprises africaines déclarent ne pas savoir par où commencer leur transformation IA — étude HCP/IDC 2025")

# 3 colonnes
add_three_col_slide(prs,
    eyebrow="Notre approche",
    title_main="Trois phases,",
    title_accent="un même cap.",
    columns=[
        {"title": "Cadrer", "desc": "2 semaines pour identifier les use-cases qui produisent un ROI mesurable, et écarter ceux qui n'en produiront pas."},
        {"title": "Démontrer", "desc": "6 semaines pour construire un POC fonctionnel, qui valide la faisabilité technique et économique."},
        {"title": "Industrialiser", "desc": "12 semaines pour passer le POC en production, avec montée en compétence des équipes internes."}
    ])

prs.save("/mnt/user-data/outputs/ACT_PRES_Cadrage-IA_Client-X_20260428_v01.pptx")
```

---

## 8. Bonnes pratiques de design ACT

- **Une idée par slide.** Si on a deux idées, c'est deux slides.
- **30 % de blanc minimum.** Si le slide paraît "rempli", il l'est trop.
- **Maximum 5 bullets** par slide. Au-delà, séparer.
- **Italique orange sur 1-3 mots du titre.** Toujours. C'est la signature.
- **Numérotation des slides** : en bas à droite, Consolas 9 pt Muted, format `12 / 36`.
- **Pas de transitions animées entre slides** (fade simple acceptable, rien de plus).
- **Pas de clipart, jamais.** Les visuels sont des photos traitées (duotone) ou des schémas en SVG.
- **Logo ACT compact** en bas à droite des slides de contenu uniquement (pas sur les slides hero/transition).

---

## 9. Checklist de validation

Avant export final :

- [ ] Tous les slides utilisent FONT_DISPLAY (Georgia/Lora) pour les titres et FONT_BODY (Calibri/Poppins) pour le corps
- [ ] L'italique orange est appliqué sur 1-3 mots-clés du titre de chaque slide
- [ ] Les bullets utilisent le losange `◆` orange — jamais les puces natives PowerPoint
- [ ] Le ratio 60/30/10 des couleurs est respecté (l'orange ne sature pas)
- [ ] Aucun slide ne dépasse 70 % de remplissage visuel
- [ ] Le slide de couverture comporte eyebrow + titre + sous-titre + date + ancrage
- [ ] Le slide final comporte un CTA clair ou une ouverture à la discussion
- [ ] L'export PDF (si prévu) garde les caractères ◆ et les italiques orange — vérifier visuellement
- [ ] Le nom du fichier suit `ACT_PRES_..._YYYYMMDD_vXX.pptx`
