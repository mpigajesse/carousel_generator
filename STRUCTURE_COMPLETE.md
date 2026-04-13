# Skill — Structurer un Article en Carousel

Ce document est la référence complète pour transformer un article en carousel prêt à générer.
Il définit les règles de contenu, les formats attendus, et les contraintes de chaque type de slide.

---

## 1. Format de Sortie Attendu

Tout carousel est un fichier Markdown avec :
1. Un **front matter YAML** (series + author)
2. Des **blocs de slides** séparés par `---`

```markdown
---
series: "Titre de la série"
author: "@compte"
---

# Titre de la slide cover

Accroche courte optionnelle.

---

## Titre slide 2

Contenu...

---

## Titre slide 3

Contenu...
```

Le parser détecte automatiquement :
- Le **type cover** : toujours le premier bloc (après le front matter)
- Le **type compare** : si le titre contient "vs", "versus", "contre", ou si le bloc contient deux `###` de même niveau
- Le **type content** : tous les autres blocs

---

## 2. Plateformes & Contraintes de Longueur

| Plateforme | Dimensions | Slides recommandées | Caractères max / slide |
|-----------|-----------|---------------------|----------------------|
| LinkedIn | 1080 × 1080 px | 5 à 10 slides | 600 caractères body |
| Instagram | 1080 × 1350 px | 6 à 12 slides | 500 caractères body |

**Règle absolue :** mieux vaut une slide trop courte qu'une slide qui déborde.
Si un concept nécessite plus de 600 caractères, le couper en deux slides.

---

## 3. Structure de la Slide Cover

La slide cover est **obligatoirement la première**. Elle accroche, elle ne résume pas.

```markdown
# [Titre court et percutant — max 60 caractères]

[Accroche ou question provocatrice — 1 phrase max, optionnelle]
```

**Règles du titre cover :**
- Majuscules non obligatoires (le template les met en uppercase automatiquement)
- Pas de liste, pas de chiffres, pas de bullet points
- Doit donner envie de swiper
- Exemples de formules qui marchent :
  - "Le problème que personne ne montre"
  - "Pourquoi X ne suffit plus"
  - "Ce que j'ai appris en faisant Y"
  - "X vs Y : la vraie différence"

**Ne pas mettre dans la cover :**
- Des listes
- Plus d'une idée
- Des statistiques
- Du jargon technique sans contexte

---

## 4. Structure des Slides Content

Une slide content = **une seule idée développée**.

```markdown
## [Titre de l'idée — max 55 caractères]

Phrase d'introduction ou contexte (optionnel, 1-2 lignes max).

- **Point clé 1** — explication courte
- **Point clé 2** — explication courte
- **Point clé 3** — explication courte
```

**Règles du contenu :**
- Maximum **4 bullet points** par slide (3 est idéal)
- Chaque bullet : **max 80 caractères** (sinon il passe sur 2 lignes)
- Le gras `**mot**` sert à highlighter le concept clé du bullet, pas toute la phrase
- Pas de sous-bullets (pas de niveau 2 dans les listes)
- Une slide = une idée, pas un résumé de paragraphe

**Markdown supporté dans le body :**

| Syntaxe | Effet | Usage |
|---------|-------|-------|
| `**texte**` | Texte blanc gras | Mot-clé ou concept important |
| `*texte*` | Texte italique accent | Nuance ou terme étranger |
| `` `code` `` | Fond semi-transparent | Termes techniques, noms de lib |
| `> citation` | Blockquote encadré | Citer une source ou une idée forte |
| `- item` | Bullet stylisé | Liste de points |
| `1. item` | Liste numérotée | Étapes séquentielles |
| `### Sous-titre` | Titre accent (jaune) | Sous-section dans une slide dense |

---

## 5. Structure des Slides Compare

Une slide compare = **deux concepts mis en opposition directe**.

```markdown
## [Concept A] vs [Concept B]

### [Concept A]
- Point distinctif 1
- Point distinctif 2
- Point distinctif 3

### [Concept B]
- Point distinctif 1
- Point distinctif 2
- Point distinctif 3
```

**Règles du compare :**
- Les deux colonnes doivent avoir **le même nombre de bullets** (équilibre visuel)
- Maximum **3 bullets par colonne**
- Les titres `###` deviennent les en-têtes de chaque colonne
- Le titre `##` est affiché au-dessus des deux colonnes
- Pas de texte libre entre `##` et les `###`

---

## 6. Types Exclusifs Instagram

Ces types ne sont disponibles que pour la plateforme Instagram.

### Quote (Citation)

```markdown
## [Texte de la citation entre guillemets]

> [Auteur de la citation]
```

**Règles :**
- La citation doit tenir en **2-3 lignes max** (max 180 caractères)
- Pas de liste, pas de bullet
- Idéal pour une phrase forte extraite de l'article
- Le `>` est utilisé pour l'attribution (auteur)

---

### Stat (Statistiques clés)

```markdown
## [Titre de contexte pour les stats]

| 73% | Développeurs utilisant l'IA en 2025 |
| 10× | Gain de vitesse sur les prototypes |
| 2027 | Année estimée de maturité des agents |
```

**Règles :**
- **2 à 3 stats maximum** (au-delà ça devient illisible)
- La valeur (`73%`, `10×`, `2027`) doit être **courte et frappante**
- Le label doit tenir sur **une ligne** (max 45 caractères)
- Utiliser des chiffres réels, pas des approximations floues

---

### CTA (Call to Action — dernière slide)

```markdown
## [Question ou appel à l'action]

[1-2 phrases invitant à l'engagement, optionnelles]
```

**Règles :**
- Toujours la **dernière slide** du carousel Instagram
- Poser une question ouverte ou inviter au commentaire
- Ne pas lister des choses à faire — juste une seule action claire
- Exemples : "Quelle friction vous bloque le plus ?", "Partagez votre expérience ci-dessous", "Suivez pour la suite"

---

## 7. Règles de Découpage d'un Article

### Processus de structuration

```
Article brut
    ↓
1. Identifier la thèse centrale → Cover
2. Identifier les 3-6 idées principales → slides Content
3. Y a-t-il des oppositions binaires ? → slides Compare
4. Y a-t-il des chiffres forts ? → slide Stat (Instagram uniquement)
5. Y a-t-il une citation mémorable ? → slide Quote (Instagram uniquement)
6. Quelle question poser à l'audience ? → slide CTA (Instagram uniquement)
    ↓
Carousel structuré
```

### Nombre de slides par plateforme

| Plateforme | Minimum | Idéal | Maximum |
|-----------|---------|-------|---------|
| LinkedIn | 4 | 6–8 | 12 |
| Instagram | 5 | 7–10 | 15 |

### Ce qu'il faut **garder** de l'article
- Les idées fortes et contre-intuitives
- Les exemples concrets et mémorables
- Les tensions (X mais Y, on pense que… or en réalité…)
- Les chiffres et données précises
- La conclusion actionnable

### Ce qu'il faut **supprimer** de l'article
- Les transitions entre paragraphes ("Comme nous l'avons vu…", "Ainsi…")
- Les répétitions et reformulations
- Les nuances académiques non essentielles
- Les introductions trop longues
- Les conclusions qui répètent ce qui a déjà été dit

---

## 8. Exemples Complets

### Exemple LinkedIn — Article tech

**Article source (résumé) :** "Le Vibe Coding promet de révolutionner le développement, mais se heurte à des plafonds réels : boucles infinies, hallucinations, code opaque. Le vrai problème n'est pas le modèle, c'est l'écosystème conçu pour les humains."

**Résultat structuré :**

```markdown
---
series: "Vibe Coding · Réflexion"
author: "@Sohaib Baroud"
---

# Le potentiel est prouvé. Et si les vraies limites venaient de l'écosystème ?

---

## La promesse est réelle

On est passé de *"l'IA complète mes lignes"* à *"l'IA génère un module entier"*.

- **Claude Code, Cursor, Copilot** — les démos sont bluffantes
- **Les progrès** sont spectaculaires et mesurables
- **Et pourtant** — ceux qui pratiquent se heurtent à des plafonds

---

## Les plafonds que personne ne montre

- **Boucles infinies** — l'agent se corrige sans converger
- **Hallucinations** — la librairie n'existe tout simplement pas
- **Code opaque** — généré, mais impossible à faire évoluer
- **Perte de contexte** — dès qu'on sort d'un seul fichier

---

## Le vrai problème : l'écosystème

> On demande à des LLM de travailler avec des outils optimisés pendant 70 ans pour les humains.

- **Python** est lisible — *pour un humain*
- **Git** structure la collaboration — *entre humains*
- **Les frameworks** évitent la réécriture — *à un humain*

---

## 4 Paradigmes pour la prochaine étape

- **Représentations intermédiaires** pensées pour la génération machine
- **Vérification formelle** — l'IA génère, un prouveur certifie
- **Protocoles inter-agents** avec gestion d'incertitude
- **Versionnement sémantique** qui trace les intentions métier

---

## Générer du code, c'est acquis

Le prochain palier :

- **Concevoir** une architecture complète
- **Vérifier** la qualité de façon formelle
- **Orchestrer** un déploiement de bout en bout

Il ne sera atteignable que si **l'écosystème suit**.

---

## Quelles frictions viennent des modèles ?

Et lesquelles viennent des **outils dans lesquels ils opèrent** ?

Partagez vos retours — et surtout vos **désaccords**.
```

---

### Exemple Instagram — Même article, format Instagram

```markdown
---
series: "Vibe Coding · Réflexion"
author: "@Sohaib Baroud"
---

# Vibe Coding · Réflexion

Le potentiel est prouvé. Et si les vraies limites venaient de **l'écosystème** ?

---

## La promesse est réelle

- **Claude Code. Cursor. Copilot.** Les démos sont bluffantes
- On passe de *"complète mes lignes"* à *"génère un module entier"*
- Et pourtant — les praticiens se heurtent à des **plafonds réels**

---

## Les plafonds que personne ne montre

- **Boucles infinies** — l'agent se corrige sans converger
- **Hallucinations** — la librairie n'existe pas
- **Code opaque** — généré mais non maintenable
- **Perte de fil** — dès qu'on sort d'un seul fichier

---

## Et si le problème venait de l'écosystème ?

> On demande à des LLM de travailler avec des outils optimisés pendant 70 ans pour les humains.

---

## Humain vs Agent IA

### Outils actuels
- Lisibilité humaine prioritaire
- Git pour la collaboration
- Frameworks évitant la réécriture

### Ce qu'il faudrait
- Représentations compactes et vérifiables
- Protocoles inter-agents natifs
- Versionnement sémantique des intentions

---

## 4 Paradigmes à construire

- **Représentations intermédiaires** pour la génération machine
- **Vérification formelle** — prouveur certifie ce que l'IA génère
- **Protocoles inter-agents** avec négociation de capacités
- **Versionnement sémantique** des intentions métier

---

## Le prochain palier

- Concevoir une **architecture complète**
- Vérifier la **qualité formellement**
- Orchestrer un **déploiement autonome**

Atteignable seulement si **l'écosystème suit**.

---

## Quelles frictions viennent des modèles ?

Et lesquelles viennent des **outils** dans lesquels ils opèrent ?

Partagez vos **désaccords** ci-dessous.
```

---

## 9. Erreurs Fréquentes à Éviter

| Erreur | Problème | Correction |
|--------|---------|------------|
| Body > 600 caractères | Débordement visuel | Couper en 2 slides |
| Plus de 4 bullets | Trop dense, illisible | Garder les 3 plus forts |
| Titre > 60 caractères | Trop petit ou coupé | Reformuler plus court |
| Transition textuelle dans body | Paraît copié-collé | Supprimer les liaisons |
| Répéter l'idée de la cover | Slide inutile | Remplacer par un exemple concret |
| Bullet sans **gras** | Pas d'ancre visuelle | Mettre le concept clé en gras |
| Compare avec colonnes déséquilibrées | Layout cassé | Équilibrer le nombre de bullets |
| CTA pas en dernière position | Confus pour l'audience | Toujours terminer par le CTA |
| Stat vague ("beaucoup", "souvent") | Pas crédible | Chiffre précis ou supprimer |

---

## 10. Prompt Type pour Structurer un Article

Quand tu reçois un article brut à transformer en carousel, applique ce processus :

```
1. Lire l'article en entier
2. Identifier : thèse centrale, idées principales, oppositions, chiffres, citations fortes
3. Décider : LinkedIn (corporate, analytique) ou Instagram (visuel, émotionnel) ?
4. Construire le plan :
   - Slide 1 : Cover (thèse en titre percutant)
   - Slides 2-N : une idée par slide (content ou compare)
   - Instagram uniquement : 1 quote, 1 stat si pertinent, 1 CTA en dernier
5. Rédiger chaque slide en respectant les contraintes de longueur
6. Vérifier : chaque slide tient-elle seule, sans lire les autres ?
7. Outputter le Markdown complet avec front matter
```

**Critère de qualité final :** chaque slide doit être compréhensible et impactante même vue seule, sans contexte des autres slides.

---

## 11. Compréhension de l'Application — Workflow Complet

Cette section décrit comment l'application fonctionne de bout en bout. La connaître permet de guider l'utilisateur à chaque étape et d'anticiper les problèmes.

### Vue Macro du Pipeline

```
Article brut (texte, PDF, LinkedIn post, blog...)
        ↓
  [Claude structure] → Markdown formaté
        ↓
  [App — Import Markdown] → Slides parsées + aperçu
        ↓
  [Utilisateur ajuste] → Slides éditées dans l'UI
        ↓
  [Génération] → Playwright screenshot chaque slide
        ↓
  [Re-thème optionnel] → Changer les couleurs sans repasser par l'éditeur
        ↓
  [Téléchargement] → ZIP (PNG individuels) ou PDF fusionné
```

---

### Étape 1 — Import du Markdown

**Accès :** bouton "Importer un fichier MD" dans la sidebar de l'interface web.

**Deux méthodes :**
- **Coller le texte** : onglet "Coller le contenu", coller le Markdown, cliquer "Analyser"
- **Upload fichier** : glisser-déposer ou sélectionner un `.md` ou `.markdown`

**Ce que l'app fait automatiquement à l'import :**
1. Extrait le front matter YAML → remplit les champs `series` et `author`
2. Analyse la structure : séparateurs `---` > hiérarchie `##` > listes > non structuré
3. Détecte les types de slides (cover / content / compare)
4. Calcule la densité de texte → ajuste `text_size` et flag `is_compact`
5. Retourne un rapport `structure_analysis` : format détecté, confiance, nombre de slides

**Ce que l'utilisateur voit après l'import :**
- Les slides apparaissent dans l'éditeur, modifiables une par une
- Un résumé de l'analyse (format détecté, nombre de slides)
- Il peut ajuster titre, body, badge, type avant de générer

**Points de vigilance à l'import :**
- Si le Markdown utilise des `---` comme séparateurs ET a un front matter, le parser privilégie les séparateurs (comportement correct depuis le fix de `has_real_separators`)
- Les `###` dans un bloc sont convertis en `slide-h3` (texte accent jaune), pas en nouvelles slides
- Un `>` blockquote devient un bloc encadré dans le body, pas une slide Quote Instagram

---

### Étape 2 — Édition dans l'Interface

**Structure de la sidebar (gauche) :**

```
[Plateforme]       LinkedIn  |  Instagram
[Thème]            Grille de couleurs filtrée par plateforme
[Slides]           Liste des slides avec drag-and-drop
[Ajouter une slide] Boutons par type : Cover / Content / Compare
                    + Quote / Stat / CTA (Instagram uniquement)
[Footer]           Champs series + author
[Générer]          PNG ou PDF + lancer la génération
```

**Champs éditables par type de slide :**

| Champ | Cover | Content | Compare | Quote | Stat | CTA |
|-------|-------|---------|---------|-------|------|-----|
| Badge | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Titre | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Body  | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Code (LinkedIn cover) | ✅ | — | — | — | — | — |
| CTA label | ✅ | — | — | — | — | ✅ |
| Colonnes (×2) | — | — | ✅ | — | — | — |
| Stats (valeur + label) | — | — | — | — | ✅ | — |
| Author (quote) | — | — | — | ✅ | — | — |
| Eyebrow (IG cover) | ✅ | — | — | — | — | — |

---

### Étape 3 — Génération

**Déclenchement :** clic sur "Générer PNG" ou "Générer PDF".

**Ce qui se passe en arrière-plan :**
1. L'app crée un job avec un ID descriptif : `2026-04-13_14-30-00_vibe-coding`
2. Un thread daemon démarre la génération
3. Pour chaque slide, l'app :
   - Injecte les données de la slide + le thème dans le template Jinja2
   - Calcule `text_size` et `is_compact` selon le nombre de caractères
   - Injecte `slide_index` et `slide_total` pour le compteur
   - Ouvre Playwright (Chromium headless), charge la page HTML
   - Attend 800ms pour le chargement des polices
   - Exécute le script JS d'auto-sizing (réduit le texte si débordement)
   - Screenshot à la résolution exacte (1080×1080 ou 1080×1350)
4. En mode PDF : encapsule chaque PNG dans une page HTML, imprime en PDF, fusionne
5. Le job passe à l'état `done` avec la liste des fichiers générés

**Suivi du statut :**
- L'interface polle `/api/status/{job_id}` toutes les secondes
- Quand `done` : affiche les slides dans l'onglet Aperçu, active le re-thème

**Nommage des fichiers de sortie :**
```
static/generated/2026-04-13_14-30-00_vibe-coding/
├── 01_vibe-coding.png
├── 02_vibe-coding.png
├── ...
└── carousel.zip
```

---

### Étape 4 — Re-thème (sans revenir à l'éditeur)

**Accès :** barre de thèmes affichée dans l'onglet Aperçu après génération.

**Fonctionnement :**
- L'app mémorise le dernier payload de génération (`lastPayload`)
- Cliquer sur un autre thème envoie le même payload avec le nouveau thème
- Un nouveau job est créé, les slides se régénèrent
- L'aperçu se met à jour automatiquement

**Ce que ça permet :**
- Tester plusieurs palettes de couleur sur le même contenu
- Choisir la version finale avant de télécharger
- Passer de `ig_aurora_dark` à `ig_minimal_white` en un clic

**Limitation :** le re-thème ne modifie pas le contenu. Si on veut changer du texte, il faut revenir à l'éditeur.

---

### Étape 5 — Téléchargement

**Deux formats disponibles :**

| Format | Contenu | Usage |
|--------|---------|-------|
| **ZIP** | Toutes les slides en PNG individuels | Publication manuelle slide par slide (Instagram, LinkedIn) |
| **PDF** | Toutes les slides fusionnées en un seul PDF | Partage, archivage, impression |

**Téléchargement individuel :** cliquer sur une slide dans l'aperçu télécharge cette slide seule en PNG.

---

### Comportement des Templates — Ce que Claude doit Savoir

#### Slide Cover LinkedIn
- Logo **450px centré** dans le contenu
- Terminal box avec le titre (style code/terminal)
- **Pas de footer** sur la slide cover
- Le CTA devient le label du bouton swipe en bas

#### Slide Cover Instagram
- **Pas de topbar** (pas de compteur)
- **Pas de footer**
- Logo **420px centré** en haut du contenu
- Titre et tous les éléments **centrés horizontalement**
- Le contenu est centré verticalement dans toute la hauteur de la slide

#### Slides Content/Compare/Quote/Stat/CTA Instagram
- **Topbar** avec uniquement le compteur `01 / 06` (pas de logo)
- **Footer** avec series (gauche) + author (gauche) + logo 120px (droite)
- Contenu centré verticalement dans l'espace disponible

#### Auto-sizing JS (dans les deux templates)
Le script JS s'exécute après le rendu HTML et réduit itérativement la taille du texte si le contenu déborde sur le footer. Il s'arrête quand le contenu tient ou quand une taille minimum est atteinte. C'est le filet de sécurité — mais il ne remplace pas un bon découpage du contenu.

---

### Arbre de Décision pour Guider l'Utilisateur

```
L'utilisateur a un article à transformer en carousel
        │
        ├─ Quelle plateforme ?
        │       ├─ LinkedIn → ton corporate, analytique, 1:1
        │       └─ Instagram → ton visuel, émotionnel, 4:5
        │
        ├─ Il a déjà le Markdown structuré ?
        │       ├─ Oui → Import Markdown → vérifier → générer
        │       └─ Non → Claude structure l'article → coller en import
        │
        ├─ Combien de slides ?
        │       ├─ LinkedIn : 6-8 idéal, 12 max
        │       └─ Instagram : 7-10 idéal, 15 max
        │
        ├─ Le contenu a-t-il débordé à la génération ?
        │       ├─ Oui → revenir à l'éditeur, couper le body en deux slides
        │       └─ Non → passer au re-thème
        │
        ├─ Le thème est-il satisfaisant ?
        │       ├─ Non → cliquer un autre thème dans la barre de re-thème
        │       └─ Oui → télécharger
        │
        └─ Format de téléchargement ?
                ├─ Publication Instagram/LinkedIn → ZIP (PNG individuels)
                └─ Partage/archive → PDF fusionné
```

---

### Erreurs Courantes de Workflow et Solutions

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| Les slides ne correspondent pas à l'article | Mauvaise détection de structure à l'import | Vérifier que les `---` séparateurs sont bien présents dans le Markdown |
| Le front matter n'est pas reconnu | Espaces ou caractères incorrects autour des `---` | Le front matter doit être **exactement** en première ligne du fichier |
| Une slide a un contenu trop petit | Auto-sizer a réduit à cause du débordement | Raccourcir le body : passer sous 500 caractères |
| Le type "compare" n'est pas détecté | Les `###` ne sont pas au bon niveau | S'assurer que les deux colonnes sont bien des `### Titre` dans le même bloc `## Titre vs Titre` |
| Le thème Instagram apparaît dans LinkedIn | Sélecteur de plateforme non changé | Changer la plateforme dans la sidebar avant de choisir le thème |
| Le re-thème ne fonctionne pas | La page a été rechargée, `lastPayload` perdu | Régénérer une première fois depuis l'éditeur |
| Le logo n'apparaît pas | Fichier `static/logo/logo.png` absent | Vérifier que le logo est présent dans `static/logo/` |
