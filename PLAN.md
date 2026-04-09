# 🚀 Plan de Déploiement Production - Carousel Generator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONTEXTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Application : Carousel Generator (Flask + Playwright)
Objectif    : Rendre l'outil accessible à toute l'entreprise via le web
Contrainte  : 100% open source, hébergé sur GitHub
Public      : Employés de l'entreprise (usage interne)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ARCHITECTURE ACTUELLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```
carousel_generator/
├── app.py                 # Application Flask
├── generate.py            # Script de génération
├── themes.py              # 19 thèmes premium
├── md_parser.py           # Parseur Markdown intelligent
├── slide.html.j2          # Template Jinja2
├── templates/
│   └── index.html         # Interface web
└── static/
    └── generated/         # Sorties générées
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPTIONS DE DÉPLOIEMENT OPEN SOURCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Option 1 : Hugging Face Spaces ⭐ RECOMMANDÉ

**Coût : GRATUIT**
**Stack : Docker + Flask + Playwright**

### Pourquoi Hugging Face Spaces ?
- ✅ 100% gratuit (CPU basique : 2 vCPU, 16GB RAM)
- ✅ Supporte Docker nativement
- ✅ HTTPS automatique
- ✅ URL publique : `https://huggingface.co/spaces/ton-org/carousel-generator`
- ✅ Accès contrôlable (public ou privé)
- ✅ Persistance des fichiers (10GB gratuit)
- ✅ Authentification HF possible
- ✅ Backed by GPU si besoin futur

### Prérequis
```
• Compte Hugging Face (gratuit)
• Organisation entreprise sur HF
• Docker Desktop installé
```

### Structure du projet
```
carousel_generator/
├── app.py
├── Dockerfile              ← Nouveau
├── requirements.txt
└── ...
```

### Dockerfile
```dockerfile
FROM python:3.12-slim

# Dépendances système pour Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer Playwright
RUN playwright install chromium

# Copier le code
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p static/generated

EXPOSE 7860

CMD ["python", "app.py"]
```

### Déploiement
```bash
# 1. Créer le Space sur Hugging Face
#    → https://huggingface.co/new-space
#    → SDK: Docker
#    → Public ou Private

# 2. Pousser le code
git clone https://huggingface.co/spaces/ton-org/carousel-generator
cd carousel-generator
cp -r ../carousel_generator/* .
git add .
git commit -m "Deploy carousel generator"
git push

# 3. L'app est en ligne ! 🎉
#    URL: https://huggingface.co/spaces/ton-org/carousel-generator
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Option 2 : GitHub Pages + GitHub Actions + Serverless

**Coût : GRATUIT**
**Stack : GitHub Pages (frontend) + GitHub Actions (backend)**

### Architecture
```
Utilisateur → GitHub Pages (HTML/JS)
                  ↓
            GitHub Actions API (Python/Flask)
                  ↓
            Generation des slides
                  ↓
            Retour des fichiers
```

### Limitation
- ⚠️ GitHub Pages = statique uniquement (pas de Flask)
- ⚠️ Nécessite une API externe ou serverless

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Option 3 : Render.com

**Coût : GRATUIT (Free Tier)**
**Stack : Python + Flask**

### Avantages
- ✅ Déploiement direct depuis GitHub
- ✅ HTTPS automatique
- ✅ URL: `https://carousel-generator.onrender.com`
- ✅ Base de données PostgreSQL gratuite (si besoin)

### Inconvénients
- ⚠️ Mise en veille après 15 min d'inactivité
- ⚠️ 512MB RAM max (suffisant pour notre usage)
- ⚠️ 750 heures/mois gratuites

### Fichier nécessaire : `render.yaml`
```yaml
services:
  - type: web
    name: carousel-generator
    env: python
    buildCommand: pip install -r requirements.txt && playwright install chromium
    startCommand: python app.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Option 4 : Auto-hébergement sur serveur entreprise

**Coût : Serveur interne**
**Stack : Docker + Nginx + Gunicorn + Flask**

### Architecture professionnelle
```
Internet → Nginx (reverse proxy)
              ↓
         Gunicorn (WSGI server)
              ↓
            Flask App
              ↓
         Playwright (generation)
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:7860"
    environment:
      - FLASK_ENV=production
    volumes:
      - generated_data:/app/static/generated
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  generated_data:
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RECOMMANDATION FINALE : HUGGING FACE SPACES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Pourquoi Hugging Face Spaces ?

| Critère | Hugging Face | Render | GitHub Pages | Auto-hébergé |
|---------|-------------|--------|-------------|-------------|
| **Coût** | ✅ Gratuit | ✅ Gratuit | ✅ Gratuit | 💰 Serveur requis |
| **Facilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **HTTPS** | ✅ Inclus | ✅ Inclus | ✅ Inclus | 🔧 À configurer |
| **Playwright** | ✅ Supporté | ⚠️ Limité | ❌ Non | ✅ Oui |
| **Persistance** | ✅ 10GB | ⚠️ Éphémère | ❌ Non | ✅ Illimité |
| **Authentification** | ✅ HF OAuth | ❌ Non | ❌ Non | 🔧 À faire |
| **Accès entreprise** | ✅ Public/Privé | ✅ Public | ✅ Public | 🔧 Interne |
| **Monitoring** | ✅ Dashboard | ✅ Dashboard | ❌ Non | 🔧 À faire |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PLAN D'ACTION ÉTAPE PAR ÉTAPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Phase 1 : Préparation (30 min)
- [ ] Créer un compte Hugging Face
- [ ] Créer une organisation entreprise (ex: `@mon-entreprise`)
- [ ] Créer un nouveau Space (SDK: Docker)
- [ ] Ajouter le `Dockerfile` au projet

### Phase 2 : Déploiement (15 min)
- [ ] Cloner le repository du Space
- [ ] Copier le code du carousel generator
- [ ] Commit et push
- [ ] Vérifier le build sur HF
- [ ] Tester l'application en ligne

### Phase 3 : Configuration (20 min)
- [ ] Configurer l'accès (public ou privé)
- [ ] Ajouter les membres de l'entreprise
- [ ] Tester la génération de slides
- [ ] Vérifier le téléchargement des fichiers

### Phase 4 : Documentation (30 min)
- [ ] Créer un README.md pour l'entreprise
- [ ] Rédiger un guide d'utilisation
- [ ] Partager le lien aux équipes
- [ ] Former les utilisateurs clés

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FICHIERS À CRÉER POUR LE DÉPLOIEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```
carousel_generator/
├── Dockerfile                    ← Nouveau (obligatoire)
├── .dockerignore                 ← Nouveau (recommandé)
├── render.yaml                   ← Optionnel (si Render)
├── docker-compose.yml            ← Optionnel (si auto-hébergé)
├── nginx.conf                    ← Optionnel (si auto-hébergé)
├── DEPLOYMENT_GUIDE.md          ← Nouveau (documentation)
└── (fichiers existants...)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COÛT TOTAL ESTIMÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Service | Coût mensuel |
|---------|-------------|
| Hugging Face Spaces | **0€** |
| GitHub (code source) | **0€** |
| Authentification entreprise | **0€** |
| Stockage (10GB) | **0€** |
| **TOTAL** | **0€ / mois** 🎉 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROCHAINES ÉTAPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **Valider cette proposition** → Dis-moi si ça te convient
2. **Créer le Dockerfile** → Je peux le générer automatiquement
3. **Créer le Space HF** → Tu crées le compte, je pousse le code
4. **Tester en production** → On vérifie que tout fonctionne
5. **Former l'équipe** → Documentation + session de formation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ALTERNATIVES SI BESOIN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si l'entreprise a des contraintes spécifiques :

- **Azure Static Web Apps** → Si l'entreprise utilise déjà Azure
- **AWS Amplify** → Si l'entreprise est sur AWS
- **Google Cloud Run** → Si l'entreprise utilise GCP
- **Koyeb** → Alternative à Render (gratuit)
- **Fly.io** → 3 VMs gratuites, bon pour la prod

Mais **Hugging Face Spaces** reste le meilleur choix pour :
- Simplicité de déploiement
- Support natif de Playwright
- Gratuité totale
- Pas de carte bancaire requise

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PRÊT À DÉPLOYER ? 🚀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dis-moi quelle option tu préfères et je prépare tous les fichiers nécessaires !
