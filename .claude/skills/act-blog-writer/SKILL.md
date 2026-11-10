---
name: act-blog-writer
description: >
  Production d'articles de blog de qualité journalistique pour le blog ACT.
  Déclencher pour toute demande de : écrire, rédiger, générer, préparer, ébaucher
  un article, un tutoriel, un comparatif, une opinion ou une liste pour le blog.
  Ce skill impose une méthode rigoureuse : recherche bibliographique préalable,
  référencement systématique de toutes les données chiffrées avec leur source primaire,
  structure narrative adaptée au type d'article, style clair et factuel, évitement des
  prises de position non étayées et des conclusions faciles. S'applique à tout sujet —
  technique universel, analyse de marché, tutoriel, panorama d'outils ou opinion documentée.
---

# ACT Blog Writer

Ce skill impose la **méthode de construction** d'un article de blog de qualité — indépendamment
du sujet traité. L'objectif n'est pas de produire vite, mais de produire juste : chaque chiffre
sourcé, chaque affirmation étayée, chaque conclusion méritée par l'argumentation qui la précède.

**Principes fondateurs :**
- Aucun chiffre sans source primaire identifiée
- Aucune conclusion qui dépasse ce que les données permettent
- Aucune prise de position sans argumentation développée
- La nuance n'est pas une faiblesse — c'est la marque d'un travail sérieux

---

## Étape 0 — Identifier le type d'article avant tout

Lire la demande et identifier le type parmi les cinq suivants :

| Type | Déclencheurs | Template |
|---|---|---|
| **Article d'analyse** | "écris un article sur", "analyse", "explique" | `references/template-article.md` |
| **Tutoriel pratique** | "tutoriel", "guide pas à pas", "comment faire", code impliqué | `references/template-tutoriel.md` |
| **Opinion / prise de position** | "opinion", "point de vue", "est-ce que X est vraiment...", "faut-il..." | `references/template-opinion.md` section A |
| **Comparatif** | "vs", "comparer", "lequel choisir", "différence entre" | `references/template-opinion.md` section B |
| **Liste / panorama** | "top X", "les N meilleurs", "panorama", "cartographie", "état de l'art" | `references/template-opinion.md` section C |

Si le type est ambigu → demander avant de produire.
Si le sujet n'est pas précisé → demander : "Sur quel sujet précis voulez-vous l'article ?"

---

## Étape 1 — Recherche bibliographique préalable (non négociable)

Avant d'écrire une seule ligne de contenu, effectuer la recherche.
**Un article de blog qui n'a pas de recherche derrière n'est pas un article — c'est une opinion.**

### Principe du sourçage à la source primaire

La chaîne de citation acceptable : **fait → source primaire → article**.
La chaîne inacceptable : fait → blog B → blog A → article.

Toujours remonter à la source primaire :
- Un chiffre de croissance → rapport de l'institution qui l'a produit (IDC, Gartner, Statista, HCP, BAM...)
- Une étude → le papier original, pas le résumé presse
- Une version d'outil → pypi.org, changelog GitHub officiel, documentation maintenue par l'éditeur
- Une déclaration → la source directe (communiqué officiel, interview primaire), pas une dépêche qui la cite

### Ce qu'il faut chercher selon le type d'article

**Pour tout article factuel :**
- Les 3 premiers résultats Google sur le sujet → identifier ce qui existe déjà et l'angle non couvert
- Les chiffres clés → vérification sur source primaire, date de publication
- Les affirmations susceptibles d'avoir évolué → actualité récente sur le sujet

**Pour les articles techniques :**
- Version stable actuelle des outils mentionnés → pypi.org, docs officielles
- Changements d'API depuis la dernière version majeure → changelog
- Benchmarks ou comparaisons cités → vérifier la méthodologie et la date

**Pour les articles de marché :**
- Données institutionnelles → HCP, BAM, APEBI, ITU, GSMA, rapports annuels d'entreprises cotées
- Données sectorielles → organismes professionnels du secteur concerné
- Actualité récente → presse spécialisée, communiqués officiels datés

### Sources prioritaires par domaine

| Domaine | Sources officielles prioritaires |
|---|---|
| **IA & LLM** | huggingface.co/blog · arxiv.org · openai.com/blog · anthropic.com/news |
| **Data Engineering** | docs.getdbt.com · duckdb.org/docs · iceberg.apache.org/docs |
| **Marché marocain** | hcp.ma · bam.org.ma · apebi.ma · mcinet.gov.ma · rapports annuels publiés |
| **Tech africaine & global** | itu.int · gsma.com · worldbank.org/tech |
| **Réglementation** | cndp.ma · legifrance.gouv.fr · ompi.int |
| **Emploi & salaires** | linkedin.com/jobs · données publiques sectorielles |
| **Recherche académique** | arxiv.org · scholar.google.com · hal.science |

### Protocole en 3 étapes

1. **Chercher** : requête ciblée sur le sujet et ses chiffres clés
2. **Vérifier** : fetcher les pages sources pour confirmer chiffres et contexte exact
3. **Inventorier** : noter chaque source utilisée avec son URL, auteur et date — elle figurera dans l'article

### Format de citation dans le texte

Chaque donnée chiffrée ou affirmation factuelle non triviale doit être accompagnée de sa source, intégrée naturellement dans la phrase :

```
✓ "Selon le rapport ITU 2024, la pénétration d'internet mobile en Afrique subsaharienne 
   atteint 47% — contre 89% en Europe occidentale."

✓ "D'après les données HCP publiées en mars 2025, le secteur du numérique représente 
   4,2% du PIB marocain."

✗ "Selon les experts, l'adoption de l'IA progresse rapidement au Maroc."
✗ "Des études montrent que 70% des entreprises ont adopté l'IA."
```

---

## Étape 2 — Règles éditoriales ACT (toujours appliquer)

### Voix et style rédactionnel

**Registre :** clair, factuel, accessible. Ni académique ni démagogique. Le lecteur ne devrait jamais avoir à relire une phrase pour en comprendre le sens.

**Personne :** variable selon le type d'article — "nous" pour les analyses collectives, "vous" pour s'adresser au lecteur, troisième personne pour les faits. Ne pas mélanger les registres dans un même article.

**Rythme :** phrases courtes et moyennes alternées. Pas de paragraphes de plus de 5 lignes. Les listes structurent, mais ne remplacent pas l'argumentation développée en prose.

**Précision :** préférer un mot juste à une périphrase. Définir les termes techniques dès leur première apparition. Éviter les anglicismes non expliqués.

**Ton et prises de position :**

Un article de blog de qualité n'est pas un manifeste. La force d'un article vient de la solidité de son argumentation, pas de la fermeté de sa conclusion.

- Formuler les constats comme des constats, les hypothèses comme des hypothèses, les opinions comme des opinions — ne pas confondre les trois.
- Une nuance honnête ("les données disponibles suggèrent que", "dans le contexte étudié") renforce la crédibilité ; elle n'affaiblit pas l'article.
- Les positions tranchées sont acceptables uniquement quand elles sont entièrement soutenues par les faits présentés dans l'article. Si les faits ne permettent pas une conclusion ferme, ne pas en formuler une.
- **Éviter les raccourcis rhétoriques :** ne pas résoudre une complexité par une formule frappante. Si le sujet est complexe, le dire honnêtement et en montrer la complexité.

**Limites à signaler :**
- Si des données manquent pour étayer une affirmation, le signaler explicitement plutôt que de généraliser depuis des données insuffisantes.
- Si un sujet a évolué depuis la dernière vérification, le mentionner avec la date de la vérification effectuée.

### Contextualisation marocaine/africaine — conditionnelle selon le sujet

Le blog ACT couvre des sujets **divers et variés** : techniques universels, analyses de marché, tutoriels de code, panoramas d'outils. La contextualisation n'est pas systématique — elle dépend de la nature du sujet.

**Évaluer le sujet avant de décider :**

| Type de sujet | Contextualisation | Approche |
|---|---|---|
| Sujet technique universel | Non obligatoire | "RAG vs fine-tuning", "Polars vs pandas" → exemples neutres ou universels, ne pas forcer le Maroc |
| Sujet marché / business | Obligatoire | "L'IA dans les banques", "salaires data au Maroc" → ancrage local incontournable |
| Tutoriel avec données | Recommandée | Préférer un dataset marocain si disponible, mais ne pas inventer un contexte artificiel |
| Panorama d'outils | Optionnelle | Ajouter une note "Applicabilité au Maroc" si pertinente, sinon omettre |
| Éco-IA / responsable | Recommandée | Mentionner les implications pour les entreprises africaines quand c'est naturel |
| Opinion / tendances globales | Optionnelle | Ajouter un encadré "Et au Maroc ?" uniquement si la réalité locale diverge significativement |

**Règle générale : la contextualisation s'ajoute quand elle apporte de la valeur, jamais pour cocher une case.** Un article technique de qualité sans ancrage marocain vaut mieux qu'un article avec un exemple marocain forcé et artificiel.

**Quand contextualiser naturellement :**
- Les données de l'exemple existent dans le contexte marocain
- La réglementation marocaine s'applique (loi 09-08, BAM, CNDP)
- La réalité marocaine diverge de la réalité globale de manière intéressante
- L'audience marocaine a une contrainte spécifique à signaler (coûts, accès, compétences)

**Ressources disponibles si contextualisation retenue :**
Entreprises : Attijariwafa Bank, CIH Bank, OCP, ONCF, Inwi, Marjane, avito.ma, Jumia Maroc.
Prénoms marocains : Youssef, Fatima, Amine, Nadia, Khalid, Zineb (jamais John/Jane dans un contexte marocain explicite).
Montants : en MAD si le contexte est marocain, en USD/EUR si le sujet est international.

### Longueurs cibles par type

| Type | Longueur cible | Note |
|---|---|---|
| Article d'analyse | 1500–2500 mots | En dessous de 1200 mots = trop court pour le SEO |
| Tutoriel | 2000–3500 mots | Inclure le code complet, pas de raccourcis |
| Opinion | 1000–1800 mots | Plus court = plus de punch |
| Comparatif | 1500–2500 mots | Tableau de synthèse obligatoire |
| Liste / panorama | 1200–2000 mots | Au moins 6 items avec développement |

---

## Étape 3 — Structure SEO minimale (toujours inclure)

Chaque article produit doit inclure, en fin de document :

```
## Méta SEO (à remplir avant publication)

**Titre SEO** : [60 caractères max, mot-clé principal en tête]
**Meta description** : [155 caractères max, reformulation de la valeur de l'article]
**Mot-clé principal** : [1 expression, 2–4 mots]
**Mots-clés secondaires** : [3–5 expressions longue traîne]
**Balise H1** : [= Titre SEO sauf si reformulation nécessaire]
**Slug URL** : [kebab-case, 3–6 mots, sans stop words]
**Image à la une** : [description de ce qu'il faudrait illustrer]
**CTA de fin** : [lien vers formation ACT University liée, si pertinent]
```

---

## Anti-patterns à bannir

### Problèmes de structure et de style
- ❌ Intro générique "Dans un monde où l'IA évolue rapidement..." → commencer par un fait, un chiffre ou une question directe
- ❌ Conclusion résumé "En conclusion, nous avons vu que..." → terminer sur une perspective, une question ouverte ou une action concrète
- ❌ Anglicismes non expliqués collés en français → définir ou franciser au premier usage
- ❌ Longueur artificielle par répétition → chaque paragraphe apporte une information nouvelle ou un angle différent
- ❌ Code non testé dans les tutoriels → tout code doit être exécutable tel quel

### Problèmes de rigueur factuelle — les plus graves
- ❌ Chiffre sans source → jamais "selon une étude", "d'après les experts", "on estime que" — toujours : source, auteur, date
- ❌ Source secondaire présentée comme primaire → si un blog cite une étude McKinsey, aller chercher l'étude McKinsey, pas citer le blog
- ❌ Chiffre sorti de son contexte → un pourcentage sans dénominateur, une croissance sans base, une comparaison sans même périmètre invalident l'argumentation
- ❌ Statistique ancienne présentée comme actuelle → vérifier la date des données, signaler si les chiffres datent de plus de 18 mois
- ❌ Extrapolation non signalée → si on infère depuis des données partielles, le dire explicitement

### Problèmes de positionnement éditorial — à éviter absolument
- ❌ Conclusion qui dépasse les données → si l'article n'a présenté que des éléments favorables à une thèse, ne pas conclure comme si la thèse était prouvée
- ❌ Prise de position sans argumentation développée → une opinion exprimée en une phrase sans les paragraphes qui la justifient n'est pas de l'analyse, c'est du bruit
- ❌ Fausse nuance → "d'un côté... de l'autre côté... il faudrait trouver un équilibre" sans dire lequel ni pourquoi — c'est esquiver la question, pas la traiter
- ❌ Généralisation abusive → "toutes les PME marocaines", "les développeurs pensent que", "le marché africain est..." → préciser le périmètre exact
- ❌ Hype non interrogée → adopter sans distance critique le discours d'un éditeur, d'un rapport commandité, ou d'une tendance médiatique
- ❌ Comparatifs sans critères explicites → poser les critères de comparaison avant le verdict, jamais après

---

## Étape 4 — Lire le template correspondant

Après avoir identifié le type et effectué la recherche web, lire le template dans `references/` :

- Article d'analyse → `references/template-article.md`
- Tutoriel → `references/template-tutoriel.md`
- Opinion → `references/template-opinion.md` section A
- Comparatif → `references/template-opinion.md` section B
- Liste / panorama → `references/template-opinion.md` section C
- Checklist SEO → `references/template-opinion.md` section D (présente dans tous les articles)

---

## Comportement attendu

- Lire le template correspondant **avant** de rédiger.
- Signaler en **début de production** : type détecté, angle retenu, sources consultées (avec URLs).
- Signaler en **fin de production** :
  - (a) Chiffres ou affirmations qui n'ont pas pu être vérifiés — à confirmer avant publication
  - (b) Sections où les données manquent et où la conclusion est donc provisoire
  - (c) Points sur lesquels une mise à jour sera nécessaire dans 6 à 12 mois
- Si une conclusion ne peut pas être étayée par les données trouvées → ne pas la formuler, signaler le manque.
- Si un sujet est trop incertain ou trop récent pour une analyse fiable → le dire dans l'article, pas le taire.
- Si un article demandé figure dans le catalogue des 70 sujets → utiliser l'angle défini comme point de départ, mais la recherche bibliographique reste obligatoire.
