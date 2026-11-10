# ACT — Checklist de validation finale

À utiliser **avant de livrer** toute production marquée ACT, peu importe le support.
La checklist est organisée en 5 catégories : **identité**, **typographie**, **couleurs**,
**ton**, **livrable**.

Si un point n'est pas validé → corriger avant livraison. Si un point n'est pas applicable
au support, le marquer N/A et passer au suivant.

---

## A — Identité et signature

- [ ] Le **logo ACT** apparaît au moins une fois (sauf cas particulier : signature email texte simple, post LinkedIn texte sans visuel)
- [ ] Si logo présent : taille ≥ 32 px (écran) ou 12 mm (print) pour la version principale ; ≥ 20 px / 8 mm pour la compacte
- [ ] La **zone de protection** du logo est respectée (1× hauteur du losange en marge)
- [ ] Le **losange** est orienté à exactement −43,264° (pas 45°, pas droit)
- [ ] L'**ancrage géographique** « Casablanca · Rabat · Dakar » figure sur les supports marketing (site, post, livre blanc, plaquette, roll-up)
- [ ] La **baseline** « L'IA opérationnelle. Vraiment. » figure sur les supports d'image de marque

---

## B — Typographie

- [ ] Les titres sont en **Lora** (web/PDF) ou **Georgia** (Word/Office) — jamais Inter, Roboto, Arial ou autre
- [ ] Le corps est en **Poppins** (web/PDF) ou **Calibri** (Word/Office)
- [ ] Le code/data est en **JetBrains Mono** ou **Consolas**
- [ ] Les Google Fonts sont effectivement chargées sur les pages web (vérifier dans le navigateur)
- [ ] L'**italique orange** est appliqué sur 1 à 3 mots-clés des titres principaux (et seulement là)
- [ ] L'italique orange est en **Lora Italic** (jamais Poppins italique) couleur exact `#D35400`
- [ ] Les **eyebrows** (surtitres) sont en Poppins 11 pt SemiBold capitales avec letter-spacing 0,24em couleur Orange
- [ ] Aucun paragraphe n'est en capitales (réservé aux eyebrows et boutons courts)
- [ ] L'interlignage du body est ≥ 1,5 (web) ou ≥ 1,4 (print) pour le confort de lecture
- [ ] Les chiffres dans les tableaux/data utilisent `font-variant-numeric: tabular-nums`

---

## C — Couleurs

- [ ] Les couleurs respectent les **HEX exacts** :
  - Orange `#D35400` (pas `#D55400`, pas `#FF5400`)
  - Dark `#0A1410` (pas noir pur `#000000`)
  - Cream `#FCF9F2` (pas blanc pur `#FFFFFF` sauf cas spécifique signature email)
  - Green `#1B3022`, Gold `#F39C12`
- [ ] Le **ratio 60/30/10** est respecté : pas de section où l'orange occupe plus de 10 % de la surface
- [ ] L'**orange n'est jamais un aplat plein page**
- [ ] Le **contraste WCAG** est ≥ AA pour tout texte body (cf. `tokens.md` section WCAG)
- [ ] L'orange `#D35400` n'est **pas** utilisé sur du body text sur fond Dark (contraste insuffisant)
- [ ] Aucune couleur **bleu tech** générique n'est utilisée par paresse (si une couleur paraît "manquer", utiliser Gold ou Green)
- [ ] Les fonds Dark utilisent `#0A1410` (pas un noir pur, pas un gris foncé corporate)

---

## D — Système visuel

- [ ] Les **bullets** utilisent le losange `◆` orange (pas •, pas –, pas ›, pas ✓)
- [ ] Les **icônes**, si utilisées, sont en style **outline** (pas filled, pas duotone) — Lucide Icons recommandée
- [ ] Aucun cliché IA générique n'apparaît : cerveau stylisé, circuit imprimé, robot humanoïde, hologramme bleu, ondes cosmiques
- [ ] Les **photos**, si présentes, ont été légèrement désaturées et chaud-balanced (cf. `visual-system.md` section 5)
- [ ] Les **graphiques** utilisent la palette ACT (Orange + Gold + Dark + Cream + Muted) — pas d'arc-en-ciel, pas de palette pré-fab Excel
- [ ] Les **labels** des graphiques sont placés directement sur les courbes/barres quand possible (évite le va-et-vient légende)

---

## E — Ton et rédaction

- [ ] **Affirmer avant de nuancer** : aucune ouverture en « Il semblerait que », « Peut-être que », « On pourrait »
- [ ] **Concret avant abstrait** : chaque idée générale est suivie d'un exemple, d'un chiffre ou d'un cas
- [ ] **Vous avant nous** : ratio « vous »/« nous » ≥ 2:1 sur les supports commerciaux
- [ ] **Clarté avant élégance** : aucune phrase de plus de 30 mots sans découpage
- [ ] Aucun mot de la **liste bannie** n'apparaît : révolutionnaire, disruptif, game-changer, next-gen, solutions innovantes, synergies, leverage, scaler, etc.
- [ ] Les **anglicismes** non tolérés ont été traduits (meeting → réunion, deadline → échéance, etc.)
- [ ] Les **espaces insécables** sont placés correctement avant `;` `:` `!` `?` `»`, après `«`, et entre chiffre+unité
- [ ] Les **apostrophes typographiques** ` ' ` sont utilisées partout dans le texte (pas `'`)
- [ ] Les **tirets cadratins** `—` sont utilisés pour les incises ; les demi-cadratins `–` pour les intervalles
- [ ] Les **guillemets français** « … » sont utilisés (anglais " … " uniquement pour citations imbriquées)
- [ ] Les **formules d'ouverture/fermeture** (email) figurent dans la liste autorisée (cf. `voice-and-tone.md`)

---

## F — Livrable et nomenclature

- [ ] Le **nom du fichier** suit le pattern `ACT_[TYPE]_[SUJET]_[CLIENT-ou-INTERNE]_[YYYYMMDD]_[vXX].[ext]`
- [ ] Le code [TYPE] est correct : `DOC`, `PRES`, `VISU`, `CODE`, `CONTR`, `RAPP`
- [ ] La date est au format `YYYYMMDD` (ex : `20260428`, pas `28-04-26`)
- [ ] Le fichier final est dans le dossier de livraison correct (`/mnt/user-data/outputs/` pour les sorties Claude)
- [ ] Si **PDF** : la conversion préserve les couleurs et les caractères spéciaux (◆ notamment) — vérifier visuellement
- [ ] Si **HTML** : la page se charge correctement seule (Google Fonts présentes, CSS inline ou liés correctement)
- [ ] Si **Word** : le document s'ouvre sans avertissement de police manquante
- [ ] Si **PowerPoint** : tester le mode présentation sur un autre écran que celui de production (calibrage couleurs)
- [ ] La **version** est explicite (v01, v02…) — éviter v0, v1, final, FINAL, vrai-final

---

## G — Accessibilité (web & PDF)

- [ ] Le HTML utilise des **balises sémantiques** (`<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<footer>`)
- [ ] L'attribut `lang="fr"` est sur le `<html>`
- [ ] Toutes les **images** ont un `alt` descriptif (ou `alt=""` si purement décoratives)
- [ ] Les **liens icône-seule** ont un `aria-label`
- [ ] Le focus clavier est **visible** (pas de `outline: none` sans replacement)
- [ ] Les zones **cliquables mobile** ≥ 44 × 44 px
- [ ] `prefers-reduced-motion` est respecté pour les animations
- [ ] Le PDF a un **titre de document** renseigné (métadonnées)

---

## H — Cas particuliers à signaler

Si un de ces cas s'applique, **vérifier deux fois** plutôt qu'une :

- [ ] Production **destinée à un grand compte sensible** (banque, assurance, secteur public) : ton plus institutionnel, pas de baseline alt, vocabulaire conservateur
- [ ] Production **multilingue** (FR + AR + EN) : vérifier que la baseline et les eyebrows sont traduits ; le losange et les couleurs restent identiques
- [ ] Production **à fort enjeu visibilité** (livre blanc, post viral, page d'accueil) : passer par les 3 étapes de validation (brand → métier → direction)
- [ ] Production **avec partenaire** (co-branding) : vérifier que les deux logos respectent leur zone de protection mutuelle ; séparateur middle-dot ` · ` entre les deux
- [ ] Production **sensible juridiquement** (contrat, devis, CGV) : faire valider par le service juridique avant publication

---

## Process de validation en 3 étapes

Pour les productions publiques importantes (campagnes, prises de parole officielles, livres blancs) :

| Étape | Délai | Validateur | Sortie |
|---|---|---|---|
| 1 — Brand | 24 h ouvrées | Responsable marketing/brand | GO / GO avec remarques / NO GO |
| 2 — Métier | 48 h ouvrées | Expert·e du sujet | GO / corrections à intégrer |
| 3 — Direction | 48 h ouvrées | Direction générale | GO FINAL + autorisation de publication |

Pour les productions internes ou de routine (slide deck client, email standard, post LinkedIn standard) :
**étape 1 suffit**.
