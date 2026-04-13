# Carousel Generator

Générateur de carrousels professionnels pour **LinkedIn** et **Instagram** — à partir d'un fichier Markdown ou YAML, il produit des slides 1080×1080 px en PNG ou PDF, via une interface web ou en ligne de commande.

---

## Fonctionnalités

- **Import Markdown intelligent** — détecte automatiquement la structure (front matter YAML, hiérarchie de titres `#`/`##`/`###`, séparateurs `---`, listes)
- **Rendu HTML complet** — tableaux, gras, italique, code inline, blocs `<pre>`, listes à puces, highlights `.hl1/.hl2/.hl3`
- **19 thèmes premium** — dark purple, neon green, ocean, sunset, forest, et plus — ou mode `random`
- **Deux plateformes** — LinkedIn (carré 1080×1080) et Instagram (carré 1080×1080, 6 types de slides)
- **Export PNG ou PDF** — PDF multi-pages avec fusion automatique via `pypdf`
- **Interface web** — Flask + JS, responsive mobile/tablette/desktop, sidebar collapsible
- **CLI** — génération batch depuis le terminal, sans interface graphique

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

L'interface permet de :
- Coller ou uploader un fichier Markdown
- Choisir la plateforme (LinkedIn / Instagram) et le thème
- Prévisualiser les slides parsés avant génération
- Télécharger le résultat en PNG ou PDF

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
├── generate.py             # Moteur de génération (Playwright)
├── md_parser.py            # Parseur Markdown → slides
├── themes.py               # 19 thèmes LinkedIn + Instagram
├── slide.html.j2           # Template Jinja2 LinkedIn
├── slide_instagram.html.j2 # Template Jinja2 Instagram
├── templates/
│   └── index.html          # Interface web (SPA vanilla JS)
├── static/
│   └── generated/          # Sortie des carrousels générés
├── requirements.txt
└── Dockerfile
```

---

## API REST

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/generate` | POST | Lancer une génération |
| `/api/status/<job_id>` | GET | Statut du job |
| `/api/download/<job_id>` | GET | Télécharger le résultat |
| `/api/themes` | GET | Liste des thèmes disponibles |
| `/api/import-markdown` | POST | Parser un Markdown → slides JSON |
| `/api/upload-markdown` | POST | Upload fichier .md |

### Exemple de payload `/api/generate`

```json
{
  "slides": [...],
  "theme": "dark_purple",
  "platform": "linkedin",
  "format": "png",
  "series": "Ma série",
  "author": "@username"
}
```

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
