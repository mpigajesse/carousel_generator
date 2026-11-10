# ACT — Système visuel

Au-delà des couleurs et typographies, ACT dispose d'un vocabulaire visuel signature. Cette référence
détaille tous les éléments graphiques non typographiques : losange, patterns, traitement photo, data viz,
icônes, illustrations.

---

## 1. Le losange — élément signature

### Identité

Le losange n'est pas un élément décoratif — c'est la **ponctuation visuelle** d'ACT. Sa présence
discrète mais systématique signe nos supports sans que le logo ait besoin d'être présent.

### Spécifications techniques

| Caractéristique | Valeur |
|---|---|
| Forme | Carré parfait (1:1) |
| Rotation | **−43,264°** exactement (non négociable) |
| Couleur par défaut | Orange `#D35400` |
| Couleurs autorisées | Orange, Gold `#F39C12`, Cream `#FCF9F2`, Dark `#0A1410` |
| Tailles standards | 10 · 16 · 24 · 40 · 64 · 80 px |
| Variantes | Plein (défaut) · Outline 2px · Creux (couleur du parent) |

### Implémentation

**HTML/CSS :**
```html
<span class="act-diamond"></span>
```
```css
.act-diamond {
  display: inline-block;
  width: 10px; height: 10px;
  background: #D35400;
  transform: rotate(-43.264deg);
}
```

**SVG (autonome, sans CSS) :**
```html
<svg viewBox="0 0 24 24" width="10" height="10">
  <g transform="translate(12 12) rotate(-43.264)">
    <rect x="-5" y="-5" width="10" height="10" fill="#D35400"/>
  </g>
</svg>
```

**Caractère Unicode (fallback texte uniquement)** : `◆` (U+25C6).
À utiliser **seulement** quand on ne peut pas générer une vraie forme (signature email texte simple,
post LinkedIn texte). Dans tout autre contexte, utiliser le losange réel CSS/SVG.

### Usages canoniques

- **Bullet point** des listes (remplace les puces classiques)
- **Avant les eyebrows** (surtitres) de section
- **Séparateur** entre items d'une marquee horizontale
- **Texture de fond** à très faible opacité (5–8 %)
- **Puce d'activation pulsante** dans les barres d'alerte
- **Favicon** — losange seul, format 16×16 px ou plus
- **Élément de signature** discret en bas à droite des cartes, posters, slides

### Ce qu'il ne faut pas faire

- Faire pivoter à un autre angle (l'angle est fixe à −43,264°)
- Le déformer (proportions 1:1 strictes)
- L'aligner sans rotation (ce serait un carré, pas un losange)
- Ajouter un contour gris ou neutre (les outlines doivent être en couleur de marque)
- L'utiliser à des tailles non-standard (en dehors de 10/16/24/40/64/80 px)
- L'utiliser en très grande taille comme aplat de fond (perd son rôle de ponctuation)

---

## 2. Patterns signature

Trois patterns officiels, à utiliser pour donner de la matière sans bruit visuel.

### Pattern « Grille ACT »

**Description** : grille fine orthogonale, 80×80 px, trait 1 px, opacité 2.5 %.

**Usage** : fonds de section hero, fonds de carte sombre, en-têtes de slide impact.

**CSS** :
```css
background-image:
  linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
background-size: 80px 80px;
mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 75%);
```

Sur fond clair, remplacer `rgba(255,255,255,0.025)` par `rgba(10,20,16,0.04)`.

### Pattern « Constellation de losanges »

**Description** : semis irrégulier de losanges à différentes tailles (6 à 16 px) et opacités
(15 à 40 %), tous orientés au même angle de −43,264°.

**Usage** : fonds de carte, textures de remplissage, transitions de slide, posters.

**Implémentation** : positionner manuellement 6 à 12 losanges en CSS absolute ou en SVG.

### Pattern « Grain éditorial »

**Description** : bruit fractal subtil en overlay sur les fonds pleins. 4 % d'opacité, blend
mode `overlay`. Apporte une matière "papier" qui éloigne des aplats digitaux trop parfaits.

**SVG inline** :
```html
<div style="position: relative;">
  <!-- contenu -->
  <div style="position: absolute; inset: 0; pointer-events: none;
              background-image: url('data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'256\' height=\'256\'%3E%3Cfilter id=\'n\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.85\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23n)\'/%3E%3C/svg%3E');
              background-size: 160px 160px;
              opacity: 0.04; mix-blend-mode: overlay;"></div>
</div>
```

### Combinaisons recommandées

- **Hero web** : Dark + Grille + radial-gradient orange + radial-gradient vert
- **Couverture livre blanc** : Dark + Grain + losange Gold haut-droit
- **Slide transition PPT** : Green + Constellation + numéro chapitre Lora Italic Gold

---

## 3. Iconographie

### Style

ACT utilise des icônes **outline** uniformes :

- Trait constant, pas de remplissage par défaut
- Grille 24×24 px, padding 2 px intérieur
- Épaisseur de trait 1.5 px (icônes ≤ 24 px) ou 2 px (≥ 32 px)
- Coins arrondis 2 px (`stroke-linejoin: round`)
- Extrémités arrondies (`stroke-linecap: round`)

### Bibliothèque recommandée

**Lucide Icons** — `lucide.dev` — gratuite, open source, 1 000+ icônes cohérentes.

```html
<!-- Exemple d'inclusion (CDN) -->
<script src="https://unpkg.com/lucide@latest"></script>
<i data-lucide="check-circle"></i>
<script>lucide.createIcons();</script>
```

### Variantes

- **Outline** : par défaut
- **Filled** : uniquement pour l'état actif/sélectionné
- **Duotone** : interdit (rappelle trop les esthétiques génériques 2020)

### Couleurs autorisées pour les icônes

- Cream `#FCF9F2` ou Dark `#0A1410` selon le fond
- Orange `#D35400` pour signaler une action
- Muted `#6B7A72` pour les icônes secondaires

---

## 4. Style illustratif — « Terres & signaux »

### Direction artistique

Les illustrations ACT mêlent **formes géométriques simples** (extension du losange) et
**textures organiques** (référence à la terre, au bois, au tissu).

### À rejeter explicitement

- Cerveaux stylisés
- Circuits imprimés
- Robots humanoïdes
- Hologrammes bleus
- Ondes cosmiques génériques
- Visages 3D rendus IA
- Globes filaires "tech corporate"

Toute génération qui dérive vers ces clichés est à recommencer.

### Principes

- Formes géométriques simples (cercles, losanges, arcs) en compositions abstraites
- Palette restreinte : maximum 3 couleurs ACT par illustration
- Espace négatif structuré, partie intégrante de la composition
- Texture grain discrète sur les aplats (2–4 % d'opacité — feel print)
- Pas d'effets 3D ni de rendus photo-réalistes IA

---

## 5. Photographie

### Direction

- **Lumière naturelle** privilégiée — pas de studio lisse et surexposé
- **Sujets réels** : équipes, lieux, ateliers en situation — pas de stock photo générique
- **Cadrages éditoriaux** : légèrement décalés, pas de composition frontale symétrique

### Post-traitement standard

| Réglage | Valeur |
|---|---|
| Contraste | +10 à +15 |
| Saturation | −10 à −20 (légèrement désaturée) |
| Grain | Léger grain photographique (simulation Kodak Portra 400) |
| Balance des blancs | +200 K (légèrement chaude) |

### Traitement duotone (signature campagne)

Pour les visuels de campagne forte (couvertures de livres blancs, bannières LinkedIn, affiches
d'événement), appliquer un duotone qui unifie des photos d'origine disparate :

- **Zones sombres** : Dark `#0A1410`
- **Zones claires** : Orange `#D35400` ou Cream `#FCF9F2`

Implémentation Photoshop : `Image > Adjustments > Duotone`. Implémentation web : filtre CSS
ou overlay multiply.

---

## 6. Data visualisation

### Principes généraux

- **Typographie monospace** (JetBrains Mono) pour tous les chiffres et axes
- **Palette restreinte** : Orange + Gold + Dark + Cream. **Jamais** d'arc-en-ciel, jamais de palette
  pastel pré-fabriquée d'Excel ou de PowerPoint
- **Fonds transparents** ou Cream — pas de fonds gris clairs Excel
- **Grilles** à 8 % d'opacité maximum. Les données ressortent, pas les cadres
- **Légendes** en Poppins 11–12 px, gris moyen. **Labels directs sur les courbes** quand possible
  (évite le va-et-vient œil ↔ légende)

### Types de graphiques préférés

| Cas d'usage | Type recommandé |
|---|---|
| Comparaison catégories nominales | Barres **horizontales** (pas verticales : meilleure lisibilité des labels) |
| Série temporelle | Lignes avec aire dégradée faible (≤ 20 %) |
| Répartition (parts) | **Donut** plutôt que camembert, avec chiffre central en Lora Italic Orange |
| Densité bivariée | Heatmap en dégradé Cream → Orange (jamais rouge/vert : exclut les daltoniens) |
| Comparaison multi-série | Barres groupées, max 3 séries (Orange + Gold + Muted) |

### Couleurs sémantiques en data viz

- **Orange** : la valeur principale, la métrique d'intérêt
- **Gold** : valeur de comparaison ou benchmark
- **Cream / blanc** : axes, grille
- **Muted** : labels secondaires
- **Success `#6ECF8A`** : tendance positive ponctuelle
- **Danger `#C84B4B`** : tendance négative ponctuelle

### Anti-patterns en data viz

- Camemberts à 5+ tranches (illisibles)
- Barres 3D (trompeuses)
- Axes Y tronqués sans avertissement (manipulent le lecteur)
- Couleurs arc-en-ciel sur série continue
- Légendes en haut à droite (l'œil les rate, préférer labels directs)

---

## 7. Schémas et diagrammes techniques

Pour les schémas d'architecture, organigrammes, diagrammes de flux :

- **Boîtes** : rectangles cream sur fond dark (ou inverse), filet 1 px Orange `#D35400`
- **Connecteurs** : 2 px solid, couleur Muted `#6B7A72`
- **Flèches** : tête simple, taille 8–10 px
- **Titres de boîte** : Poppins SemiBold 14 px
- **Légendes de boîte** : Poppins Regular 11 px Muted
- **Mise en page** : grille 8 px, alignements stricts
- **Outils recommandés** : Excalidraw (style brouillon-pro), tldraw, Figma

---

## 8. Logo ACT — rappel rapide

Pour le détail complet, voir `tokens.md > section 3`. Rappels critiques :

- Trois éléments : losange Orange (-43.264°) · sigle « ACT » Lora · mention « Africa **Centred** Technology » Poppins avec « Centred » Lora Italic Orange
- Tailles minimales : 32 px (écran), 12 mm (print), 16 px (favicon)
- Zone de protection : 1× hauteur losange autour
- Cinq variantes officielles : Principale · Mono foncé · Mono inversé · Compact · Favicon
- Ne **jamais** : déformer, recolorer, faire tourner, ombrer, dégrader, biseauter

L'asset SVG officiel est dans `assets/logo.svg`.
