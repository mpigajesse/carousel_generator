# Workflow détaillé — du fichier source au carousel généré

## Phase 1 — Lecture et analyse de l'article

1. **Localiser** le fichier `.md` source dans `ACT-PUBLICATION-RESEAUX/<categorie>/<NN-slug>/<slug>.md`.
2. **Lire** intégralement avec l'outil Read (un seul appel si possible).
3. **Extraire** dans un bloc de notes mental :
   - Titre + slug + catégorie (front matter)
   - Excerpt / chapeau
   - Liste ordonnée des sections H2 (titres + 1 phrase de résumé chacune)
   - Chiffres marquants avec leur source
   - Citations notables avec leur auteur
   - Conclusion / takeaway principal
   - URL source (`source_url`) — **uniquement pour ta référence interne**, jamais imprimée sur les slides

## Phase 2 — Décisions de format

| Décision | Critère |
|---|---|
| Plateforme | ≥ 3 chiffres OU ≥ 1 citation forte → Instagram, sinon LinkedIn. Demander confirmation si ambigu. |
| Nombre de slides | 1 cover + 1 hook + N sections + 1 synthèse + 1 CTA = 6-12 |
| Thème | Selon catégorie (voir `SKILL.md` Étape 6) — vérifier l'existence dans `themes.py` |
| Type par section | H2 explicatif → `content` ; H2 "X vs Y" → `compare` ; chiffre central → `stat` (IG) ; phrase choc → `quote` (IG) |

## Phase 3 — Plan détaillé (avant rédaction)

Pour chaque slide, noter :

| # | Type | Titre | Source dans l'article | Budget chars |
|---|---|---|---|---|
| 1 | cover | <titre court> | front matter `title` | titre 60 |
| 2 | content | Pourquoi ça compte | excerpt + 1ère phrase intro | 280 |
| 3 | content | <H2 #1> | section H2 #1 condensée | 280 |
| ... | ... | ... | ... | ... |
| n-1 | content | À retenir | conclusion | 280 |
| n | content/cta | Et vous ? | question ouverte (PAS de lien, PAS de hashtag) | 160 |

## Phase 4 — Rédaction

Pour chaque slide, dans l'ordre :
1. Écrire le titre (≤ 50 chars idéal)
2. Écrire le body en respectant le budget
3. Ajouter au max 2 `<span class="hl*">` sur les éléments importants
4. Ajouter `<span class="bold">` sur les têtes de liste si `<ul class="bullets">`
5. Vérifier le compte de chars du texte visible
6. Si dépassement → condenser (voir `budgets.md` patterns) ou scinder

## Phase 5 — Assemblage du fichier

Structure exacte du `.carousel.md` :

```
---
series: "..."
author: "@ACT"
title: "..."
---

# <Titre cover>

<!-- type:cover -->
<!-- badge:... -->
<!-- cta:... -->

---

## <Titre slide 2>

<body>

---

## <Titre slide 3>

<body>

---

...
```

Sauvegarde : `D:/Generator/carousel_generator/ACT-PUBLICATION-RESEAUX/<cat>/<NN-slug>/<slug>.carousel.md`

## Phase 6 — Validation finale

Parcourir la `quality-checklist.md` complète. Si une case n'est pas cochable, **corriger avant de livrer**.

## Phase 7 — Réponse utilisateur

Format de réponse :

```
Carousel construit pour <slug> :

- Fichier : <chemin complet>
- Plateforme : <LinkedIn 1080×1080 | Instagram 1080×1350>
- Slides : <N> (<n_cover> cover, <n_content> content, <n_compare> compare, ...)
- Thème suggéré : <nom_du_thème>

Pour générer :
1. python app.py
2. http://localhost:5000 → Importer un fichier MD
3. Coller / uploader <slug>.carousel.md
4. Thème : <nom_du_thème>, plateforme : <linkedin|instagram>
5. Générer
```

## Cas particuliers

### Article avec beaucoup de code

Si l'article contient des blocs de code (rare pour ACT mais possible pour `code-and-dev`) :
- Slides `cover` peuvent avoir un champ `code` (snippet ≤ 30 chars affiché en mono)
- Pour le code dans le body : `<code>token</code>` inline uniquement
- Les blocs multi-lignes : reformuler en prose courte ou screenshot externe

### Article très long (> 15 sections H2)

- Demander à l'utilisateur s'il veut un **carousel résumé** (10-12 slides) ou un **série** (2-3 carousels de 8-10 slides chacun, numérotés `Part 1/3`, `Part 2/3`...)
- Si série : produire un fichier `.carousel.md` par partie avec un `series` cohérent

### Article sans front matter complet

- Demander la catégorie si absente
- Déduire `series` du titre + contexte
- Author par défaut : `@ACT`
