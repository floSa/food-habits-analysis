# Application Streamlit — Enquête Alimentation

L'application est la **vitrine interactive de l'analyse** : chaque page présente, avec
graphiques + tests + interprétation, l'un des cinq volets traités dans les notebooks
(`notebooks/`) et les rapports (`reports/`).

## 🚀 Lancer l'application

```bash
.venv/bin/streamlit run app.py        # puis http://localhost:8501
```

## 🗂️ Structure

### 🏠 Accueil (`app.py`)
Présentation du projet : chiffres de cadrage, les cinq analyses, **résultats phares**,
données & méthodologie.

### 👥 Page 1 — Population
Profil des répondants (sexe, âge, géographie, CSP, étude, régimes) et **ACM
démographique** (l'espace social se résume à un gradient d'âge). → `reports/01_population.md`

### 🍔 Page 2 — Habitudes & scores
Fréquences de consommation, **Score Santé**, tests avec **tailles d'effet** (t-test/ANOVA
de Welch, Games-Howell) et **régression OLS** : l'**âge** est le premier déterminant.
→ `reports/02_habitudes.md`

### 🎓 Page 3 — Sociologie (ACM)
Espace social alimentaire avec **correction de Benzécri** et interprétation par
contributions. Constat : les consommations sont **faiblement structurées socialement**.
→ `reports/03_sociologie_acm.md`

### 🧠 Page 4 — Croyances & pratiques
Idées reçues, score de connaissance (indépendant du diplôme), et le **fossé savoir/faire** :
appliquer la règle des « 5 fruits & légumes » va de pair avec un Score Santé bien supérieur
(*d* ≈ 1,0). → `reports/04_croyances_pratiques.md`

### 🛒 Page 5 — Marketing & choix
Critères d'achat (goût > prix > santé), **influence publicitaire** (parsée) → plus de
produits industriels (*d* ≈ 0,5), nuage de mots « manger équilibré ».
→ `reports/05_marketing_choix.md`

## 🛠️ Technique

- **Données / scores** : `utils/data_loader.py` (chargement, recodage, scores).
- **Calculs d'analyse partagés** app ↔ notebooks : `utils/analysis.py` (Benzécri, grille
  des croyances, parsing des questions à choix multiples) — garantit des résultats identiques.
- **Librairies** : `streamlit`, `pandas`, `matplotlib`/`seaborn`, `pingouin`, `statsmodels`,
  `prince`, `wordcloud`.
