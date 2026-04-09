# 🚀 Guide de Déploiement - Carousel Generator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DÉPLOIEMENT SUR HUGGING FACE SPACES (RECOMMANDÉ)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Étape 1 : Créer un compte Hugging Face

1. Aller sur https://huggingface.co
2. Cliquer sur **Sign Up** (gratuit)
3. Créer un compte avec email ou GitHub
4. Vérifier l'email

## Étape 2 : Créer une organisation (optionnel)

Pour un usage entreprise :

1. Cliquer sur ton avatar → **New Organization**
2. Nommer l'organisation (ex: `mon-entreprise`)
3. Choisir le plan **Free**
4. Inviter les membres de l'équipe

## Étape 3 : Créer un Space

1. Aller sur https://huggingface.co/new-space
2. Configurer :
   - **Space name**: `carousel-generator`
   - **License**: `MIT` (open source)
   - **Visibility**: `Public` ou `Private` (selon besoin)
   - **SDK**: `Docker`
   - **Owner**: Ton compte ou l'organisation

3. Cliquer sur **Create Space**

## Étape 4 : Préparer le code

```bash
# Cloner le Space
git clone https://huggingface.co/spaces/TON_COMPTE/carousel-generator
cd carousel-generator

# Copier les fichiers du projet
cp -r D:/Generator/carousel_generator/* .

# Vérifier les fichiers essentiels
ls -la
# Doit contenir:
#   Dockerfile
#   app.py
#   generate.py
#   themes.py
#   md_parser.py
#   slide.html.j2
#   requirements.txt
#   templates/
#   static/
```

## Étape 5 : Pousser le code

```bash
# Ajouter tous les fichiers
git add .

# Commit
git commit -m "🚀 Initial deployment - Carousel Generator"

# Pousser vers Hugging Face
git push
```

## Étape 6 : Vérifier le déploiement

1. Aller sur la page du Space
2. L'onglet **App** montre le statut du build
3. Attendre que le build se termine (~2-5 minutes)
4. L'app est accessible à l'URL :
   ```
   https://huggingface.co/spaces/TON_COMPTE/carousel-generator
   ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TEST LOCAL AVEC DOCKER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Prérequis

- Docker Desktop installé : https://www.docker.com/products/docker-desktop

## Build et run

```bash
# Se placer dans le dossier du projet
cd D:\Generator\carousel_generator

# Build l'image
docker build -t carousel-generator .

# Run le conteneur
docker run -p 7860:7860 carousel-generator

# Accéder à l'app
# Ouvrir: http://localhost:7860
```

## Arrêter le conteneur

```bash
# Lister les conteneurs
docker ps

# Arrêter
docker stop <container_id>
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONFIGURATION AVANCÉE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Variables d'environnement

Le Dockerfile définit déjà :
```env
PORT=7860
FLASK_APP=app.py
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=7860
```

## Augmenter le stockage

Hugging Face Spaces offre 10GB gratuit. Pour augmenter :

1. Aller dans les **Settings** du Space
2. Section **Storage**
3. Activer **Persistent Storage**

## Authentification

Pour restreindre l'accès :

1. Aller dans **Settings** du Space
2. Section **Access**
3. Choisir :
   - **Public** : Tout le monde peut accéder
   - **Private** : Seuls les membres autorisés

## Monitoring

- Onglet **Logs** du Space : Voir les logs en temps réel
- Onglet **Metrics** : CPU, RAM, usage disque

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ALTERNATIVE : RENDER.COM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Étape 1 : Créer un compte

1. Aller sur https://render.com
2. Sign up avec GitHub

## Étape 2 : Créer un Web Service

1. Cliquer sur **New +** → **Web Service**
2. Connecter le repository GitHub
3. Configurer :
   - **Name**: `carousel-generator`
   - **Region**: `Frankfurt` (plus proche de l'Europe)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `python app.py`

4. Cliquer sur **Create Web Service**

## Étape 3 : Attendre le déploiement

- Le build prend ~5 minutes
- L'URL sera : `https://carousel-generator.onrender.com`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ALTERNATIVE : AUTO-HÉBERGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Prérequis

- Serveur Linux (Ubuntu 22.04 recommandé)
- Docker et Docker Compose installés
- Nom de domaine (optionnel)

## Étape 1 : Cloner le projet

```bash
git clone https://github.com/ton-compte/carousel-generator.git
cd carousel-generator
```

## Étape 2 : Créer docker-compose.yml

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

volumes:
  generated_data:
```

## Étape 3 : Démarrer

```bash
docker-compose up -d
```

## Étape 4 : Accéder à l'app

```
http://IP_DU_SERVEUR:5000
```

## Étape 5 : Ajouter HTTPS (optionnel)

### Avec Nginx + Let's Encrypt

```bash
# Installer Nginx
sudo apt install nginx

# Configurer le reverse proxy
sudo nano /etc/nginx/sites-available/carousel-generator
```

```nginx
server {
    listen 80;
    server_name carousel.mon-entreprise.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/carousel-generator /etc/nginx/sites-enabled/

# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Générer le certificat SSL
sudo certbot --nginx -d carousel.mon-entreprise.com
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PARTAGER L'APP À L'ENTREPRISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Email d'annonce aux équipes

```
Subject: 🚀 Nouveau : Générateur de Carrousels Instagram

Bonjour à tous,

Un nouvel outil est disponible pour créer des carrousels Instagram 
professionnels en quelques clics !

🔗 Accès : https://huggingface.co/spaces/TON_COMPTE/carousel-generator

✨ Fonctionnalités :
  • Import de fichiers Markdown (.md)
  • 19 thèmes professionnels
  • Génération PNG et PDF
  • Mode présentation plein écran
  • Texte auto-adaptatif

📖 Guide d'utilisation : [Lien vers la doc]

Pour toute question, contactez [ton-email].

Bonne création !
```

## Session de formation

1. **Durée** : 30 minutes
2. **Contenu** :
   - Démonstration live
   - Import d'un fichier Markdown
   - Choix du thème
   - Génération et téléchargement
3. **Support** : Enregistrer une vidéo tutoriel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MAINTENANCE ET MISES À JOUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Mettre à jour l'app

```bash
# Pull les derniers changements
git pull origin main

# Pousser vers Hugging Face
git push huggingface main

# Le rebuild est automatique !
```

## Nettoyer les anciennes générations

```bash
# Supprimer les fichiers de +30 jours
find static/generated -type f -mtime +30 -delete
```

## Surveiller l'usage

- Onglet **Logs** du Space
- Section **Storage** pour l'espace utilisé
- **Settings** → **Factory Rebuild** si problème

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DÉPANNAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Le build échoue

```bash
# Vérifier les logs
docker build -t carousel-generator . 2>&1 | tee build.log

# Erreurs courantes :
# - requirements.txt manquant
# - Dockerfile mal configuré
# - Playwright non installé
```

## L'app ne démarre pas

```bash
# Tester en local
docker run -p 7860:7860 carousel-generator

# Vérifier les logs
docker logs <container_id>
```

## Playwright ne trouve pas Chromium

```bash
# Rebuild avec les bonnes dépendances
docker build --no-cache -t carousel-generator .
```

## L'espace disque est plein

```bash
# Nettoyer Docker
docker system prune -a

# Supprimer les anciennes générations
rm -rf static/generated/*
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CONTACT ET SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- **Développeur** : [Ton nom]
- **Email** : [ton-email]
- **Repository** : https://github.com/ton-compte/carousel-generator
- **Documentation** : [Lien vers la doc]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
