# _PUSH.md — Workflow de déploiement multi-remote
> Fichier interne. Ne pas inclure dans la documentation publique.

## Remotes configurés

| Alias | Destination | Branche |
|-------|-------------|---------|
| `origin` | `github.com/mpigajesse/carousel_generator` | `main` |
| `act` | `github.com/Africa-centred-technology/carousel_generator_officiel` | `main` |
| `hf` | `huggingface.co/spaces/mpigajesse23/carousel-generator` | `main` |

---

## Commandes rapides

### Push vers les deux GitHub (origin + act)
```bash
bash push-all.sh
```

### Push manuel step by step
```bash
# 1. S'assurer que tout est commité
git status

# 2. Push origin (repo personnel)
git push origin main

# 3. Push act (Africa-centred-technology)
git push act main
```

### Push vers Hugging Face uniquement
```bash
git push hf main
```

### Push vers tous les remotes (origin + act + hf)
```bash
git push origin main && git push act main && git push hf main
```

---

## Workflow commit → push complet

```bash
# 1. Ajouter les fichiers modifiés
git add app.py generate.py md_parser.py themes.py
git add slide.html.j2 slide_instagram.html.j2
git add templates/index.html

# 2. Créer le commit (conventional commits)
git commit -m "feat: description courte de la fonctionnalité"

# 3. Push sur les deux GitHub
bash push-all.sh
```

### Types de commits conventionnels
| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `refactor` | Refactoring sans changement de comportement |
| `style` | CSS, design, UI |
| `docs` | Documentation |
| `chore` | Config, dépendances, scripts |
| `perf` | Optimisation de performances |

---

## Vérifier l'état des remotes

```bash
# Lister tous les remotes
git remote -v

# Voir l'historique des pushs
git log --oneline --decorate -10

# Vérifier les branches locales vs remotes
git branch -vv
```

---

## Ajouter un nouveau remote

```bash
git remote add <alias> https://<TOKEN>@github.com/<org>/<repo>.git
git push <alias> main
```

---

## Résolution de conflits entre remotes

Si un remote a des commits que l'autre n'a pas :
```bash
# Forcer la mise à jour d'un remote secondaire pour qu'il suive origin
git push act main --force-with-lease
```

> **Note** : `--force-with-lease` est plus sûr que `--force` — il échoue si quelqu'un d'autre a poussé entre-temps.

---

## Token et sécurité

- Les tokens sont stockés dans `.git/config` via l'URL du remote (ajoutés par `git remote add`)
- **Ne jamais commiter** de token dans un fichier source
- Si un token est exposé : le révoquer immédiatement sur GitHub → Settings → Developer settings → Personal access tokens
- Pour renouveler le token du remote `act` :
  ```bash
  git remote set-url act https://<NOUVEAU_TOKEN>@github.com/Africa-centred-technology/carousel_generator_officiel.git
  ```
