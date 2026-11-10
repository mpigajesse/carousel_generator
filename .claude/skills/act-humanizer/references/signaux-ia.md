# Signaux IA — Référence de diagnostic

Liste complète des marqueurs qui trahissent un texte généré par IA.
Lire avant de traiter un texte. Cocher ceux qui sont présents pour cibler les transformations.

---

## Catégorie A — Signaux lexicaux (mots et expressions)

### A1. Mots-valises sans contenu

Ces mots sonnent importants mais ne disent rien de précis.
Présence de 2+ de ces mots dans un texte court = signal fort.

```
crucial · essentiel · fondamental · primordial · capital
innovant · révolutionnaire · disruptif · avant-gardiste
pertinent · approprié · adéquat · adapté
robuste · solide · fiable · pérenne
significatif · notable · considérable · substantiel
optimal · optimisé · efficace (sans comparatif)
holistique · global · intégré · transversal
paradigme · écosystème · synergie · valeur ajoutée
stratégique (sans préciser la stratégie)
challenges · enjeux (sans les nommer)
```

### A2. Formules d'intro et de transition IA

Ces formules annoncent ce que le texte va faire au lieu de le faire.

```
"Dans un monde où..."
"À l'ère du numérique / de l'IA..."
"De plus en plus..."
"Il est important de noter que..."
"Il convient de souligner que..."
"Force est de constater que..."
"Dans cette section, nous allons voir..."
"Comme nous l'avons vu précédemment..."
"Il convient maintenant d'aborder..."
"En ce qui concerne..."
"Dans le cadre de..."
"À cet égard..."
"En termes de..."
"Sur ce point..."
"Pour ce faire..."
"Cela étant dit..."
"Il va sans dire que..."
"Bien entendu..."
"Notons que..."
```

### A3. Formules de conclusion IA

```
"En conclusion, nous avons vu que..."
"Pour résumer les points clés abordés..."
"En somme, cet article a exploré..."
"À travers cette analyse, nous avons..."
"En définitive, il apparaît clairement que..."
"Pour conclure, retenons que..."
```

### A4. Hedging excessif (sur-précaution)

```
"Il semblerait que..."
"On pourrait penser que..."
"Certains pourraient arguer que..."
"Dans une certaine mesure..."
"Plus ou moins..."
"D'une certaine façon..."
"En quelque sorte..."
```

---

## Catégorie B — Signaux structurels

### B1. Listes à puces abusives

- Tout converti en listes, même ce qui est naturellement une phrase ou un argument
- Listes de 3 items exactement (pattern IA très fréquent)
- Listes sans hiérarchie ni logique entre les items
- Items de longueur presque identique

### B2. Symétrie mécanique

- Toutes les sections font la même longueur
- Toutes les phrases ont la même structure syntaxique
- Même nombre de sous-points dans chaque partie
- Rythme parfaitement régulier sans aucune rupture

### B3. Exhaustivité forcée

- L'article couvre "tous les angles" sans prioriser
- Chaque pour a un contre, chaque avantage a un inconvénient — mécaniquement
- Aucun point de vue assumé — pure présentation des "différentes perspectives"

### B4. Titres de sections vides

```
"Introduction"
"Contexte"
"Analyse"
"Discussion"
"Conclusion"
"Les avantages"
"Les limites"
"Perspectives"
```
Ces titres ne disent rien sur le contenu — un titre humain dit ce que la section apporte.

---

## Catégorie C — Signaux rhétoriques

### C1. Absence de voix

- On ne peut pas identifier qui parle
- Aucun "je pense que", "notre expérience montre", "ce qui me frappe"
- Aucune anecdote, aucun exemple personnel
- Tout est présenté de façon neutre et omnisciente

### C2. Questions rhétoriques factices

```
"Mais qu'est-ce que cela signifie vraiment ?"
"Comment alors aborder cette problématique ?"
"Quelles sont les implications pour les entreprises ?"
```
Posées, mais jamais vraiment répondues avec une position.

### C3. Fausse modestie et fausse ouverture

```
"Il n'y a pas de réponse universelle..."
"Chaque situation est unique..."
"Tout dépend du contexte..."
```
Utilisé pour éviter de prendre position plutôt que pour nuancer honnêtement.

### C4. Accumulation sans crescendo

L'IA accumule des arguments de même poids. Un texte humain construit une progression
— les arguments montent en puissance ou en spécificité.

---

## Catégorie D — Signaux de fluidité

### D1. Répétitions de début de phrase

Plusieurs phrases consécutives qui commencent par le même mot ou la même structure.
Souvent : "Cette approche...", "Cette méthode...", "Cette solution..."

### D2. Longueur de phrase uniforme

Toutes les phrases font entre 15 et 25 mots. Aucune phrase de 4 mots. Aucune de 40.

### D3. Absence de ponctuation expressive

Pas de tirets longs (—), pas de deux-points introduisant une surprise, pas de points
d'exclamation, très rares points de suspension. Ponctuation strictement grammaticale.

### D4. Transitions trop lisses

Chaque paragraphe enchaîne trop proprement sur le précédent. Les textes humains ont
parfois des ruptures délibérées, des changements brusques de sujet, des apartés.

---

## Échelle de diagnostic rapide

Compter les signaux présents dans le texte :

| Nombre de signaux | Diagnostic | Action |
|---|---|---|
| 0–2 | Texte déjà naturel | Interventions légères seulement |
| 3–5 | Texte modérément IA | Appliquer T1, T2 et T5 en priorité |
| 6–9 | Texte fortement IA | Appliquer T1 à T5 systématiquement |
| 10+ | Texte entièrement IA | Réécriture profonde — garder le fond, refaire la forme |
