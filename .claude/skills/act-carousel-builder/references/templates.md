# Templates de slides — par type

Tous les templates sont en Markdown avec séparateurs `---` entre slides et HTML inline pour la mise en forme du body.

---

## Cover (LinkedIn et Instagram)

```markdown
# <Titre court accrocheur ≤ 60 chars>

Badge: <Catégorie ACT>
CTA: Swipe pour comprendre →
```

Pour les besoins du parser, préférer la forme :

```markdown
# Cybersécurité 2026 : l'instabilité permanente

<!-- type:cover -->
<!-- badge:Cybersecurity -->
<!-- cta:Swipe pour comprendre -->
```

Le parser détecte la première slide comme `cover` automatiquement si elle a un `#` suivi de très peu de contenu. Pour forcer un type explicite, utiliser le format YAML produit en aval.

---

## Content — explicatif simple

```markdown
## C'est quoi vraiment ?

Le sujet en une phrase claire qui pose le décor.<br><br>
<span class="hl1">Le point central :</span> ce que le lecteur doit retenir, formulé en une phrase courte.<br><br>
Conséquence directe pour le lecteur ou pour le marché.
```

Budget : ≤ 280 chars (texte visible, hors balises).

---

## Content — liste à puces

```markdown
## Les 3 facteurs structurels

<ul class="bullets">
  <li><span class="bold">Position géographique</span> : carrefour Europe-Afrique.</li>
  <li><span class="bold">Énergie renouvelable</span> : objectifs solaire et éolien.</li>
  <li><span class="bold">Maturité réglementaire</span> : loi 09-08, CNDP, Digital Morocco 2030.</li>
</ul>
```

Règles :
- 3 à 5 items max
- Chaque item ≤ 80 chars (visible)
- Verbes ou substantifs en `<span class="bold">` au début de chaque ligne pour scanner

---

## Compare — deux colonnes (LinkedIn et Instagram)

```markdown
## Cloud souverain vs Cloud public

<!-- columns:2 -->

### Cloud souverain
Données sensibles : santé, finance, gouvernement.<br>
Hébergement local, conformité CNDP.<br>
Tag: Souveraineté

### Cloud public
Applications standards : bureautique, CRM.<br>
Azure, AWS, GCP — coûts optimisés.<br>
Tag: Élasticité
```

Budget : par colonne ≤ 140 chars (le calculateur multiplie par 1.5×).
Toujours 2 colonnes — pas 3, pas 1.

---

## Quote (Instagram uniquement)

```markdown
## Citation

> "78 millions de dollars pour apprendre à prédire le mot suivant."

— Stanford AI Index 2025
```

Budget body : ≤ 200 chars. Toujours créditer l'auteur ou la source.

---

## Stat (Instagram uniquement)

```markdown
## Les chiffres qui marquent

<!-- stats -->
- 78M$ | Coût d'entraînement GPT-4
- 500MW | Datacenter Maroc 2026
- 6 | Datacenters inwi déjà actifs
```

Règles :
- Max 3 stats par slide
- `value` ≤ 8 chars (utiliser des suffixes : K, M, MW, %, ×)
- `label` ≤ 40 chars

---

## CTA (Instagram uniquement, ou content de fin LinkedIn)

**Règle stricte** : pas de lien, pas de domaine, pas de hashtag dans le body. Le CTA doit déclencher un **commentaire** ou un **partage**, pas un clic externe.

```markdown
## Et vous ?

Quelle est la **première chose** que vous allez tester demain matin ?<br><br>
<span class="hl2">Dites-le</span> en commentaire.
```

Variantes acceptées :
- Question ouverte directe : *« Et vous, où en êtes-vous ? »*
- Provocation douce : *« Honnêtement — la première réponse compte plus que la deuxième. »*
- Choix binaire : *« Pile ou face : auriez-vous fait le même pari ? »*

Body ≤ 160 chars. **Aucune mention** de blog, site, formation, lien, sous-domaine, ou hashtag.

---

## Squelette complet d'un carousel ACT (LinkedIn, 9 slides)

```markdown
---
series: "Africa Focus"
author: "@ACT"
title: "Maroc Hub Numérique"
---

# Maroc, hub numérique de l'Afrique

<!-- type:cover -->
<!-- badge:Africa Focus -->
<!-- cta:Swipe pour décrypter -->

---

## En mars 2026, ça bouge

Igoudar à Dakhla. 500 MW renouvelables. Cloud UM6P.<br><br>
<span class="hl1">Le Maroc construit physiquement</span> ce dont il parlait.

---

## Les 4 atouts structurels

<ul class="bullets">
  <li><span class="bold">Géographie</span> : carrefour Europe-Afrique.</li>
  <li><span class="bold">Énergie</span> : solaire et éolien à coût compétitif.</li>
  <li><span class="bold">Réglementation</span> : loi 09-08, CNDP, Digital Morocco 2030.</li>
  <li><span class="bold">Écosystème</span> : inwi, N+One, Maroc Datacenter.</li>
</ul>

---

## Dakhla : pari de l'énergie propre

Igoudar + Institut Jazari : infrastructure et souveraineté énergétique en parallèle.<br><br>
<span class="hl2">Signal fort :</span> la périphérie devient centre quand l'investissement suit.

---

## Cloud souverain vs cloud public

### Cloud souverain
Santé, finance, gouvernement.<br>
Hébergement local, CNDP.<br>
Tag: Souveraineté

### Cloud public
Bureautique, CRM, collaboration.<br>
Azure, AWS, GCP.<br>
Tag: Élasticité

---

## Pour qui ça compte ?

<ul class="bullets">
  <li>Entrepreneurs : data hébergée localement, latence basse.</li>
  <li>Investisseurs : hub Afrique de l'Ouest émergent.</li>
  <li>Talents tech : opportunités cloud + IA souveraine.</li>
</ul>

---

## La feuille de route 2030

Cloud hybride national, IA souveraine, éducation tech.<br><br>
<span class="hl1">Objectif :</span> Maroc plateforme régionale, pas simple consommateur.

---

## À retenir

<ul class="bullets">
  <li>Stratégie cohérente, pas effet d'annonce.</li>
  <li>Énergie verte = avantage compétitif durable.</li>
  <li>Sahara comme pôle d'innovation.</li>
</ul>

---

## Et vous ?

Quelle pièce de cette stratégie vous semble la **plus structurante** ?<br><br>
Partagez votre lecture en commentaire.
```
