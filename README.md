# Enquête Alimentation — analyse des habitudes & dynamiques alimentaires

Analyse d'une enquête déclarative (1 681 répondants, 51 variables) sur les habitudes
alimentaires, les croyances nutritionnelles et les déterminants sociologiques. Le projet
comprend une **application Streamlit** interactive et une **série de notebooks** d'analyse
accompagnés de rapports lisibles.

## Installation

```bash
uv venv .venv --python 3.12
uv sync                 # installe les dépendances depuis pyproject.toml / uv.lock
```

## Application Streamlit

```bash
.venv/bin/streamlit run app.py
```

Détails des pages dans [README_APP.md](README_APP.md).

## Notebooks & rapports d'analyse

Cinq analyses thématiques, chacune disponible en notebook exécuté (`.ipynb`) et en
**rapport sans code** (`reports/*.md`, texte + tableaux + images) pour la lecture et le
partage. Voir l'index : **[notebooks/README.md](notebooks/README.md)**.

| # | Thème | Rapport |
|---|---|---|
| 01 | Population | [reports/01_population.md](reports/01_population.md) |
| 02 | Habitudes & scores de santé | [reports/02_habitudes.md](reports/02_habitudes.md) |
| 03 | Espace social alimentaire (ACM) | [reports/03_sociologie_acm.md](reports/03_sociologie_acm.md) |
| 04 | Croyances vs pratiques | [reports/04_croyances_pratiques.md](reports/04_croyances_pratiques.md) |
| 05 | Marketing & choix | [reports/05_marketing_choix.md](reports/05_marketing_choix.md) |

Régénération depuis les sources jupytext : `bash notebooks/build.sh`.
