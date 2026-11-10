# Template — Article d'analyse ACT Blog

## Utilisation
Article d'analyse, explicatif, panorama non-tutoriel. Longueur : 1500–2500 mots.
Audience cible : professionnels tech, décideurs, praticiens.

---

## Structure obligatoire

### 1. Titre

Format : **[Verbe d'action ou question directe] — [Bénéfice ou contexte marocain/africain]**

Exemples corrects :
- "L'IA dans les banques marocaines : ce qui se passe vraiment en coulisses"
- "dbt : pourquoi cet outil change la vie des data analysts (avec exemples)"
- "RAG vs fine-tuning : comment choisir selon votre budget et vos données"

Éviter :
- "Tout ce que vous devez savoir sur..." (cliché)
- "Introduction à..." (trop académique)
- Titres sans verbe d'action ni bénéfice clair

---

### 2. Accroche (150–200 mots)

**Règle absolue : ne pas commencer par "Dans un monde où..."**

Trois approches efficaces :

**Option A — Le fait surprenant :**
```
[Chiffre contre-intuitif ou peu connu]. [Contexte qui explique pourquoi c'est important 
pour le lecteur marocain/africain]. [Transition vers le sujet de l'article.]
```

**Option B — Le problème concret :**
```
[Scénario réel que beaucoup reconnaissent]. [Ce que ça coûte ou ce que ça bloque]. 
[Ce que cet article va résoudre ou éclairer.]
```

**Option C — La question dérangeante :**
```
[Question directe qui remet en cause une idée reçue]. [Observation terrain ou donnée]. 
[Promesse de l'article : ce que le lecteur va comprendre différemment à la fin.]
```

---

### 3. Corps de l'article

#### Chapitrage

- 3 à 5 sections principales avec titres H2 explicites (pas "Introduction", pas "Développement")
- Chaque section = une idée centrale, développée en 300–500 mots
- Alterner : argumentation → exemple concret → implication pratique

#### Structure d'une section type

```markdown
## [Titre H2 explicite — ce que la section apporte]

[Affirmation principale de la section — 1–2 phrases courtes, tranchées.]

[Développement en 2–3 paragraphes. Alterner : concept → exemple marocain/africain → 
nuance ou limite. Jamais plus de 5 lignes par paragraphe.]

> **En pratique :** [encadré pratique — ce que le lecteur peut faire concrètement 
> avec cette information dans son contexte marocain]
```

#### Éléments visuels à intégrer

Indiquer dans le texte où placer :
- `[IMAGE : description de l'illustration recommandée]`
- `[TABLEAU : titre du tableau et colonnes suggérées]`
- `[ENCADRÉ : titre — contenu de l'encadré]`
- `[CALLOUT : citation ou chiffre à mettre en avant]`

---

### 4. Section "Contexte marocain / africain" — à ajouter si pertinent

Cette section n'est **pas systématique**. L'ajouter uniquement si le sujet le justifie naturellement.

**Ajouter cette section si :**
- L'article porte sur le marché, l'économie ou la réglementation marocaine/africaine
- La réalité locale diverge significativement de la réalité globale traitée dans l'article
- Des contraintes spécifiques marocaines (réglementation, accès, coûts) méritent d'être signalées

**Ne pas ajouter cette section si :**
- L'article est technique et universel (comparatif d'outils, tutoriel de code générique)
- Forcer le contexte local produirait un encadré artificiel qui n'apporte pas de valeur

**Si pertinent, format recommandé :**

```markdown
## Ce que ça change pour les entreprises marocaines / africaines

[2–3 paragraphes spécifiques : comment le sujet s'applique au Maroc,
quelles entreprises ou secteurs sont concernés, quelles spécificités locales
(réglementation, infrastructure, compétences disponibles, coûts en MAD).]
```

---

### 5. Conclusion — pas de résumé, une ouverture

**Ne pas résumer l'article.** Le lecteur vient de le lire.

Format recommandé :
```markdown
## [Titre d'appel à l'action ou de perspective]

[1 paragraphe qui tire la conséquence principale de l'article — "ce que ça change" 
plutôt que "ce qu'on a vu".]

[1 paragraphe qui ouvre : prochaine étape pour le lecteur, question restée ouverte, 
ou annonce d'un article de suite.]

[CTA naturel : lien vers formation ACT University liée OU invitation à commenter 
OU demande de partage avec une phrase spécifique.]
```

---

### 6. Bloc méta SEO (toujours en fin d'article)

```
---
## Méta SEO

**Titre SEO** : [max 60 caractères — mot-clé en tête]
**Meta description** : [max 155 caractères — bénéfice + mot-clé + contexte]
**Mot-clé principal** : [expression 2–4 mots recherchée par la cible]
**Mots-clés secondaires** : [3–5 expressions longue traîne]
**Slug URL** : /blog/[3-5-mots-kebab-case]
**Temps de lecture estimé** : [X] min
**CTA recommandé** : [Lien vers formation ACT liée ou article connexe]
**Image à la une** : [Description précise de l'illustration idéale]
---
```

---

## Checklist avant livraison

- [ ] Accroche sans "Dans un monde où..."
- [ ] Si sujet marché/business : au moins 2 ancrages marocains/africains présents
- [ ] Si sujet technique universel : exemples neutres ou pertinents au sujet, contextualisation non forcée
- [ ] Tous les chiffres ont une source citée
- [ ] Chaque H2 dit quelque chose (pas juste un label)
- [ ] Conclusion ≠ résumé
- [ ] Bloc méta SEO rempli
- [ ] Longueur entre 1500 et 2500 mots
