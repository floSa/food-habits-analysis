# Enquête Alimentation — habitudes & dynamiques alimentaires

Analyse d'une enquête déclarative (**1 681 répondants**, 51 variables) sur les habitudes
alimentaires, les croyances nutritionnelles et leurs déterminants sociologiques.

Le dépôt contient **deux livrables complémentaires** :

1. 🖥️ une **application Streamlit** interactive (exploration libre, filtres, ACM en direct) ;
2. 📓 une **série de 5 notebooks** d'analyse, chacun accompagné d'un **rapport lisible**
   (texte + tableaux + images, sans code) pour le partage.

## Structure du projet

```
.
├── app.py                  # 🖥️ point d'entrée de l'application Streamlit
├── pages/                  #    pages de l'app (Population, Habitudes, Sociologie, Marketing)
├── utils/                  #    code partagé app + notebooks (chargement, nettoyage, graphiques)
│   ├── data_loader.py      #    load_data() / clean_data() / scores
│   └── dict_questions_colonnes.py   # libellés des questions
├── data/                   # 📊 données brutes (enquete_alimentation.csv)
├── notebooks/              # 📓 analyses
│   ├── src/                #    sources jupytext (.md, éditables)
│   ├── *.ipynb             #    notebooks exécutés (code + sorties)
│   ├── build.sh            #    régénère ipynb + rapports depuis src/
│   └── README.md           #    index détaillé des analyses
├── reports/                # 📄 rapports sans code (.md + images) — pour lecture/partage
├── scripts/                # 🔧 scripts d'exploration / dev (hors app)
└── docs/                   # 📚 Plan.md, README_APP.md, captures, sorties annexes
```

## Installation

```bash
uv venv .venv --python 3.12
uv sync            # installe les dépendances (pyproject.toml / uv.lock)
```

## 🖥️ Lancer l'application Streamlit

```bash
.venv/bin/streamlit run app.py      # puis ouvrir http://localhost:8501
```

Description des pages : [docs/README_APP.md](docs/README_APP.md).

## 📓 Notebooks & rapports d'analyse

Pour lire les analyses **sans rien exécuter**, ouvrir les rapports dans `reports/` :

| # | Thème | Rapport |
|---|---|---|
| 01 | Population | [reports/01_population.md](reports/01_population.md) |
| 02 | Habitudes & scores de santé | [reports/02_habitudes.md](reports/02_habitudes.md) |
| 03 | Espace social alimentaire (ACM) | [reports/03_sociologie_acm.md](reports/03_sociologie_acm.md) |
| 04 | Croyances vs pratiques | [reports/04_croyances_pratiques.md](reports/04_croyances_pratiques.md) |
| 05 | Marketing & choix | [reports/05_marketing_choix.md](reports/05_marketing_choix.md) |

Index complet et méthode : [notebooks/README.md](notebooks/README.md).
Régénération depuis les sources : `bash notebooks/build.sh`.
```bash
bash notebooks/build.sh                 # tout
bash notebooks/build.sh 02_habitudes    # un seul
```
