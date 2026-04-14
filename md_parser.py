"""
md_parser.py - Parseur ultra-intelligent de Markdown pour Carousel Generator
Reorganise automatiquement du Markdown non-structuré en slides standardisées.
"""

import re
from typing import Any, Dict, List
from urllib.parse import urlparse

import yaml


def parse_markdown_to_slides(md_content: str) -> Dict[str, Any]:
    """
    Parse du contenu Markdown et retourne une structure de carousel complète.

    Support avancé:
    - Réorganisation automatique du contenu non-structuré
    - Détection de thèmes/logiques pour regrouper le contenu
    - Extraction intelligente de la structure implicite
    - YAML front matter (--- ... ---) pour footer/series/author
    - Séparateurs --- ou *** entre slides
    - Headings # ## ### comme titres de slides
    - Listes à puces converties en bullet points
    - Code blocks inline et multi-lignes
    - Détection automatique du type de slide (cover vs content vs compare)
    - Découpage intelligent des gros blocs de texte
    """

    # 1. Extraire le front matter YAML si présent
    front_matter = {}
    content = md_content.strip()  # Strip leading/trailing whitespace first
    front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if front_matter_match:
        try:
            front_matter = yaml.safe_load(front_matter_match.group(1)) or {}
            content = content[front_matter_match.end():]
        except yaml.YAMLError:
            pass

    # 2. Nettoyage préliminaire
    content = _clean_content(content)

    # 3. Analyser la structure du contenu
    structure = _analyze_structure(content)

    # 4. Parser selon la structure détectée
    # Le front matter est déjà extrait de `content` — les séparateurs restants sont réels.
    # Priorité: separators > headings > lists > unstructured
    has_real_separators = structure['has_explicit_separators']
    if has_real_separators:
        slides = _parse_with_separators(content)
    elif structure['has_heading_hierarchy']:
        slides = _parse_with_headings(content)
    elif structure['has_list_structure']:
        slides = _parse_with_lists(content)
    else:
        # Contenu complètement non structuré → réorganisation intelligente
        slides = _reorganize_unstructured_content(content)

    # 5. Réorganiser les slides selon la structure standard
    slides = _reorganize_slides(slides, structure)

    # 6. Enrichir les slides
    slides = _enrich_slides(slides)

    # 7. Construire la structure finale
    raw_author = front_matter.get('author', front_matter.get('username', ''))
    # Normaliser : ton_compte / vide → auteur par défaut
    DEFAULT_AUTHOR = '@Sohaib Baroud'
    author = raw_author if raw_author and raw_author not in ('ton_compte', 'username', '@username') else DEFAULT_AUTHOR
    footer = {
        'series': front_matter.get('series', front_matter.get('title', 'Series')),
        'author': author
    }

    return {
        'footer': footer,
        'slides': slides,
        'structure_info': structure  # Infos sur la structure détectée
    }


def _clean_content(content: str) -> str:
    """Nettoie le contenu Markdown des éléments inutiles."""
    # Supprimer les commentaires HTML
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Normaliser les sauts de ligne multiples
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Supprimer les espaces en fin de ligne
    content = '\n'.join(line.rstrip() for line in content.split('\n'))

    return content.strip()


def _analyze_structure(content: str) -> Dict[str, Any]:
    """Analyse la structure du contenu Markdown pour déterminer la meilleure approche."""
    lines = content.split('\n')

    # Compter les éléments structurels
    heading_counts = {'h1': 0, 'h2': 0, 'h3': 0}
    # Ignorer les séparateurs qui font partie du front matter YAML
    has_separators = bool(re.search(r'\n---+\s*\n|\n\*\*\*+\s*\n', content)) and not content.strip().startswith('---')
    list_items = 0
    code_blocks = 0
    paragraphs = 0

    for line in lines:
        if re.match(r'^#\s+', line):
            heading_counts['h1'] += 1
        elif re.match(r'^##\s+', line):
            heading_counts['h2'] += 1
        elif re.match(r'^###\s+', line):
            heading_counts['h3'] += 1
        elif re.match(r'^[-*]\s+', line):
            list_items += 1
        elif line.strip().startswith('```'):
            code_blocks += 1
        elif line.strip() and not line.strip().startswith('#'):
            paragraphs += 1

    # Détecter la hiérarchie des headings
    has_heading_hierarchy = (heading_counts['h1'] > 0 or heading_counts['h2'] > 0)

    # Détecter les patterns de comparaison
    compare_indicators = 0
    for line in lines:
        if re.search(r'\bvs\.?\b|\bversus\b|\bcompar[ée]\b|\bdifference\b', line, re.IGNORECASE):
            compare_indicators += 1

    # Calculer la densité de contenu
    total_lines = len([ln for ln in lines if ln.strip()])

    return {
        'heading_counts': heading_counts,
        'has_explicit_separators': has_separators,
        'has_heading_hierarchy': has_heading_hierarchy,
        'has_list_structure': list_items > 5,
        'list_items': list_items,
        'code_blocks': code_blocks,
        'paragraphs': paragraphs,
        'compare_indicators': compare_indicators,
        'total_lines': total_lines,
        'content_density': 'high' if total_lines > 50 else 'medium' if total_lines > 20 else 'low'
    }


def _parse_with_separators(content: str) -> List[Dict[str, Any]]:
    """Parse le Markdown en utilisant --- ou *** comme séparateur de slides."""
    sections = re.split(r'\n(?:---+|\*\*\*+)\s*\n', content.strip())

    slides = []
    for section in sections:
        section = section.strip()
        if not section:
            continue

        slide = _parse_section_to_slide(section)
        slides.append(slide)

    return slides


def _parse_with_headings(content: str) -> List[Dict[str, Any]]:
    """Parse le Markdown en utilisant les headings (# ## ###) comme délimiteurs."""
    lines = content.split('\n')
    slides = []
    current_slide_lines = []

    for line in lines:
        heading_match = re.match(r'^(#{1,2})\s+(.+)$', line)
        if heading_match:
            # Sauvegarder la slide précédente
            if current_slide_lines:
                slide_text = '\n'.join(current_slide_lines).strip()
                if slide_text:
                    slides.append(_parse_section_to_slide(slide_text))
                current_slide_lines = []
            # heading trouvé — la slide précédente a été sauvegardée ci-dessus

        current_slide_lines.append(line)

    # Dernière slide
    if current_slide_lines:
        slide_text = '\n'.join(current_slide_lines).strip()
        if slide_text:
            slides.append(_parse_section_to_slide(slide_text))

    # Si aucune slide détectée (pas de headings), créer une seule slide
    if not slides and content.strip():
        slides.append(_parse_section_to_slide(content.strip()))

    return slides


def _parse_with_lists(content: str) -> List[Dict[str, Any]]:
    """Parse le contenu structuré en listes pour créer des slides."""
    lines = content.split('\n')
    slides = []
    current_list = []
    current_title = ''

    for line in lines:
        # Détecter un heading
        heading_match = re.match(r'^(#{1,2})\s+(.+)$', line)
        if heading_match:
            # Sauvegarder la liste précédente
            if current_list:
                slides.append({
                    'type': 'content',
                    'title': current_title or 'Content',
                    'body': _markdown_to_html('\n'.join(current_list))
                })
                current_list = []
            current_title = heading_match.group(2).strip()
            continue

        # Détecter un item de liste
        list_match = re.match(r'^[-*]\s+(.+)$', line.strip())
        if list_match:
            current_list.append(line.strip())
        elif line.strip() and not list_match:
            # Ligne normale → potentiel titre ou description
            if not current_title:
                current_title = line.strip()

    # Dernière liste
    if current_list:
        slides.append({
            'type': 'content',
            'title': current_title or 'Content',
            'body': _markdown_to_html('\n'.join(current_list))
        })

    return slides


def _reorganize_unstructured_content(content: str) -> List[Dict[str, Any]]:
    """
    Réorganise un contenu complètement non structuré en slides cohérentes.
    C'est la fonction la plus intelligente du parser.
    """
    lines = content.split('\n')
    slides = []

    # Stratégie 1: Détecter les paragraphes thématiques
    paragraphs = []
    current_para = []

    for line in lines:
        if not line.strip():
            if current_para:
                paragraphs.append('\n'.join(current_para).strip())
                current_para = []
        else:
            current_para.append(line.strip())

    if current_para:
        paragraphs.append('\n'.join(current_para).strip())

    # Si on a des paragraphes, les transformer en slides
    if len(paragraphs) >= 2:
        for i, para in enumerate(paragraphs):
            # Extraire un titre depuis le premier segment
            para_lines = para.split('\n')
            title = para_lines[0][:60] if para_lines[0] else f'Section {i+1}'
            body = '\n'.join(para_lines[1:]) if len(para_lines) > 1 else para

            slides.append({
                'type': 'content',
                'title': title,
                'body': body
            })
    else:
        # Stratégie 2: Découper par taille (max 100 mots par slide)
        words = content.split()
        chunk_size = 80  # mots par slide
        chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

        for i, chunk in enumerate(chunks):
            slides.append({
                'type': 'content',
                'title': f'Part {i+1}',
                'body': chunk
            })

    return slides


def _reorganize_slides(slides: List[Dict[str, Any]], structure: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Réorganise les slides selon une structure standard de carousel.
    Standard: Cover → Content slides → (Compare slides) → Conclusion (optionnel)
    """
    if not slides:
        return slides

    # Identifier les types de slides
    has_cover = any(s.get('type') == 'cover' for s in slides)

    # Si pas de cover, en créer une depuis la première slide
    if not has_cover and slides:
        first_slide = slides[0]
        cover_slide = {
            'type': 'cover',
            'badge': '',
            'title': first_slide.get('title', 'Presentation'),
            'code': '',
            'cta': 'Swipe to learn'
        }

        # Extraire du code si présent
        if first_slide.get('body'):
            code_match = re.search(r'```(?:\w+)?\n(.*?)```', first_slide['body'], re.DOTALL)
            if code_match:
                cover_slide['code'] = code_match.group(1).strip().split('\n')[0][:20]

        slides[0] = cover_slide

    # Réorganiser: comparer les slides détectées
    # S'assurer que les slides de comparaison sont bien formattées
    for slide in slides:
        if slide.get('type') == 'compare' and 'columns' not in slide:
            if slide.get('body'):
                slide['columns'] = _extract_compare_columns(
                    slide['body'],
                    slide['body'].split('\n')
                )
                if 'body' in slide:
                    del slide['body']

    # Améliorer la détection des comparaisons — uniquement sur le titre (jamais sur le body)
    for slide in slides:
        if slide.get('type') == 'content' and slide.get('title'):
            title = slide.get('title', '')
            if re.search(r'\b(?:vs\.?|versus|compar[ée])\b', title, re.IGNORECASE):
                body = slide.get('body', '')
                slide['type'] = 'compare'
                slide['columns'] = _extract_compare_columns(body, body.split('\n'))
                if 'body' in slide:
                    del slide['body']

    return slides


def _parse_section_to_slide(section: str) -> Dict[str, Any]:
    """Analyse une section de texte et détermine le type de slide approprié."""
    lines = section.strip().split('\n')

    # Extraire le premier heading comme titre
    title = ''
    body_lines = []

    heading_match = re.match(r'^(#{1,2})\s+(.+)$', lines[0])
    if heading_match:
        title = heading_match.group(2).strip()
        body_lines = lines[1:]
    else:
        # Pas de heading, utiliser la première ligne comme titre
        title = lines[0].strip()
        body_lines = lines[1:]

    # Nettoyer et formater le body
    body = '\n'.join(body_lines).strip()

    # Détecter le type de slide
    slide_type = _detect_slide_type(title, body, lines)

    slide = {
        'type': slide_type,
        'title': title,
    }

    # Ajouter badge par défaut
    if slide_type == 'cover':
        slide['badge'] = ''
        slide['code'] = ''
        slide['cta'] = 'Swipe to learn'
        # Si le body contient du code, l'utiliser
        code_match = re.search(r'```(?:\w+)?\n(.*?)```', body, re.DOTALL)
        if code_match:
            slide['code'] = code_match.group(1).strip().split('\n')[0][:20]
    else:
        slide['badge'] = ''
        # Convertir le Markdown en HTML pour le body
        slide['body'] = _markdown_to_html(body)

    # Détecter si c'est une slide de comparaison
    if slide_type == 'compare':
        slide['columns'] = _extract_compare_columns(body, lines)
        if 'body' in slide:
            del slide['body']

    return slide


def _detect_slide_type(title: str, body: str, lines: List[str]) -> str:
    """Détecte intelligemment le type de slide basé sur le contenu."""

    title_lower = title.lower()

    # Cover keywords
    cover_keywords = ['cover', 'welcome', 'presentation', 'guide']
    if any(kw in title_lower for kw in cover_keywords):
        return 'cover'

    # CTA / Conclusion slide — titre interrogatif ou mots d'action
    cta_keywords = ['et vous', 'à vous', 'conclusion', 'retenir', 'commentaire',
                    'partagez', 'rejoins', 'suivez', 'prêt', 'passer à']
    if any(kw in title_lower for kw in cta_keywords):
        return 'cta'
    if title.rstrip().endswith('?') and len(title) > 15:
        return 'cta'

    # Quote slide — corps dominé par une citation blockquote
    if body:
        body_stripped = body.strip()
        if body_stripped.startswith('> ') or re.match(r'^\s*<blockquote', body_stripped):
            return 'quote'

    # Compare — uniquement sur le titre (jamais sur le body pour éviter les faux positifs)
    compare_keywords = [' vs ', ' versus ', ' vs.', 'comparé', 'comparaison', 'compare',
                        'annonces vs', 'vs réalité']
    if any(kw in title_lower for kw in compare_keywords):
        return 'compare'

    # Compare via structure ### dans le body (deux sous-sections opposées)
    if body and re.search(r'^###\s+', body, re.MULTILINE):
        h3_sections = [m.group(0) for m in re.finditer(r'^###\s+.+', body, re.MULTILINE)]
        if len(h3_sections) == 2:
            return 'compare'

    # Par défaut: contenu
    return 'content'


def _extract_compare_columns(body: str, lines: List[str]) -> List[Dict[str, str]]:
    """Extrait deux colonnes de comparaison depuis le contenu."""

    def _build_col(section_text: str, fallback_title: str) -> Dict[str, str]:
        section_lines = section_text.strip().split('\n')
        col_title = section_lines[0].strip() if section_lines else fallback_title
        col_body = '\n'.join(section_lines[1:]).strip() if len(section_lines) > 1 else section_text.strip()
        return {'title': col_title, 'body': _markdown_to_html(col_body), 'tag': ''}

    # Stratégie 1: chercher deux sections avec headings ## ou ###
    for pattern in (r'(?:^|\n)##\s+', r'(?:^|\n)###\s+'):
        parts = re.split(pattern, body)
        non_empty = [p.strip() for p in parts if p.strip()]
        if len(non_empty) >= 2:
            return [_build_col(non_empty[0], 'Colonne 1'),
                    _build_col(non_empty[1], 'Colonne 2')]

    # Stratégie 2: deux blocs séparés par une ligne vide avec labels clairs
    # (ex: "### Ce qui est promis" already handled above)

    # Stratégie 3: chercher une liste en deux groupes séparés par une ligne vide
    groups = re.split(r'\n{2,}', body.strip())
    non_empty_groups = [g.strip() for g in groups if g.strip()]
    if len(non_empty_groups) >= 2:
        # Utiliser la première ligne de chaque groupe comme titre de colonne
        def _group_to_col(group: str, fallback: str) -> Dict[str, str]:
            glines = group.split('\n')
            first = glines[0].lstrip('#').strip()
            rest = '\n'.join(glines[1:]).strip()
            return {'title': first or fallback, 'body': _markdown_to_html(rest or group), 'tag': ''}

        return [_group_to_col(non_empty_groups[0], 'Colonne 1'),
                _group_to_col(non_empty_groups[1], 'Colonne 2')]

    # Stratégie 4: diviser en deux parties égales (fallback)
    mid = len(lines) // 2
    return [
        {'title': 'Colonne 1', 'body': _markdown_to_html('\n'.join(lines[:mid]).strip()), 'tag': ''},
        {'title': 'Colonne 2', 'body': _markdown_to_html('\n'.join(lines[mid:]).strip()), 'tag': ''},
    ]


def _markdown_to_html(md: str) -> str:
    """Convertit du Markdown basique en HTML pour les slides."""
    if not md:
        return ''

    # ── Étape 1 : extraire les tableaux Markdown dans des placeholders ──
    # On le fait AVANT le traitement ligne-par-ligne pour éviter que
    # _inline_formatting n'échappe les balises < > du HTML généré.
    html_blocks: dict = {}
    if _has_markdown_table(md):
        md, html_blocks = _extract_tables_as_placeholders(md)

    lines = md.split('\n')
    html_lines = []
    list_type = None  # None, 'ul', ou 'ol'
    in_code_block = False
    in_blockquote = False
    in_paragraph = False

    def close_list():
        nonlocal list_type
        if list_type == 'ul':
            html_lines.append('</ul>')
        elif list_type == 'ol':
            html_lines.append('</ol>')
        list_type = None

    def close_paragraph():
        nonlocal in_paragraph
        if in_paragraph:
            html_lines.append('</p>')
            in_paragraph = False

    def close_all():
        close_list()
        close_paragraph()
        if in_blockquote:
            html_lines.append('</blockquote>')

    for line in lines:
        stripped = line.strip()

        # Blocs HTML protégés (tableaux convertis) — passer en direct
        if stripped.startswith('\x00HTMLBLOCK'):
            close_all()
            html_lines.append(stripped)
            continue

        # Code blocks ```
        if stripped.startswith('```'):
            close_all()
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                # Allowlist: only alphanumerics + safe symbols for language names
                raw_lang = stripped[3:].strip()
                lang = re.sub(r'[^a-zA-Z0-9_\-+#]', '', raw_lang)
                html_lines.append(f'<pre style="background:rgba(0,0,0,.3);padding:16px;border-radius:8px;margin:12px 0;"><code class="language-{lang}">')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(stripped.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue

        # Blockquotes >
        bq_match = re.match(r'^>\s*(.+)$', stripped)
        if bq_match:
            close_all()
            if not in_blockquote:
                html_lines.append('<blockquote class="slide-quote">')
                in_blockquote = True
            html_lines.append(_inline_formatting(bq_match.group(1)))
            continue
        else:
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False

        # Séparateurs horizontaux *** ou ---
        if re.match(r'^\*{3,}$', stripped) or re.match(r'^-{3,}$', stripped):
            close_all()
            html_lines.append('<hr class="slide-hr">')
            continue

        # Headings H3
        h3_match = re.match(r'^###\s+(.+)$', stripped)
        if h3_match:
            close_all()
            html_lines.append(f'<h3 class="slide-h3">{_inline_formatting(h3_match.group(1))}</h3>')
            continue

        # Headings H4
        h4_match = re.match(r'^####\s+(.+)$', stripped)
        if h4_match:
            close_all()
            html_lines.append(f'<h4 class="slide-h4">{_inline_formatting(h4_match.group(1))}</h4>')
            continue

        # Lignes vides
        if not stripped:
            close_all()
            continue

        # Listes à puces - ou *
        list_match = re.match(r'^[-*]\s+(.+)$', stripped)
        if list_match:
            close_paragraph()
            if not list_type:
                html_lines.append('<ul class="bullets">')
                list_type = 'ul'
            html_lines.append(f'<li>{_inline_formatting(list_match.group(1))}</li>')
            continue

        # Listes numérotées 1. 2. etc
        num_list_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if num_list_match:
            close_paragraph()
            if not list_type:
                html_lines.append('<ol class="bullets numbered">')
                list_type = 'ol'
            html_lines.append(f'<li>{_inline_formatting(num_list_match.group(2))}</li>')
            continue

        # Pas dans une liste
        if list_type:
            close_list()

        # Paragraphes normaux
        if not in_paragraph:
            html_lines.append(f'<p>{_inline_formatting(stripped)}')
            in_paragraph = True
        else:
            # Continuer le paragraphe (même bloc de texte, plusieurs lignes)
            html_lines.append(' ' + _inline_formatting(stripped))

    # Fermer les blocs ouverts
    close_all()
    if in_code_block:
        html_lines.append('</code></pre>')

    # Nettoyer
    result = '\n'.join(html_lines).strip()

    # Nettoyer les paragraphes vides
    result = re.sub(r'<p>\s*</p>', '', result)

    # ── Étape 3 : restaurer les blocs HTML (tableaux) ──
    for placeholder, html in html_blocks.items():
        result = result.replace(placeholder, html)

    return result


def _extract_tables_as_placeholders(md: str) -> tuple:
    """
    Remplace chaque tableau Markdown par un placeholder unique et retourne
    (md_avec_placeholders, {placeholder: html_table}).
    Cela protège le HTML des tableaux du traitement inline ultérieur.
    """
    html_blocks: dict = {}
    lines = md.split('\n')
    result_lines = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Détecter l'en-tête d'un tableau
        if line.startswith('|') and line.endswith('|') and i + 1 < len(lines):
            if re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i + 1]):
                table_lines = [line]
                i += 2  # Sauter header + séparateur

                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('|') and next_line.endswith('|'):
                        table_lines.append(next_line)
                        i += 1
                    else:
                        break

                placeholder = f'\x00HTMLBLOCK{len(html_blocks)}\x00'
                html_blocks[placeholder] = _build_html_table(table_lines)
                result_lines.append(placeholder)
                continue

        result_lines.append(lines[i])
        i += 1

    return '\n'.join(result_lines), html_blocks


def _has_markdown_table(text: str) -> bool:
    """Détecte si le texte contient un tableau Markdown (pipe-separated)."""
    lines = text.strip().split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            # Vérifier si la ligne suivante est une ligne séparatrice |---|---|
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if re.match(r'^\|[\s\-:|]+\|$', next_line):
                    return True
    return False


def _convert_tables(md: str) -> str:
    """Convertit les tableaux Markdown en HTML stylisé pour les slides."""
    lines = md.split('\n')
    result_lines = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Détecter le début d'un tableau
        if line.startswith('|') and line.endswith('|'):
            # Vérifier si la ligne suivante est le séparateur
            if i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i + 1]):
                # Parser le tableau
                table_lines = [line]
                i += 2  # Sauter la ligne header + séparateur

                # Collecter toutes les lignes du tableau
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('|') and next_line.endswith('|'):
                        table_lines.append(next_line)
                        i += 1
                    else:
                        break

                # Convertir en HTML
                html_table = _build_html_table(table_lines)
                result_lines.append(html_table)
                continue
            else:
                # Ce n'est pas un tableau, juste une ligne avec des pipes
                result_lines.append(line)
                i += 1
        else:
            result_lines.append(lines[i])
            i += 1

    return '\n'.join(result_lines)


def _build_html_table(table_lines: List[str]) -> str:
    """Construit un HTML table à partir de lignes Markdown pipe-separated."""
    rows = []
    for line in table_lines:
        # Split par | et nettoyer
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(cells)

    if not rows:
        return ''

    header_cells = rows[0]
    data_rows = rows[1:]

    # Construire le HTML
    html_parts = ['<table class="slide-table">']

    # Header
    html_parts.append('<thead><tr>')
    for cell in header_cells:
        html_parts.append(f'<th>{_inline_formatting(cell)}</th>')
    html_parts.append('</tr></thead>')

    # Body
    if data_rows:
        html_parts.append('<tbody>')
        for row in data_rows:
            html_parts.append('<tr>')
            for cell in row:
                html_parts.append(f'<td>{_inline_formatting(cell)}</td>')
            html_parts.append('</tr>')
        html_parts.append('</tbody>')

    html_parts.append('</table>')
    return '\n'.join(html_parts)


def _safe_href(url: str) -> str:
    """Bloque les URLs javascript:, data: et vbscript: dans les attributs href."""
    url = url.strip()
    scheme = urlparse(url).scheme.lower()
    if scheme in ('javascript', 'data', 'vbscript'):
        return '#'
    return url


def _inline_formatting(text: str) -> str:
    """Applique le formatage inline: **gras**, *italique*, `code`."""
    # Extraire d'abord les segments code inline pour les protéger de l'échappement HTML
    code_segments = {}
    placeholder_base = '\x00CODE\x00'

    def protect_code(m):
        key = f'{placeholder_base}{len(code_segments)}\x00'
        code_segments[key] = m.group(1)
        return key

    text = re.sub(r'`([^`]+)`', protect_code, text)

    # Échapper les entités HTML dans le texte brut (pas dans le code)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Réinjecter les balises code avec leur contenu échappé
    for key, code_content in code_segments.items():
        safe_code = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = text.replace(key, f'<code>{safe_code}</code>')

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Links — sanitize href to block javascript: / data: URIs
    def _make_link(m: re.Match) -> str:
        # Échapper le label explicitement (la passe globale a déjà traité le texte environnant,
        # mais m.group(1) est le groupe brut capturé avant cette substitution)
        raw_label = m.group(1)
        label = raw_label.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        href  = _safe_href(m.group(2))
        return f'<a href="{href}" style="color:var(--accent2);text-decoration:underline;">{label}</a>'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _make_link, text)

    # Strikethrough
    text = re.sub(r'~~(.+?)~~', r'<del style="opacity:0.6;">\1</del>', text)

    return text


def _enrich_slides(slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrichit les slides avec des badges et métadonnées automatiques."""
    if not slides:
        return slides

    # Si la première slide n'est pas une cover OU si elle n'a pas de corps
    first_slide = slides[0]
    needs_cover = (first_slide['type'] != 'cover' or
                   not first_slide.get('body') or
                   first_slide.get('title', '').startswith('#'))

    if needs_cover:
        # Utiliser le titre de la première slide si possible
        cover_title = first_slide.get('title', 'Presentation')
        # Si la première slide est un H1, l'utiliser comme cover
        if first_slide['type'] == 'cover':
            # Déjà une cover, ne pas en ajouter une autre
            pass
        else:
            cover_slide = {
                'type': 'cover',
                'badge': '',
                'title': cover_title,
                'code': '',
                'cta': 'Swipe to learn'
            }

            # Extraire du code si présent
            if first_slide.get('body'):
                code_match = re.search(r'```(?:\w+)?\n(.*?)```', first_slide['body'], re.DOTALL)
                if code_match:
                    cover_slide['code'] = code_match.group(1).strip().split('\n')[0][:20]

            # Remplacer la première slide par la cover
            slides[0] = cover_slide

    # Ajouter des badges automatiques aux slides de contenu
    for _i, slide in enumerate(slides):
        if slide['type'] in ('content', 'compare') and not slide.get('badge'):
            slide['badge'] = ''

    return slides
