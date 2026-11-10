---
name: act-humanizer
description: >
  Humanise et réécrit du texte pour le rendre plus naturel, plus vivant et moins
  "généré par IA". Déclencher quand l'utilisateur demande : rendre plus humain,
  humaniser, réécrire de façon plus naturelle, enlever le style IA, rendre plus
  fluide, moins robotique, moins formel, moins prévisible, plus conversationnel.
  S'applique à tout type de contenu : articles de blog, emails, posts LinkedIn,
  contenus pédagogiques, introductions, conclusions, paragraphes isolés.
  Produit le texte réécrit + un bref commentaire sur les transformations effectuées.
---

# ACT Humanizer

Ce skill transforme un texte pour qu'il sonne comme écrit par un être humain —
pas comme généré par un modèle de langage qui optimise pour la complétude.

**Principe central :** un texte humain est imparfaitement parfait. Il a un rythme
irrégulier, des opinions assumées, des phrases courtes qui cassent la cadence,
des transitions inattendues. Il ne couvre pas tout — il choisit quoi dire.

---

## Étape 0 — Lire et diagnostiquer avant de réécrire

Avant de toucher au texte, identifier les signaux IA présents.
Lire `references/signaux-ia.md` pour la liste complète.

**Les 6 signaux IA les plus fréquents à détecter :**

1. **Mots-valises** : crucial, essentiel, innovant, pertinent, robuste, significatif, optimal, holistique, paradigme, synergies — sans contenu derrière
2. **Listes à puces qui remplacent la prose** : tout transformé en bullet points, y compris ce qui aurait été naturellement une phrase
3. **Symétrie mécanique** : toutes les sections de même longueur, toutes les phrases de même structure sujet-verbe-complément
4. **Transitions de rédacteur-robot** : "Dans cette section, nous allons explorer...", "Il convient de noter que...", "En ce qui concerne..."
5. **Exhaustivité forcée** : l'article couvre tous les angles d'un sujet de façon égale, sans point de vue
6. **Conclusion résumé** : dernier paragraphe qui répète ce qui vient d'être dit, sans rien ajouter

---

## Étape 1 — Identifier le type de contenu et le registre cible

Ce skill s'applique à trois contextes ACT distincts. Le registre humain cible est différent dans chacun — identifier avant de réécrire.

### Contexte A — Article de blog ACT

**Registre cible :** praticien qui partage ce qu'il a appris, pas un journaliste qui rapporte.
Direct, opinioné, avec des apartés. Des phrases qui tranchent. Des exemples nommés.
Le lecteur doit sentir qu'il y a quelqu'un derrière le texte — avec un avis.

**Signaux spécifiques à corriger en priorité :**
- Intro générique ("Dans un monde où...")
- Sections de longueur parfaitement égale
- Absence de position assumée
- Conclusion qui résume au lieu d'ouvrir

**Longueur après réécriture :** identique ou légèrement plus courte. La densité augmente, pas le volume.

---

### Contexte B — Contenu pédagogique ACT University

**Registre cible :** formateur bienveillant qui explique à un pair curieux — pas un manuel scolaire.
Clair, avec des métaphores du quotidien, une progression logique, et une voix constante.
Le lecteur doit se sentir accompagné, pas évalué.

**Signaux spécifiques à corriger en priorité :**
- Listes à puces qui remplacent des explications (très fréquent dans les cours)
- Vouvoiement/tutoiement incohérent selon les sections
- Phrases passives qui distancent ("il est recommandé de", "on peut noter que")
- Exemples génériques ou sans contexte (Alice, Bob, foo/bar)

**Règle clé pour les cours :** les concepts doivent être introduits par le problème qu'ils résolvent, pas par leur définition. Transformer "X est une méthode qui permet de..." en "Quand vous faites Y, vous vous heurtez à un problème. X est la réponse à ce problème."

**Longueur après réécriture :** peut augmenter légèrement si l'explication gagnait en clarté.

---

### Contexte C — Post LinkedIn / réseaux sociaux

**Registre cible :** professionnel qui réfléchit à voix haute — personnel, concret, qui part d'une vraie observation.
Les 2 premières lignes sont cruciales (coupure "voir plus"). Le post doit se lire à voix haute sans accroc.
Pas d'hashtags en milieu de texte. Pas de listes à 5 items avec des emojis en bullet.

**Format humain pour LinkedIn :**
```
[Observation ou fait concret — 1 phrase, max 15 mots]

[Développement en 3–5 paragraphes courts, 1–3 phrases chacun]
[Ligne blanche entre chaque paragraphe — jamais de mur de texte]
[Un paragraphe peut faire 1 seule phrase. C'est voulu.]

[Conclusion ou question ouverte — 1–2 phrases]

[Hashtags en fin — 3 max, pas plus]
```

**Signaux spécifiques à corriger en priorité :**
- Post qui commence par "Je suis ravi(e) de partager..."
- Listes à puces avec emojis → convertir en prose avec sauts de ligne
- Phrases de 30+ mots → couper en 2
- Absence de première ligne accrocheuse (tout repose sur elle)
- Conclusion qui ne dit rien : "N'hésitez pas à partager vos commentaires !"

---

## Étape 2 — Appliquer les transformations

Appliquer dans cet ordre de priorité. Ne pas toutes les appliquer mécaniquement —
choisir celles qui répondent aux signaux IA diagnostiqués à l'étape 0.

### T1 — Briser la symétrie rythmique

L'IA produit des phrases du même gabarit. L'humain varie instinctivement.

**Techniques :**
- Intercaler une phrase très courte (3–6 mots) après 2–3 phrases longues. Elle tranche. Elle marque.
- Commencer une phrase par une conjonction : "Mais." / "Et pourtant." / "Sauf que."
- Laisser une phrase incomplète si l'effet le justifie — la langue parlée le fait.
- Varier la position du verbe, du sujet, des compléments.

**Avant :**
> "Il est important de noter que la transformation digitale représente un enjeu majeur pour les entreprises marocaines. Cette transformation implique plusieurs dimensions qui doivent être prises en compte."

**Après :**
> "La transformation digitale change tout pour les PME marocaines. Pas seulement les outils — les façons de décider, d'embaucher, de se tromper."

---

### T2 — Remplacer les mots-valises par du concret

Chaque mot vague doit être remplacé par ce qu'il signifie réellement dans le contexte.

**Dictionnaire de remplacement :**

| Mot IA | Remplacer par |
|---|---|
| crucial / essentiel | [préciser pourquoi — "sans ça, X ne fonctionne pas"] |
| innovant | [préciser en quoi — "pour la première fois, X permet..."] |
| pertinent | [préciser pour qui et dans quel contexte] |
| robuste | [préciser ce qu'il résiste — "fonctionne même quand..."] |
| significatif | [donner le chiffre ou l'ordre de grandeur] |
| holistique / global | [décomposer — "à la fois X, Y et Z"] |
| optimal | [comparé à quoi — "mieux que..."] |
| paradigme | [expliquer ce qui change concrètement] |
| synergies | [donner l'exemple concret de la combinaison] |
| il convient de noter | [supprimer — commencer directement par le fait] |
| il est important de | [supprimer — si c'est important, le dire directement] |
| dans le contexte actuel | [supprimer ou préciser — "depuis 2023..."] |
| à l'ère du numérique | [supprimer — cliché pur, reformuler sans] |

---

### T3 — Convertir les listes en prose (priorité haute)

C'est le signal IA le plus fréquent dans les trois contextes ACT.
**La règle par défaut : si c'est une liste de phrases, c'est de la prose déguisée. La convertir.**

**Quand convertir une liste en prose :**
- Les items sont des phrases complètes (sujet + verbe + complément)
- Les items ont une logique entre eux (cause → effet, général → particulier, problème → solution)
- La liste a 4 items ou moins
- Le lecteur doit *comprendre* la relation entre les items, pas juste les *voir*

**Quand garder une liste :**
- C'est une vraie énumération : étapes numérotées, outils, ressources, prérequis
- Les items sont des labels courts (2–4 mots) sans logique à expliquer
- La liste a 6 items ou plus et le parallélisme est intentionnel

**Technique de conversion — les 3 connecteurs humains :**

Au lieu de répéter les items séparés, les relier avec un connecteur qui dit la relation :
- **Conséquence** : "ce qui signifie que", "du coup", "résultat :"
- **Addition significative** : "mais aussi", "et plus encore", "sans oublier que"
- **Contraste** : "en revanche", "sauf que", "là où X..., Y..."

**Avant (liste IA) :**
> Les avantages de dbt sont les suivants :
> - Amélioration de la qualité des données
> - Documentation automatique
> - Facilitation de la collaboration entre équipes

**Après (prose humaine) :**
> Ce qui change avec dbt, c'est d'abord la confiance dans les données — chaque transformation est testée. La documentation se génère automatiquement, ce qui veut dire que les nouveaux arrivants comprennent le pipeline en quelques heures. Et quand tout le monde travaille sur les mêmes modèles versionnés, les silos entre data analysts disparaissent d'eux-mêmes.

**Cas LinkedIn spécifique :**
Sur LinkedIn, les listes à emojis sont particulièrement problématiques.
```
❌ À éviter :
✅ Ce que dbt change concrètement :
• 📊 Meilleure qualité des données
• 📝 Documentation automatique
• 🤝 Meilleure collaboration

✓ Remplacer par : prose avec sauts de ligne entre les idées
```

---

### T4 — Injecter un point de vue

L'IA présente, l'humain juge. Ajouter une opinion, une réserve, une surprise.

**Techniques :**
- Ajouter "Ce qui est surprenant, c'est que..." ou "Ce qu'on oublie souvent..."
- Formuler une position : "Personnellement, je pense que..." ou "Notre conviction chez ACT, c'est que..."
- Reconnaître une limite honnêtement : "Ça ne marchera pas si...", "La limite, c'est..."
- Nommer l'éléphant dans la pièce : ce que l'article évite généralement de dire

**Règle :** le point de vue doit être étayé — une opinion ne flotte pas dans le vide.

---

### T5 — Reconstruire les transitions

Les transitions IA expliquent ce qu'elles font. Les transitions humaines font la transition.

**Supprimer systématiquement :**
- "Dans cette section, nous allons..."
- "Comme nous l'avons vu précédemment..."
- "Il convient maintenant d'aborder..."
- "En ce qui concerne la question de..."

**Remplacer par :**
- Un lien de sens direct (cause, conséquence, contraste, exemple)
- Une question rhétorique
- Un fait qui ouvre la section suivante

**Avant :**
> "Nous venons d'explorer les avantages. Il convient maintenant d'aborder les limites."

**Après :**
> "Sauf que rien n'est gratuit."

---

### T6 — Réparer l'accroche et la conclusion

Ce sont les deux endroits où l'IA est la plus prévisible.

**Accroche humaine — règles :**
- Commencer par un fait concret, un chiffre, une scène ou une question directe
- Jamais : "Dans un monde où...", "À l'ère du numérique...", "De plus en plus..."
- La première phrase doit créer une tension ou une surprise
- Idéalement : le lecteur ne sait pas encore où l'article va — il veut le savoir

**Conclusion humaine — règles :**
- Ne pas résumer ce qui vient d'être dit
- Terminer sur : une question ouverte, une implication pratique, une mise en perspective, un appel à action précis
- La dernière phrase doit rester — pas s'évaporer

---

### T7 — Ancrage sensoriel et concret

L'IA abstrait. L'humain montre.

**Remplacer :**
- Les noms génériques par des noms propres (une entreprise réelle ou fictive crédible, un prénom)
- Les situations hypothétiques par des scénarios concrets ("Imaginez Fatima, data analyst chez un distributeur casablancais...")
- Les affirmations générales par des exemples spécifiques

### T8 — Assouplir les tournures formelles et rigides

Les tournures formelles créent une distance entre le texte et le lecteur.
Elles signalent "document officiel" là où le blog et LinkedIn demandent "conversation entre pairs".

**Tournures formelles → reformulations humaines :**

| Formel et rigide | Humain et direct |
|---|---|
| "Il est nécessaire de procéder à..." | "Il faut..." ou "La première chose à faire, c'est..." |
| "Dans le cadre de cette analyse..." | Supprimer — commencer directement |
| "Nous allons examiner les différents aspects de..." | "Voici ce qui change concrètement." |
| "Cette approche présente plusieurs avantages..." | "Pourquoi ça marche ? Parce que..." |
| "Il convient de mentionner que..." | Supprimer — dire directement le fait |
| "L'utilisation de cet outil permet de..." | "[L'outil] fait X. Ce qui veut dire que vous pouvez..." |
| "Dans un premier temps... dans un second temps..." | "D'abord... Ensuite... Mais surtout..." |
| "Nous pouvons constater que..." | Supprimer — énoncer directement la conclusion |
| "Cette problématique est complexe et multidimensionnelle." | Décomposer la complexité au lieu de la nommer |
| "Il va sans dire que..." | Supprimer — si ça va sans dire, ne pas le dire |
| "À titre d'exemple..." | "Par exemple" ou "Concrètement :" |
| "Ledit outil / ladite approche" | Répéter le nom — c'est plus clair |

**Règle générale :** si une formule pourrait figurer dans un rapport administratif, la supprimer ou la reformuler.

**Cas pédagogique spécifique :**
Dans les cours ACT University, la rigidité formelle tue l'engagement.

| Formel pédagogique | Humain pédagogique |
|---|---|
| "L'apprenant sera en mesure de..." | "À la fin de ce module, vous saurez..." |
| "Il est recommandé de consulter..." | "Lisez ça avant — ça change tout :" |
| "Ce concept sera abordé ultérieurement." | "On reviendra là-dessus au module 4." |
| "La notion de X peut être définie comme..." | "X, c'est quoi exactement ?" |

---

## Étape 3 — Vérification avant livraison

Après réécriture, lire une fois à voix haute (mentalement) et cocher :

- [ ] Y a-t-il une voix identifiable derrière ce texte — un humain avec un point de vue ?
- [ ] Y a-t-il au moins une phrase courte (≤ 8 mots) dans les 100 premiers mots ?
- [ ] A-t-on supprimé tous les mots de la liste T2 (crucial, essentiel, innovant...) ?
- [ ] Les listes restantes sont-elles des vraies énumérations — pas de la prose déguisée ?
- [ ] A-t-on supprimé les tournures formelles de la liste T8 ?
- [ ] La conclusion dit-elle quelque chose de nouveau (pas un résumé) ?
- [ ] Le texte a-t-il un rythme irrégulier — ou est-il encore mécaniquement régulier ?
- [ ] **LinkedIn spécifique :** les 2 premières lignes donnent-elles envie de cliquer "voir plus" ?
- [ ] **Cours spécifique :** chaque concept est-il introduit par le problème qu'il résout ?

---

## Format de sortie

Produire dans cet ordre :

```
## Texte humanisé

[Texte réécrit — complet, propre, sans commentaires inline]

---

## Transformations effectuées

[Liste courte (3–6 items) des principales interventions.
Format : T[N] — [description en 1 ligne de ce qui a changé et pourquoi]
Exemple : T2 — "crucial" et "essentiel" remplacés par des formulations concrètes
         T3 — 2 listes converties en prose argumentative
         T5 — 3 transitions IA supprimées, remplacées par des liens de sens]

## Signaux IA résiduels (si applicable)

[Ce qui n'a pas pu être corrigé sans changer le fond de l'article.
Si aucun : "Aucun signal IA résiduel détecté."]
```

---

## Ce que le skill ne fait PAS

- Ne change pas les faits, les chiffres ni les sources — il modifie la forme, pas le fond
- Ne raccourcit pas artificiellement — il densifie si nécessaire
- Ne rend pas informel ce qui doit rester professionnel
- Ne supprime pas la précision technique pour "simplifier"
- Ne réécrit pas si le texte est déjà humain — signaler que peu d'interventions sont nécessaires
