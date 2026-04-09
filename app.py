"""
app.py - Application web Flask pour le générateur de carousel
Lancement : python app.py
Accès      : http://localhost:5000
"""

import os
import uuid
import json
import zipfile
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, abort
from generate import generate_carousel
from themes import THEMES, get_theme
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


@app.route('/api/themes')
def api_themes():
    """Retourne les thèmes disponibles avec aperçu des couleurs."""
    result = {}
    for name, t in THEMES.items():
        result[name] = {
            'accent1': t['accent1'],
            'accent2': t['accent2'],
            'bg':      t['bg'],
        }
    result['random'] = {'accent1': '#ffffff', 'accent2': '#aaaaaa', 'bg': '#111111'}
    return jsonify(result)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Lance la génération en arrière-plan, retourne un job_id."""
    data = request.json or {}

    slides_raw = data.get('slides', [])
    theme_name = data.get('theme', 'dark_purple')
    fmt        = data.get('format', 'png')
    footer     = data.get('footer', {'series': 'My Series', 'author': 'author'})

    if not slides_raw:
        return jsonify({'error': 'Aucune slide fournie'}), 400

    # Construire la config en mémoire (sans fichier YAML)
    config = {'footer': footer, 'slides': slides_raw}

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {'status': 'running', 'files': [], 'error': None}

    def run():
        try:
            out_dir = app.config['OUTPUT_DIR'] / job_id
            files = generate_carousel_from_dict(config, theme_name, str(out_dir), fmt)
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

    return send_file(str(zip_path), as_attachment=True, download_name='carousel.zip')


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

def generate_carousel_from_dict(config: dict, theme_name: str, output_dir: str, fmt: str):
    """Génère le carousel directement depuis un dict Python (sans fichier YAML)."""
    import yaml, tempfile

    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False, encoding='utf-8') as tmp:
        yaml.dump(config, tmp, allow_unicode=True)
        tmp_path = tmp.name

    try:
        files = generate_carousel(tmp_path, theme_name, output_dir, fmt)
    finally:
        os.unlink(tmp_path)

    return files


# ─────────────────────────────────────────

if __name__ == '__main__':
    print("🚀 Carousel Generator Web — http://localhost:5000")
    app.run(debug=True, port=5000)
