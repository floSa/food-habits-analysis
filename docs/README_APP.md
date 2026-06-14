# Application d'Analyse Enquête Alimentation

L'application Streamlit est prête ! Elle permet d'explorer les données de l'enquête, de tester des hypothèses statistiques et de visualiser l'espace social alimentaire.

## 🚀 Comment lancer l'application

1.  Ouvrez un terminal dans le dossier du projet :
    ```bash
    cd /home/florian/mes_projets/Alimentation
    ```

2.  Activez l'environnement virtuel (si ce n'est pas déjà fait) et lancez Streamlit :
    ```bash
    source .venv/bin/activate
    streamlit run app.py
    ```

3.  L'application s'ouvrira dans votre navigateur (généralement à l'adresse `http://localhost:8501`).

## 📱 Structure de l'Application

### 🏠 Accueil (`app.py`)
Présentation générale et aperçu des données brutes.

### 👥 Page 1 : Population
*   **Objectif :** Connaître le profil des répondants.
*   **Visualisations :** Pyramide des âges, répartition géographique, CSP.
*   **Filtres :** Possibilité de filtrer toute la page par Sexe.

### 🍔 Page 2 : Habitudes Alimentaires & Scores
*   **Analyses Univariées :** Explorez la fréquence de consommation de chaque aliment.
*   **Score Santé :** Une variable synthétique calculée pour évaluer la qualité nutritionnelle globale.
*   **Tests Statistiques (Pingouin) :** Vérifiez si le Score Santé diffère significativement selon le Sexe, la Zone Rurale, etc. (Tests T-test/ANOVA automatiques).

### 🎓 Page 3 : Sociologie (ACM/MCA)
*   **Analyse Factorielle :** Utilise la librairie **Prince** pour projeter les individus selon leurs consommations.
*   **Exploration :** Découvrez quels aliments "vont ensemble" et comment les profils sociaux (Cadres vs Étudiants) se positionnent dans cet espace.

### 🛒 Page 4 : Marketing
*   **Déterminants :** Qu'est-ce qui influence l'achat ? (Prix, Goût, Santé).
*   **Focus Pub :** Analyse du lien entre sensibilité à la publicité et consommation de produits industriels.

## 🛠️ Technique
*   **Nettoyage Données :** `utils/data_loader.py` gère le chargement et la conversion des fréquences en scores numériques.
*   **Librairies :** `streamlit`, `pandas`, `plotly`, `pingouin`, `prince`.
