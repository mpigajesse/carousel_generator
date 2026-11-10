# ACT — Templates d'application

Spécifications complètes pour produire les supports les plus fréquents : carte de visite,
signature email, post LinkedIn, bannière, livre blanc, newsletter, roll-up, goodies.

Pour chaque template, sont précisés : format, tokens, structure, et règles d'usage.

---

## 1. Carte de visite

### Format
- **Dimensions** : 85 × 55 mm (standard international)
- **Papier** : 350 g/m², finition mate
- **Finition recommandée** : vernis sélectif sur le losange uniquement (effet tactile subtil)

### Recto

| Zone | Contenu | Spécifications |
|---|---|---|
| Fond | Cream `#FCF9F2` plein | toute la surface |
| Logo (haut-gauche) | Logo principal horizontal | hauteur 8 mm, marge 8 mm |
| Losange (haut-droit) | Diamant orange | 6 × 6 mm, marge 8 mm |
| Nom (centre-bas) | Prénom Nom | Lora Medium 14 pt, couleur Dark |
| Fonction (sous le nom) | Titre du poste | Poppins Medium 9 pt, capitales, tracking +0,2 em, couleur Orange |
| Coordonnées (bas-gauche) | email, téléphone | Poppins Regular 8,5 pt, couleur Ink-soft |

### Verso

| Zone | Contenu | Spécifications |
|---|---|---|
| Fond | Dark `#0A1410` plein | toute la surface |
| Baseline (centré) | « L'IA opérationnelle. Vraiment. » | Lora Italic 20 pt couleur Cream, mot-clé en Orange |
| Sous-baseline | URL + villes | Poppins Regular 8 pt couleur Muted |
| Pied (centré) | Micro-losange Gold | 4 × 4 mm |

---

## 2. Signature email

### Format
- **Largeur totale** : 480 px maximum (s'affiche correctement sur mobile et desktop)
- **Format** : HTML inline (pas de CSS externe — pas supporté par tous les clients mail)

### Structure

```html
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Calibri, sans-serif; max-width: 480px;">
  <tr><td style="padding: 0;">
    <div style="font: 500 16px/1.2 Georgia, serif; color: #0A1410;">Prénom Nom</div>
    <div style="font: 600 10px/1 Calibri, sans-serif; letter-spacing: 0.2em; text-transform: uppercase; color: #D35400; margin-top: 4px;">Directrice conseil IA</div>
    <div style="width: 60px; height: 2px; background: #D35400; margin: 10px 0;"></div>
    <div style="font: 400 12px/1.4 Calibri, sans-serif; color: #0A1410; margin-bottom: 6px;">ACT &middot; <em style="font-family: Georgia, serif; color: #D35400;">Africa Centred Technology</em></div>
    <div style="font: 400 11px/1.5 Calibri, sans-serif; color: #6B7A72;">
      +212 6 XX XX XX XX &nbsp;<span style="color: #D35400;">◆</span>&nbsp; nom@act-tech.com<br>
      Casablanca &middot; Rabat &middot; Dakar
    </div>
    <div style="font: 400 8px/1.4 Calibri, sans-serif; color: #6B7A72; margin-top: 12px; opacity: 0.7;">
      [Mentions RGPD optionnelles]
    </div>
  </td></tr>
</table>
```

### Interdits

- Photo personnelle dans la signature
- Icônes de réseaux sociaux colorées et saturées (utiliser des icônes Lucide monochromes)
- Citations littéraires personnelles
- GIF animés
- Images embedded (utiliser uniquement HTML/CSS pour la robustesse cross-client)

---

## 3. Post LinkedIn — trois formats

### Format A : Citation (1080 × 1080 px)

| Zone | Contenu |
|---|---|
| Fond | Cream `#FCF9F2`, texture grain |
| Guillemet décor | Lora Italic 180 pt Orange, très haut, très gros — décoratif, pas lu |
| Citation | Lora 28 pt Dark — 1-3 mots-clés en italique Orange |
| Attribution + fonction | Poppins 11 pt Muted |
| Logo ACT compact | Bas-droite, taille 24 mm largeur |

### Format B : Visuel simple (1200 × 1200 px)

| Zone | Contenu |
|---|---|
| Fond | Dark `#0A1410` + pattern grille |
| Citation/accroche | Lora Italic 52 pt Cream avec mot-clé Orange |
| Auteur (bas) | Poppins 14 pt capitales Muted |
| Losange Gold + logo ACT compact | Bas-droite |

### Format C : Carrousel (1080 × 1350 px, 10 slides max)

| Slide | Contenu |
|---|---|
| 1 | Accroche forte, fond Dark, fond Orange pour le numéro de série |
| 2-9 | 1 idée = 1 slide, fond alterné Cream / Dark |
| 10 (final) | CTA clair + logo + URL ou handle |
| Pagination | « 01 / 10 » en Consolas 14 pt en bas |

### Texte d'accompagnement (post)

Voir `voice-and-tone.md > section 5.B`. Longueur cible : 800-1500 caractères. Toujours terminer
par 3-5 hashtags sobres : `#ACT #IA #[contexte spécifique]`. Pas plus.

---

## 4. Bannière LinkedIn

### Bannière entreprise

- **Format** : 1128 × 191 px (attention : LinkedIn affiche 1128 × 376 px sur desktop quand la photo
  de profil est en bas — prévoir une "safe zone" en haut)
- **Fond** : Dark + pattern constellation de losanges à gauche
- **Promesse courte** : Lora 44 pt Cream au centre-droit avec mot-clé Orange italique
- **Filet orange** sous la promesse (60 px large, 2 px haut)
- **Villes** : « Casablanca · Rabat · Dakar » en Poppins capitales 11 pt Gold

### Bannière collaborateurs

- **Format** : idem
- **Fond** : Dark, filet vertical orange à gauche (16 px large)
- **Texte centré** : Prénom + fonction
  - Prénom en Lora 36 pt Cream
  - Fonction en Lora Italic Orange 28 pt
- **Logo ACT compact** en bas à droite
- **Zone neutre au centre** pour éviter le recouvrement par la photo de profil

---

## 5. Livre blanc

### Couverture (A4 — 210 × 297 mm)

| Zone | Contenu |
|---|---|
| Fond | Dark `#0A1410` pleine page, texture grain 4% |
| Losange Gold (haut-droit) | 28 × 28 mm, marge 20 mm |
| Eyebrow (haut-gauche) | « LIVRE BLANC · 2026 » en capitales Orange Poppins 9 pt, letter-spacing 0,24em |
| Titre principal | Lora 52 pt Cream avec mot-clé Orange italique |
| Sous-titre | Poppins Light 18 pt Muted |
| Auteur(s) + ACT | Pied de page, Poppins 10 pt Muted capitales |

### Pages intérieures

- **Fond** : Cream `#FCF9F2`
- **Grille** : 12 colonnes, gouttière 5 mm
- **Marge extérieure** : 30 mm (respire, élégant)
- **Numéros de chapitre** : Lora Italic 72 pt Gold (décor en début de chapitre)
- **Chapeaux** : Lora 20 pt Dark
- **Corps** : Poppins 11 pt Ink-soft, interlignage 1,6
- **Citations remarquables** : pavé latéral avec filet orange à gauche, Lora Italic 16 pt Dark
- **Tableaux** : style ACT (en-tête Dark, lignes alternées Cream / Cream-deep)
- **Encadrés "À retenir"** : fond Cream-deep, filet orange à gauche, label « ◆ À RETENIR » Poppins capitales Orange

---

## 6. Newsletter

### Format
- **Largeur de colonne principale** : 600 px (standard email)
- **Fond** : Cream `#FCF9F2` (mode sombre du client mail : fallback sur Dark)

### Structure

| Bloc | Contenu |
|---|---|
| En-tête | Logo ACT centré, filet orange fin dessous (60 px, 2 px haut) |
| Eyebrow | « ACT · ÉDITION N° XX · DATE » en Poppins capitales Orange 10 pt |
| Titre principal | Lora 28 pt Dark, mot-clé en italique Orange |
| Chapeau | Poppins 16 pt Dark, 1 paragraphe |
| Sections de contenu | Filet orange à gauche (3 px), titre H3 Lora 18 pt, texte Poppins 14 pt |
| CTA bouton | Centré, fond Orange, texte Cream capitales Poppins 12 pt, padding 14×28 px |
| Footer | Adresse légale + lien désabonnement + villes, Poppins 10 pt Muted |

### Interdits

- Trop de visuels : maximum 2 images dans le corps, 1 par section
- Animations GIF
- Vidéos embed (utiliser un lien vers une miniature)
- Plus de 600 mots de texte total (au-delà, c'est un article qui mérite une page web)

---

## 7. Roll-up salon (kakémono)

### Format
- **Dimensions** : 85 × 200 cm (standard salon professionnel)
- **Impression** : bâche PVC, encre solvant ou latex
- **Lecture** : visible à 5+ mètres → typographie XXL

### Structure

| Zone (de haut en bas) | Contenu |
|---|---|
| Haut (0–40 cm) | Fond Dark + pattern grille, logo ACT grand format (hauteur 25 cm) |
| Milieu-haut (40–110 cm) | Accroche en Lora 120 pt Cream avec mot-clé Orange italique |
| Milieu-bas (110–160 cm) | 3 à 4 bullets en Poppins 32 pt Cream, losanges Orange |
| Bas (160–200 cm) | Fond Cream, QR code (5×5 cm) vers une landing dédiée + ville de l'événement + baseline en italique |

### Règles
- Lisible à 5 mètres → tester en réduisant l'image à 10 % et en se mettant à 1 m de l'écran
- Maximum **3 idées principales** sur le roll-up
- Toujours un **CTA clair** (QR code ou URL courte) en bas

---

## 8. Goodies

### T-shirt (coton bio, couleur Dark ou Cream)

- **Au dos** : losange orange grand format (10 × 10 cm) + baseline « L'IA opérationnelle. Vraiment. »
  en Lora Italic Cream (sur t-shirt Dark) ou Dark (sur t-shirt Cream)
- **Au cœur** (côté gauche poitrine) : logo ACT compact brodé, hauteur 25 mm
- **Éviter** les impressions intégrales : élégance = sobriété
- **Tailles** : grilles standardisées XS à 3XL, coupes hommes / femmes / unisexe

### Mug (céramique blanche ou noire mate)

- **Face 1** : logo ACT complet (largeur 80 mm)
- **Face 2** : un losange orange (40 × 40 mm) et la baseline en italique
- **Impression** : quadrichromie sublimation haute qualité, **pas** de sticker thermocollant
- **Lavable au lave-vaisselle** obligatoire (impression résistante)

### Sticker (vinyle découpé, finition mate)

| Variante | Dimension | Usage |
|---|---|---|
| Losange seul | 60 × 60 mm | Ordinateur portable, sticker discret |
| Logo complet | 100 × 40 mm | Voiture, vitrine, casque vélo |
| Baseline | 120 × 25 mm | Bumper, signature murale |

### Roll-up portable

Pour les événements sans matériel lourd :
- Format X-banner ou Y-banner 60 × 160 cm
- Reprendre la structure du roll-up standard, simplement réduite

### Notebook / carnet

- **Couverture** : Cream cartonnée, logo ACT débossé (sans encre), losange orange en bas-droite
- **Pages** : pointillées (style Bullet Journal) ou unies — pas de lignes lourdes
- **Format** : A5 standard
- **Reliure** : couture apparente ou spirale métallique noire

---

## 9. Page d'accueil site web

### Direction visuelle

- **Mode sombre par défaut** sur le site principal
- **Mode clair** disponible pour les landings de conversion
- Animations subtiles au scroll (fade-up, slight scale)
- Hero avec radial-gradient orange + radial-gradient vert + grille masquée (voir `web-recipes.md`)

### Wireframe condensé

```
[Top bar fine Orange — optionnelle, pour offres limitées]
[Nav principale glassmorphism léger sur fond Dark semi-transparent]

[HERO plein viewport]
  └─ Eyebrow + losange
  └─ Titre Lora XXL avec italique orange (clamp 54-112px)
  └─ Sous-titre Poppins 20 px
  └─ 2 CTA (primary orange + ghost cream)
  └─ Trust bar : logos clients, certifications

[3 BLOCS PAIN] — problèmes adressés (cards sombres, hover orange)

[3 BLOCS VALEUR] — ce que l'on apporte

[DÉTAIL PROGRAMME / SERVICES]
  └─ Carrousel ou onglets, fond alterné

[TÉMOIGNAGES]
  └─ Carrousel sur fond Green
  └─ 3 à 5 clients référents

[TARIFS / FORMULES]
  └─ 2-3 cartes
  └─ Recommandée mise en avant (badge Orange)

[FAQ repliable] — accordion

[FINAL CTA pleine largeur]
  └─ Fond Dark + pattern grille

[FOOTER minimal]
```

### Performance

- LCP < 2,5 s → préchargement des fonts critiques
- CLS < 0,1 → dimensions explicites pour toutes les images
- TBT < 200 ms → JavaScript minimal, défer pour les non-critiques
- Score Lighthouse cible : ≥ 90 en performance + accessibilité

---

## 10. Templates publicitaires

### LinkedIn Single Image Ad (1200 × 627 px)

- **Fond** : Dark + pattern grille
- **Promesse courte** (< 8 mots) en Lora 48 pt avec mot-clé Orange
- **CTA secondaire** en Poppins SemiBold 14 pt capitales Orange sous la promesse
- **Logo ACT** en bas à droite

### Google Display

| Format | Dimensions |
|---|---|
| Medium Rectangle | 300 × 250 |
| Leaderboard | 728 × 90 |
| Wide Skyscraper | 160 × 600 |
| Large Mobile Banner | 320 × 100 |

Règles :
- Utiliser la **version compacte du logo** (losange + ACT)
- **Une seule idée** par bannière. Pas de surcharge
- **CTA clair** avec fond Orange et texte Cream capitales
- **Animations discrètes** autorisées : fade-in progressif, jamais de clignotement agressif
- Poids du fichier ≤ 150 Ko (recommandation Google)
