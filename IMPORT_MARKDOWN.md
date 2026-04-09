# Guide d'Import Markdown

## Comment utiliser l'import Markdown

Le Carousel Generator supporte maintenant l'import intelligent de fichiers Markdown (.md) pour générer automatiquement vos slides.

### Accès à la fonctionnalité

1. Ouvrez l'application web: `http://localhost:5000`
2. Dans la sidebar, cliquez sur **"📄 Importer un fichier MD"**
3. Un modal s'ouvre avec deux options:
   - **Coller le contenu**: Copiez-collez votre Markdown directement
   - **Uploader un fichier**: Glissez-déposez ou sélectionnez un fichier .md

## Formats Supportés

### Format 1: Headings comme structure

Le parser utilise les headings (# ## ###) pour détecter les slides:

```markdown
---
series: "Ma Série"
author: "@mon_compte"
---

# Titre de la Présentation

## Introduction au Sujet

Voici le contenu de la première slide avec du texte **important**.

### Points Clés

- Premier point important
- Deuxième point crucial
- Troisième élément essentiel

## Comparaison: Option A vs Option B

**Option A**: Description détaillée...

**Option B**: Autre description...
```

### Format 2: Séparateurs explicites

Utilisez `---` ou `***` pour séparer les slides:

```markdown
---
series: "Ma Série"
author: "@mon_compte"
---

# Slide 1: Introduction

Contenu de la première slide.

---

## Slide 2: Concepts

- Point 1
- Point 2
- Point 3

---

## Slide 3: Comparaison

Colonne 1 vs Colonne 2
```

## Fonctionnalités Intelligentes

### ✅ Détection automatique du type de slide

- **Cover Slide**: Détectée si c'est la première slide ou si le titre contient des mots comme "intro", "welcome", "cover"
- **Content Slide**: Texte normal avec paragraphes et listes
- **Compare Slide**: Détecté si le titre contient "vs", "versus", "comparaison" ou si le corps présente deux sections parallèles

### ✅ Extraction du Front Matter

Les métadonnées YAML en début de fichier sont automatiquement extraites:

```yaml
---
series: "AI Series"        # → Footer série
author: "@username"        # → Footer auteur
title: "ML Basics"         # → Optionnel
---
```

### ✅ Conversion Markdown → HTML

Le parser convertit automatiquement:
- `**texte**` → **Gras** (avec classe CSS)
- `*texte*` → *Italique*
- `` `code` `` → Code inline (style monospace)
- `- item` → Listes à puces (avec classe `bullets`)
- ` ```code``` ` → Blocs de code (avec formatage)
- `[lien](url)` → Liens hypertextes

## Exemples de Fichiers

Deux exemples sont fournis dans le dossier racine:
- `test_import.md`: Format avec headings
- `test_separators.md`: Format avec séparateurs ---

## Workflow Recommandé

1. **Écrivez votre contenu** dans un fichier Markdown (VS Code, Obsidian, etc.)
2. **Structurez avec des headings** ou des séparateurs ---
3. **Importez dans l'app** via le modal
4. **Vérifiez l'aperçu** des slides détectées
5. **Appliquez** pour remplir l'éditeur
6. **Personnalisez** si besoin dans l'éditeur visuel
7. **Générez** le carousel final!

## Conseils

### Pour les Covers
Utilisez `#` pour le titre principal, il deviendra automatiquement une slide de couverture:

```markdown
# Titre Accrocheur
```

### Pour le Contenu
Utilisez `##` pour chaque nouvelle slide de contenu:

```markdown
## Concept Important

Explication détaillée avec:
- Des listes à puces
- Du **gras** pour emphasis
- Et du texte normal
```

### Pour les Comparaisons
Séparez les deux options avec "vs" ou "---":

```markdown
## Méthode A vs Méthode B

**Avantages:**
- Rapide
- Simple

**Inconvénients:**
- Moins précis

---

**Avantages:**
- Très précis

**Inconvénients:**
- Plus complexe
```

## Dépannage

### Le parser ne détecte pas assez de slides
- Vérifiez que vos headings utilisent bien `#`, `##`, ou `###`
- Assurez-vous qu'il y a du contenu après chaque heading
- Utilisez des séparateurs `---` si la structure est ambiguë

### Le footer n'est pas rempli
- Vérifiez que le front matter YAML est bien formaté avec `---` au début
- Les clés supportées sont: `series`, `author`, `username`, `title`

### Erreur de parsing
- Vérifiez que le fichier est bien encodé en UTF-8
- Assurez-vous que le YAML front matter est valide
- Le fichier doit avoir l'extension `.md` ou `.markdown`

## Support

Pour toute question ou bug, consultez le fichier `README.md` principal du projet.
