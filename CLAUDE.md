# CLAUDE.md

Guidance pour Claude Code lorsqu'il travaille dans `D:\Generator\carousel_generator`.

## Vue d'ensemble

Application Flask + Playwright qui génère des carousels (LinkedIn 1080×1080, Instagram 1080×1350) depuis du YAML ou du Markdown. Sortie : PNG par slide ou PDF mergé.

## Commandes

```bash
# Setup
pip install -r requirements.txt
playwright install chromium

# Web app (Flask, port 5000)
python app.py
# → http://localhost:5000

# CLI
python generate.py --config carousel.yaml --theme dark_purple --output output/
python generate.py --config carousel.yaml --theme random
python generate.py --config carousel.yaml --format pdf
python generate.py --config carousel.yaml --variants 5

# Lint & tests
ruff check .
ruff check --fix .
pytest
pytest tests/test_image_support.py
pytest -k test_name
```

## Variables d'environnement (`.env`)

| Variable | Rôle | Obligatoire |
|----------|------|-------------|
| `SECRET_KEY` | Clé Flask pour signer les sessions | Prod uniquement (sinon clé éphémère générée) |
| `APP_PASSWORD` | Mot de passe d'accès. Vide = mode dev libre | Recommandé |
| `FLASK_ENV` | `production` active HSTS + cookies secure + exige SECRET_KEY | Optionnel |

## Architecture

Pipeline : **YAML/Markdown → dicts slides → Jinja2 HTML → Playwright screenshot → PNG ou PDF mergé**.

### Modules clés

| Fichier | Rôle |
|---------|------|
| `app.py` | Serveur Flask : auth, rate-limit, CSP, jobs en thread, library API |
| `generate.py` | `generate_carousel()` : YAML → HTML → screenshot Chromium headless |
| `md_parser.py` | `parse_markdown_to_slides()` + `_analyze_structure()` (4 stratégies auto) |
| `themes.py` | `THEMES` (LinkedIn) + `IG_THEMES` (Instagram) + `random_theme()` |
| `slide.html.j2` | Template LinkedIn (1080×1080) — types : `cover`, `content`, `compare` |
| `slide_instagram.html.j2` | Template Instagram (1080×1350) — types : `cover`, `content`, `compare`, `quote`, `stat`, `cta` |

### Endpoints REST principaux

- `POST /login`, `GET /logout` — auth (rate-limit 10/min, 30/h)
- `GET /` `/generator` `/guide` — pages
- `GET /health` — healthcheck
- `POST /api/generate` — démarre un job (thread daemon)
- `GET /api/status/<job_id>` — polling
- `GET /api/download/<job_id>` — ZIP/PDF
- `GET /api/themes` — liste des thèmes
- `POST /api/import-markdown` — Markdown → slides
- `POST /api/upload-markdown` — fichier `.md` → slides
- `GET /api/library`, `DELETE/PATCH /api/library/<job_id>`, `/api/library/<id>/pdf|thumbnail|slide|download` — bibliothèque

### Parsing Markdown (`md_parser.py`)

`parse_markdown_to_slides()` détecte automatiquement la structure dans cet ordre :
1. **Séparateur** (`---` / `***`) — sauf si confondu avec YAML front matter
2. **Hiérarchie de titres** (`#` / `##` / `###`)
3. **Listes** (contenu majoritairement à puces)
4. **Non structuré** — réorganisation intelligente fallback

Le YAML front matter (`---\nseries: …\nauthor: …\n---`) alimente le footer du carousel.

### Types de slides

**LinkedIn (`slide.html.j2`)**

| Type | Champs requis | Optionnels |
|------|---------------|------------|
| `cover` | `title` | `badge`, `code`, `cta` |
| `content` | `title`, `body` | `badge` |
| `compare` | `title`, `columns[]{title,body}` | `badge`, `columns[].tag` |

**Instagram (`slide_instagram.html.j2`)**

| Type | Champs requis | Optionnels |
|------|---------------|------------|
| `cover` | `title` | `badge`, `eyebrow`, `body`, `cta` |
| `content` | `title`, `body` | `badge` |
| `compare` | `title`, `columns[]{title,body}` | `badge`, `columns[].tag` |
| `quote` | `title` ou `body` | `author`, `badge` |
| `stat` | `title`, `stats[]{value,label}` | `badge`, `body` |
| `cta` | `title` | `badge`, `body`, `cta` |

Le HTML du `body` accepte : `.bold`, `.hl1`/`.hl2`/`.hl3` (highlights via accents), `<ul class="bullets">`, `<code>` inline, `<pre>` blocs.

### Auto-sizing texte

`_calculate_text_size(slide)` dans `generate.py` mappe le nombre de caractères vers `text_size` (px) et un flag `is_compact`, injectés dans le contexte Jinja2. Les slides `compare` multiplient le compte par 1.5× (espace partagé).

### Système de jobs

- Stockage en RAM : `jobs = {}` dans `app.py`
- Job ID lisible : `YYYY-MM-DD_HH-MM-SS_series_name`
- Génération en `threading.Thread` daemon
- **Limites** : jobs perdus au redémarrage du serveur ; `static/generated/` jamais nettoyé automatiquement

### Sécurité (déjà en place)

- CSP stricte (sauf `unsafe-inline` pour scripts/styles inline existants)
- `X-Content-Type-Options`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`, `Permissions-Policy`
- HSTS en production
- Cookies de session : `HttpOnly`, `SameSite=Lax`, `Secure` en prod
- Anti path-traversal : `_safe_job_folder()` valide le confinement dans `OUTPUT_DIR`
- Anti open-redirect : `_safe_next_url()` n'accepte que les paths locaux
- Rate-limit `/login` : 10/min, 30/h (flask-limiter)
- Upload max : 2 MB

## Frontend

`static/css/` — design system préfixé `ds-*` (tokens, layout, forms, controls, slides, modals, themes-ui, etc.) + `app.css`.
`static/js/` — `app.js` (générateur), `guide.js`/`guide-interactive.js` (guide), `slide-core.js` + `slide-linkedin.js` / `slide-instagram.js` (rendus templates).
`templates/` — `index.html`, `generator.html`, `guide.html`, `login.html`.

## Déploiement

```bash
# Docker local
docker build -t carousel-generator .
docker run -d -p 5000:5000 --name carousel carousel-generator
docker run -d -p 5000:5000 -v $(pwd)/output:/app/static/generated --name carousel carousel-generator

# docker-compose
docker-compose up -d

# Hugging Face Spaces
# → Dockerfile.hf (port 7860), scripts deploy-hf*.bat
```

Sortie : `static/generated/<job_id>/` (auto-créé).

## Notes & gotchas

- **Windows asyncio** : `generate.py` force `WindowsProactorEventLoopPolicy` pour Playwright.
- **Threads + asyncio** : `_run_async()` crée un nouvel event loop par appel (thread-safe).
- **Click 8.1.3+** requis (Flask 3) — un paquet parasite `p` bloquait click en 7.1.2 (résolu).
- **Logo** : encodé base64 dans `logo_base64.txt` pour intégration directe dans les templates.
- **Polices** : `download_fonts.py` télécharge les TTF dans `static/fonts/`.
