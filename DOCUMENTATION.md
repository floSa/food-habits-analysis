# Documentation technique — Enquête Alimentation

Documentation de la méthodologie d'analyse : du questionnaire brut aux scores
synthétiques, aux tests statistiques et à l'analyse factorielle. Chaque valeur citée
provient du code (`utils/`) ou des rapports (`reports/`). Les livrables (application
Streamlit, notebooks, rapports) reposent tous sur le même cœur de calcul.

---

## 1. Problème métier

Comprendre les **habitudes alimentaires** d'un échantillon de **1 681 répondants** à une
enquête déclarative, et répondre à cinq questions :

| # | Question | Notebook / rapport |
|---|---|---|
| 1 | Qui sont les répondants ? | `reports/01_population.md` |
| 2 | Que mangent-ils, et qui mange le mieux ? | `reports/02_habitudes.md` |
| 3 | Les habitudes sont-elles socialement structurées ? | `reports/03_sociologie_acm.md` |
| 4 | Savoir, est-ce manger mieux ? | `reports/04_croyances_pratiques.md` |
| 5 | Qu'est-ce qui guide l'achat ? | `reports/05_marketing_choix.md` |

**Difficultés spécifiques** : données **déclaratives** (biais de désirabilité),
échantillon **non représentatif** (voir §8), variables majoritairement **catégorielles /
ordinales** (fréquences textuelles, questions Vrai/Faux, questions à choix multiples), et
plusieurs questions ouvertes.

---

## 2. Données & préparation

**Source** : `data/enquete_alimentation.csv` (séparateur `;`, lu par
[utils/data_loader.py](utils/data_loader.py)). **1 681 lignes**, **51 variables brutes**
du questionnaire ; après enrichissement, `clean_data` porte le tableau à **62 colonnes**
(scores `*_num` et scores synthétiques).

Étapes de nettoyage (`clean_data`) :

- **Conversion des fréquences** : chaque colonne de consommation `C_*` reçoit une colonne
  numérique `C_*_num` (voir §3).
- **Imputation ciblée** : pour les composantes des scores (`C_leg_num`, `C_frui_num`,
  `C_poi_num`, `C_indu_num`, `C_viaR_num`, `C_viaB_num`), les valeurs manquantes sont
  remplacées par la **médiane** de la colonne — choix assumé, voir la limite au §4.
- **Recodage catégoriel** : `Sexe` (manquants → `Non Renseigné`), `Age` (suppression des
  espaces par regex puis mapping explicite vers `-18`, `18-34`, `35-60`, `+60`).

Le chemin du CSV est résolu par rapport à la racine du projet, de sorte que l'app (lancée
à la racine), les notebooks (`notebooks/`) et les scripts (`scripts/`) chargent la même
donnée sans dépendre du répertoire courant.

---

## 3. Feature engineering

### 3.1 Fréquences textuelles → échelle numérique hebdomadaire

`map_frequencies_to_numeric` projette les modalités de fréquence sur une échelle
approximative de consommations **par semaine** :

| Modalité | Valeur |
|---|---|
| Jamais | 0 |
| Très rarement | 0,5 |
| 1 x par semaine | 1 |
| 3 x par semaine | 3 |
| 5 x par semaine | 5 |
| 1 x par jour | 7 |
| À tous les repas | 14 |

> **Échelle hebdomadaire plutôt qu'ordinale simple** (0,1,2,…) **parce que** les écarts
> réels entre modalités ne sont pas uniformes (« 1 x par jour » ≈ 7×/semaine, « à tous les
> repas » ≈ 2 repas × 7). **Limite** : le pas reste une approximation déclarative, sans
> valeur nutritionnelle absolue.

### 3.2 Scores synthétiques

Définis dans `clean_data` :

$$\text{Score\_Sante} = C_{leg} + C_{frui} + C_{poi} - C_{indu}$$

$$\text{Score\_Carné} = C_{viaR} + C_{viaB}$$

où chaque terme est la fréquence hebdomadaire numérique. Statistiques observées
(rapport 02) : Score Santé moyen **12,1** (écart-type 9, de −14 à +41,5) ; Score Carné
moyen **4,7**.

### 3.3 Score de connaissance

`add_knowledge_score` ([utils/analysis.py](utils/analysis.py)) agrège **9 idées reçues**
Vrai/Faux (`VF_*`) : chaque bonne réponse vaut 1, d'où

$$\text{Score\_Connaissance} = \sum_{i=1}^{9} \mathbb{1}[\text{réponse}_i = \text{correcte}_i] \in [0, 9]$$

La grille des bonnes réponses est la constante `BELIEFS`. Score moyen observé : **6,44/9**.

### 3.4 Questions à choix multiples

`multi_pct` éclate les réponses séparées par `, ` et compte la fréquence de chaque option
(dénominateur = répondants non manquants). Les libellés contenant des virgules internes
(catégories de produits de la question `Pub`) sont détectés par **sous-chaîne** et non par
`split`, pour ne pas les fragmenter (`pub_category_rates`, `PUB_OPTS`).

---

## 4. Traitement de la cible (Score Santé)

Le Score Santé est la variable expliquée centrale (rapport 02). Deux partis pris :

- **Imputation par la médiane** des composantes **avant** calcul : préserve l'effectif au
  lieu de perdre toute ligne partiellement manquante.
- **Usage relatif** : le score sert à **comparer des sous-groupes**, pas à mesurer une
  qualité nutritionnelle absolue.

> **Imputation médiane plutôt que suppression des NaN parce que** les comparaisons de
> groupes exigent de conserver l'effectif ; **limite** : le score n'est pas
> manquant-robuste et sa valeur absolue n'a pas de sens « clinique » — d'où l'usage
> strictement relatif.

---

## 5. Méthodes statistiques

Choix guidés par la nature des données (échantillon large, non-normalité, variances
inégales). Test de **Shapiro-Wilk** rejetant la normalité du Score Santé (p < 0,001) sur
1 681 observations → on privilégie des tests **robustes**.

| Besoin | Méthode retenue | Pourquoi |
|---|---|---|
| Comparer 2 groupes | **t-test de Welch** (pingouin) | robuste à l'hétéroscédasticité |
| Comparer > 2 groupes | **ANOVA de Welch** + Levene | ne suppose pas l'égalité des variances |
| Post-hoc | **Games-Howell** | adapté aux variances/effectifs inégaux |
| Taille d'effet (2 groupes) | ***d* de Cohen**, *g* de Hedges | ampleur au-delà de la significativité |
| Taille d'effet (ANOVA) | **η² partiel** (`np2`) | part de variance expliquée |
| Association ordinale | **corrélation de Spearman** (ρ) | échelles ordinales, monotone |

$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$

> **Welch / Games-Howell plutôt que Student / Tukey parce que** les variances et effectifs
> des sous-groupes (sexe, âge, profession) sont inégaux ; **la taille d'effet est
> systématiquement reportée** car sur 1 681 observations le moindre écart devient
> significatif (p faible ≠ effet notable).

---

## 6. Modélisation

### 6.1 Régression OLS du Score Santé

Pour démêler les effets confondus (« retraité » porte de l'âge, etc.), le Score Santé est
régressé (**statsmodels OLS**) sur sexe, âge, niveau d'étude et territoire (références :
Femme, +60 ans, Bac, Citadin). Résultat (rapport 02) : **R² = 0,088** (ajusté 0,084),
p global = 2,6e-29.

| Effet | Coefficient | p-val |
|---|---|---|
| Âge 18-34 (vs +60) | −9,37 | < 0,001 |
| Âge 35-60 (vs +60) | −4,82 | < 0,001 |
| Étude Bac+5 (vs Bac) | +3,14 | < 0,001 |
| Étude Brevet (vs Bac) | −3,14 | 0,003 |
| Sexe Homme (vs Femme) | −1,05 | 0,028 |
| Rural (vs Citadin) | −0,01 | 0,982 |

Lecture : **l'âge domine**, l'éducation joue à la marge, le sexe devient significatif une
fois l'âge neutralisé (effet masqué), le territoire est sans effet.

### 6.2 Analyse des Correspondances Multiples (ACM)

**prince.MCA** sur les **8 variables actives** de consommation (`ACM_ACTIVES`), les
manquants traités comme une modalité « Non répondu ». Ajustement sur 5 axes.

**Correction de Benzécri** (`benzecri_percentages`) : l'ACM brute sous-estime l'inertie
des premiers axes (codage disjonctif). On ne retient que les axes dont la valeur propre
dépasse $1/K$ (ici $K = 8$) et on recalcule des pourcentages réalistes :

$$\lambda_{ben} = \left(\frac{K}{K-1}\left(\lambda - \tfrac{1}{K}\right)\right)^2 \quad \text{si } \lambda > \tfrac{1}{K}, \text{ sinon } 0$$

puis normalisation sur la somme. Effet observé (rapport 03) : le premier axe passe de
**4,86 % brut à 36,1 % corrigé** ; le **plan 1-2 capte ≈ 62 %** de l'inertie corrigée.

> **ACM (prince) plutôt qu'ACP parce que** les variables actives sont **catégorielles**
> (fréquences) ; **correction de Benzécri parce que** les % bruts du codage disjonctif ne
> sont pas comparables à ceux d'une ACP et écrasent l'information.

---

## 7. Inférence & résultats par volet

| Volet | Résultat principal | Chiffre |
|---|---|---|
| 02 — Habitudes | L'âge est le premier déterminant du Score Santé | OLS R² ≈ 0,09 |
| 02 — Habitudes | Ni sexe ni territoire en brut | p = 0,085 / 0,06 ; *d* ≈ 0,09 |
| 03 — ACM | Axe 1 = non-consommation ; Axe 2 = intensité carnée (croît avec l'âge) | plan 1-2 ≈ 62 % |
| 03 — ACM | Espace faiblement structuré socialement | nuages superposés |
| 04 — Croyances | Connaissance indépendante du diplôme | ANOVA Welch p = 0,16 |
| 04 — Croyances | Savoir ↔ pratique faible | Spearman ρ = 0,18 |
| 04 — Croyances | Appliquer les « 5 F&L » : 14,1 vs 6,0 | *d* ≈ 0,99 |
| 05 — Marketing | Choix : goût (65 %) > santé (50 %) > prix (40 %) | déclaratif |
| 05 — Marketing | Influencés par la pub : + de produits industriels | 3,95 vs 2,35 ; *d* ≈ 0,50 |

---

## 8. Analyse critique des résultats

- **Représentativité** : échantillon **non représentatif** — surreprésentation des femmes
  (≈ 73 %), des 18-34 ans (64 %), des diplômés du supérieur (≈ 72 % Bac+3 ou plus) et du
  Sud (≈ 79 %). Les résultats valent d'abord **au sein de l'échantillon** ; leur
  généralisation n'est pas garantie.
- **Déclaratif** : consommations et croyances sont auto-rapportées (biais de désirabilité,
  possible style de réponse — l'axe 1 de l'ACM capte en partie des réponses « Jamais »).
- **Pouvoir explicatif modeste** : le socio-démographique n'explique que **~9 %** du Score
  Santé ; l'essentiel se joue ailleurs (goûts, contraintes, passage à l'acte).
- **Score synthétique** : construit et relatif (imputation médiane, pondération simple),
  à ne pas sur-interpréter en valeur absolue.

---

## 9. Explicabilité

- **ACM** : interprétation des axes par les **contributions** des modalités (% de l'inertie
  de l'axe) avec le signe de la coordonnée (rapport 03, §5) — l'axe 1 est porté par les
  modalités « Jamais », l'axe 2 par les consommations fréquentes de protéines animales.
- **Régression** : coefficients OLS avec IC 95 %, chaque effet rapporté à sa modalité de
  référence.
- **Corrélations** : heatmap de Spearman entre consommations (fruits ↔ légumes ρ = 0,47 ;
  industriels ↔ légumes ρ ≈ −0,26).

---

## 10. Pipeline d'exécution

De la donnée brute aux livrables :

1. **Source** : `data/enquete_alimentation.csv`.
2. **Nettoyage & scores** : `utils/data_loader.py` (partagé app ↔ notebooks).
3. **Calculs d'analyse** : `utils/analysis.py` (Benzécri, croyances, parsing).
4. **Application** : `app.py` + `pages/` (Streamlit, port 8507).
5. **Notebooks** : sources jupytext `notebooks/src/*.md`, régénérées par
   `notebooks/build.sh` : `jupytext` (md → ipynb) → `nbconvert --execute` →
   `nbconvert --no-input` (rapport sans code, images dans `reports/NN_*_files/`).

```bash
bash notebooks/build.sh                 # régénère tout
bash notebooks/build.sh 02_habitudes    # un seul thème
```

---

## 11. Améliorations possibles (non implémentées)

| Piste | Bénéfice attendu |
|---|---|
| Pondération / redressement de l'échantillon | Atténuer le biais de représentativité |
| Score Santé manquant-robuste (au lieu de l'imputation médiane) | Robustesse des comparaisons |
| Analyse Factorielle Multiple (MFA) croyances × pratiques | Confronter directement les deux blocs (envisagée dans `docs/Plan.md`) |
| Clustering des profils sur les axes de l'ACM | Typologies de mangeurs (« tradi-viandard », « éco-végétal »…) |
| Traitement NLP des questions ouvertes (au-delà du nuage de mots) | Structurer les représentations de « manger équilibré » |
| Fichier `LICENSE` explicite | Clarifier la licence du code |

---

## Licences & composants

| Composant | Rôle | Licence |
|---|---|---|
| pandas / NumPy | Manipulation & calcul | BSD-3-Clause |
| SciPy / statsmodels | Tests statistiques, régression OLS | BSD-3-Clause |
| pingouin | Tests robustes, tailles d'effet, Games-Howell | GPL-3.0 |
| prince | ACM + correction de Benzécri | MIT |
| matplotlib / seaborn | Visualisation | matplotlib (PSF-based) / BSD-3-Clause |
| plotly | Visualisation interactive | MIT |
| wordcloud | Nuages de mots | MIT |
| jupytext / nbconvert | Notebooks (source ⇄ ipynb ⇄ rapports) | MIT / BSD-3-Clause |
| Streamlit | Application web | Apache-2.0 |
| openpyxl | Lecture Excel | MIT |
| **Ce projet** | Code applicatif | MIT — Copyright (c) 2026 floSa (aucun fichier LICENSE présent) |
