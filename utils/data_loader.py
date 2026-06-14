import pandas as pd
import numpy as np
import sys
import os

# Racine du projet = dossier parent de utils/ (contient app.py, data/, ...)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.dict_questions_colonnes import code_to_question
except ImportError:
    # Fallback si exécuté hors package (ex: cwd dans utils/)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from dict_questions_colonnes import code_to_question
    except ImportError:
        code_to_question = {}

def load_data(filepath=None):
    """
    Charge les données brutes depuis data/enquete_alimentation.csv.

    Le chemin est résolu par rapport à la racine du projet : le fichier est
    donc trouvé quel que soit le dossier d'exécution (app Streamlit lancée
    depuis la racine, notebooks dans notebooks/, scripts dans scripts/).
    """
    if filepath is None:
        filepath = os.path.join(PROJECT_ROOT, "data", "enquete_alimentation.csv")
    try:
        return pd.read_csv(filepath, sep=";")
    except Exception as e:
        print(f"Erreur de chargement: {e}")
        return None

def map_frequencies_to_numeric(val):
    """
    Convertit les échelles de fréquence textuelles en scores numériques (approximatif hebdo).
    """
    if pd.isna(val):
        return np.nan
    
    val = str(val).lower().strip()
    
    mapping = {
        'jamais': 0,
        'très rarement': 0.5, # < 1/semaine
        '1 x par semaine': 1,
        '3 x par semaine': 3,
        '5 x par semaine': 5,
        '1 x par jour': 7,
        'a tous les repas': 14, # 2 repas par jour * 7
        'à tous les repas': 14
    }
    
    return mapping.get(val, np.nan)

def clean_data(df):
    """
    Nettoie et enrichit le dataframe : conversion types, création scores.
    """
    df_clean = df.copy()
    # 1. Conversion des fréquences de consommation en numérique pour analyse
    # Colonnes commençant par 'C_' (Consommation)
    consommation_cols = [col for col in df_clean.columns if col.startswith('C_')]
    
    for col in consommation_cols:
        new_col_name = f"{col}_num"
        df_clean[new_col_name] = df_clean[col].apply(map_frequencies_to_numeric)
    
    # 2. Création de Scores Synthétiques
    # Score Santé : Légumes + Fruits + Poisson - Indus
    # On gère les NaNs en les remplaçant par 0 pour le calcul de score simplifié, ou on garde NaN
    # Ici on remplit par la médiane pour ne pas perdre trop de données sur le score
    fill_cols = ['C_leg_num', 'C_frui_num', 'C_poi_num', 'C_indu_num', 'C_viaR_num', 'C_viaB_num']
    for c in fill_cols:
        if c in df_clean.columns:
            df_clean[c] = df_clean[c].fillna(df_clean[c].median())

    if all(x in df_clean.columns for x in ['C_leg_num', 'C_frui_num', 'C_poi_num', 'C_indu_num']):
        df_clean['Score_Sante'] = (
            df_clean['C_leg_num'] + 
            df_clean['C_frui_num'] + 
            df_clean['C_poi_num'] - 
            df_clean['C_indu_num']
        )
    
    if all(x in df_clean.columns for x in ['C_viaR_num', 'C_viaB_num']):
         df_clean['Score_Carné'] = df_clean['C_viaR_num'] + df_clean['C_viaB_num']

    # 3. Recodage de variables catégorielles simples
    # Sexe
    df_clean['Sexe'] = df_clean['Sexe'].fillna('Non Renseigné')
    df_clean['Sexe'] = df_clean['Sexe'].astype('category')
    
    # Age - Ordre logique
    # Standardisation extrême : regex pour retirer tout whitespace
    df_clean['Age'] = df_clean['Age'].astype(str).str.replace(r'\s+', '', regex=True)
    
    # Correction explicite des valeurs mal formattées
    age_mapping = {
        '60': '+60',
        '60+': '+60',
        '+60': '+60',
        '18-34': '18-34',
        '35-60': '35-60',
        '-18': '-18'
    }
    # On applique le mapping si la valeur est dans les clés, sinon on garde l'original (pour debug) ou on force
    df_clean['Age'] = df_clean['Age'].replace(age_mapping)

    # On laisse pandas inférer les catégories pour ne pas perdre de données si le mapping échoue
    # Simple conversion en catégorie sans forcer l'ordre (l'ordre sera géré au plot)
    df_clean['Age'] = df_clean['Age'].astype('category')
    
    return df_clean

def get_questions_dict():
    return code_to_question
