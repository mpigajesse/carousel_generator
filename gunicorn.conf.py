# =============================================================================
# gunicorn.conf.py — Configuration Gunicorn (production)
# =============================================================================
#
# Architecture : 1 worker / 4 threads (gthread)
#
# Pourquoi 1 worker ?
#   L'app utilise un dict `jobs` en mémoire pour tracker les générations
#   en cours. Plusieurs workers (processus) ne partagent pas la mémoire →
#   /api/status/<job_id> ne retrouverait pas un job lancé par un autre worker.
#   Avec gthread, on a 1 processus + 4 threads qui partagent bien le dict.
#
# Pourquoi 120s de timeout ?
#   Playwright + Chromium peut prendre 30-60s pour un carousel dense.
#   120s offre une marge confortable sans bloquer trop longtemps.
# =============================================================================

import os
import multiprocessing

# ── Liaison ──
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# ── Worker ──
worker_class = "gthread"
workers = 1                  # 1 seul processus pour partager le dict jobs en mémoire
threads = 4                  # 4 threads simultanés pour les requêtes concurrentes

# ── Timeouts ──
timeout = 120                # Playwright peut prendre jusqu'à 60s sur un gros carousel
graceful_timeout = 30        # Laisse les threads en cours terminer proprement
keepalive = 5                # Keep-alive HTTP en secondes

# ── Performances ──
max_requests = 500           # Redémarre le worker après N requêtes (évite les fuites mémoire)
max_requests_jitter = 50     # Étale les redémarrages pour éviter le thundering herd

# ── Logs ──
accesslog = "-"              # stdout → Docker logs
errorlog = "-"               # stderr → Docker logs
loglevel = "info"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(D)sµs'

# ── Sécurité ──
limit_request_line = 4094    # Limite la taille des URLs
limit_request_fields = 100   # Limite le nombre d'en-têtes HTTP
limit_request_field_size = 8190

# ── Hooks de cycle de vie ──
def on_starting(server):
    server.log.info("Carousel Generator démarré (Gunicorn gthread)")

def worker_exit(server, worker):
    server.log.info(f"Worker {worker.pid} arrêté proprement")
