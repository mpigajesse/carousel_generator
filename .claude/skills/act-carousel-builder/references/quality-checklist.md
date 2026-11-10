# Quality checklist — avant de livrer

À cocher mentalement avant d'écrire le fichier final et avant de rendre la main.

## Fond

- [ ] Le titre cover résume l'angle, pas juste le sujet
- [ ] Le hook (slide 2) répond à "pourquoi je devrais lire ça maintenant"
- [ ] Chaque chiffre cité a sa source dans la slide ou la slide finale
- [ ] Aucune affirmation n'est plus forte que ce que dit l'article source
- [ ] Les nuances de l'article ne sont pas écrasées par la condensation
- [ ] La conclusion mène à un takeaway concret, pas à une généralité

## Forme

- [ ] Front matter présent et valide (`series`, `author`, `title`)
- [ ] 6 à 12 slides exactement
- [ ] Première slide = `cover` avec ≤ 60 chars de titre
- [ ] Dernière slide = synthèse OU **question ouverte au lecteur** (engagement commentaire) — **jamais** de lien ni de hashtag
- [ ] **Aucun hashtag** (`#IA`, `#GenAI`, etc.) dans le body des slides — réservés aux captions LinkedIn/Instagram
- [ ] **Aucun lien ni domaine** (`a-ct.ma`, `blog`, URL externe) — le carrousel se suffit à lui-même
- [ ] Séparateurs `---` UNIQUEMENT entre slides (pas d'autre usage)
- [ ] Aucun `**`, `*`, `_`, `` ` `` Markdown dans les body — uniquement HTML inline
- [ ] Tous les body respectent les budgets de `budgets.md`
- [ ] Maximum 2 `<span class="hl*">` par slide
- [ ] Listes `<ul class="bullets">` : 3-5 items, ≤ 80 chars chacun
- [ ] Slides `compare` : exactement 2 colonnes, équilibrées en longueur
- [ ] Slides `stat` (IG) : max 3 stats, value ≤ 8 chars

## Compatibilité parser

- [ ] Le YAML front matter est sur les premières lignes (avant tout autre contenu)
- [ ] Pas de séparateur `---` à l'intérieur d'un body de slide
- [ ] Encodage UTF-8 (caractères français : é, à, ç, etc. corrects)
- [ ] Pas de tabulations dans les body — espaces uniquement
- [ ] Pas de balise HTML non supportée (pas de `<div>`, `<table>`, `<img>` dans le body)

## Cohérence thème

- [ ] Le thème suggéré existe dans `themes.py` (vérifié)
- [ ] La plateforme (LinkedIn / Instagram) est annoncée explicitement
- [ ] Si Instagram : exploitation des types `quote`/`stat` quand l'article s'y prête
- [ ] Si LinkedIn : pas de slide `quote`/`stat`/`cta` (non supportées)

## Livrable

- [ ] Fichier sauvegardé sous `<slug>.carousel.md` dans le **même dossier** que l'article source
- [ ] Résumé final affiché à l'utilisateur :
  - Nom du fichier produit
  - Nombre de slides
  - Plateforme
  - Thème suggéré
  - Commande / procédure d'import
- [ ] Si l'utilisateur a demandé YAML : fichier `<slug>.carousel.yaml` produit en complément

## Erreurs fréquentes à éviter

| Erreur | Symptôme | Correction |
|---|---|---|
| Markdown `**bold**` dans body | Affichage `**bold**` brut sur la slide | Utiliser `<span class="bold">bold</span>` |
| Plus de 380 chars dans content | Texte qui déborde | Scinder en 2 slides |
| Séparateur `---` dans une citation | Slide coupée en deux | Utiliser `—` ou `***` interne uniquement |
| 4+ surlignages sur une slide | Plus rien ne ressort | Garder max 2 |
| Stat avec value de 12 chars | Chiffre tronqué au rendu | Utiliser suffixes (M, K, %, ×) |
| Compare déséquilibré (50 vs 200 chars) | Colonnes asymétriques moches | Équilibrer ou condenser |
| Front matter mal formé (YAML invalide) | Footer vide | Vérifier que `---` ouvrant et fermant sont seuls sur leur ligne |
| Hashtags `#IA #LLM` dans une slide | Carrousel qui ressemble à un post brut, perte de premium | Retirer — les hashtags vont dans la **caption** du post, pas sur les visuels |
| Lien `a-ct.ma` ou domaine sur une slide | Renvoi externe qui dilue l'attention | Remplacer par une question ouverte au lecteur (commentaire) |
| Slide finale "Allez plus loin" + URL | CTA web faible (clic externe rare) | Slide finale = **question ouverte** ou choix binaire (déclenche commentaires) |
