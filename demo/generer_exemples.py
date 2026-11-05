"""Génère les carrousels d'exemple de la démo publique.

Lancé une fois à la construction de l'image (Dockerfile.demo) : la bibliothèque
n'est jamais vide quand un recruteur arrive, même après un redémarrage de
l'instance gratuite, qui efface le disque.

Les exemples sont listés dans static/generated/exemples.json : app.py les
protège de la suppression et du renommage en mode DEMO_PUBLIQUE.
"""

import json
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))

from generate import generate_carousel  # noqa: E402
from md_parser import parse_markdown_to_slides  # noqa: E402

SORTIE = RACINE / "static" / "generated"

EXEMPLES = [
    # (identifiant, source, plateforme, thème, format)
    ("2026-11-05_09-00-00_Exemple_Instagram", "exemple-instagram.md", "instagram", "ig_ocean_deep", "png"),
    ("2026-11-05_09-05-00_Exemple_LinkedIn", "exemple-linkedin.yaml", "linkedin", "dark_purple", "pdf"),
]


def charger(source: Path) -> dict:
    texte = source.read_text(encoding="utf-8")
    if source.suffix == ".md":
        resultat = parse_markdown_to_slides(texte)
        return {"footer": resultat.get("footer", {}), "slides": resultat["slides"]}
    return yaml.safe_load(texte)


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    ids = []
    for job_id, nom, plateforme, theme, fmt in EXEMPLES:
        config = charger(Path(__file__).parent / nom)
        generate_carousel(None, theme, str(SORTIE / job_id), fmt, plateforme, config_dict=config)
        ids.append(job_id)
        print(f"Exemple prêt : {job_id}")
    (SORTIE / "exemples.json").write_text(json.dumps(ids), encoding="utf-8")


if __name__ == "__main__":
    main()
