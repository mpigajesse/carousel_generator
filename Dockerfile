# =============================================================================
# Dockerfile - Carousel Generator
# Déploiement production pour Hugging Face Spaces / Render / Auto-hébergement
# =============================================================================

# ── Image de base Python 3.12 slim ──
FROM python:3.12-slim

# ── Variables d'environnement ──
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=7860

# ── Dépendances système pour Playwright (Chromium) ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Navigateur Chromium et dépendances
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    # Nettoyage pour réduire la taille de l'image
    && rm -rf /var/lib/apt/lists/*

# ── Installer Google Chrome stable (requis par Playwright) ──
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# ── Répertoire de travail ──
WORKDIR /app

# ── Installer les dépendances Python ──
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Installer Playwright et Chromium ──
RUN playwright install chromium && \
    playwright install-deps chromium

# ── Copier le code source ──
COPY . .

# ── Créer les dossiers nécessaires ──
RUN mkdir -p static/generated && \
    mkdir -p output

# ── Exposer le port (7860 pour Hugging Face Spaces) ──
EXPOSE 7860

# ── Healthcheck ──
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/')" || exit 1

# ── Commande de démarrage ──
CMD ["python", "app.py"]
