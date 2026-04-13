# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install
pip install -r requirements.txt
playwright install chromium

# Local web app (Flask, port 5000)
python app.py

# CLI generator
python generate.py --config carousel.yaml --theme dark_purple --output output/
python generate.py --config carousel.yaml --theme random
python generate.py --config carousel.yaml --format pdf
python generate.py --config carousel.yaml --variants 5   # 5 random color variants

# Lint (install first: pip install ruff)
ruff check .
ruff check --fix .

# Tests (install first: pip install pytest)
pytest
pytest test_parser.py
pytest -k test_name
```

## Architecture

The pipeline flows: **input (YAML or Markdown) → slide data dicts → Jinja2 HTML → Playwright screenshot → PNG or merged PDF**.

### Server

| File | Framework | Port | Purpose |
|------|-----------|------|---------|
| `app.py` | Flask | 5000 | Web application (dev + prod) |

Exposes REST endpoints: `/api/generate`, `/api/status/<job_id>`, `/api/download/<job_id>`, `/api/themes`, `/api/import-markdown`, `/api/upload-markdown`.

### Core modules

**`generate.py`** — `generate_carousel(config_path, theme_name, output_dir, format, platform)` is the main entry point. It loads YAML, calls `get_theme()`, renders each slide with the appropriate Jinja2 template (`slide.html.j2` for LinkedIn, `slide_instagram.html.j2` for Instagram), then uses Playwright headless Chromium to screenshot each slide. LinkedIn: 1080×1080px, Instagram: 1080×1350px. PDF mode screenshots to PNG first then wraps each in an HTML image page, prints to PDF, and merges all per-slide PDFs with `pypdf`. HTML intermediates are always cleaned up.

**`md_parser.py`** — `parse_markdown_to_slides(md_content)` auto-detects content structure and picks one of four parsing strategies in order of priority:
1. **Separator** (`---` / `***`) — only if not mistaken for YAML front matter
2. **Heading hierarchy** (`#` / `##` / `###`)
3. **List structure** (bullet-heavy content)
4. **Unstructured** — falls back to intelligent reorganization

YAML front matter (`---\nseries: …\nauthor: …\n---`) is extracted first and maps to the carousel footer. `_analyze_structure()` is exposed directly and used by `app.py` to return `structure_analysis` metadata to the frontend.

**`themes.py`** — LinkedIn themes in `THEMES` dict, Instagram themes in `IG_THEMES` dict + `random_theme()`. Each theme dict has fixed keys: `bg`, `bg2`, `blob1`, `blob2`, `accent1–3`, `text`, `text_muted`, `badge_bg`, `rule`, `terminal_bg`, `terminal_border`. IG themes add: `bg_gradient`, `is_light`, `surface`, `surface2`.

**`slide.html.j2`** — Jinja2 template for LinkedIn (1080×1080px), 3 slide types: `cover`, `content`, `compare`.

**`slide_instagram.html.j2`** — Jinja2 template for Instagram (1080×1350px), 6 slide types: `cover`, `content`, `compare`, `quote`, `stat`, `cta`. Cover slide: large centered logo, no topbar, no footer. Other slides: topbar with counter + footer with logo.

### Slide types

**LinkedIn (`slide.html.j2`)**

| Type | Required fields | Optional fields |
|------|----------------|-----------------|
| `cover` | `title` | `badge`, `code`, `cta` |
| `content` | `title`, `body` | `badge` |
| `compare` | `title`, `columns[]{title,body}` | `badge`, `columns[].tag` |

**Instagram (`slide_instagram.html.j2`)**

| Type | Required fields | Optional fields |
|------|----------------|-----------------|
| `cover` | `title` | `badge`, `eyebrow`, `body`, `cta` |
| `content` | `title`, `body` | `badge` |
| `compare` | `title`, `columns[]{title,body}` | `badge`, `columns[].tag` |
| `quote` | `title` or `body` | `author`, `badge` |
| `stat` | `title`, `stats[]{value,label}` | `badge`, `body` |
| `cta` | `title` | `badge`, `body`, `cta` |

Body HTML supports: `.bold`, `.hl1`/`.hl2`/`.hl3` (accent color highlights), `<ul class="bullets">`, inline `<code>`, `<pre>` blocks.

### Job system

Jobs are tracked in a plain in-memory `dict` (`jobs = {}`). Job IDs are human-readable: `YYYY-MM-DD_HH-MM-SS_series_name`. Generation runs in a daemon `threading.Thread`. **Jobs are lost on server restart; `static/generated/` is never auto-cleaned.**

### Text auto-sizing

`_calculate_text_size(slide)` in `generate.py` maps character count ranges to `text_size` (px) and sets `is_compact` flag — both injected into the Jinja2 template context. Compare slides multiply char count by 1.5× to account for split-column space.

## Deployment

**Ubuntu Server 24 + Docker:**

```bash
# Build
docker build -t carousel-generator .

# Run (port 5000 exposed)
docker run -d -p 5000:5000 --name carousel carousel-generator

# With volume for persisted output
docker run -d -p 5000:5000 -v $(pwd)/output:/app/static/generated --name carousel carousel-generator
```

Output written to `static/generated/<job_id>/` (auto-created).
