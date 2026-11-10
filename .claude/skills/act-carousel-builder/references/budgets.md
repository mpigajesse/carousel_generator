# Budgets caractères — comment compter et respecter

## Pourquoi c'est critique

`generate.py::_calculate_text_size` mappe le nombre de caractères du `body` rendu vers une taille de police et un flag `is_compact`. Si le budget est dépassé, le texte déborde du cadre 1080×1080 (ou 1080×1350) au screenshot Playwright, et la slide est inutilisable.

## Règle de comptage

Le calculateur compte le **body après extraction du texte visible** :
- Les balises `<span>`, `<ul>`, `<li>`, `<br>`, `<code>` **ne sont pas comptées**
- Le contenu textuel **entre** les balises **est compté**
- Pour les slides `compare`, le compte total = somme des deux colonnes ×1.5 (correctif d'espace partagé)

## Budgets cibles (texte visible uniquement)

| Type | Budget confortable | Limite stricte | Au-delà |
|---|---|---|---|
| `cover` titre | ≤ 50 chars | 60 chars | reformuler plus court |
| `cover` body | absent ou ≤ 100 chars | 120 chars | déplacer en slide 2 |
| `content` body | ≤ 280 chars | 380 chars (compact) | scinder en 2 slides |
| `compare` par colonne | ≤ 110 chars | 140 chars | scinder en 2 compares |
| `quote` body | ≤ 150 chars | 200 chars | citer un extrait |
| `stat` value | ≤ 6 chars | 8 chars | suffixe (K, M, %, ×) |
| `stat` label | ≤ 30 chars | 40 chars | reformuler |
| `cta` body | ≤ 130 chars | 160 chars | retirer un détail |

## Comptage rapide en tête

Une phrase française moyenne fait **~80 chars**. Repères mentaux :
- 1 phrase courte ≈ 60 chars
- 1 phrase moyenne ≈ 100 chars
- 1 phrase longue ≈ 140 chars
- 1 paragraphe condensé de 2 phrases ≈ 200 chars
- 1 paragraphe complet de 3 phrases ≈ 280 chars (= budget content idéal)

## Procédure de validation avant écriture

Pour chaque slide :
1. Écrire le body en texte brut
2. Compter (mentalement par phrase ou avec un comptage explicite)
3. Si > limite stricte : **scinder** ou **condenser**
4. **Ne jamais** réduire la taille de police côté template — c'est la responsabilité du parser

## Patterns de condensation

| Avant | Après |
|---|---|
| "Il est important de noter que la stratégie marocaine repose sur plusieurs piliers" | "La stratégie marocaine repose sur plusieurs piliers" |
| "Selon les estimations du Stanford AI Index 2025" | "(Stanford AI Index 2025)" |
| "permet d'accomplir efficacement la tâche de" | "permet de" |
| Listes en prose ("D'abord X, ensuite Y, enfin Z") | `<ul class="bullets">` |
| Données numériques noyées dans le texte | Slide `stat` dédiée (Instagram) |

## Exemple de scission

**Source article (450 chars)** :
> Le data center Igoudar à Dakhla illustre une stratégie où infrastructure numérique et souveraineté énergétique avancent de concert. Dakhla, avec son potentiel éolien et solaire exceptionnel, offre un coût énergétique imbattable pour alimenter des serveurs 24/7. Ce choix géographique est aussi un signal diplomatique et économique : en développant le Sahara marocain comme pôle d'innovation, le Royaume démontre que la périphérie peut devenir le centre.

**Slide 1 (220 chars)** :
```markdown
## Dakhla : le pari énergie propre

Igoudar associe data center et institut Jazari (IA + transition énergétique).<br><br>
<span class="hl1">Coût énergétique imbattable</span> grâce au potentiel éolien et solaire exceptionnel.
```

**Slide 2 (180 chars)** :
```markdown
## Un signal stratégique

En faisant du Sahara un pôle d'innovation, le Royaume démontre que <span class="hl2">la périphérie peut devenir le centre</span> quand l'investissement suit.
```
