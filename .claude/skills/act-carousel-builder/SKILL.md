---
name: act-carousel-builder
description: >
  Convertit les articles ACT (D:/Generator/carousel_generator/ACT-PUBLICATION-RESEAUX/<categorie>/<nn-slug>/<slug>.md)
  en Markdown structuré prêt à être importé dans le Carousel Generator (app Flask) pour produire un carousel
  LinkedIn (1080×1080, types cover/content/compare) ou Instagram (1080×1350, types cover/content/compare/quote/stat/cta).
  Déclencher pour : "fais un carousel à partir de cet article", "transforme cet article en carousel",
  "génère le MD carousel pour <slug>", "structure cet article pour l'import MD", "carousel ACT".
  Le skill applique les budgets de caractères du `_calculate_text_size`, choisit les bons types de slides,
  écrit un fichier `<slug>.carousel.md` à côté de l'article source, et donne la commande d'import.
---

# ACT Carousel Builder

Ce skill transforme un article rédigé selon la méthode `act-blog-writer` en **Markdown carousel** que `md_parser.py` va parser correctement et que `generate.py` va rendre en carousel sans débordement de texte.

## Objectifs non négociables

1. **Aucun débordement de texte** — chaque slide respecte les budgets caractères de `_calculate_text_size`.
2. **Aucun fait inventé** — uniquement reformuler, condenser, structurer ce qui est dans l'article source.
3. **Aucune perte de chiffres ni de sources** — chaque chiffre cité doit avoir sa source dans la slide ou dans la dernière slide "Sources".
4. **Format compatible parser** — séparateurs `---` entre slides, front matter YAML pour le footer, balises HTML inline supportées (`<span class="bold|hl1|hl2|hl3">`, `<ul class="bullets"><li>`, `<br>`).
5. **Aucun hashtag dans le contenu des slides** — pas de `#IA`, `#GenAI`, etc. Les hashtags sont réservés aux **captions** des posts LinkedIn/Instagram, jamais imprimés sur les slides du carrousel.
6. **Aucun lien web ni domaine sur les slides** — pas de `a-ct.ma`, `a-ct.ma/blog`, URLs externes ou sous-domaines. Le carrousel doit fonctionner **sans dépendance externe** : le lecteur reste sur le visuel, le call to action est conversationnel (commentaire, partage), pas un renvoi vers un site tiers.

---

## Étape 0 — Identifier la source

Le skill est déclenché avec un chemin ou un slug. Localiser le fichier :

```
D:/Generator/carousel_generator/ACT-PUBLICATION-RESEAUX/<categorie>/<NN-slug>/<slug>.md
```

Front matter d'un article ACT : `title`, `slug`, `category`, `format`, `author`, `date`, `read_time`, `excerpt`, `keywords`, `featured_image`, `source_url`.

Si plusieurs articles correspondent ou si le slug est ambigu, **demander** avant de produire.

---

## Étape 1 — Choisir la plateforme

| Plateforme | Format slide | Types disponibles | Idéal pour |
|---|---|---|---|
| **LinkedIn** | 1080×1080 | `cover`, `content`, `compare` | Analyses, articles longs, comparatifs B2B |
| **Instagram** | 1080×1350 | `cover`, `content`, `compare`, `quote`, `stat`, `cta` | Articles à fort potentiel visuel, listes, citations, statistiques marquantes |

**Règle par défaut** : si l'article contient ≥ 3 chiffres marquants ou ≥ 1 citation, proposer **Instagram** (slides `stat` et `quote` exploitent ces éléments). Sinon **LinkedIn**.

Toujours **annoncer** la plateforme retenue avant d'écrire et permettre à l'utilisateur de basculer.

---

## Étape 2 — Plan de slides

Cibler **8 à 12 slides** (jamais moins de 6, jamais plus de 12).

Schéma standard :

| # | Slide | Rôle |
|---|---|---|
| 1 | `cover` | Titre accrocheur de l'article + badge catégorie |
| 2 | `content` | Hook : pourquoi le sujet importe (extrait du chapeau / excerpt) |
| 3..n-2 | `content` / `compare` / `stat` / `quote` | Une slide par section H2 majeure de l'article |
| n-1 | `content` ou `cta` | Synthèse / 3 takeaways |
| n | `content` ou `cta` | **Question ouverte au lecteur** (engagement commentaire) — **pas de lien**, **pas de hashtag**, **pas de mention de blog** |

Mapping des sections de l'article :

- Section H2 explicative → `content` (LinkedIn) ou `content`/`stat` (Instagram si chiffre central)
- Section H2 du type "X vs Y" → `compare`
- Citation ou phrase choc isolée → `quote` (Instagram uniquement)
- Section "Top N" / liste numérotée → 1 `content` par item OU 1 `content` global avec `<ul class="bullets">`

---

## Étape 3 — Budgets de caractères (CRITIQUE)

`generate.py::_calculate_text_size` mappe le nombre de caractères du `body` vers une taille de police. Pour rester confortable et lisible :

| Type | Budget body (chars) | text_size visé |
|---|---|---|
| `cover` | titre ≤ 60, body absent ou ≤ 120 | titre 96px |
| `content` | **≤ 280 chars** (idéal), 280-380 (compact), > 400 = redécouper | 42px / 38px |
| `compare` | par colonne ≤ 140 chars (compté ×1.5 par le calculateur) | 36-40px |
| `quote` (IG) | ≤ 200 chars | 48px |
| `stat` (IG) | `value` ≤ 8 chars, `label` ≤ 40 chars, max 3 stats | – |
| `cta` (IG) | body ≤ 160 chars | 40px |

**Règle d'or** : compter le body **après conversion HTML** (les balises `<span>`, `<ul>`, `<li>`, `<br>` ne comptent pas dans le rendu visible mais comptent dans le calcul interne — donc les minimiser).

Si une section dépasse → la **scinder** en deux slides avec sous-titres explicites.

---

## Étape 4 — Style visuel et balises supportées

Body HTML accepté (LinkedIn et Instagram) :

- `<span class="bold">mot</span>` — gras avec contraste accentué
- `<span class="hl1">…</span>` `<span class="hl2">…</span>` `<span class="hl3">…</span>` — surlignage avec accents 1/2/3 du thème
- `<ul class="bullets"><li>point</li></ul>` — liste à puces stylisée
- `<br>` ou `<br><br>` — saut de ligne (préférer `<br><br>` pour aérer)
- `<code>token</code>` — code inline (police mono)

**Règles de mise en valeur** :

1. Maximum **2 surlignages** (`hl1/hl2/hl3`) par slide — sinon plus rien ne ressort.
2. **1 seul thème de couleur** par carousel (cohérence visuelle) — choisir selon la catégorie de l'article (voir Étape 6).
3. Les `<ul class="bullets">` : 3 à 5 items max par slide, chaque item ≤ 80 chars.
4. Pas de Markdown (`**`, `*`, ``` `` ```) dans le body — toujours le HTML inline. Le parser Markdown amont casse certains contextes.

---

## Étape 5 — Front matter du carousel

Toujours commencer le fichier `.carousel.md` par :

```yaml
---
series: "<Catégorie ACT>"
author: "@Sohaib Baroud"
title: "<Titre court ≤ 50 chars dérivé du title de l'article>"
---
```

`series` : reprendre `category` de l'article (`Africa Focus`, `Data & IA`, `Cybersecurity`, etc.).
`author` : **toujours `@Sohaib Baroud`** — fondateur d'ACT, signataire unique des publications. Ne jamais utiliser `@ACT`, `@username` ou un autre alias.
`title` : titre court qui rentre dans le badge cover.

---

## Étape 6 — Identité ACT et choix du thème

### Couleurs de marque ACT (référence : skill `act-brand`)

Source de vérité : `.claude/skills/act-brand/assets/act-tokens.json`. À garder en tête lors du choix de thème pour assurer la cohérence visuelle avec les autres supports ACT.

| Token | Hex | Rôle |
|---|---|---|
| **Orange** (primaire) | `#D35400` | CTA, accents, italique signature |
| Orange Hot (hover) | `#FF6B00` | Hover, accent secondaire |
| **Gold** | `#F39C12` | Chiffres-clés, premium, highlights |
| **Dark** (fond digital) | `#0A1410` | Fond principal digital |
| Dark Deep | `#070E1C` | Sections d'impact |
| **Green** (panneaux) | `#1B3022` | Cartes, fond secondaire |
| Green Mid | `#2C4A35` | Hover, séparateurs |
| **Cream** (fond clair) | `#FCF9F2` | Fond clair, texte sur dark |
| Cream Deep | `#F4EFE4` | Fond clair secondaire |

**Règles immuables ACT** (extraites de `act-brand`) :
- Ratio **60/30/10** : 60% dominante (Dark ou Cream), 30% secondaire (Green + gris), 10% accent (Orange + Gold)
- L'orange n'est **jamais un aplat plein page**
- Italique orange sur **1-3 mots-clés max** par titre
- Pas de bleu corporate, pas d'iconographie Silicon Valley générique
- Ancrage géographique sur supports marketing : *Casablanca · Rabat · Dakar*

Pour toute production éditoriale en parallèle (post LinkedIn, email d'annonce du carousel), invoquer `act-brand` pour le ton et `act-humanizer` pour finaliser.

### Thèmes existants dans `themes.py` (vérifié — ne JAMAIS inventer)

**LinkedIn** (1080×1080) — 32 thèmes :
- *Couleur* : `dark_purple`, `dark_blue`, `dark_green`, `dark_red`, `dark_orange`, `midnight_ocean`, `sunset_glow`, `neon_tokyo`, `emerald_city`, `cyber_punk`, `arctic_frost`, `golden_aura`, `lavender_dream`, `forest_night`, `crimson_tide`, `cosmic_void`, `tropical_breeze`, `volcanic_fire`, `aurora_borealis`, `kente_tech`
- *Neutres (11)* : `neutral_charcoal` (dark), `neutral_stone` (light), `neutral_paper` (light), `neutral_slate` (dark), `neutral_warm` (dark), `neutral_mono` (light), `neutral_linen` (light), `neutral_carbon` (dark), `neutral_fog` (light), `neutral_clay` (light), `neutral_obsidian` (dark)
- *Charte ACT* : **`act_brand`**

**Instagram** (1080×1350) — 22 thèmes :
- *Couleur* : `ig_aurora_dark`, `ig_sunset_vibes`, `ig_minimal_white`, `ig_cream_luxury`, `ig_neon_pulse`, `ig_ocean_deep`, `ig_rose_pop`, `ig_sage_earth`, `ig_midnight_gold`, `ig_coral_burst`
- *Neutres (11)* : `ig_neutral_charcoal`, `ig_neutral_paper`, `ig_neutral_stone`, `ig_neutral_slate`, `ig_neutral_warm`, `ig_neutral_mono`, `ig_neutral_linen`, `ig_neutral_carbon`, `ig_neutral_fog`, `ig_neutral_clay`, `ig_neutral_obsidian`
- *Charte ACT* : **`ig_act_brand`**

### Lisibilité garantie — audit WCAG intégré

**Tous les thèmes passent WCAG AA minimum** (53/54 en AAA, 1 en AA). Vérifier soi-même avant validation finale :

```powershell
python themes.py
```

Affiche pour chaque thème : ratio `text/bg`, `accent1/bg`, niveau (AAA/AA/FAIL), warnings éventuels.

Règle d'or : **toujours préférer un thème AAA pour des slides avec beaucoup de texte** (content/compare avec ≥ 200 chars). Un thème AA reste lisible mais avec moins de marge sur les conditions d'affichage dégradées (téléphone au soleil, mode économie de données).

API disponible :
```python
from themes import audit_theme, contrast_ratio
audit_theme("act_brand")        # rapport detaillé
contrast_ratio("#FCF9F2", "#0A1410")  # → 17.82
```

### Quand utiliser un thème neutre

Privilégier un neutre quand le contenu doit primer sur le visuel :
- **Annonce officielle** (partenariat, levée, recrutement senior) → `neutral_charcoal` / `ig_neutral_charcoal` ou `neutral_slate`
- **Article de fond, livre blanc, étude** → `neutral_paper` / `ig_neutral_paper` ou `neutral_linen` / `ig_neutral_linen`
- **Communication corporate B2B** → `neutral_slate` / `ig_neutral_slate` ou `neutral_fog` / `ig_neutral_fog`
- **Magazine lifestyle, mode, art de vivre** → `neutral_warm` / `ig_neutral_warm` ou `neutral_clay` / `ig_neutral_clay`
- **Communiqué de presse, journalistique** → `neutral_mono` / `ig_neutral_mono`
- **Hommage, in memoriam, ton sobre** → `neutral_stone` / `ig_neutral_stone`
- **Tech profonde / R&D / longue lecture** → `neutral_carbon` / `ig_neutral_carbon` ou `neutral_obsidian` / `ig_neutral_obsidian`
- **Édition haut de gamme, papier de luxe** → `neutral_linen` / `ig_neutral_linen`
- **Architecture / minimalisme / design** → `neutral_fog` / `ig_neutral_fog`
- **Crafted / artisanal / local** → `neutral_clay` / `ig_neutral_clay`
- **Naturel / wellness / vert sobre** → `neutral_obsidian` / `ig_neutral_obsidian`

Les neutres complètent (et n'effacent pas) les thèmes colorés pour les sujets où l'orange ACT primaire pourrait paraître trop affirmé.

### Mapping catégorie ACT → thème

**Règle par défaut** : `act_brand` (LinkedIn) / `ig_act_brand` (Instagram) pour toute production où l'alignement strict charte ACT prime sur la signalétique catégorielle. Sinon, choisir un thème accordé à la catégorie ci-dessous.

| Catégorie | Thème LinkedIn (1er choix · 2nd) | Thème Instagram (1er choix · 2nd) |
|---|---|---|
| **Charte ACT stricte** | `act_brand` · — | `ig_act_brand` · — |
| **Africa Focus** | `kente_tech` · `act_brand` | `ig_sunset_vibes` · `ig_act_brand` |
| **Data & IA** | `dark_blue` · `midnight_ocean` | `ig_ocean_deep` · `ig_aurora_dark` |
| **Cybersecurity** | `dark_red` · `crimson_tide` | `ig_aurora_dark` · `ig_neon_pulse` |
| **Cloud & Infra** | `midnight_ocean` · `arctic_frost` | `ig_ocean_deep` · `ig_aurora_dark` |
| **Code & Dev** | `dark_green` · `cyber_punk` | `ig_neon_pulse` · `ig_aurora_dark` |
| **Carrière & Skills** | `lavender_dream` · `dark_purple` | `ig_cream_luxury` · `ig_sage_earth` |
| **Digital Strategy** | `act_brand` · `dark_orange` | `ig_act_brand` · `ig_sunset_vibes` |
| **Tech Trends** | `aurora_borealis` · `neon_tokyo` | `ig_neon_pulse` · `ig_aurora_dark` |
| **Veille hebdo** | `dark_blue` · `act_brand` | `ig_ocean_deep` · `ig_act_brand` |

### Suggestions par carousel déjà produit (dossier `articles/`)

| Fichier carousel | Catégorie | Thème LinkedIn suggéré | Thème Instagram suggéré |
|---|---|---|---|
| `maroc-hub-numerique-afrique-data-centers.md` | Africa Focus | `kente_tech` ou `act_brand` | `ig_sunset_vibes` ou `ig_act_brand` |
| `cybersecurite-2026-instabilite-permanente.md` | Cybersecurity | `dark_red` ou `crimson_tide` | `ig_aurora_dark` |
| `chatgpt-gemini-claude-explication.md` | Data & IA / LLM | `dark_blue` ou `midnight_ocean` | `ig_ocean_deep` |
| `ia-generative-80-pourcent-sans-impact.md` | Data & IA / GenAI | `dark_blue` ou `cosmic_void` | `ig_aurora_dark` |
| `carousel-instagram-digital-morocco-2030.md` | Africa Focus / Strategy | `act_brand` ou `dark_orange` | `ig_act_brand` ou `ig_midnight_gold` |
| `vibe_coding_instagram.md` | Code & Dev | `cyber_punk` ou `dark_green` | `ig_neon_pulse` |

### Thème `act_brand` — palette officielle ACT

Disponible dans `themes.py` (LinkedIn) et `IG_THEMES` (Instagram) :

| Token | LinkedIn `act_brand` | Instagram `ig_act_brand` |
|---|---|---|
| `bg` | `#0A1410` (Dark) | `#0A1410` (Dark) |
| `bg2` | `#070E1C` (Dark Deep) | `#070E1C` (Dark Deep) |
| `blob1` / `blob2` | Green `#1B3022` / Green Mid `#2C4A35` | idem + gradient diagonal |
| `accent1` | **`#D35400`** (Orange ACT primaire) | **`#D35400`** |
| `accent2` | `#F39C12` (Gold) | `#F39C12` |
| `accent3` | `#FF6B00` (Orange Hot) | `#FF6B00` |
| `text` | `#FCF9F2` (Cream) | `#FCF9F2` |
| `rule` | gradient Orange → Gold | gradient Orange → Gold |

**Toujours** privilégier `act_brand` / `ig_act_brand` lorsque la production doit cohabiter avec un autre support ACT (livre blanc, post LinkedIn, présentation), pour garantir le ratio 60/30/10 et la signature visuelle de la marque.

**Ne jamais inventer un nom de thème** : valider l'existence dans `themes.py` avant de l'imposer à l'utilisateur.

---

## Étape 7 — Production

1. **Lire** l'article source en entier.
2. **Extraire** : titre, excerpt, sections H2, chiffres clés (avec leurs sources), citations, conclusion.
3. **Construire** le plan (Étape 2) en notant pour chaque slide : type, titre, body cible, budget chars.
4. **Rédiger** chaque slide en respectant les budgets — condenser, pas paraphraser à outrance.
5. **Vérifier** : compter les caractères de chaque body avant validation.
6. **Écrire** le fichier `<slug>.carousel.md` à côté de l'article source (même dossier).
7. **Afficher** le résumé : nombre de slides, plateforme, thème suggéré, commande d'import.

---

## Étape 8 — Livrable et import

Toujours terminer la réponse en donnant à l'utilisateur les **deux options d'import** :

**Option A — Web UI (recommandé)** :
1. Lancer `python app.py`
2. Ouvrir http://localhost:5000
3. Cliquer "📄 Importer un fichier MD"
4. Coller le contenu de `<slug>.carousel.md` ou uploader le fichier
5. Choisir thème `<thème suggéré>` et plateforme `<linkedin|instagram>`
6. Générer

**Option B — CLI** : convertir le `.carousel.md` en `.yaml` (le générateur CLI consomme du YAML). Le skill peut produire en plus un `<slug>.carousel.yaml` si l'utilisateur le demande.

---

## Checklist finale (avant de rendre la main)

- [ ] Front matter présent et valide (`series`, `author`, `title`)
- [ ] Entre 6 et 12 slides
- [ ] Première slide = `cover` avec titre court
- [ ] Dernière slide = synthèse ou CTA avec lien source
- [ ] Tous les body ≤ budget caractères de leur type
- [ ] Aucun chiffre sans source (in-slide ou slide "Sources")
- [ ] Aucun Markdown dans les body — uniquement HTML inline supporté
- [ ] Maximum 2 surlignages par slide
- [ ] Séparateurs `---` entre slides (et seulement entre slides)
- [ ] Plateforme choisie + thème nommé existent dans `themes.py`
- [ ] Fichier sauvegardé sous `<slug>.carousel.md` dans le dossier de l'article

Voir `references/templates.md`, `references/budgets.md` et `references/quality-checklist.md` pour les détails.
