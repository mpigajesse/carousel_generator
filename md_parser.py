"""
md_parser.py - Parseur ultra-intelligent de Markdown pour Carousel Generator
Reorganise automatiquement du Markdown non-structuré en slides standardisées.
"""

import re
import yaml
from typing import List, Dict, Any, Tuple, Optional


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
        except:
            pass
    
    # 2. Nettoyage préliminaire
    content = _clean_content(content)
    
    # 3. Analyser la structure du contenu
    structure = _analyze_structure(content)
    
    # 4. Parser selon la structure détectée
    # Ne pas utiliser separators si c'est juste le front matter qui a été enlevé
    has_real_separators = structure['has_explicit_separators'] and not front_matter_match
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
    footer = {
        'series': front_matter.get('series', front_matter.get('title', 'Series')),
        'author': front_matter.get('author', front_matter.get('username', 'author'))
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
    total_lines = len([l for l in lines if l.strip()])
    
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
    first_heading_found = False
    
    for line in lines:
        heading_match = re.match(r'^(#{1,2})\s+(.+)$', line)
        if heading_match:
            # Sauvegarder la slide précédente
            if current_slide_lines:
                slide_text = '\n'.join(current_slide_lines).strip()
                if slide_text:
                    slides.append(_parse_section_to_slide(slide_text))
                current_slide_lines = []
            first_heading_found = True
        
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
            'badge': 'Knowledge Drop',
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
    
    # Améliorer la détection des comparisons
    for slide in slides:
        if slide.get('type') == 'content' and slide.get('title') and slide.get('body'):
            # Vérifier si le titre ou le body contient des indices de comparaison
            title = slide.get('title', '')
            body = slide.get('body', '')
            if re.search(r'\b(?:vs\.?|versus|compar[ée])\b', title + ' ' + body, re.IGNORECASE):
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
        slide['badge'] = 'Knowledge Drop'
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
    
    # Cover keywords - mais seulement si c'est le premier heading H1
    cover_keywords = ['cover', 'welcome', 'presentation', 'guide']
    if any(kw in title.lower() for kw in cover_keywords):
        return 'cover'
    
    # Compare keywords
    compare_keywords = ['vs', 'versus', 'vs.', 'comparé', 'comparaison', 'compare', 'difference', 'diff']
    if any(kw in title.lower() for kw in compare_keywords):
        return 'compare'
    if body and re.search(r'\b(?:vs\.?|versus|compar[ée])\b', body, re.IGNORECASE):
        return 'compare'
    
    # Détecter les structures de comparaison dans le corps (seulement s'il y a un H2 réel, pas H3)
    if body and re.search(r'\n##\s+', body):
        return 'compare'
    
    # Par défaut: contenu
    return 'content'


def _extract_compare_columns(body: str, lines: List[str]) -> List[Dict[str, str]]:
    """Extrait deux colonnes de comparaison depuis le contenu."""
    # Stratégie 1: chercher deux sections avec headings ##
    sections = re.split(r'\n##\s+', body)
    if len(sections) >= 2:
        columns = []
        for i, section in enumerate(sections[:2]):
            section_lines = section.strip().split('\n')
            col_title = section_lines[0].strip() if section_lines else f'Colonne {i+1}'
            col_body = '\n'.join(section_lines[1:]).strip() if len(section_lines) > 1 else section.strip()
            columns.append({
                'title': col_title,
                'body': _markdown_to_html(col_body),
                'tag': ''
            })
        return columns
    
    # Stratégie 2: diviser sur "vs" ou "versus"
    vs_match = re.split(r'\b(?:vs\.?|versus)\b', body, maxsplit=1, flags=re.IGNORECASE)
    if len(vs_match) == 2:
        return [
            {
                'title': 'Option A',
                'body': _markdown_to_html(vs_match[0].strip()),
                'tag': ''
            },
            {
                'title': 'Option B',
                'body': _markdown_to_html(vs_match[1].strip()),
                'tag': ''
            }
        ]
    
    # Stratégie 3: diviser en deux parties égales
    mid = len(lines) // 2
    return [
        {
            'title': 'Colonne 1',
            'body': _markdown_to_html('\n'.join(lines[:mid]).strip()),
            'tag': ''
        },
        {
            'title': 'Colonne 2',
            'body': _markdown_to_html('\n'.join(lines[mid:]).strip()),
            'tag': ''
        }
    ]


def _markdown_to_html(md: str) -> str:
    """Convertit du Markdown basique en HTML pour les slides."""
    if not md:
        return ''
    
    lines = md.split('\n')
    html_lines = []
    in_list = False
    in_code_block = False
    
    for line in lines:
        # Code blocks ```
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                lang = line.strip()[3:].strip()
                html_lines.append(f'<pre style="background:rgba(0,0,0,.3);padding:12px;border-radius:8px;margin:8px 0;"><code class="language-{lang}">')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue
        
        # Headings H3
        h3_match = re.match(r'^###\s+(.+)$', line.strip())
        if h3_match:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3 class="slide-h3">{_inline_formatting(h3_match.group(1))}</h3>')
            continue
            
        # Lignes vides
        if not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<br>')
            continue
        
        # Listes - ou *
        list_match = re.match(r'^[-*]\s+(.+)$', line.strip())
        if list_match:
            if not in_list:
                html_lines.append('<ul class="bullets">')
                in_list = True
            html_lines.append(f'<li>{_inline_formatting(list_match.group(1))}</li>')
            continue
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
        
        # Paragraphes normaux
        html_lines.append(_inline_formatting(line.strip()))
    
    if in_list:
        html_lines.append('</ul>')
    if in_code_block:
        html_lines.append('</code></pre>')
    
    return '\n'.join(html_lines)


def _inline_formatting(text: str) -> str:
    """Applique le formatage inline: **gras**, *italique*, `code`."""
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code style="background:rgba(255,255,255,.1);padding:2px 6px;border-radius:4px;font-family:monospace;">\1</code>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong class="bold">\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:var(--accent2);">\1</a>', text)
    
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
                'badge': 'Knowledge Drop',
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
    content_count = 0
    for i, slide in enumerate(slides):
        if slide['type'] == 'content' and not slide.get('badge'):
            content_count += 1
            slide['badge'] = f'Module {content_count:02d}'
        elif slide['type'] == 'compare' and not slide.get('badge'):
            content_count += 1
            slide['badge'] = f'Module {content_count:02d}'
    
    # Ajouter une slide de conclusion si le contenu est long
    if len(slides) > 4:
        last_slide = slides[-1]
        if last_slide['type'] != 'cover':
            # Vérifier si on a déjà une conclusion
            has_conclusion = any(
                'conclusion' in s.get('title', '').lower() or 
                'summary' in s.get('title', '').lower() or
                'résumé' in s.get('title', '').lower()
                for s in slides
            )
            if not has_conclusion:
                slides.append({
                    'type': 'content',
                    'badge': f'Module {content_count + 1:02d}',
                    'title': 'Conclusion',
                    'body': '<p>Résumé des points clés.</p>'
                })
    
    return slides
