"""
main.py - Application FastAPI pour Carousel Generator
Déploiement sur Hugging Face Spaces
"""

import os
import uuid
import json
import zipfile
import threading
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import des modules du générateur
from generate import generate_carousel, _sanitize_filename
from themes import THEMES, get_theme
from md_parser import parse_markdown_to_slides, _analyze_structure

app = FastAPI(title="Carousel Generator", version="2.0.0")

# Configuration
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "static" / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Templates et static
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Stockage des jobs en mémoire
jobs: Dict[str, Dict] = {}

# ─────────────────────────────────────────
#  MODÈLES PYDANTIC
# ─────────────────────────────────────────

class SlideData(BaseModel):
    slides: List[Dict]
    theme: str = "dark_purple"
    format: str = "png"
    footer: Dict[str, str] = {"series": "My Series", "author": "author"}

class MarkdownImport(BaseModel):
    content: str

# ─────────────────────────────────────────
#  ROUTES WEB
# ─────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request):
    """Page principale de l'application."""
    theme_names = list(THEMES.keys()) + ['random']
    return templates.TemplateResponse("index.html", {
        "request": request,
        "themes": theme_names
    })

# ─────────────────────────────────────────
#  API ENDPOINTS
# ─────────────────────────────────────────

@app.get("/api/themes")
async def api_themes():
    """Retourne les thèmes disponibles avec aperçu des couleurs."""
    result = {}
    for name, t in THEMES.items():
        result[name] = {
            'accent1': t['accent1'],
            'accent2': t['accent2'],
            'bg': t['bg'],
        }
    result['random'] = {'accent1': '#ffffff', 'accent2': '#aaaaaa', 'bg': '#111111'}
    return JSONResponse(content=result)

@app.post("/api/generate")
async def api_generate(data: SlideData):
    """Lance la génération en arrière-plan, retourne un job_id."""
    if not data.slides:
        raise HTTPException(status_code=400, detail="Aucune slide fournie")

    # Créer un identifiant descriptif : date_heure_series
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H-%M-%S')
    series_name = _sanitize_filename(data.footer.get('series', 'carousel'))
    
    job_id = f"{date_str}_{time_str}_{series_name}"
    jobs[job_id] = {'status': 'running', 'files': [], 'error': None}

    def run():
        try:
            out_dir = OUTPUT_DIR / job_id
            config = {'footer': data.footer, 'slides': data.slides}
            
            # Écrire la config temporaire
            import yaml
            import tempfile
            with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False, encoding='utf-8') as tmp:
                yaml.dump(config, tmp, allow_unicode=True)
                tmp_path = tmp.name
            
            try:
                files = generate_carousel(tmp_path, data.theme, str(out_dir), data.format)
                jobs[job_id]['status'] = 'done'
                jobs[job_id]['files'] = [f"static/generated/{job_id}/{Path(f).name}" for f in files]
            finally:
                os.unlink(tmp_path)
        except Exception as e:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = str(e)

    threading.Thread(target=run, daemon=True).start()
    return JSONResponse(content={'job_id': job_id})

@app.get("/api/status/{job_id}")
async def api_status(job_id: str):
    """Vérifie le statut d'un job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job non trouvé")
    return JSONResponse(content=jobs[job_id])

@app.get("/api/download/{job_id}")
async def api_download(job_id: str):
    """Télécharge toutes les slides d'un job en ZIP."""
    if job_id not in jobs or jobs[job_id]['status'] != 'done':
        raise HTTPException(status_code=404, detail="Job non terminé")

    out_dir = OUTPUT_DIR / job_id
    zip_path = out_dir / 'carousel.zip'

    with zipfile.ZipFile(zip_path, 'w') as zf:
        for f in out_dir.iterdir():
            if f.suffix in ('.png', '.pdf'):
                zf.write(f, f.name)

    return FileResponse(
        str(zip_path),
        media_type='application/zip',
        filename='carousel.zip'
    )

@app.post("/api/import-markdown")
async def api_import_markdown(data: MarkdownImport):
    """Importe du contenu Markdown et retourne les slides parsées."""
    if not data.content.strip():
        raise HTTPException(status_code=400, detail="Contenu Markdown vide")

    try:
        result = parse_markdown_to_slides(data.content)
        structure = _analyze_structure(data.content)
        result['structure_analysis'] = {
            'detected_format': 'separators' if structure['has_explicit_separators'] else 
                              'headings' if structure['has_heading_hierarchy'] else
                              'lists' if structure['has_list_structure'] else 'unstructured',
            'confidence': 'high' if structure['has_heading_hierarchy'] or structure['has_explicit_separators'] else 'medium',
            'reorganization_applied': structure['content_density'] == 'high' and not structure['has_heading_hierarchy'],
            'heading_counts': structure['heading_counts'],
            'total_paragraphs': structure['paragraphs'],
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de parsing: {str(e)}")

@app.post("/api/upload-markdown")
async def api_upload_markdown(file: UploadFile = File(...)):
    """Reçoit un fichier Markdown et retourne les slides parsées."""
    if not file.filename or not file.filename.endswith(('.md', '.markdown')):
        raise HTTPException(status_code=400, detail="Format non supporté. Utilisez .md ou .markdown")

    try:
        content = await file.read()
        content_str = content.decode('utf-8')
        result = parse_markdown_to_slides(content_str)
        structure = _analyze_structure(content_str)
        result['structure_analysis'] = {
            'detected_format': 'separators' if structure['has_explicit_separators'] else 
                              'headings' if structure['has_heading_hierarchy'] else
                              'lists' if structure['has_list_structure'] else 'unstructured',
            'confidence': 'high' if structure['has_heading_hierarchy'] or structure['has_explicit_separators'] else 'medium',
            'reorganization_applied': structure['content_density'] == 'high' and not structure['has_heading_hierarchy'],
            'heading_counts': structure['heading_counts'],
            'total_paragraphs': structure['paragraphs'],
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de lecture: {str(e)}")
