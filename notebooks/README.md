# Notebooks d'analyse — Enquête Alimentation

Cinq notebooks thématiques analysent l'enquête (1 681 répondants). Chaque thème existe en
**trois formats** :

| Format | Emplacement | Pour quoi faire |
|---|---|---|
| Source **jupytext** (`.md`, avec code) | `notebooks/src/NN_*.md` | la **source éditable** — on ne modifie que celle-ci |
| Notebook **exécuté** (`.ipynb`, code + sorties) | `notebooks/NN_*.ipynb` | explorer / relancer dans Jupyter |
| **Rapport** sans code (`.md`, texte + tableaux + images) | `reports/NN_*.md` | **lecture / partage** |

## Les cinq analyses

| # | Thème | Rapport (lecture) | Notebook |
|---|---|---|---|
| 01 | Population — qui sont les répondants ? | [reports/01_population.md](../reports/01_population.md) | [01_population.ipynb](01_population.ipynb) |
| 02 | Habitudes alimentaires & scores de santé | [reports/02_habitudes.md](../reports/02_habitudes.md) | [02_habitudes.ipynb](02_habitudes.ipynb) |
| 03 | L'espace social alimentaire (ACM) | [reports/03_sociologie_acm.md](../reports/03_sociologie_acm.md) | [03_sociologie_acm.ipynb](03_sociologie_acm.ipynb) |
| 04 | Croyances, connaissances et pratiques | [reports/04_croyances_pratiques.md](../reports/04_croyances_pratiques.md) | [04_croyances_pratiques.ipynb](04_croyances_pratiques.ipynb) |
| 05 | Déterminants du choix & marketing | [reports/05_marketing_choix.md](../reports/05_marketing_choix.md) | [05_marketing_choix.ipynb](05_marketing_choix.ipynb) |

## Régénérer

Les notebooks et rapports se régénèrent depuis les sources `.md` :

```bash
bash notebooks/build.sh                 # tout
bash notebooks/build.sh 02_habitudes    # un seul
```

Le script enchaîne : `jupytext` (md → ipynb) → exécution (`nbconvert --execute`) →
rapport sans code (`nbconvert --no-input`, images extraites dans `reports/NN_*_files/`).

## Méthode

- Les notebooks réutilisent `utils/data_loader.py` (mêmes nettoyage et scores que
  l'application Streamlit) — analyses et appli restent cohérentes.
- Graphiques en **matplotlib/seaborn** (export image fiable dans les rapports `.md`).
- Statistiques avec **pingouin** (t-test/ANOVA de Welch, tailles d'effet, post-hoc
  Games-Howell), **statsmodels** (régression OLS) et **prince** (ACM, correction de
  Benzécri).
