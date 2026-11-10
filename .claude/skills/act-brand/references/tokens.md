# ACT — Tokens de référence

Source de vérité unique pour toutes les valeurs techniques. Si une information dans cette page
contredit une autre référence, **cette page fait foi**. Les tokens machine sont dans
`assets/act-tokens.json`.

---

## 1. Couleurs

### Couleurs de marque

| Token | HEX | RGB | CMJN | Pantone | Rôle |
|---|---|---|---|---|---|
| `--act-orange`     | `#D35400` | `211, 84, 0`   | `0, 60, 100, 17` | 471 C | Primaire — CTA, accent, signature |
| `--act-orange-hot` | `#FF6B00` | `255, 107, 0`  | `0, 58, 100, 0`  | —     | Hover, accent secondaire |
| `--act-gold`       | `#F39C12` | `243, 156, 18` | `0, 36, 93, 5`   | —     | Chiffres-clés, premium, highlights |
| `--act-dark`       | `#0A1410` | `10, 20, 16`   | —                | —     | Fond principal digital |
| `--act-dark-deep`  | `#070E1C` | `7, 14, 28`    | —                | —     | Fond ultra-sombre (sections d'impact) |
| `--act-green`      | `#1B3022` | `27, 48, 34`   | —                | —     | Cartes, panneaux, fond secondaire |
| `--act-green-mid`  | `#2C4A35` | `44, 74, 53`   | —                | —     | Hover sur green, séparateurs |
| `--act-cream`      | `#FCF9F2` | `252, 249, 242`| —                | —     | Fond clair, texte sur dark |
| `--act-cream-deep` | `#F4EFE4` | `244, 239, 228`| —                | —     | Fond clair secondaire (cartes sur cream) |

### Neutres

| Token | HEX | Rôle |
|---|---|---|
| `--act-ink`       | `#0A1410` | Texte principal sur fond clair (= dark) |
| `--act-ink-soft`  | `#3A4540` | Texte secondaire sur fond clair |
| `--act-muted`     | `#6B7A72` | Texte tertiaire, légendes, métadonnées |
| `--act-line`      | `#D5CFBE` | Filets, séparateurs sur fond clair |
| `--act-line-soft` | `#E8E4D7` | Filets très discrets |

### Sémantiques

| Token | HEX | Rôle |
|---|---|---|
| `--act-success` | `#6ECF8A` | Validation, statut OK |
| `--act-warning` | `#F39C12` | Alerte modérée (= gold) |
| `--act-danger`  | `#C84B4B` | Erreur, à bannir, interdit |

### Conformité WCAG (vérifiée)

| Combinaison | Ratio | Statut | Usage |
|---|---|---|---|
| Cream sur Dark   | 16.5:1 | AAA | tout texte |
| Dark sur Cream   | 16.5:1 | AAA | tout texte |
| Orange sur Cream | 4.9:1  | AA  | tout texte normal |
| Orange sur Dark  | 3.5:1  | AA  | **texte large uniquement** (≥24px ou ≥18pt gras) |
| Gold sur Dark    | 7.4:1  | AAA | tout texte |
| Muted sur Cream  | 4.6:1  | AA  | tout texte normal |

⚠ **Ne jamais utiliser** Orange sur Dark pour du body text. Utiliser Cream ou Gold à la place.

### Règle des 60/30/10

- **60 %** — Dominante : Dark (digital) ou Cream (impression)
- **30 %** — Secondaire : Green + neutres gris
- **10 %** — Accent : Orange + Gold, jamais en aplat plein page

---

## 2. Typographies

### Familles officielles

**Lora** — *display, titres, citations, italique signature*
- Source : Google Fonts (libre)
- Import : `https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap`
- Graisses : 400, 500, 600, 700 (+ italiques)
- Fallback : `Georgia, 'Times New Roman', serif`

**Poppins** — *body, UI, labels, boutons*
- Source : Google Fonts (libre)
- Import : `https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap`
- Graisses : 300, 400, 500, 600, 700
- Fallback : `-apple-system, system-ui, Calibri, Arial, sans-serif`

**JetBrains Mono** — *code, données, monospace*
- Source : Google Fonts (libre)
- Import : `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap`
- Graisses : 400, 500
- Fallback : `Consolas, 'SF Mono', Menlo, monospace`

### Échelle typographique

| Niveau | Famille | Taille | Graisse | Line-height | Usage |
|---|---|---|---|---|---|
| H1 | Lora | clamp(48px, 8vw, 96px) | 500 | 1.0 | Titre de page |
| H2 | Lora | clamp(36px, 5vw, 56px) | 500 | 1.1 | Section principale |
| H3 | Lora | clamp(24px, 3vw, 32px) | 500 | 1.25 | Sous-section |
| H4 | Poppins | 18–20px | 600 | 1.3 | Titre de carte |
| Body Large | Poppins | 20px | 300 | 1.6 | Chapeau, intro |
| Body | Poppins | 16px | 400 | 1.6 | Texte courant |
| Caption | Poppins | 13px | 400 | 1.5 | Légendes |
| Eyebrow | Poppins | 11px | 600 | 1.4 | Surtitre, capitales, letter-spacing 0.24em, **orange** |
| Code | JetBrains Mono | 14–16px | 400 | 1.5 | Extraits techniques |

### Règles de composition

- **Letter-spacing** : −0.025em sur les gros titres Lora ; +0.18 à +0.24em sur les eyebrows et boutons en capitales.
- **Text-wrap balance** sur tous les H1/H2 (évite les veuves de fin de titre).
- **Italique orange Lora** : 1 à 3 mots-clés par titre maximum. C'est notre signature, elle ne doit pas saturer.
- **Capitales** : réservées aux eyebrows, boutons et labels courts (< 5 mots). Jamais de paragraphe en capitales.
- **Chiffres** : utiliser `font-variant-numeric: tabular-nums` dans les tableaux et data viz.

---

## 3. Logo

### Composition

Trois éléments :
1. **Losange orange** (`#D35400`) — carré tourné de −43,264° (angle exact, à conserver)
2. **Sigle « ACT »** en Lora Regular 500
3. **Mention « Africa Centred Technology »** en Poppins Medium 500, capitales mixtes, letter-spacing +40‰. Le mot **« Centred »** est en Lora Italic Orange.

### Tailles minimales

| Support | Version principale | Version compacte |
|---|---|---|
| Écran (web/mobile) | 32 px | 20 px |
| Impression | 12 mm | 8 mm |
| Favicon / app icon | — | 16×16 px (losange seul) |

### Zone de protection

Définie par la hauteur du losange, notée X :
- Marge supérieure et inférieure : 1 X
- Marges gauche et droite : 1.5 X

Aucun élément ne doit pénétrer cette zone (texte, autres logos, bord de page, élément graphique).

### Variantes officielles (cinq)

1. **Principale** — losange orange + texte noir, sur fond clair
2. **Monochrome foncé** — tout en `#0A1410`, sur fond très clair
3. **Monochrome inversé** — tout en `#FCF9F2`, sur fond très sombre
4. **Compact** — losange + sigle ACT seul (sans la mention), pour < 120 px de large
5. **Favicon** — losange seul, orange

### Interdits (jamais, sous aucune condition)

- Modifier les proportions (étirement, écrasement)
- Changer les couleurs hors des cinq versions
- Ajouter ombre portée, contour, biseau, dégradé, 3D
- Détourer ou recadrer le logo
- Faire tourner le logo (l'angle du losange est fixe)
- Remplacer la police, même par une proche
- Intégrer le logo dans une phrase comme s'il était un mot

---

## 4. Élément signature : le losange

### Construction

- **Forme** : carré parfait (1:1)
- **Rotation** : `-43.264deg` (angle exact, non négociable — issu de la version originale)
- **Tailles standards** : 10, 16, 24, 40, 64, 80 px
- **Couleurs autorisées** : Orange (par défaut), Gold, Cream, Dark
- **Variantes** : Plein (par défaut) · Outline 2px · Creux (couleur du parent)

### CSS minimal

```css
.act-diamond {
  display: inline-block;
  width: 10px; height: 10px;
  background: #D35400;
  transform: rotate(-43.264deg);
}
```

### Usages

- **Bullet point** des listes (remplace les puces classiques)
- **Avant les eyebrows** (surtitres) de section
- **Séparateur** entre items d'une marquee horizontale
- **Texture de fond** à très faible opacité (5 à 8 %)
- **Puce d'activation pulsante** dans les barres d'alerte
- **Favicon** — losange seul

---

## 5. Espacements

| Token | Valeur | Usage |
|---|---|---|
| `--act-space-xs`  | 4px   | Très petits gaps internes |
| `--act-space-sm`  | 8px   | Gap entre items proches |
| `--act-space-md`  | 16px  | Padding standard, gap modérés |
| `--act-space-lg`  | 24px  | Padding large, sections proches |
| `--act-space-xl`  | 40px  | Séparation entre blocs |
| `--act-space-2xl` | 64px  | Padding section vertical |
| `--act-space-3xl` | 96px  | Padding section large |
| `--act-space-4xl` | 144px | Hero, sections d'impact |

---

## 6. Identité de marque (textes officiels)

| Élément | Valeur |
|---|---|
| Nom court | **ACT** |
| Nom complet | **Africa Centred Technology** |
| Activité | Conseil, ingénierie & formation en Intelligence Artificielle |
| Baseline officielle | *« L'IA opérationnelle. Vraiment. »* |
| Baseline alt. 1 | *« Former. Déployer. Transmettre. »* |
| Baseline alt. 2 | *« L'expertise IA, à hauteur d'Afrique. »* |
| Villes d'ancrage | Casablanca · Rabat · Dakar |
| Séparateur villes | middle-dot ` · ` (espaces autour) |
| Archétype | Le Sage-Artisan |
| Adjectifs | Expert · Rigoureux · Ancré · Moderne · Chaleureux |

---

## 7. Nomenclature des fichiers

**Pattern unique** : `ACT_[TYPE]_[SUJET]_[CLIENT-ou-INTERNE]_[YYYYMMDD]_[vXX].[ext]`

### Codes [TYPE]

| Code | Usage |
|---|---|
| `DOC` | Document Word ou PDF |
| `PRES` | Présentation PowerPoint, Keynote |
| `VISU` | Visuel marketing (post, bannière, affiche) |
| `CODE` | Livrable technique |
| `CONTR` | Contrat, devis, document administratif |
| `RAPP` | Rapport (audit, benchmark, cadrage) |

### Exemples

```
ACT_PRES_Formation-IA_ATW-Maroc_20260415_v03.pptx
ACT_DOC_Charte-Graphique_INTERNE_20260420_v01.docx
ACT_VISU_LinkedIn-Ad_INTERNE_20260418_v02.png
ACT_CODE_POC-Agent-Support_Orange-Finances_20260412_v05.zip
ACT_RAPP_Audit-IA_Banque-X_20260330_v02.pdf
```
