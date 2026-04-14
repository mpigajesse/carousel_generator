# Carousel Generator

Générateur de carrousels professionnels pour **LinkedIn** et **Instagram** — à partir d'un fichier Markdown ou YAML, il produit des slides 1080×1080 px en PNG ou PDF, via une interface web ou en ligne de commande.

---

## Fonctionnalités

- **Import Markdown intelligent** — détecte automatiquement la structure (front matter YAML, hiérarchie `#`/`##`/`###`, séparateurs `---`, listes)
- **Import multi-fichiers** — importer plusieurs `.md` simultanément ou coller plusieurs blocs ; chaque fichier génère son propre carrousel en parallèle
- **Rendu HTML complet** — tableaux, gras, italique, code inline, blocs `<pre>`, listes à puces, highlights `.hl1/.hl2/.hl3`
- **19 thèmes premium** — dark purple, neon green, ocean, sunset, forest et plus — ou mode `random`
- **Deux plateformes** — LinkedIn (1080×1080) et Instagram (1080×1350, 6 types de slides)
- **Export PNG ou PDF** — PDF multi-pages avec fusion automatique via `pypdf`
- **Génération parallèle** — jusqu'à 5 slides rendus simultanément (Playwright batch) pour une vitesse 5× supérieure
- **Panneau de jobs en temps réel** — suivi de progression de chaque génération avec barre de statut
- **Badge animé** — compteur de slides sur le bouton « Générer le carousel » avec animation pop + décompte 60 s post-génération
- **Son de fin** — chime Web Audio API (3 notes) quand la génération est terminée, sans fichier externe
- **Bibliothèque persistante** — tous les carrousels générés sont archivés, consultables et gérables depuis `/generator`
- **Sélection multiple** — suppression, restauration, téléchargement et suppression définitive groupés dans la bibliothèque
- **Aperçu PDF inline** — les PDF s'affichent directement dans l'app (plein écran, rendu natif du navigateur)
- **Interface web** — Flask + JS, responsive mobile/tablette/desktop
- **CLI** — génération batch depuis le terminal sans interface graphique

---

## Interface web

### Éditeur (`/`)

L'éditeur principal est organisé en deux zones : **modal d'import** et **sidebar de génération**.

#### Modal d'import (icône ↑ ou bouton Importer)

| Action | Résultat |
|--------|----------|
| Coller du Markdown | Parse automatiquement les slides, affiche le comptage par fichier/bloc |
| Uploader un ou plusieurs `.md` | Chaque fichier est parsé et listé séparément |
| Sélectionner PNG ou PDF | Synchronise le format avec la sidebar (les deux restent alignés) |
| Cliquer « ← Importer dans l'éditeur » | Charge le contenu dans l'éditeur sans lancer la génération |

> La génération ne se lance **jamais** depuis le modal. Elle est toujours déclenchée manuellement via le bouton sidebar.

#### Sidebar de génération

| Contrôle | Description |
|----------|-------------|
| **Plateforme** | LinkedIn ou Instagram |
| **Thème** | 19 thèmes + aléatoire |
| **Format de sortie** | PNG (ZIP) ou PDF — synchronisé avec le modal |
| **Générer le carousel** | Lance la génération ; affiche le nombre de slides en badge animé |

**Badge du bouton Générer :**
- Apparaît après import (nombre total de slides à générer)
- Tourne en **ambre** après génération et décompte 60 secondes
- Se masque automatiquement à zéro → prêt pour le prochain import

#### Génération multi-fichiers

Quand plusieurs fichiers `.md` sont importés :
1. Le badge affiche le total cumulé de slides (`Σ slides de tous les fichiers`)
2. Un clic sur « Générer le carousel » lance **N jobs en parallèle** (un par fichier)
3. Chaque job a sa propre barre de progression dans le panneau de statut
4. Le son de fin retentit quand **tous** les jobs sont terminés

### Bibliothèque (`/generator`)

Page de gestion de tous les carrousels générés :

| Fonctionnalité | Description |
|----------------|-------------|
| **Vue grille / liste** | Basculer entre les deux modes d'affichage |
| **Sélection multiple** | Bouton « Sélectionner » → coches sur chaque carte + barre d'actions groupées |
| **Aperçu lightbox** | Naviguer entre les slides PNG avec clavier (←/→) ou swipe tactile |
| **Aperçu PDF plein écran** | Lecture du PDF directement dans l'app, comme dans un onglet navigateur |
| **Renommage inline** | Double-clic sur le nom de la carte pour renommer |
| **Téléchargement individuel** | ZIP (PNG + PDF) ou PDF direct |
| **Téléchargement groupé** | Sélectionner plusieurs carrousels → télécharger en séquentiel |
| **Corbeille douce (individuelle)** | Suppression locale (localStorage) avec annulation 5 s |
| **Corbeille douce (groupée)** | Sélectionner plusieurs → « Supprimer » dans la barre d'actions |
| **Restauration groupée** | Dans la vue Corbeille, restaurer plusieurs carrousels en une action |
| **Suppression définitive groupée** | Supprime dossiers + fichiers serveur pour tous les sélectionnés |
| **Filtres intelligents** | Par format (PNG/PDF), par période (aujourd'hui/hier/7 jours/ce mois/plage custom) |
| **Recherche** | Correspond au nom, à la date ISO, à la date formatée, à l'heure |
| **Tri** | Plus récent, plus ancien, nom A→Z, plus de slides, plus lourd |
| **Groupes de dates** | Les cartes se regroupent automatiquement par période lors du tri par date |
| **Statistiques** | Total, slides, espace disque, dernier ajout |

#### Raccourcis clavier (bibliothèque)

| Touche | Action |
|--------|--------|
| `←` / `→` | Slide précédente / suivante dans le lightbox |
| `Échap` | Fermer le lightbox ou le panneau PDF |

---

## Types de slides

### LinkedIn
| Type | Description |
|------|-------------|
| `cover` | Slide de couverture — titre, badge, code snippet optionnel, CTA |
| `content` | Slide de contenu — badge, titre, corps texte riche |
| `compare` | Deux colonnes — titre + corps + tag par colonne |

### Instagram (types supplémentaires)
| Type | Description |
|------|-------------|
| `quote` | Citation mise en valeur avec auteur |
| `stat` | Statistiques visuelles avec valeurs et labels |
| `cta` | Call-to-action final |

---

## Installation

```bash
# Cloner le projet
git clone https://github.com/mpigajesse/carousel_generator.git
cd carousel_generator

# Installer les dépendances Python
pip install -r requirements.txt

# Installer le navigateur headless
playwright install chromium
```

---

## Utilisation

### Interface web (recommandé)

```bash
python app.py
# → http://localhost:5000
```

### CLI

```bash
# Génération depuis un fichier YAML
python generate.py --config carousel.yaml --theme dark_purple --output output/

# Thème aléatoire
python generate.py --config carousel.yaml --theme random

# Export PDF
python generate.py --config carousel.yaml --format pdf

# 5 variantes de couleurs aléatoires
python generate.py --config carousel.yaml --variants 5

# Plateforme Instagram
python generate.py --config carousel.yaml --platform instagram --theme neon_green
```

---

## Format Markdown

```markdown
---
series: "Titre de la série"
author: "@votre_handle"
---

# Titre du carrousel

## Premier slide de contenu

Corps du texte avec **gras**, *italique*, `code inline`.

- Point 1
- Point 2
- Point 3

---

## Slide comparatif

### Colonne Gauche
Avantages de l'approche A.

### Colonne Droite
Avantages de l'approche B.
```

### Import multi-fichiers

Tous les fichiers importés via le modal sont traités indépendamment — chacun génère son propre carrousel avec son propre thème/format choisi dans la sidebar.

```
Fichier 1 → job_id_1 → slides 1–5  ┐
Fichier 2 → job_id_2 → slides 1–8  ├─ exécutés en parallèle
Fichier 3 → job_id_3 → slides 1–3  ┘
```

### Syntaxe enrichie dans le corps

| Syntaxe | Rendu |
|---------|-------|
| `**texte**` | Gras |
| `*texte*` | Italique |
| `` `code` `` | Code inline |
| `.hl1 texte .hl1` | Highlight couleur accent 1 |
| `.hl2 texte .hl2` | Highlight couleur accent 2 |
| `.hl3 texte .hl3` | Highlight couleur accent 3 |
| `- item` | Liste à puces |
| `\| col \| col \|` | Tableau HTML rendu |

---

## Thèmes disponibles

### LinkedIn
`dark_purple` · `neon_green` · `ocean_blue` · `sunset_orange` · `forest_green` · `midnight_black` · `rose_gold` · `arctic_blue` · `lava_red` · `golden_hour` · `deep_space` · `coral_reef` · `emerald_city` · `royal_purple` · `copper_flame` · `ice_storm` · `carbon_fiber` · `jade_temple` · `solar_flare`

### Instagram
Mêmes thèmes avec variantes adaptées au format portrait + dégradés de fond.

---

## Structure du projet

```
carousel_generator/
├── app.py                  # Serveur Flask + API REST
├── generate.py             # Moteur de génération (Playwright, batch parallèle)
├── md_parser.py            # Parseur Markdown → slides (4 stratégies)
├── themes.py               # 19 thèmes LinkedIn + Instagram
├── slide.html.j2           # Template Jinja2 LinkedIn
├── slide_instagram.html.j2 # Template Jinja2 Instagram
├── STRUCTURE_COMPLETE.md   # Guide de structure (téléchargeable depuis l'app)
├── templates/
│   ├── index.html          # Éditeur principal (SPA vanilla JS)
│   └── generator.html      # Bibliothèque — CRUD + multi-sélection
├── static/
│   └── generated/          # Sortie persistante — <job_id>/<slides>
├── requirements.txt
└── Dockerfile
```

---

## API REST

### Génération

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/generate` | POST | Lancer une génération en arrière-plan |
| `/api/status/<job_id>` | GET | Statut du job (`running` / `done` / `error`) + progression (`current_slide`/`total_slides`) |
| `/api/themes` | GET | Liste des thèmes avec aperçu des couleurs |
| `/api/import-markdown` | POST | Parser un contenu Markdown → slides JSON |
| `/api/upload-markdown` | POST | Upload fichier `.md` → slides JSON |
| `/api/download-structure` | GET | Télécharger `STRUCTURE_COMPLETE.md` |

### Bibliothèque

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/library` | GET | Lister tous les carrousels (lecture disque) |
| `/api/library/<id>` | DELETE | Supprimer un carousel (dossier + fichiers) |
| `/api/library/<id>/rename` | PATCH | Renommer un carousel |
| `/api/library/<id>/thumbnail` | GET | Miniature (1er PNG ou `cover_thumb.png`) |
| `/api/library/<id>/slide/<n>` | GET | PNG à l'index `n` pour le viewer lightbox |
| `/api/library/<id>/pdf` | GET | PDF inline pour aperçu natif dans le navigateur |
| `/api/library/<id>/download` | GET | Télécharger tout en ZIP |

### Exemple de payload `/api/generate`

```json
{
  "slides": [...],
  "theme": "dark_purple",
  "platform": "linkedin",
  "format": "png",
  "footer": {
    "series": "Ma série",
    "author": "@username"
  }
}
```

### Réponse `/api/status/<job_id>`

```json
{
  "status": "running",
  "current_slide": 3,
  "total_slides": 8,
  "percent": 37
}
```

---

## Détails techniques

### Pipeline de génération parallèle

`generate.py` divise les slides en lots (`BATCH_SIZE = 5`) et les rend en parallèle avec `asyncio.gather`. Chaque slide est une page Playwright indépendante ouverte simultanément, puis fermée après screenshot — gain de vitesse ≈ 5× sur les carrousels longs.

### Badge animé et décompte

Le badge du bouton « Générer le carousel » suit un cycle :

```
Import → badge.pop (vert, N slides)
Génération → badge.countdown (ambre, 60 s)
Expiration → badge masqué → prêt pour le prochain import
```

L'animation `pop` est ré-déclenchée via double `requestAnimationFrame` pour contourner la règle de reflow CSS.

### Son de fin (Web Audio API)

Trois oscillateurs (`OscillatorNode + GainNode`) à 880 Hz, 1100 Hz et 1320 Hz avec décroissance exponentielle — aucun fichier audio externe, fonctionne offline.

### Miniature des carrousels PDF

Lors de la génération PDF, chaque slide est d'abord rendu en PNG puis converti en PDF.
Avant la suppression des PNG intermédiaires, le premier slide est copié sous `cover_thumb.png`
dans le dossier du job — il sert de miniature dans la bibliothèque sans alourdir le résultat final.

### Identifiant de job

Les jobs sont nommés selon le format : `YYYY-MM-DD_HH-MM-SS_nom_de_serie`.
Ce format permet à `_scan_job_folder()` d'extraire date, heure et nom sans base de données.

### Taille du texte auto-adaptée

`_calculate_text_size()` calcule automatiquement la taille de police optimale (21–46 px)
en fonction du nombre de caractères du corps, pour que le contenu tienne toujours dans les 936 px disponibles.

### Format synchronisé modal ↔ sidebar

Le sélecteur PNG/PDF dans le modal et celui dans la sidebar partagent le même état via `setFormat(fmt)`.
Toutes les instances de `.fmt-btn` sont mises à jour simultanément — pas de désynchronisation possible.

### Multi-sélection dans la bibliothèque

La sélection multiple utilise un `Set<jobId>` pour une vérification O(1). La barre d'actions flottante
apparaît automatiquement dès qu'au moins un élément est sélectionné et propose des actions adaptées
à la vue courante (normale ou corbeille).

---

## Déploiement

### Docker (local ou serveur Ubuntu)

```bash
# Build
docker build -t carousel-generator .

# Run
docker run -d -p 5000:5000 --name carousel carousel-generator

# Avec volume persistant
docker run -d -p 5000:5000 \
  -v $(pwd)/output:/app/static/generated \
  --name carousel carousel-generator
```

### Hugging Face Spaces

```bash
git push hf main
```

Le `Dockerfile.hf` cible le port 7860 requis par HF Spaces.

### Multi-remote (double push)

Le projet est mirroring sur deux dépôts GitHub automatiquement :

```bash
bash push-all.sh          # push origin + act en une commande
```

| Remote | Dépôt |
|--------|-------|
| `origin` | `github.com/mpigajesse/carousel_generator` |
| `act` | `github.com/Africa-centred-technology/carousel_generator_officiel` |

---

## Développement

```bash
# Linter
pip install ruff
ruff check .
ruff check --fix .

# Tests
pip install pytest
pytest
pytest test_parser.py
pytest -k test_name
```

---

## Licence

MIT — voir [LICENSE](LICENSE) pour les détails.

---

*Généré avec soin pour les créateurs de contenu africains et francophones.*
