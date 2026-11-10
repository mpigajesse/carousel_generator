---
series: "Data & IA · Décryptage"
author: "@Sohaib Baroud"
---

# ChatGPT, Gemini, Claude…

Enfin une explication qui **ne brûle pas vos neurones**.

---

## 78 millions de dollars

C'est ce qu'a coûté l'entraînement de **GPT-4** en calcul (Stanford AI Index 2025).

Pour apprendre à faire **une seule chose** : prédire le mot suivant.

---

## Pas de magie, juste 3 mécanismes

- **Tokenisation** — votre texte devient des numéros
- **Transformer** — l'attention en parallèle, pas séquentielle
- **Génération probabiliste** — chaque mot est un pari

Aucune équation. Aucune ligne de code dans cet article.

---

## Avant : l'IA qui lisait avec une main devant les yeux

Les **RNN** lisaient mot par mot, de gauche à droite.

Plus le texte était long, plus les premiers mots **disparaissaient du radar**.

> Une phrase courte, ça passait. Un paragraphe, c'était autre chose.

---

## 2017 : « Attention Is All You Need »

Une équipe Google publie le papier qui change tout.

Le **transformer** : lire **tout en même temps**, pas séquentiellement.

Plusieurs « têtes d'attention » en parallèle, chacune cherchant un type de relation.

---

## La tokenisation, étape oubliée

Le modèle ne lit pas vos mots. Il lit des **numéros**.

- Un token = fragment de texte (bout de mot, mot, fragment)
- **GPT-2** : ~50 000 tokens · **GPT-4** : ~100 000 · récents : **+200 000**
- Plus de tokens = meilleure qualité, mais rendements décroissants

---

## Pourquoi le modèle compte mal les « r » de strawberry

Le mot « strawberry » est représenté par **un seul numéro**.

Ses lettres individuelles sont **invisibles** au modèle.

> C'est comme demander de décrire un colis depuis son code-barres.

Pas un bug. Conséquence directe de la représentation.

---

## L'entraînement : deviner le token suivant

Des **milliards** de séquences. À chaque fois :

- On cache le dernier token
- Le modèle propose
- On compare et on ajuste les paramètres
- On recommence — **des centaines de milliards de fois**

---

## Génération : chaque mot est un pari

> « Quelle est la capitale de la France ? »

Le modèle calcule sur 100 000 tokens : **Paris** 41%, **La** 12%, **C'est** 8%…

Il tire selon ces probabilités. Le token choisi nourrit l'étape suivante. **Génération autoregressive**.

---

## La température, ce dé pipé

- **Basse** — prudent, prévisible — code, faits, juridique
- **Haute** — risque, créativité — fiction, brainstorming

Vous réglez l'irrégularité du dé. Pas la connaissance du modèle.

---

## Les hallucinations ne sont **pas** un bug

Quand le modèle génère « Comme le disait Camus, », il calcule juste les tokens probables.

Parfois c'est juste. Parfois c'est **faux mais plausible**.

> L'hallucination est une propriété **structurelle**, pas une défaillance à corriger.

Toute citation, tout chiffre = à vérifier.

---

## Toutes les langues ne sont pas égales

Modèle entraîné à **80% sur l'anglais** = probabilités moins calibrées en arabe, wolof, dari.

- Tokenisation moins efficace
- Plus de tokens = plus de calcul = précision moindre
- Critique pour les déploiements **multilingues** africains

---

## La fenêtre de contexte = mémoire courte

GPT-4 Turbo : jusqu'à **128 000 tokens** dans un échange.

Au-delà, le modèle « oublie » — pas progressivement, **brutalement**.

Comme si on arrachait les premières pages.

---

## Ce que ça change pour vous, demain

- Prompts **précis et structurés** — réduire l'espace des suites
- **Vérifier** chiffres et citations — toujours
- Architecturer les workflows longs autour de la **fenêtre de contexte**
- Utiliser la **température** selon le cas d'usage

---

## Les LLM ne sont pas des oracles

Ce sont des **systèmes de complétion** extraordinairement puissants.

Avec des forces et des angles morts **prévisibles** et documentés.

Ceux qui comprennent les deux s'en servent **mieux**.

---

## Et vous ?

Quelle erreur d'usage de ces outils vous a **le plus surpris** quand vous avez compris ce mécanisme ?

Racontez-moi en commentaire.
