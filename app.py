"""
app.py - Application web Flask pour le générateur de carousel
Lancement : python app.py
Accès      : http://localhost:5000

Authentification : définir APP_PASSWORD dans l'environnement (ou fichier .env).
"""

import os
import re
import secrets
import shutil
import zipfile
import threading
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse
from flask import (Flask, render_template, request, jsonify,
                   send_file, abort, session, redirect, url_for)
from werkzeug.utils import secure_filename
from generate import generate_carousel
from themes import THEMES, IG_THEMES
from md_parser import parse_markdown_to_slides, _analyze_structure

# Support optionnel pour .env (pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─────────────────────────────────────────
#  Configuration et validation au démarrage
# ─────────────────────────────────────────

SECRET_KEY = os.environ.get('SECRET_KEY', '')
_is_production = os.environ.get('FLASK_ENV') == 'production'
if not SECRET_KEY:
    if _is_production:
        raise RuntimeError(
            "SECRET_KEY doit être définie en production. "
            "Générez une clé : python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    import warnings
    warnings.warn(
        "SECRET_KEY non définie — clé aléatoire éphémère utilisée (sessions invalidées au redémarrage). "
        "Définissez SECRET_KEY dans votre .env.",
        RuntimeWarning, stacklevel=1
    )
    SECRET_KEY = secrets.token_hex(32)

APP_PASSWORD = os.environ.get('APP_PASSWORD', '')
if not APP_PASSWORD:
    import warnings
    warnings.warn(
        "APP_PASSWORD n'est pas définie — l'application est accessible sans authentification. "
        "Définissez APP_PASSWORD dans votre .env pour activer la protection.",
        RuntimeWarning, stacklevel=1
    )

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['OUTPUT_DIR'] = Path('static/generated')
app.config['OUTPUT_DIR'].mkdir(parents=True, exist_ok=True)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB max upload

# Sécurité des cookies de session
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# SESSION_COOKIE_SECURE activé uniquement en production (HTTPS)
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV', 'development') == 'production'

# ─────────────────────────────────────────
#  Rate limiting (flask-limiter)
# ─────────────────────────────────────────

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[],
        storage_uri='memory://',
    )
    _login_limit = limiter.limit('10 per minute; 30 per hour')
except ImportError:
    # flask-limiter non installé — continuer sans rate limiting (avertir)
    import warnings
    warnings.warn("flask-limiter non installé — le rate limiting sur /login est désactivé.", RuntimeWarning)
    def _login_limit(f):
        return f


# Stockage en mémoire des jobs en cours
jobs = {}


# ─────────────────────────────────────────
#  HELPERS DE SÉCURITÉ
# ─────────────────────────────────────────

def _safe_next_url(next_param: str) -> str:
    """Valide que l'URL de redirection est locale (prévient open redirect).
    Rejette toute URL avec un host ou un schéma externe."""
    if not next_param:
        return url_for('index')
    parsed = urlparse(next_param)
    # Rejeter les URLs absolues (avec netloc ou schéma)
    if parsed.netloc or parsed.scheme:
        return url_for('index')
    # Rejeter les paths vides ou suspects
    if not next_param.startswith('/') or '//' in next_param:
        return url_for('index')
    return next_param


def _safe_job_folder(job_id: str) -> Path:
    """Retourne le Path résolu du dossier de job en vérifiant le confinement.
    Lève HTTP 400 si job_id tente de sortir du dossier de sortie (path traversal)."""
    out_dir = app.config['OUTPUT_DIR'].resolve()
    folder = (out_dir / job_id).resolve()
    try:
        folder.relative_to(out_dir)
    except ValueError:
        abort(400)
    return folder


# ─────────────────────────────────────────
#  EN-TÊTES DE SÉCURITÉ (after_request)
# ─────────────────────────────────────────

@app.after_request
def security_headers(response):
    """Ajoute les en-têtes de sécurité HTTP à chaque réponse."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # PDF iframe nécessite SAMEORIGIN (pas DENY)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: blob:; "
        "connect-src 'self'; "
        "frame-src 'self'; "
        "object-src 'none';"
    )
    # HSTS uniquement en production (HTTPS requis)
    if os.environ.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


# ─────────────────────────────────────────
#  AUTHENTIFICATION (before_request)
# ─────────────────────────────────────────

# Routes publiques (pas besoin d'être connecté)
_PUBLIC_PREFIXES = ('/login', '/static/css/', '/static/js/', '/static/fonts/',
                    '/static/img/', '/favicon')

@app.before_request
def require_login():
    """Vérifie l'authentification avant chaque requête."""
    # Pas de mot de passe configuré → accès libre (mode dev)
    if not APP_PASSWORD:
        return

    # Routes publiques toujours accessibles
    if any(request.path.startswith(p) for p in _PUBLIC_PREFIXES):
        return

    # Déjà authentifié
    if session.get('authenticated'):
        return

    # API → 401 JSON
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Non authentifié'}), 401

    # Pages → redirection vers login
    return redirect(url_for('login', next=request.path))


@app.route('/login', methods=['GET', 'POST'])
@_login_limit
def login():
    # Déjà connecté
    if session.get('authenticated'):
        return redirect(url_for('index'))

    # Valider next dès le GET pour ne passer que des URLs sûres au template
    safe_next = _safe_next_url(request.args.get('next', ''))

    error = None
    if request.method == 'POST':
        pwd = request.form.get('password', '')
        # Comparaison en temps constant pour éviter timing attacks
        if APP_PASSWORD and secrets.compare_digest(pwd.encode(), APP_PASSWORD.encode()):
            session.permanent = True
            session['authenticated'] = True
            sep = '&' if '?' in safe_next else '?'
            return redirect(safe_next + sep + 'toast=connected')
        error = 'Mot de passe incorrect.'

    return render_template('login.html', error=error, safe_next=safe_next)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login') + '?toast=disconnected')

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
    # cover_thumb.png is a library thumbnail saved before PDF cleanup — exclude from slide count
    all_pngs   = sorted([f for f in files if f.suffix == '.png'], key=lambda f: f.name)
    slide_pngs = [f for f in all_pngs if f.name != 'cover_thumb.png']
    thumb_png  = next((f for f in all_pngs if f.name == 'cover_thumb.png'), None)
    pdfs  = [f for f in files if f.suffix == '.pdf']

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

    # Thumbnail: prefer first slide PNG, fall back to cover_thumb.png (PDF-only carousels)
    has_any_png = len(slide_pngs) > 0 or thumb_png is not None
    thumbnail   = f'/api/library/{job_id}/thumbnail' if has_any_png else None

    return {
        'job_id':       job_id,
        'display_name': display_name,
        'created_at':   created_iso,
        'slide_count':  len(slide_pngs),
        'has_pdf':      len(pdfs) > 0,
        'has_png':      len(slide_pngs) > 0,
        'file_count':   len(files),
        'size_bytes':   total_size,
        'thumbnail':    thumbnail,
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
    folder = _safe_job_folder(job_id)
    if not folder.exists():
        abort(404)
    shutil.rmtree(folder)
    jobs.pop(job_id, None)
    return jsonify({'ok': True})


@app.route('/api/library/<path:job_id>/rename', methods=['PATCH'])
def api_library_rename(job_id):
    """Renomme l'affichage d'un carousel (renomme le dossier sur le disque)."""
    folder = _safe_job_folder(job_id)
    data     = request.json or {}
    new_name = data.get('name', '').strip()
    if not new_name:
        return jsonify({'error': 'Nom invalide'}), 400
    if len(new_name) > 200:
        return jsonify({'error': 'Nom trop long (max 200 caractères)'}), 400

    if not folder.exists():
        abort(404)

    # Conserver la date/heure, remplacer la partie nom
    m = re.match(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_(.+)$', job_id)
    prefix   = m.group(1) if m else job_id
    new_slug = _sanitize_folder_name(new_name)
    new_id   = f"{prefix}_{new_slug}"

    new_folder = _safe_job_folder(new_id)
    if new_folder.exists():
        return jsonify({'error': 'Un carousel avec ce nom existe déjà'}), 409

    folder.rename(new_folder)
    jobs.pop(job_id, None)
    return jsonify({'ok': True, 'new_job_id': new_id})


@app.route('/api/library/<path:job_id>/pdf')
def api_library_pdf(job_id):
    """Sert le PDF d'un carousel pour visualisation inline (pas en téléchargement)."""
    folder = _safe_job_folder(job_id)
    if not folder.exists():
        abort(404)
    pdfs = sorted([f for f in folder.glob('*.pdf') if f.name != 'carousel.zip'])
    if not pdfs:
        abort(404)
    return send_file(str(pdfs[0]), mimetype='application/pdf')


@app.route('/api/library/<path:job_id>/thumbnail')
def api_library_thumbnail(job_id):
    """Retourne le premier PNG d'un carousel comme miniature.
    Pour les carousels PDF, utilise cover_thumb.png comme fallback."""
    folder = _safe_job_folder(job_id)
    if not folder.exists():
        abort(404)
    slide_pngs = sorted([f for f in folder.glob('*.png') if f.name != 'cover_thumb.png'])
    if slide_pngs:
        return send_file(str(slide_pngs[0]), mimetype='image/png')
    thumb = folder / 'cover_thumb.png'
    if thumb.exists():
        return send_file(str(thumb), mimetype='image/png')
    abort(404)


@app.route('/api/library/<path:job_id>/slide/<int:index>')
def api_library_slide(job_id, index):
    """Retourne le PNG à l'index donné (pour le viewer lightbox).
    Exclut cover_thumb.png des slides numérotées."""
    folder = _safe_job_folder(job_id)
    pngs   = sorted([f for f in folder.glob('*.png') if f.name != 'cover_thumb.png']) if folder.exists() else []
    if index < 0 or index >= len(pngs):
        abort(404)
    return send_file(str(pngs[index]), mimetype='image/png')


@app.route('/api/library/<path:job_id>/download')
def api_library_download(job_id):
    """Télécharge un carousel en ZIP (lecture disque, sans mémoire jobs)."""
    folder = _safe_job_folder(job_id)
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
    except Exception:
        app.logger.exception("Error in api_themes")
        return jsonify({'error': 'Erreur interne du serveur'}), 500


# Balises HTML dangereuses à interdire dans les corps de slides (exécution dans Playwright)
_DANGEROUS_TAGS = re.compile(
    r'<\s*/?\s*(script|iframe|object|embed|form|input|base|meta|link|svg|math)'
    r'(\s[^>]*)?>',
    re.IGNORECASE
)

def _sanitize_slide_body(body: str) -> str:
    """Supprime les balises HTML dangereuses du corps d'une slide avant le rendu Playwright."""
    return _DANGEROUS_TAGS.sub('', body) if isinstance(body, str) else body


@app.route('/api/generate', methods=['POST'])
@limiter.limit('15 per minute; 100 per hour')
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

    # Sanitiser les corps HTML avant rendu Playwright (H5 — XSS dans Chromium headless)
    for slide in slides_raw:
        if 'body' in slide:
            slide['body'] = _sanitize_slide_body(slide['body'])
        if 'columns' in slide:
            for col in slide.get('columns', []):
                if 'body' in col:
                    col['body'] = _sanitize_slide_body(col['body'])

    config = {'footer': footer, 'slides': slides_raw}

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H-%M-%S')
    series_name = _sanitize_folder_name(footer.get('series', 'carousel'))
    job_id = f"{date_str}_{time_str}_{series_name}"
    jobs[job_id] = {'status': 'running', 'files': [], 'error': None}

    def run():
        try:
            out_dir = app.config['OUTPUT_DIR'] / job_id
            files = generate_carousel_from_dict(config, theme_name, str(out_dir), fmt, platform)
            jobs[job_id]['status'] = 'done'
            jobs[job_id]['files'] = [f"static/generated/{job_id}/{Path(f).name}" for f in files]
        except Exception:
            app.logger.exception(f"Error generating job {job_id}")
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['error'] = 'Erreur interne de génération.'

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

    return send_file(str(zip_path), as_attachment=True, download_name=f'{job_id}.zip')


_MD_MAX_BYTES = 500_000  # 500 KB — protection contre les bombes YAML/Markdown


@app.route('/api/import-markdown', methods=['POST'])
@limiter.limit('30 per minute')
def api_import_markdown():
    """Importe du contenu Markdown et retourne les slides parsées avec analyse de structure."""
    data = request.json or {}
    md_content = data.get('content', '')

    if not md_content.strip():
        return jsonify({'error': 'Contenu Markdown vide'}), 400

    if len(md_content) > _MD_MAX_BYTES:
        return jsonify({'error': f'Contenu trop volumineux (max {_MD_MAX_BYTES // 1000} KB)'}), 413

    try:
        result = parse_markdown_to_slides(md_content)
        structure = _analyze_structure(md_content)
        result['structure_analysis'] = {
            'detected_format': ('separators' if structure['has_explicit_separators'] else
                                'headings' if structure['has_heading_hierarchy'] else
                                'lists' if structure['has_list_structure'] else 'unstructured'),
            'confidence': ('high' if structure['has_heading_hierarchy'] or structure['has_explicit_separators']
                           else 'medium'),
            'reorganization_applied': (structure['content_density'] == 'high' and
                                       not structure['has_heading_hierarchy']),
            # heading_counts est un dict de valeurs entières — sans données utilisateur
            'heading_counts': structure['heading_counts'],
            'total_paragraphs': structure['paragraphs'],
        }
        return jsonify(result)
    except Exception:
        app.logger.exception("Error in api_import_markdown")
        return jsonify({'error': 'Erreur de parsing du Markdown'}), 500


@app.route('/api/download-structure')
def api_download_structure():
    """Télécharge STRUCTURE_COMPLETE.md."""
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

    safe_name = secure_filename(file.filename)
    if not safe_name.lower().endswith(('.md', '.markdown')):
        return jsonify({'error': 'Format de fichier non supporté. Utilisez .md ou .markdown'}), 400

    try:
        content = file.read().decode('utf-8')
    except (UnicodeDecodeError, Exception):
        return jsonify({'error': 'Impossible de lire le fichier (encodage invalide)'}), 400

    if len(content) > _MD_MAX_BYTES:
        return jsonify({'error': f'Fichier trop volumineux (max {_MD_MAX_BYTES // 1000} KB)'}), 413

    try:
        result = parse_markdown_to_slides(content)
        structure = _analyze_structure(content)
        result['structure_analysis'] = {
            'detected_format': ('separators' if structure['has_explicit_separators'] else
                                'headings' if structure['has_heading_hierarchy'] else
                                'lists' if structure['has_list_structure'] else 'unstructured'),
            'confidence': ('high' if structure['has_heading_hierarchy'] or structure['has_explicit_separators']
                           else 'medium'),
            'reorganization_applied': (structure['content_density'] == 'high' and
                                       not structure['has_heading_hierarchy']),
            'heading_counts': structure['heading_counts'],
            'total_paragraphs': structure['paragraphs'],
        }
        return jsonify(result)
    except Exception:
        app.logger.exception("Error in api_upload_markdown")
        return jsonify({'error': 'Erreur de lecture du fichier Markdown'}), 500


# ─────────────────────────────────────────
#  HELPER : sanitisation et génération
# ─────────────────────────────────────────

def _sanitize_folder_name(name: str) -> str:
    """Nettoie un nom pour qu'il soit valide comme nom de dossier."""
    # Remplacer les caractères interdits par des underscores
    clean = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remplacer les espaces multiples par un seul underscore
    clean = re.sub(r'[\s_]+', '_', clean)
    # Supprimer underscores et points en début/fin (évite fichiers cachés + noms invalides Windows)
    clean = clean.strip('_').strip('.')
    if len(clean) > 40:
        clean = clean[:40]
    return clean if clean else 'carousel'


def generate_carousel_from_dict(config: dict, theme_name: str, output_dir: str, fmt: str,
                                platform: str = "linkedin"):
    """Génère le carousel directement depuis un dict Python (sans fichier YAML)."""
    import yaml
    import tempfile

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
    _debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    print("Carousel Generator Web — http://localhost:5000")
    app.run(debug=_debug, port=5000, use_reloader=False)
