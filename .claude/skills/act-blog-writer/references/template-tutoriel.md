# Template — Tutoriel pratique ACT Blog

## Utilisation
Guide pas à pas avec code exécutable. Longueur : 2000–3500 mots.
Audience : développeurs et data engineers. Règle d'or : le lecteur doit pouvoir
finir le tutoriel en moins de 2 heures avec un résultat visible.

---

## Structure obligatoire

### 1. Titre

Format : **[Ce qu'on construit] + [Outils] + [Durée ou niveau de difficulté]**

Exemples corrects :
- "Construire un chatbot RAG avec LangChain et Ollama — tutoriel complet en 1h"
- "Détecter la fraude bancaire avec Python et scikit-learn — pipeline complet"
- "Déployer FastAPI sur un VPS OVH : guide production en 30 minutes"

---

### 2. En-tête technique (avant le contenu)

```markdown
> **Difficulté :** [Débutant / Intermédiaire / Avancé]
> **Durée estimée :** [X minutes / X heures]
> **Prérequis :** [Liste courte et honnête — pas de "aucun" si Python est requis]
> **Ce que vous allez construire :** [Description en 1 phrase du livrable final]
> **Environnement :** [Google Colab gratuit / VPS / Local — aucun cloud propriétaire requis]
> **Code complet :** [lien GitHub ou note "disponible en fin d'article"]
```

---

### 3. Accroche contextuelle (100–150 mots)

Partir d'un problème métier marocain concret, pas d'une définition technique.

```markdown
**Contexte :** [Entreprise fictive marocaine crédible + problème métier réel.]
Par exemple : "Darija Commerce SARL reçoit 200 emails clients par jour. 
Trier manuellement prend 3 heures à l'équipe support..."

**Ce que ce tutoriel résout :** [En 2 phrases maximum — ce que le lecteur 
sait faire à la fin et comment ça s'applique à son contexte.]
```

---

### 4. Installation et prérequis

```markdown
## Installation

### Environnement recommandé

[Préciser Google Colab / Jupyter local / VPS. Justifier le choix.
Toujours proposer une option gratuite et accessible.]

### Dépendances

```bash
# Vérifier les versions sur pypi.org à la date de production
pip install [lib1==X.Y.Z] [lib2==X.Y.Z]
```

> **Note :** Versions testées le [DATE]. Vérifier la compatibilité 
> si vous utilisez des versions différentes.
```

---

### 5. Corps du tutoriel — structure en étapes numérotées

Chaque étape suit ce schéma :

```markdown
## Étape [N] : [Titre de l'étape — action claire, pas "Configuration"]

**Objectif de cette étape :** [1 phrase sur ce qu'on accomplit ici.]

### Contexte

[2–3 lignes expliquant POURQUOI on fait cette étape avant de montrer COMMENT.
Relier au contexte métier marocain établi en accroche.]

### Code

[Toujours précéder le code d'un commentaire de contexte.
Commenter chaque décision non évidente dans le code.]

```python
# Contexte : [entreprise fictive] — [ce que ce code fait dans le projet]
# Données synthétiques marocaines — faker fr_FR + listes manuelles
from faker import Faker
fake = Faker('fr_FR')

PRENOMS = ['Youssef', 'Fatima', 'Amine', 'Nadia', 'Khalid', 'Zineb']
VILLES = ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir']

# [code commenté ligne par ligne pour les décisions non triviales]
```

### Ce que vous devez voir

[Description du résultat attendu — output console, screenshot décrit, fichier créé.]

> **Si ça ne marche pas :** [Solution à l'erreur la plus courante à cette étape.]
```

---

### 6. Données synthétiques — marocaines si pertinent, universelles sinon

Les données marocaines sont **recommandées** quand le tutoriel porte sur un cas d'usage métier marocain. Elles ne sont pas obligatoires pour un tutoriel purement technique ou universel.

**Utiliser des données marocaines si :**
- Le tutoriel porte sur un sujet business (fraude bancaire, e-commerce, supply chain)
- Le contexte marocain enrichit l'exemple sans être artificiel

**Utiliser des données universelles si :**
- Le tutoriel est technique pur (benchmark de librairies, déploiement infra, NLP multilingue)
- Forcer le contexte marocain alourdiraient inutilement la préparation

**Si données marocaines retenues :**

```python
from faker import Faker
import random, numpy as np

fake = Faker('fr_FR')  # fr_MA n'existe pas dans Faker
random.seed(42); np.random.seed(42)

PRENOMS = ['Youssef','Fatima','Amine','Nadia','Khalid','Zineb','Omar','Imane']
NOMS = ['Benali','Idrissi','Cherkaoui','Bennani','Tazi','Alami','Berrada']
VILLES = ['Casablanca','Rabat','Marrakech','Fès','Tanger','Agadir','Oujda']

def nom_marocain():
    return f"{random.choice(PRENOMS)} {random.choice(NOMS)}"
```

---

### 7. Section "Résultat et prochaines étapes"

```markdown
## Résultat final

[Description du ce qu'on a construit. Screenshot ou output décrit.
Résumer en 2–3 lignes ce que l'apprenant peut faire avec ça maintenant.]

## Pour aller plus loin

[3–4 extensions naturelles du tutoriel, avec liens vers ressources officielles.]

- [Extension 1] → [URL documentation officielle vérifiée]
- [Extension 2] → [URL]
- [Extension 3] → [URL]
```

---

### 8. Bloc méta SEO

```
---
## Méta SEO

**Titre SEO** : [max 60 caractères — "tutoriel" + outil + résultat]
**Meta description** : [max 155 caractères — ce qu'on construit + stack + niveau]
**Mot-clé principal** : [ex: "tutoriel RAG LangChain français"]
**Mots-clés secondaires** : [requêtes longue traîne liées]
**Slug URL** : /blog/tutoriel-[outil]-[résultat]
**Temps de lecture** : [X] min
**CTA recommandé** : [Formation ACT University correspondante]
**Code GitHub** : [lien repo ou note à créer]
---
```

---

## Règles absolues pour les tutoriels

1. **Tout code doit être exécutable** — tester avant de publier, sans exception
2. **Versions fixées** — ne jamais laisser `pip install langchain` sans version
3. **Données marocaines** — pas de "Alice bought a pizza", toujours un contexte local
4. **Erreurs courantes documentées** — anticiper les 2–3 problèmes les plus fréquents
5. **Environnement précisé** — Colab gratuit préféré pour l'accessibilité
6. **Pas de clés API en clair** — toujours `os.getenv()` ou variable Colab
7. **GitHub** — chaque tutoriel a un repo ou gist associé
