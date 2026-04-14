# Guide de déploiement — Carousel Generator
## Serveur Ubuntu 24 LTS

> **À qui s'adresse ce document**
> Ce guide est destiné à l'administrateur du serveur local Ubuntu.
> Le pipeline CI/CD côté GitHub est déjà configuré par l'équipe dev.
> Ton rôle : préparer le serveur, installer le runner GitHub Actions,
> et lancer l'application. Après ça, chaque push de l'équipe déploie automatiquement.

---

## Prérequis serveur

- Ubuntu Server 24.04 LTS
- Accès `sudo`
- Connexion internet sortante (GitHub, Docker Hub)
- Minimum recommandé : **2 vCPU / 4 GB RAM / 20 GB disque**

---

## Étape 1 — Installer Docker

```bash
# Mettre à jour le système
sudo apt-get update && sudo apt-get upgrade -y

# Installer les dépendances
sudo apt-get install -y ca-certificates curl gnupg

# Ajouter la clé GPG officielle Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Ajouter le dépôt Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker Engine + Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# Vérifier l'installation
docker --version
docker compose version
```

```bash
# Autoriser ton utilisateur à lancer Docker sans sudo
sudo usermod -aG docker $USER
newgrp docker

# Tester
docker run --rm hello-world
```

---

## Étape 2 — Cloner le projet

```bash
# Créer le dossier de l'application
sudo mkdir -p /opt/carousel_generator
sudo chown $USER:$USER /opt/carousel_generator

# Cloner depuis GitHub
git clone https://github.com/mpigajesse/carousel_generator.git \
  /opt/carousel_generator

cd /opt/carousel_generator
```

---

## Étape 3 — Configurer les secrets (.env)

```bash
# Copier le modèle
cp .env.example .env

# Éditer avec les vraies valeurs
nano .env
```

Le fichier `.env` doit contenir :

```ini
# Mot de passe d'accès à l'application (choisir quelque chose de fort)
APP_PASSWORD=VotreMotDePasseSecretIci

# Clé de session Flask — générer avec la commande ci-dessous
SECRET_KEY=coller_la_valeur_generee_ici
```

**Générer une SECRET_KEY solide :**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copier la valeur affichée dans le .env
```

> ⚠️ Ne jamais partager ce fichier `.env`. Il ne doit pas être commité sur GitHub.

---

## Étape 4 — Premier lancement (test manuel)

```bash
cd /opt/carousel_generator

# Build de l'image Docker et démarrage
docker compose up -d --build

# Suivre les logs du démarrage (Ctrl+C pour quitter les logs)
docker compose logs -f carousel
```

**Vérifier que l'application est opérationnelle :**
```bash
# Attendre ~30 secondes, puis tester
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/login
# Doit afficher : 200
```

Ouvrir dans le navigateur : **http://IP_DU_SERVEUR:5000**

---

## Étape 5 — Installer le runner GitHub Actions

Le runner permet aux déploiements automatiques de s'exécuter sur ce serveur
quand l'équipe dev pousse du code sur GitHub.

### 5a. Créer le dossier du runner

```bash
sudo mkdir -p /opt/actions-runner
sudo chown $USER:$USER /opt/actions-runner
cd /opt/actions-runner
```

### 5b. Récupérer le token d'installation

Sur GitHub :
1. Aller sur `https://github.com/mpigajesse/carousel_generator`
2. **Settings** → **Actions** → **Runners** → **New self-hosted runner**
3. Sélectionner **Linux** / **x64**
4. Copier et exécuter les commandes affichées (download + configure)

Les commandes ressemblent à :
```bash
# Télécharger le runner (la version exacte est affichée sur GitHub)
curl -o actions-runner-linux-x64.tar.gz -L \
  https://github.com/actions/runner/releases/download/vX.X.X/actions-runner-linux-x64-X.X.X.tar.gz

tar xzf actions-runner-linux-x64.tar.gz

# Configurer (coller la commande complète depuis GitHub — elle contient le token)
./config.sh --url https://github.com/mpigajesse/carousel_generator \
            --token VOTRE_TOKEN_GITHUB \
            --name ubuntu-local \
            --labels self-hosted,linux,ubuntu \
            --work /opt/actions-runner/_work \
            --unattended
```

### 5c. Installer comme service systemd (démarrage automatique)

```bash
# Installer le service
sudo ./svc.sh install

# Démarrer le service
sudo ./svc.sh start

# Vérifier que le runner est actif
sudo ./svc.sh status
```

### 5d. Vérifier sur GitHub

Sur GitHub → **Settings** → **Actions** → **Runners**
Le runner `ubuntu-local` doit apparaître avec le statut **Idle** (vert).

---

## Étape 6 — Tester le déploiement automatique

Depuis le PC de l'équipe dev :
```bash
git commit --allow-empty -m "test: vérification pipeline CD"
git push origin main
```

Sur GitHub → **Actions** → observer le workflow **Deploy** :
1. ✅ CI (lint, security, imports, dockerfile) — ~2 min sur serveurs GitHub
2. ✅ Deploy — s'exécute sur ton serveur Ubuntu

---

## Commandes utiles au quotidien

```bash
# Voir l'état du conteneur
docker compose ps

# Suivre les logs en temps réel
docker compose logs -f carousel

# Redémarrer manuellement
docker compose restart carousel

# Arrêter
docker compose down

# Mise à jour manuelle (sans attendre la CI/CD)
cd /opt/carousel_generator
git pull origin main
docker compose up -d --build

# Voir les carousels générés
ls /var/lib/docker/volumes/carousel_generator_carousel_data/_data/

# Espace disque utilisé par Docker
docker system df
```

---

## Gérer le runner GitHub Actions

```bash
# Voir le statut du service
sudo systemctl status actions.runner.*.service

# Arrêter le runner
sudo /opt/actions-runner/svc.sh stop

# Redémarrer le runner
sudo /opt/actions-runner/svc.sh start

# Voir les logs du runner
journalctl -u actions.runner.*.service -f
```

---

## Résolution de problèmes

### L'application ne démarre pas
```bash
docker compose logs carousel --tail=50
```

### Chromium crashe (erreur "No usable sandbox")
```bash
# Vérifier que shm_size est bien dans docker-compose.yml
grep shm_size docker-compose.yml
# Doit afficher : shm_size: "256m"
```

### Le runner apparaît Offline sur GitHub
```bash
sudo /opt/actions-runner/svc.sh status
sudo /opt/actions-runner/svc.sh start
```

### Erreur "APP_PASSWORD ou SECRET_KEY vide"
```bash
cat /opt/carousel_generator/.env
# Vérifier que les deux variables sont remplies (pas juste le nom = sans valeur)
```

### Manque d'espace disque
```bash
# Nettoyer les images Docker inutilisées
docker system prune -f

# Nettoyer les anciennes générations (carousels)
# Les fichiers sont dans le volume Docker — à supprimer manuellement si nécessaire
docker volume inspect carousel_generator_carousel_data
```

---

## Architecture résumée

```
Équipe dev (PC)
    │
    │  git push
    ▼
GitHub (cloud)
    ├── CI : lint + sécurité + dockerfile  ← serveurs GitHub, gratuit
    │        (~2 minutes)
    │
    │  CI passe ✓ → notifie le runner
    ▼
Serveur Ubuntu local (ce serveur)
    ├── Runner GitHub Actions  ← agent installé à l'étape 5
    │        connexion sortante vers GitHub, pas de port entrant requis
    │
    └── docker compose up --build
             └── carousel-generator (port 5000)
```

---

## Contact

En cas de problème avec le pipeline CI/CD ou le code :
contacter l'équipe dev — **jesse@africacentred.tech**

© 2026 Africa Centred Technology. Tous droits réservés.
