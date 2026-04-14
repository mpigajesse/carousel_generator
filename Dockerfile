# =============================================================================
# Dockerfile — Carousel Generator (Production)
# Cible : Ubuntu Server 24 + Docker
# Serveur : Gunicorn (1 worker / 4 threads) + Playwright Chromium
# =============================================================================

FROM python:3.12-slim

# ── Métadonnées ──
LABEL maintainer="jesse@africacentred.tech"
LABEL org.opencontainers.image.title="Carousel Generator"
LABEL org.opencontainers.image.description="Générateur de carousels Instagram/LinkedIn"
LABEL org.opencontainers.image.vendor="Africa Centred Technology"

# ── Variables d'environnement de build ──
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Playwright : chemin fixe pour les navigateurs (prévisible et appropriable)
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    # Flask
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# ── Dépendances système pour Playwright Chromium ──
# On n'installe PAS google-chrome-stable (lourd, redondant avec Playwright)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Réseau et certificats
    ca-certificates \
    wget \
    curl \
    # Fonts (indispensables pour le rendu des slides)
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    # Libs graphiques Chromium
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    # Nettoyage
    && rm -rf /var/lib/apt/lists/*

# ── Utilisateur non-root (sécurité conteneur) ──
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# ── Répertoire de travail ──
WORKDIR /app

# ── Dépendances Python (couche cachée séparément pour les rebuilds rapides) ──
COPY requirements.txt .
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Playwright Chromium (installé dans PLAYWRIGHT_BROWSERS_PATH) ──
# install-deps gère les libs système manquantes puis on corrige les permissions
RUN playwright install chromium && \
    playwright install-deps chromium && \
    chown -R appuser:appuser /ms-playwright

# ── Code source (ownership appuser dès la copie) ──
COPY --chown=appuser:appuser . .

# ── Dossiers de données (volume monté en production) ──
RUN mkdir -p static/generated && \
    chown -R appuser:appuser static/generated /app

# ── Passage à l'utilisateur non-root ──
USER appuser

# ── Port exposé ──
EXPOSE 5000

# ── Health check ──
# On tape /login (toujours accessible sans auth) plutôt que /
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f -s -o /dev/null -w "%{http_code}" http://localhost:5000/login | grep -q "200" || exit 1

# ── Démarrage production via Gunicorn ──
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
