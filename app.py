"""
app.py - Application web Flask pour le générateur de carousel
Lancement : python app.py
Accès      : http://localhost:5000
"""

import os
import re
import uuid
import json
import shutil
import zipfile
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, abort
from generate import generate_carousel
from themes import THEMES, IG_THEMES, get_theme
from md_parser import parse_markdown_to_slides, _analyze_structure

app = Flask(__name__)
app.config['SECRET_KEY'] = 'carousel-generator-key'
app.config['OUTPUT_DIR'] = Path('static/generated')
app.config['OUTPUT_DIR'].mkdir(parents=True, exist_ok=True)

# Stockage en mémoire des jobs en cours
jobs = {}

# ─────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────

@app.route('/')
def index():
    theme_names = list(THEMES.keys()) + ['random']
    return render_template('index.html', themes=theme_names)


@app.route('/generator')
def generator():
    return render_template('generator.html')


# ─────────────────────────────────────────
#  LIBRARY API — lecture disque (persistante)
# ─────────────────────────────────────────

def _scan_job_folder(folder: Path) -> dict | None:
    """Lit un dossier de job et retourne ses métadonnées."""
    if not folder.is_dir():
        return None
    job_id = folder.name
    files = list(folder.iterdir())
    pngs  = sorted([f for f in files if f.suffix == '.png'], key=lambda f: f.name)
    pdfs  = [f for f in files if f.suffix == '.pdf']
    zips  = [f for f in files if f.suffix == '.zip']

    total_size = sum(f.stat().st_size for f in files if f.is_file())
    stat = folder.stat()

    # Extraire date / heure / nom depuis le job_id
    m = re.match(r'^(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})_(.+)$', job_id)
    if m:
        date_part, time_part, name_part = m.group(1), m.group(2), m.group(3)
        created_iso = f"{date_part}T{time_part.replace('-', ':')}"
        display_name = name_part.replace('_', ' ')
    else:
        created_iso  = datetime.fromtimestamp(stat.st_mtime).isoformat()
        display_name = job_id

    return {
        'job_id':       job_id,
        'display_name': display_name,
        'created_at':   created_iso,
        'slide_count':  len(pngs),
        'has_pdf':      len(pdfs) > 0,
        'has_png':      len(pngs) > 0,
        'file_count':   len(files),
        'size_bytes':   total_size,
        'thumbnail':    f'/api/library/{job_id}/thumbnail' if pngs else None,
        'files': [
            {'name': f.name, 'type': f.suffix.lstrip('.'), 'size': f.stat().st_size}
            for f in sorted(files, key=lambda f: f.name) if f.is_file()
        ],
    }


@app.route('/api/library')
def api_library():
    """Liste tous les carousels générés (lecture disque)."""
    out_dir = app.config['OUTPUT_DIR']
    items = []
    for folder in sorted(out_dir.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True):
        meta = _scan_job_folder(folder)
        if meta:
            items.append(meta)

    total_slides = sum(i['slide_count'] for i in items)
    total_size   = sum(i['size_bytes']   for i in items)
    return jsonify({'items': items, 'total': len(items),
                    'total_slides': total_slides, 'total_size': total_size})


@app.route('/api/library/<path:job_id>', methods=['DELETE'])
def api_library_delete(job_id):
    """Supprime un carousel (dossier + tous ses fichiers)."""
    if '..' in job_id or job_id.startswith('/'):
        abort(400)
    folder = app.config['OUTPUT_DIR'] / job_id
    if not folder.exists():
        abort(404)
    shutil.rmtree(folder)
    jobs.pop(job_id, None)
    return jsonify({'ok': True})


@app.route('/api/library/<path:job_id>/rename', methods=['PATCH'])
def api_library_rename(job_id):
    """Renomme l'affichage d'un carousel (renomme le dossier sur le disque)."""
    if '..' in job_id or job_id.startswith('/'):
        abort(400)
    data     = request.json or {}
    new_name = data.get('name', '').strip()
    if not new_name:
        return jsonify({'error': 'Nom invalide'}), 400

    folder = app.config['OUTPUT_DIR'] / job_id
    if not folder.exists():
        abort(404)

    # Conserver la date/heure, remplacer la partie nom
    m = re.match(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_(.+)$', job_id)
    prefix   = m.group(1) if m else job_id
    new_slug = _sanitize_folder_name(new_name)
    new_id   = f"{prefix}_{new_slug}"

    new_folder = app.config['OUTPUT_DIR'] / new_id
    if new_folder.exists():
        return jsonify({'error': 'Un carousel avec ce nom existe déjà'}), 409

    folder.rename(new_folder)
    jobs.pop(job_id, None)
    return jsonify({'ok': True, 'new_job_id': new_id})


@app.route('/api/library/<path:job_id>/thumbnail')
def api_library_thumbnail(job_id):
    """Retourne le premier PNG d'un carousel comme miniature."""
    if '..' in job_id or job_id.startswith('/'):
        abort(400)
    folder = app.config['OUTPUT_DIR'] / job_id
    pngs   = sorted(folder.glob('*.png')) if folder.exists() else []
    if not pngs:
        abort(404)
    return send_file(str(pngs[0]), mimetype='image/png')


@app.route('/api/library/<path:job_id>/slide/<int:index>')
def api_library_slide(job_id, index):
    """Retourne le PNG à l'index donné (pour le viewer lightbox)."""
    if '..' in job_id or job_id.startswith('/'):
        abort(400)
    folder = app.config['OUTPUT_DIR'] / job_id
    pngs   = sorted(folder.glob('*.png')) if folder.exists() else []
    if index < 0 or index >= len(pngs):
        abort(404)
    return send_file(str(pngs[index]), mimetype='image/png')


@app.route('/api/library/<path:job_id>/download')
def api_library_download(job_id):
    """Télécharge un carousel en ZIP (lecture disque, sans mémoire jobs)."""
    if '..' in job_id or job_id.startswith('/'):
        abort(400)
    folder = app.config['OUTPUT_DIR'] / job_id
    if not folder.exists():
        abort(404)

    zip_path = folder / 'carousel.zip'
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for f in folder.iterdir():
            if f.suffix in ('.png', '.pdf'):
                zf.write(f, f.name)

    return send_file(str(zip_path), as_attachment=True,
                     download_name=f'{job_id}.zip')


@app.route('/api/themes', methods=['GET'])
@app.route('/api/themes/', methods=['GET'])
def api_themes():
    """Retourne les thèmes disponibles avec aperçu des couleurs."""
    platform = request.args.get('platform', 'all')
    try:
        result = {}
        theme_sources = {}
        if platform == 'instagram':
            theme_sources = dict(IG_THEMES)
        elif platform == 'linkedin':
            theme_sources = dict(THEMES)
        else:
            theme_sources = {**THEMES, **IG_THEMES}

        for name, t in theme_sources.items():
            result[name] = {
                'accent1':  t['accent1'],
                'accent2':  t['accent2'],
                'bg':       t['bg'],
                'is_light': t.get('is_light', False),
                'platform': 'instagram' if name in IG_THEMES else 'linkedin',
            }
        result['random'] = {
            'accent1': '#ffffff', 'accent2': '#aaaaaa', 'bg': '#111111',
            'is_light': False, 'platform': 'all',
        }
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in api_themes: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Lance la génération en arrière-plan, retourne un job_id."""
    data = request.json or {}

    slides_raw = data.get('slides', [])
    theme_name = data.get('theme', 'dark_purple')
    fmt        = data.get('format', 'png')
    platform   = data.get('platform', 'linkedin')
    footer     = data.get('footer', {'series': 'My Series', 'author': '@Sohaib Baroud'})

    if not slides_raw:
        return jsonify({'error': 'Aucune slide fournie'}), 400

    # Construire la config en mémoire (sans fichier YAML)
    config = {'footer': footer, 'slides': slides_raw}

    # Créer un identifiant descriptif : date_heure_series
    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')       # 2026-04-09
    time_str = now.strftime('%H-%M-%S')       # 14-30-45
    series_name = _sanitize_folder_name(footer.get('series', 'carousel'))
    
    # job_id utilisable comme nom de dossier
    job_id = f"{date_str}_{time_str}_{series_name}"
    jobs[job_id] = {'status': 'running', 'files': [], 'error': None}

    def run():
        try:
            out_dir = app.config['OUTPUT_DIR'] / job_id
            files = generate_carousel_from_dict(config, theme_name, str(out_dir), fmt, platform)
            jobs[job_id]['status'] = 'done'
            # Store relative paths for frontend (without leading /)
            jobs[job_id]['files'] = [f"static/generated/{job_id}/{Path(f).name}" for f in files]
        except Exception as e:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = str(e)

    threading.Thread(target=run, daemon=True).start()
    return jsonify({'job_id': job_id})


@app.route('/api/status/<job_id>')
def api_status(job_id):
    if job_id not in jobs:
        abort(404)
    return jsonify(jobs[job_id])


@app.route('/api/download/<job_id>')
def api_download(job_id):
    """Télécharge toutes les slides d'un job en ZIP."""
    if job_id not in jobs or jobs[job_id]['status'] != 'done':
        abort(404)

    out_dir = app.config['OUTPUT_DIR'] / job_id
    zip_path = out_dir / 'carousel.zip'

    with zipfile.ZipFile(zip_path, 'w') as zf:
        for f in out_dir.iterdir():
            if f.suffix in ('.png', '.pdf'):
                zf.write(f, f.name)

    download_name = f'{job_id}.zip'
    return send_file(str(zip_path), as_attachment=True, download_name=download_name)


@app.route('/api/import-markdown', methods=['POST'])
def api_import_markdown():
    """Importe du contenu Markdown et retourne les slides parsées avec analyse de structure."""
    data = request.json or {}
    md_content = data.get('content', '')

    if not md_content.strip():
        return jsonify({'error': 'Contenu Markdown vide'}), 400

    try:
        result = parse_markdown_to_slides(md_content)
        
        # Ajouter l'analyse de structure pour le frontend
        structure = _analyze_structure(md_content)
        result['structure_analysis'] = {
            'detected_format': 'separators' if structure['has_explicit_separators'] else 
                              'headings' if structure['has_heading_hierarchy'] else
                              'lists' if structure['has_list_structure'] else 'unstructured',
            'confidence': 'high' if structure['has_heading_hierarchy'] or structure['has_explicit_separators'] else 'medium',
            'reorganization_applied': structure['content_density'] == 'high' and not structure['has_heading_hierarchy'],
            'heading_counts': structure['heading_counts'],
            'total_paragraphs': structure['paragraphs'],
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Erreur de parsing: {str(e)}'}), 500


@app.route('/api/download-structure')
def api_download_structure():
    """Télécharge STRUCTURE_COMPLETE.md — le guide de structure pour les skills Claude Code."""
    structure_path = Path(__file__).parent / 'STRUCTURE_COMPLETE.md'
    if not structure_path.exists():
        abort(404, description='STRUCTURE_COMPLETE.md introuvable')
    return send_file(
        str(structure_path),
        as_attachment=True,
        download_name='STRUCTURE_COMPLETE.md',
        mimetype='text/markdown'
    )


@app.route('/api/upload-markdown', methods=['POST'])
def api_upload_markdown():
    """Reçoit un fichier Markdown et retourne les slides parsées avec analyse de structure."""
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    if not file.filename.endswith(('.md', '.markdown')):
        return jsonify({'error': 'Format de fichier non supporté. Utilisez .md ou .markdown'}), 400

    try:
        content = file.read().decode('utf-8')
        result = parse_markdown_to_slides(content)
        
        # Ajouter l'analyse de structure pour le frontend
        structure = _analyze_structure(content)
        result['structure_analysis'] = {
            'detected_format': 'separators' if structure['has_explicit_separators'] else 
                              'headings' if structure['has_heading_hierarchy'] else
                              'lists' if structure['has_list_structure'] else 'unstructured',
            'confidence': 'high' if structure['has_heading_hierarchy'] or structure['has_explicit_separators'] else 'medium',
            'reorganization_applied': structure['content_density'] == 'high' and not structure['has_heading_hierarchy'],
            'heading_counts': structure['heading_counts'],
            'total_paragraphs': structure['paragraphs'],
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Erreur de lecture: {str(e)}'}), 500


# ─────────────────────────────────────────
#  HELPER : génération depuis dict (pas YAML)
# ─────────────────────────────────────────

def _sanitize_folder_name(name: str) -> str:
    """
    Nettoie un nom pour qu'il soit valide comme nom de dossier.
    Supprime les caractères interdits et normalise les espaces.
    """
    import re
    # Remplacer les caractères spéciaux par des underscores
    clean = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remplacer les espaces multiples par un seul underscore
    clean = re.sub(r'[\s_]+', '_', clean)
    # Nettoyer les underscores en début/fin
    clean = clean.strip('_')
    # Limiter la longueur à 40 caractères
    if len(clean) > 40:
        clean = clean[:40]
    return clean if clean else 'carousel'


def generate_carousel_from_dict(config: dict, theme_name: str, output_dir: str, fmt: str,
                                platform: str = "linkedin"):
    """Génère le carousel directement depuis un dict Python (sans fichier YAML)."""
    import yaml, tempfile

    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False, encoding='utf-8') as tmp:
        yaml.dump(config, tmp, allow_unicode=True)
        tmp_path = tmp.name

    try:
        files = generate_carousel(tmp_path, theme_name, output_dir, fmt, platform)
    finally:
        os.unlink(tmp_path)

    return files


# ─────────────────────────────────────────

if __name__ == '__main__':
    print("Carousel Generator Web — http://localhost:5000")
    app.run(debug=True, port=5000, use_reloader=False)
