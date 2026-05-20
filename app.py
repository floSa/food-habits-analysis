import streamlit as st
import pandas as pd
from utils.data_loader import load_data, clean_data

st.set_page_config(
    page_title="Enquête Alimentation",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 Analyse des Habitudes et Dynamiques Alimentaires")

st.markdown("""
### Bienvenue sur l'outil d'exploration de données.

Cette application a pour but d'analyser les résultats de l'enquête sur les habitudes alimentaires, les croyances nutritionnelles et les déterminants sociologiques.
""")

st.info("Utilisez le menu latéral pour naviguer entre les différentes analyses.")

# Chargement rapide pour vérifier que tout va bien
df = load_data()
if df is not None:
    st.success(f"Données chargées avec succès : {df.shape[0]} répondants, {df.shape[1]} variables.")
    
    with st.expander("Aperçu des données brutes"):
        st.dataframe(df.head())
else:
    st.error("Impossible de charger les données 'enquete_alimentation.csv'. Vérifiez l'emplacement du fichier.")

st.markdown("""
---
**Méthodologie** :
*   Données issues d'un questionnaire déclaratif.
*   Analyses statistiques réalisées avec **Pingouin** et **Statsmodels**.
*   Analyses factorielles (ACM/AFM) réalisées avec **Prince**.
""")
