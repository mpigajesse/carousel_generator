# 🔍 Audit Complet - Carousel Generator

> **Date :** 13 avril 2026  
> **Objectif :** Détecter et corriger TOUS les problèmes de chevauchement, overflow et rendering

---

## 📊 Résumé Exécutif

| Catégorie | Problèmes Critiques | Problèmes Moyens | Problèmes Mineurs |
|-----------|-------------------|-------------------|-------------------|
| CSS / Template | **3** | 4 | 2 |
| JavaScript (adjustFontSize) | **2** | 2 | 1 |
| Python (generate.py) | **1** | 2 | 1 |
| MD Parser | 0 | 2 | 1 |

**Total : 6 critiques, 10 moyens, 5 mineurs**

---

## 🔴 PROBLÈMES CRITIQUES (À corriger IMMÉDIATEMENT)

### 1. ⚠️ Cover Slide : Logo 450px + Terminal Box = Overflow garanti

**Fichier :** `slide.html.j2`  
**Ligne :** `.cover-logo img { height: 450px; }`

**Problème :**
```
Padding top slide :     64px
Logo :                 450px
Margin-bottom logo :    20px
Terminal box (padding) : 72px (36px top + 36px bottom)
Terminal title 72px :   85px (avec line-height)
Terminal code :         46px
Swipe container :       86px
Margin swipe :          12px
Footer (absent cover) :  0px
─────────────────────────────────
TOTAL MINIMUM :        835px

SI le titre dépasse 20 caractères → font-size réduit à 52px
SI le titre dépasse 35 caractères → font-size réduit à 52px
Mais le terminal-box N'A PAS de hauteur maximale !
```

**Scénario d'overflow :**
- Titre long (>35 chars) à 52px = ~2 lignes
- Terminal box prend ~200px+
- Logo 450px + terminal 200px + swipe 86px = 736px
- Avec padding 64px top + 160px bottom = 960px ✅ (ça passe)
- **MAIS** si le titre fait 3 lignes ou plus = OVERFLOW

**Impact :** 📸 Le screenshot Playwright coupe le contenu qui dépasse

---

### 2. ⚠️ `.slide` padding-bottom 160px vs Footer à bottom:64px = CONFLIT

**Fichier :** `slide.html.j2`

**Problème :**
```css
.slide {
  padding: 64px 72px 160px 72px; /* 160px en bas */
}

.footer {
  position: absolute;
  bottom: 64px; /* Conflit ! */
}
```

**Le padding-bottom de 160px est censé réserver l'espace du footer, mais :**
- Le footer est en `position: absolute; bottom: 64px`
- Le contenu flex dans `.content` peut descendre JUSQU'À 1080 - 160 = 920px
- Le footer commence à 1080 - 64 = 1016px
- **Zone morte entre 920px et 1016px = 96px non utilisés**

** MAIS si le contenu dépasse 920px, il va SOUS le footer → CHEVAUCHEMENT**

---

### 3. ⚠️ `adjustFontSize()` : Détection d'overflow inefficace pour les slides Compare

**Fichier :** `slide.html.j2` (script JS)  
**Ligne :** `isOverflowing()` function

**Problème :**
```javascript
function isOverflowing() {
  // Vérifie footer.getBoundingClientRect().bottom > 1081
  // Vérifie lastElementChild.getBoundingClientRect().bottom > limit

  // ❌ PROBLÈME : Pour les slides compare, le lastElementChild est .compare-grid
  // .compare-grid a flex:1, donc son rect.bottom = toujours celui du parent
  // La détection NE VOIT PAS si le contenu INTERNE des colonnes dépasse
}
```

**Les colonnes de comparaison (`.compare-col`) ont :**
- `overflow: hidden` → le contenu est coupé mais PAS détecté comme overflow
- `padding: 36px` → réduit l'espace interne
- Si le body d'une colonne fait > ~400 caractères, il DÉBORDE de la colonne

**Impact :** 📸 Les slides compare ont du contenu coupé sans que le JS ne le détecte

---

### 4. ⚠️ `_calculate_text_size()` : Logique de scaling trop permissive

**Fichier :** `generate.py`  
**Lignes :** 45-65

**Problème :**
```python
if char_count < 150:
    text_size = 46  # OK
elif char_count < 300:
    text_size = 40  # OK
elif char_count < 500:
    text_size = 34  # OK
elif char_count < 750:
    text_size = 28  # ⚠️ Risqué
elif char_count < 1000:
    text_size = 24  # 🔴 TROP DE CONTENU
else:
    text_size = 21  # 🔴 IMPOSSIBLE À RENTRER
```

**Exemple concret :**
- 1000 caractères à 24px avec line-height 1.6 = ~40-50 lignes de texte
- 50 lignes × 38.4px (24 × 1.6) = 1920px de hauteur
- **Espace disponible : 1080 - 64 - 160 - titre - règle = ~750px max**

**Le JS `adjustFontSize()` va devoir réduire de 24px à ~14px = 42 itérations**
- Mais le minimum du JS est 14px pour le body
- **À 14px, 1000 caractères = toujours trop = OVERFLOW**

---

### 5. ⚠️ Playwright : `wait_for_timeout(800)` insuffisant pour les Google Fonts

**Fichier :** `generate.py`  
**Ligne :** `page.wait_for_timeout(800)`

**Problème :**
- 800ms = temps fixe, ne garantit PAS que les fonts sont chargées
- Si la connexion est lente, les fonts ne sont pas prêtes
- Résultat : les tailles de texte sont CALCULÉES avec les fonts fallback
- Puis les fonts chargent → le texte change de taille → OVERFLOW

**Solution recommandée :**
```python
page.wait_for_timeout(1200)  # Minimum 1200ms
# OU MIEUX :
page.wait_for_load_state('networkidle')  # Attend que tout soit chargé
```

---

### 6. ⚠️ `.bullets li::before` : Position top:28px fixe = chevreauchement si texte long

**Fichier :** `slide.html.j2`

**Problème :**
```css
.bullets li {
  padding: 18px 0 18px 52px;
  position: relative;
}
.bullets li:before {
  position: absolute;
  left: 6px; top: 28px; /* FIXE ! */
}
```

**Si un `<li>` fait 3 lignes de texte :**
- Hauteur du li ≈ 3 × (text_size × 1.55) ≈ 3 × 49.6px = 149px
- Le bullet point reste à top:28px → **visuellement en HAUT du li, pas centré**
- La ligne de connexion `::before` sur `.bullets` (top:35px à bottom:35px) ne suit PAS

---

## 🟡 PROBLÈMES MOYENS

### 7. `.module-title` : Pas de gestion des titres très longs (>80 chars)

```css
.module-title {
  font-size: 58px;  /* Même avec word-break, un titre de 80 chars = 2-3 lignes */
  line-height: 1.15;
}
```

**Si titre = 80 caractères à 58px :**
- ~2.5 lignes × 66.7px = 167px de hauteur
- Le inline style `{% if slide.title|length > 30 %}style="font-size:42px;"{% endif %}` n'est appliqué QUE sur les slides compare

**Correction :** Ajouter la détection de longueur sur TOUTES les slides

---

### 8. `.compare-grid` : Gap 32px + colonnes trop étroites pour le contenu

```css
.compare-grid {
  grid-template-columns: 1fr 1fr;
  gap: 32px;  /* 32px de gap = espace perdu */
}
```

**Chaque colonne fait : (1080 - 144px padding - 32px gap) / 2 = 452px**
- Moins padding 36px de la carte = 380px de contenu utilisable
- À 28px de font-size, ~12-15 caractères par ligne
- **Un body de 400 caractères = 27-33 lignes → OVERFLOW de la colonne**

---

### 9. `text-shadow` sur `.module-title` : Impact sur le rendu Playwright

```css
.module-title {
  text-shadow: 2px 2px 0px rgba(0,0,0,0.5);
}
```

**Problème :** Le text-shadow peut causer un **rendering flou** sur certains screenshots Playwright, surtout avec les fonts Google qui n'ont pas fini de charger.

---

### 10. `.terminal-box` : `box-shadow: 20px 20px 0` = peut déborder à droite

```css
.terminal-box {
  padding: 36px 50px;
  box-shadow: 20px 20px 0 rgba(0,0,0,0.2); /* Déborde de 20px à droite et en bas */
}
```

**Largeur utilisable : 1080 - 144px = 936px**
- Terminal box = 100% = 936px
- Box shadow = +20px = 956px → **dépasse de 20px**
- Avec `overflow: hidden` sur `.slide`, l'ombre est coupée (acceptable visuellement, mais pas propre)

---

### 11. `.innovation-glow` opacity trop élevée = texte moins lisible

```css
.innovation-glow {
  opacity: 0.4;  /* Avant: 0.8 → réduit à 0.4 mais encore trop */
}
```

**Les blobs colorés en arrière-plan peuvent réduire le contraste du texte**
- Recommandation : 0.25 maximum

---

### 12. MD Parser : `_detect_slide_type()` détecte trop facilement "compare"

```python
if re.search(r'\b(?:vs\.?|versus|compar[ée])\b', title + ' ' + body, re.IGNORECASE):
    slide['type'] = 'compare'
```

**Problème :** Si le body mentionne "vs" dans un contexte non-comparatif, la slide est convertie en compare → colonnes vides ou mal remplies.

---

### 13. `.body p:last-child { margin-bottom: 0; }` : Ne fonctionne pas avec le HTML safe

```css
.body p:last-child { margin-bottom: 0; }
```

**Si le body contient des `<ul>`, `<h3>`, `<table>` après les `<p>`, le dernier enfant N'EST PAS un `<p>` → margin-bottom reste appliquée**

---

### 14. `_enrich_slides()` : Ajoute une slide "Conclusion" automatique non demandée

```python
if len(slides) > 4:
    slides.append({
        'type': 'content',
        'title': 'Conclusion',
        'body': '<p>Résumé des points clés.</p>'
    })
```

**Problème :** L'utilisateur ne veut pas toujours une conclusion → slide non désirée dans le carousel final.

---

## 🟢 PROBLÈMES MINEURS

### 15. Encodage fichier HTML : `utf-8-sig` → BOM inutile

**Fichier :** `generate.py` ligne `with open(html_path, "w", encoding="utf-8-sig")`

Le BOM (Byte Order Mark) est inutile pour du HTML. Utiliser `utf-8`.

---

### 16. Logo hardcodé en absolute path

```html
<img src="file:///d:/Generator/carousel_generator/static/logo/logo.png">
```

**Problème :** Si le projet est ailleurs, le logo ne charge pas. Utiliser un chemin relatif ou variable Jinja2.

---

### 17. `.act-watermark` : 400px sur 1080px = trop grand et visible

```css
.act-watermark {
  font-size: 400px;
  opacity: 0.02;  /* Très faible, mais sur fond sombre peut être visible */
}
```

---

### 18. Pas de `@font-face` fallback si Google Fonts inaccessible

Si pas de connexion internet, les fonts ne chargent pas et le rendu est moche.

---

### 19. `_build_slide_filename` : Troncature à 50 chars coupe les mots

```python
if len(clean) > 50:
    clean = clean[:clean.rfind('_')]  # Coupe au dernier underscore
```

**Si le titre n'a pas d'underscore = coupe au milieu d'un mot**

---

### 20. `.rule::after` : Position top:10px = peut overlap le contenu suivant

```css
.rule {
  height: 6px;
  margin-bottom: 32px;
}
.rule::after {
  top: 10px;  /* Dépasse de la règle de 4px vers le bas */
}
```

---

## 📋 RECOMMANDATIONS PRIORITAIRES

### 🔥 PRIORITÉ 1 : Corriger les overflows (critique)

| # | Action | Fichier | Impact |
|---|--------|---------|--------|
| 1 | Réduire le logo cover de 450px → 320px | `slide.html.j2` | Empêche overflow cover |
| 2 | Réduire padding-bottom slide de 160px → 120px | `slide.html.j2` | Meilleur usage de l'espace |
| 3 | Baisser le footer de bottom:64px → bottom:48px | `slide.html.j2` | Espace contenu augmenté |
| 4 | Réduire char_count max de 1000 → 600 pour text_size | `generate.py` | Moins de contenu par slide |
| 5 | Augmenter wait_for_timeout de 800 → 1500ms | `generate.py` | Fonts chargées correctement |
| 6 | Améliorer détection overflow pour compare | JS template | Détecte vraiment l'overflow |

### 🟡 PRIORITÉ 2 : Améliorations visuelles

| # | Action | Fichier |
|---|--------|---------|
| 7 | Réduire glow opacity de 0.4 → 0.25 | `slide.html.j2` |
| 8 | Ajouter détection titre long sur TOUTES les slides | `slide.html.j2` |
| 9 | Réduire gap compare-grid de 32px → 24px | `slide.html.j2` |
| 10 | Corriger bullet position dynamique | `slide.html.j2` |

### 🟢 PRIORITÉ 3 : Nettoyage

| # | Action | Fichier |
|---|--------|---------|
| 11 | Supprimer slide conclusion auto | `md_parser.py` |
| 12 | Corriger encodage utf-8-sig → utf-8 | `generate.py` |
| 13 | Rendre le logo path configurable | `slide.html.j2` |
| 14 | Ajouter font-display: swap aux @import | `slide.html.j2` |

---

## 🧪 PROTOCOLE DE TEST RECOMMANDÉ

Après chaque correction, tester avec ces scénarios :

### Test 1 : Cover avec titre très long
```yaml
- type: cover
  title: "Introduction aux Réseaux de Neurones Profonds et leur Application"
  code: "model.fit()_"
  cta: "Swipe"
```
✅ Le titre ne doit PAS dépasser du terminal-box

### Test 2 : Content slide avec 800+ caractères
```yaml
- type: content
  title: "Explication détaillée"
  body: "800 caractères de texte continu sans paragraphes..."
```
✅ Le texte doit tenir SANS chevaucher le footer

### Test 3 : Compare slide avec corps déséquilibré
```yaml
- type: compare
  title: "A vs B"
  columns:
    - title: "Court"
      body: "Une phrase."
      tag: "Tag"
    - title: "Long"
      body: "200 caractères de texte dans cette colonne..."
      tag: "Tag"
```
✅ Les deux colonnes doivent avoir leur contenu VISIBLE

### Test 4 : Slide avec liste de 10 items
```yaml
- type: content
  title: "10 Points"
  body: |
    <ul class="bullets">
      <li>Item 1 avec texte long</li>
      <li>Item 2 avec texte long</li>
      ...
    </ul>
```
✅ Tous les items doivent être VISIBLES

### Test 5 : Slide avec tableau Markdown
```markdown
| Col 1 | Col 2 | Col 3 |
|-------|-------|-------|
| Data  | Data  | Data  |
| Data  | Data  | Data  |
```
✅ Le tableau doit tenir dans la slide

---

## 📐 CALCULS D'ESPACE DISPONIBLE

### Slide Content (non-cover)
```
Hauteur totale :              1080px
Padding top :                   -64px
Badge :                         -46px (18px font + 8px padding × 2 + margin 20px)
Titre 58px (1-2 lignes) :       -82px (58 × 1.15 + margin-bottom 24px)
Règle :                         -38px (6px + margin 32px)
─────────────────────────────────────
ESPACE RESTANT POUR BODY :     ~850px
Footer (bottom:64px) :         -96px (footer height + padding-top 28px)
─────────────────────────────────────
ESPACE UTILISABLE BODY :       ~754px

À 32px font-size, line-height 1.6 = 51.2px/ligne
754 / 51.2 = ~14 lignes MAXIMUM
14 lignes × ~60 chars/ligne = ~840 caractères MAX

→ Le seuil de 750 chars pour is_compact est CORRECT
→ Le seuil de 1000 chars à 24px est TROP ÉLEVÉ
```

### Cover Slide
```
Hauteur totale :              1080px
Padding top :                   -64px
Badge (optionnel) :             -46px
Logo 320px (réduit) :          -320px
Margin logo :                   -20px
Terminal box padding :          -72px (36 × 2)
Terminal title 72px :           -85px
Terminal code :                 -46px
Swipe container :               -86px
Margin swipe :                  -12px
─────────────────────────────────────
TOTAL :                        751px
Marge de sécurité :            329px ✅

SI titre long (2 lignes) :     +85px = 836px → OK (marge 244px)
SI titre très long (3 lignes) : +170px = 921px → TIGHT (marge 159px)
SI titre > 4 lignes :          OVERFLOW ❌
```

### Compare Slide
```
Hauteur totale :              1080px
Padding top :                   -64px
Badge :                         -46px
Titre 58px :                    -82px
Règle :                         -38px
─────────────────────────────────────
ESPACE AVANT GRID :            ~850px
Footer :                        -96px
─────────────────────────────────────
ESPACE POUR GRID :             ~754px

Chaque colonne :
  Padding :                     -72px (36 × 2)
  Compare head 34px :           -54px (34 × 1.15 + margin 20px)
  Tag + margin :                -50px (tag 18px + padding + margin 24px)
─────────────────────────────────────
ESPACE POUR BODY :             ~578px

À 28px font, line-height 1.5 = 42px/ligne
578 / 42 = ~13 lignes par colonne
13 lignes × ~25 chars/ligne (colonne étroite) = ~325 chars MAX par colonne
```

---

## ✅ CHECKLIST FINALE AVANT MISE EN PRODUCTION

- [ ] Logo cover réduit à 320px
- [ ] Padding-bottom slide à 120px
- [ ] Footer bottom à 48px
- [ ] Wait timeout Playwright à 1500ms
- [ ] Char count max réduit à 600
- [ ] Overflow detection améliorée pour compare
- [ ] Glow opacity à 0.25
- [ ] Détection titre long sur toutes les slides
- [ ] Compare grid gap à 24px
- [ ] Conclusion auto supprimée
- [ ] Encodage utf-8 (pas sig)
- [ ] Logo path configurable
- [ ] Testé avec 5+ scénarios de contenu lourd
- [ ] Vérifié visuellement sur 3 thèmes différents
- [ ] PDF fusionné correct (pas de slide coupée)

---

*Audit terminé — 20 problèmes identifiés, 6 critiques*
