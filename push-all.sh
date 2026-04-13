#!/usr/bin/env bash
# push-all.sh — Pousse les commits sur les deux GitHub en une commande
set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "→ Branch: $BRANCH"

echo ""
echo "[1/2] Push → origin (mpigajesse/carousel_generator)"
git push origin "$BRANCH"

echo ""
echo "[2/2] Push → act (Africa-centred-technology/carousel_generator_officiel)"
git push act "$BRANCH"

echo ""
echo "✓ Sync complet sur les deux GitHub."
