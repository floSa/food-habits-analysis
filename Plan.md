# Plan d'Analyse Révisé : Application Streamlit "Habitudes & Dynamiques Alimentaires"

## Objectif
Développer une application interactive Streamlit pour explorer en profondeur les habitudes alimentaires, les croyances et les déterminants sociologiques, en utilisant des méthodes statistiques avancées (Statsmodels, Pingouin, Prince).

---

## Structure de l'Application Streamlit

### Page 1 : Vue d'ensemble & Population
*   **Objectif :** Comprendre qui sont les répondants.
*   **Visualisations :**
    *   Pyramide des âges, Répartition Sexe, CSP, Niveau d'étude.
    *   Carte/Répartition géographique (`Card`, `Rura`).
    *   Statistiques descriptives générales (Taille de l'échantillon, taux de réponse).

### Page 2 : Habitudes Alimentaires (Au cœur de l'analyse)
*   **Objectif :** Analyser finement *ce que les gens mangent* et *comment*.
*   **Analyses Univariées :**
    *   Distributions des fréquences de consommation (`C_leg`, `C_viaR`, `C_indu`, etc.) avec tris à plat.
*   **Scores Synthétiques (Création de nouvelles variables) :**
    *   *Score Santé* (Légumes + Fruits + Poisson - Indus - Sucre).
    *   *Score Viande* (Rouge + Blanche + Charcuterie).
*   **Analyses Bivariées (Pingouin/Statsmodels) :**
    *   Tests de différence (ANOVA/Kruskal-Wallis) : Le Score Santé varie-t-il selon l'Âge ou le Sexe ?
    *   Heatmap des corrélations entre types d'aliments (ex: Viande Rouge et Prod. Industriels).

### Page 3 : Sociologie du Mangeur (Analyses Factorielles - Prince)
*   **Objectif :** Situer les individus dans un espace social et alimentaire (Bourdieu).
*   **Analyse des Correspondances Multiples (ACM/MCA) :**
    *   *Variables actives :* Consommations (`C_...`).
    *   *Variables illustratives :* CSP, Diplôme, Age, Sexe.
    *   *Visualisation :* Plan factoriel des individus et des modalités.
*   **Profilage (Clustering) :**
    *   Identification de classes (ex: "Tradi-Viandard", "Eco-Végétal", "Fast-Fooder").

### Page 4 : Croyances vs Pratiques (MFA - Prince)
*   **Objectif :** Confronter ce que les gens *pensent* (Vrai/Faux) à ce qu'ils *font*.
*   **Analyse Factorielle Multiple (MFA) :**
    *   *Groupe 1 :* Pratiques alimentaires.
    *   *Groupe 2 :* Croyances (`VF_...`) et Connaissances (`5fj`).
    *   *Analyse :* Voir si les connaissances nutritionnelles influencent réellement l'assiette.

### Page 5 : Déterminants du Choix & Marketing
*   **Objectif :** Comprendre les leviers d'achat.
*   **Analyses :**
    *   Impact des labels (`Etiqt`, `Bio`) et du prix.
    *   Lien entre sensibilité à la Pub (`Pub`) et consommation de produits transformés (`C_indu`).
    *   Analyse textuelle simple (Wourdcloud) sur les questions ouvertes (`Mangé_E`, `Repas` si pertinent).

---

## Outils & Librairies Techniques
*   **Streamlit :** Framework de l'application (Multi-page app).
*   **Pandas/Numpy :** Manipulation de données et recodage.
*   **Plotly/Seaborn :** Visualisations interactives.
*   **Pingouin :** Tests statistiques robustes (T-test, ANOVA bruts, Corrélations).
*   **Statsmodels :** Modèles de régression (si besoin d'expliquer un score).
*   **Prince :** Correspondence analysis (CA), Multiple correspondence analysis (MCA), Multiple factor analysis (MFA), Factor analysis of mixed data (FAMD), Generalized procrustes analysis (GPA).

## Étapes de Réalisation
1.  **Data Cleaning & Feature Engineering :** Recodage des variables ordinales (Jamais -> Tous les jours en numérique pour les scores), gestion des NaNs.
2.  **Dev Page Population & Habitudes :** Implémentation des stats de base.
3.  **Dev Analyses Avancées :** Intégration de Prince pour MCA/MFA.
4.  **Raffinage UX :** Filtres interactifs (par Sexe, par Région) sur la sidebar.