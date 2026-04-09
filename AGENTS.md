# Carousel Generator - AGENTS Guide

## Project Overview

Instagram carousel generator with YAML config, Jinja2 templates, and Playwright rendering.

## Installed Skills (Auto-Loaded)

### 1. docs-audit-and-refresh
**Usage**: `/skill docs-audit-and-refresh`

Audits repository's `docs/` content against current codebase, finds missing/incorrect/stale documentation, and refreshes affected pages.

**Workflow**:
1. Build current-state inventory
2. Compare implementation against `docs/`
3. Prioritize by reader impact
4. Refresh the docs
5. Validate the refresh

### 2. docs-update-from-diff
**Usage**: `/skill docs-update-from-diff`

Reviews local code changes with `git diff` and updates `docs/` to match.

**Workflow**:
1. Build the change set
2. Derive docs impact
3. Find the right docs location
4. Write the update
5. Cross-check before finishing

### 3. pr-review
**Usage**: `/skill pr-review` or `/qc code-review`

Reviews pull requests with code analysis and terminal smoke testing.

**Workflow**:
1. Fetch PR information via `gh pr`
2. Code review across 5 dimensions
3. Terminal smoke testing
4. Upload screenshots to PR comments
5. Submit review

### 4. qwen-code-claw
**Usage**: `/skill qwen-code-claw`

Uses Qwen Code as a Code Agent for code understanding, project generation, features, bug fixes, refactoring, etc.

**Key commands**:
```bash
acpx qwen 'inspect failing tests and propose a fix plan'
acpx qwen 'apply the smallest safe fix and run tests'
acpx qwen exec 'summarize repo purpose in 3 lines'
```

### 5. terminal-capture
**Usage**: `/skill terminal-capture`

Automates terminal UI screenshot testing for CLI commands.

**Architecture**: `node-pty → ANSI byte stream → xterm.js (Playwright headless) → Screenshot`

**Usage**:
```bash
npx tsx integration-tests/terminal-capture/run.ts integration-tests/terminal-capture/scenarios/about.ts
```

## Available Commands

### qc/code-review
**Usage**: `/qc code-review [PR_NUMBER]`

Expert code reviewer agent. Analyzes PRs for correctness, conventions, performance, test coverage, and security.

### qc/commit
**Usage**: `/qc commit`

Generates AI commit messages from staged changes.

**Workflow**:
1. Check `git status`
2. Review staged changes
3. Handle branch logic
4. Generate commit message
5. Commit and push after approval

### qc/create-issue
**Usage**: `/qc create-issue [DESCRIPTION]`

Creates a GitHub issue from user idea/bug description.

### qc/create-pr
**Usage**: `/qc create-pr`

Creates a PR from staged changes with proper description template.

## Build Commands

### Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

### Running CLI Generator
```bash
python generate.py --config carousel.yaml --theme dark_purple --output output/
python generate.py --config carousel.yaml --theme random
python generate.py --config carousel.yaml --format pdf
python generate.py --config carousel.yaml --variants 5  # Generate 5 color variants
```

### Running Web App
```bash
python app.py
# Access at http://localhost:5000
```

### Available Themes
- `dark_purple` (default)
- `dark_blue`
- `dark_green`
- `dark_red`
- `dark_orange`
- `random` (generates harmonious random theme)

## Linting & Testing

### No test framework configured
To add tests, install pytest:
```bash
pip install pytest
pytest                    # Run all tests
pytest tests/test_xxx.py  # Run specific test file
pytest -k test_name       # Run single test by name
```

### No linter configured
To add linting:
```bash
pip install ruff
ruff check .              # Lint all files
ruff check generate.py    # Lint single file
ruff check --fix .        # Auto-fix issues
```

## Code Style Guidelines

### General
- Python 3.8+ compatible
- 4-space indentation (no tabs)
- Maximum line length: 120 characters

### Imports
Order: stdlib → third-party → local imports
```python
import os
import sys
import uuid
import json
import zipfile
import threading
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file, abort

from generate import generate_carousel
from themes import THEMES, get_theme
```

### Naming Conventions
- **Variables/functions**: snake_case (`output_dir`, `generate_carousel`)
- **Constants**: SCREAMING_SNAKE_CASE (`THEMES`, `DEFAULT_FORMAT`)
- **Classes**: PascalCase (e.g., `PdfWriter`, if used)
- **Private functions**: prefix with underscore `_internal_func()`

### Type Hints
Use type hints for function parameters and return types:
```python
def generate_carousel(config_path: str, theme_name: str,
                     output_dir: str, format: str = "png") -> list:
def get_theme(name: str) -> dict:
```

### Error Handling
- Use specific exception types
- Provide contextual error messages
```python
if name not in THEMES:
    raise ValueError(f"Thème inconnu: {name}. Disponibles: {list(THEMES.keys())} + 'random'")
```

### Docstrings
Use triple quotes. Keep brief (1-2 sentences):
```python
def merge_pdfs(pdf_files: list, output_path: str):
    """Fusionne plusieurs PDFs en un seul carousel."""
```

### String Formatting
- Use f-strings for simple interpolation
- Use `.format()` for complex cases

### Code Organization
1. Module-level docstring
2. Imports
3. Constants (THEMES, config)
4. Helper functions
5. Main functions
6. `if __name__ == "__main__":` block (keep minimal)

### Jinja2 Templates
- Template files use `.j2` extension
- Filters defined in Python (e.g., `hex_to_rgb`)
- Keep complex logic in Python; templates should be simple

### Flask Routes
- Group routes by logical concern
- Use route decorators consistently
- Return JSON with `jsonify()` for API endpoints

### File Paths
- Use `pathlib.Path` for path operations
- Use `os.path.join()` for string paths
- Always use `encoding="utf-8"` for text file operations

### Constants
Define at module level with clear names:
```python
DEFAULT_THEME = "dark_purple"
DEFAULT_FORMAT = "png"
VIEWPORT_SIZE = {"width": 1080, "height": 1080}
```

### Configuration Files
- YAML files: use `yaml.safe_load()` for loading
- Never execute untrusted YAML (no `unsafe` loader)

### Playwright Usage
- Use `sync_playwright()` context manager
- Launch browser with `p.chromium.launch()`
- Close pages and browsers explicitly
- Use `wait_for_timeout()` for font loading

### Thread Safety
- Flask runs in threads; use thread-local storage for job tracking
- Background jobs use `threading.Thread(target=run, daemon=True)`
