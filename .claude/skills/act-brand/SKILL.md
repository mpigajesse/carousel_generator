---
name: act-brand
description: >
  Charte graphique et règles de marque officielles d'ACT — Africa Centred Technology.
  Déclencher dès qu'une production touche à l'identité visuelle ou éditoriale d'ACT :
  écrire un email, un post LinkedIn, un article, un livre blanc, une proposition commerciale,
  une présentation, une bannière, une page web, un mockup, un visuel, une signature,
  un template, une newsletter, une carte de visite, un goodies, ou tout document signé ACT.
  Ce skill fournit les couleurs exactes, les typographies, l'élément signature (losange),
  les règles de ton, le vocabulaire à privilégier ou bannir, les patterns visuels et
  les recettes prêtes à l'emploi pour HTML, Word, PowerPoint et PDF. À utiliser même
  si le mot "charte" n'est pas mentionné — toute production estampillée ACT doit la respecter.
---

# ACT Brand — Charte graphique opérationnelle

Ce skill est la source de vérité pour toute production estampillée **ACT — Africa Centred Technology**.
Il garantit la cohérence visuelle et éditoriale, peu importe le support (web, print, bureautique,
réseaux sociaux, vidéo).

**ACT en bref** — Conseil, ingénierie & formation en Intelligence Artificielle.
Implanté à Casablanca, Rabat et Dakar. Ton : expert, rigoureux, ancré, moderne, chaleureux.
Baseline officielle : *« L'IA opérationnelle. Vraiment. »*

---

## Étape 0 — Identifier le type de production

Avant toute chose, classifier la demande dans une des branches ci-dessous, puis lire **uniquement**
la (ou les) référence(s) concernée(s). Ne pas tout charger d'un coup.

| Type de production | Référence à lire | Asset à utiliser |
|---|---|---|
| **Page web, landing, mockup HTML, post LinkedIn statique en HTML, banner, prototype** | `references/web-recipes.md` | `assets/act-tokens.css` |
| **Document Word, PDF, contrat, rapport, livre blanc, proposition commerciale** | `references/docx-recipes.md` | tokens issus de `assets/act-tokens.json` |
| **Présentation PowerPoint, slide deck, pitch, formation** | `references/pptx-recipes.md` | tokens issus de `assets/act-tokens.json` |
| **Email, post LinkedIn texte, newsletter texte, script vidéo, accroche, baseline** | `references/voice-and-tone.md` | — |
| **Visuel marketing (carte de visite, signature, livre blanc cover, roll-up, goodies)** | `references/application-templates.md` | — |
| **Question sur un détail (couleur exacte, taille de logo, ratio WCAG, etc.)** | `references/tokens.md` | `assets/act-tokens.json` |
| **Système graphique (losange, patterns, photo, data viz, icônes)** | `references/visual-system.md` | — |

Si la demande couvre plusieurs types (ex : "rédige un livre blanc" = ton + structure docx + couverture visuelle),
charger les références concernées dans l'ordre : ton → structure → visuel.

---

## Règles immuables (à appliquer dans 100 % des cas)

Ces dix règles sont non négociables, peu importe le support. Toutes les autres règles sont dans les
fichiers de référence ; celles-ci doivent être en mémoire en permanence.

1. **Trois couleurs centrales :** Orange `#D35400` (signe), Dark `#0A1410` (fond digital), Cream `#FCF9F2` (fond clair). Le reste est secondaire.
2. **Deux typographies :** Lora pour les titres et l'italique signature, Poppins pour le corps. JetBrains Mono pour le code/données. Jamais d'autres polices.
3. **Le losange est notre ponctuation visuelle.** Carré tourné de **−43,264°** (angle exact). Couleur Orange par défaut. Utilisé en bullet, séparateur, signature, favicon.
4. **L'italique orange est notre signature typographique.** 1 à 3 mots-clés par titre maximum, en italique Lora couleur Orange. C'est la marque. *Exemple : « L'IA opérationnelle. **Vraiment.** »*
5. **Ratio 60/30/10.** 60 % dominante (Dark ou Cream), 30 % secondaire (Green + gris), 10 % accent (Orange + Gold). L'orange n'est **JAMAIS** un aplat plein page.
6. **WCAG AA minimum.** Contraste texte/fond ≥ 4,5:1 pour le body, ≥ 3:1 pour le texte large. Vérifier chaque combinaison.
7. **Pas de bleu tech générique.** Pas de cerveau stylisé, de circuit imprimé, de robot humanoïde, d'hologramme. Notre univers est terre + signal, pas Silicon Valley 2015.
8. **Affirmer avant de nuancer. Le concret avant l'abstrait. Le « vous » avant le « nous ». La clarté avant l'élégance.** Quatre règles qui résument tout le ton ACT.
9. **Ancrage géographique systématique** sur les supports marketing : *Casablanca · Rabat · Dakar*. Séparateur middle-dot.
10. **Nomenclature des fichiers livrables :** `ACT_[TYPE]_[SUJET]_[CLIENT-ou-INTERNE]_[YYYYMMDD]_[vXX].[ext]`. Toujours.

---

## Workflow standard

### A — Production web (HTML, mockup, landing, post visuel)

1. Lire `references/web-recipes.md` en entier
2. Inclure `assets/act-tokens.css` dans le fichier (ou inliner ses variables CSS dans le `<style>`)
3. Importer Google Fonts (Lora + Poppins, JetBrains Mono si code) dans le `<head>`
4. Construire la page en utilisant les classes `.act-*` et les variables `--act-*`
5. Appliquer la **checklist de validation** finale (`references/checklist.md`)

### B — Document Word ou PDF

1. Lire `references/docx-recipes.md` pour les patterns python-docx
2. Lire aussi `/mnt/skills/public/docx/SKILL.md` pour la création technique du fichier
3. Reprendre les helpers Python du référentiel docx (paragraphes, tables, en-têtes/pieds)
4. Appliquer les couleurs/polices ACT via les helpers fournis dans `docx-recipes.md`
5. Sortie : fichier nommé selon la nomenclature ACT, dans `/mnt/user-data/outputs/`

### C — Présentation PowerPoint

1. Lire `references/pptx-recipes.md` pour les patterns de slide
2. Lire aussi `/mnt/skills/public/pptx/SKILL.md` pour la création technique
3. Trois types de slides : couverture (Dark + grain), contenu (Cream ou Dark), transition (Green pleine page)
4. Toujours laisser ≥ 30 % de blanc — ne pas surcharger

### D — Production éditoriale pure (texte sans visuel)

1. Lire `references/voice-and-tone.md` en entier
2. Identifier les 4 règles du ton, le vocabulaire à privilégier, les bannis
3. Produire le texte en respectant les formules d'ouverture/fermeture officielles
4. Vérifier : aucun mot banni ? italique orange placé sur 1-3 mots-clés des titres ?

---

## Quand demander avant de produire

Demander confirmation à l'utilisateur **uniquement** si :

- Le destinataire ou le contexte n'est pas clair (interne ? externe ? grand compte ? étudiant ?)
- Le ton attendu est ambigu (formel client ? chaleureux candidat ? institutionnel investisseur ?)
- La langue n'est pas évidente (français par défaut, mais l'anglais/arabe sont possibles selon le contexte)
- Une couleur ou un comportement non standard est demandé (vérifier d'abord si la charte couvre déjà le cas)

Sinon, produire directement en appliquant la charte par défaut.

---

## Anti-patterns courants (à éviter activement)

- **Le bleu corporate.** Si l'orange paraît "trop fort" et qu'on est tenté de retomber sur du bleu, c'est un signal d'alerte. La charte assume cette différenciation.
- **L'italique orange placé partout.** Maximum 1–3 mots par titre. Si tout est en italique, plus rien n'est en italique.
- **Les puces classiques (•, –, *).** Le losange est notre puce. Tous les bullets passent par lui.
- **Les fonts système par défaut.** Si on génère un mockup web sans les Google Fonts, on perd 50 % de l'identité. Toujours importer Lora + Poppins.
- **Les emojis dans les titres.** Le losange `◆` est le seul "emoji" autorisé en signature.
- **L'anglicisme gratuit.** Si un mot français existe et est aussi clair, le préférer. Liste des tolérés/bannis dans `references/voice-and-tone.md`.
- **L'aplat orange plein page.** L'orange signe, il ne couvre pas. Maximum 10 % de la surface visible.

---

## Référence rapide (à mémoriser)

```
COULEURS    Orange #D35400 · Dark #0A1410 · Cream #FCF9F2 · Green #1B3022 · Gold #F39C12
TYPOS       Lora (titres + italiques) · Poppins (body) · JetBrains Mono (code)
LOSANGE     Carré tourné de -43.264° · Orange par défaut
SIGNATURE   « L'IA opérationnelle. Vraiment. »
ANCRAGE     Casablanca · Rabat · Dakar
FICHIER     ACT_[TYPE]_[SUJET]_[CLIENT]_[YYYYMMDD]_[vXX].[ext]
```

Pour le détail technique de chaque token, voir `references/tokens.md` et `assets/act-tokens.json`.
