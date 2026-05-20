import streamlit as st
import pandas as pd
import plotly.express as px
import pingouin as pg
from utils.data_loader import load_data, clean_data, get_questions_dict
from utils.plotting import plot_distribution, plot_boxplot, plot_correlation_heatmap

st.set_page_config(page_title="Habitudes Alimentaires", page_icon="🍔", layout="wide")

st.title("🍔 Habitudes Alimentaires & Scores")

# Chargement
df = load_data()
if df is None:
    st.stop()
df = clean_data(df)
questions = get_questions_dict()

# --- Section 1 : Distributions des Consommations ---
st.header("1. Fréquence de Consommation")

cols_conso = [c for c in df.columns if c.startswith('C_') and not c.endswith('_num')]
selected_conso = st.selectbox("Choisir un type d'aliment", cols_conso, format_func=lambda x: f"{x} ({questions.get(x, x)})")

st.info(f"Question : {questions.get(selected_conso, 'Non spécifié')}")

# Ordre logique des fréquences pour le graphe
freq_order = ['Jamais', 'Très rarement', '1 x par semaine', '3 x par semaine', '5 x par semaine', '1 x par jour', 'A tous les repas']

fig_dist = plot_distribution(df, selected_conso, order=freq_order, color='Sexe')
st.plotly_chart(fig_dist, use_container_width=True)

# --- Section 2 : Scores Synthétiques & Tests Stats ---
st.header("2. Analyse des Scores de Santé")

st.markdown("""
### 🍎 Comprendre le Score Santé
Nous avons construit un indicateur pour évaluer la qualité nutritionnelle globale des repas.
**Calcul du Score :**
*   **+1 point** pour chaque fréquence de consommation "positive" (Légumes, Fruits, Poisson).
*   **-1 point** pour chaque consommation "négative" (Produits Industriels).
*   Le tout est pondéré par la fréquence (manger des légumes tous les jours rapporte plus de points).

Un score élevé indique une alimentation plus proche des recommandations de santé publique.
""")

score_col = 'Score_Sante'

c1, c2 = st.columns(2)
with c1:
    fig_hist = px.histogram(df, x=score_col, nbins=20, title="Distribution du Score Santé", marginal="box")
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("Test Statistique (Pingouin)")
    st.markdown("""
    **À quoi ça sert ?**
    Ce test compare la moyenne du Score Santé entre différents groupes (ex: Hommes vs Femmes).
    
    **Comment lire le résultat ?**
    *   **p-val (p-value)** : Si ce chiffre est **inférieur à 0.05**, on considère que la différence est statistiquement significative (elle n'est pas due au hasard).
    *   **T-test** (2 groupes) ou **ANOVA** (plus de 2 groupes).
    """)
    factor_col = st.selectbox("Comparer le score selon :", ['Sexe', 'Rura', 'Card', 'Etud'])
        
    fig_box = plot_boxplot(df, factor_col, score_col, color=factor_col)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Test Statistique
    if st.button(f"Lancer test statistique ({factor_col})"):
        groups = df[factor_col].dropna().unique()
        if len(groups) == 2:
            st.write(f"**T-test** entre {groups[0]} et {groups[1]}")
            x = df[df[factor_col] == groups[0]][score_col]
            y = df[df[factor_col] == groups[1]][score_col]
            res = pg.ttest(x, y)
            st.dataframe(res)
            
            p_val = res['p-val'].values[0]
            if p_val < 0.05:
                st.success(f"Différence significative (p < 0.05) !")
            else:
                st.warning("Pas de différence significative.")
                
        elif len(groups) > 2:
            st.write(f"**ANOVA** entre les groupes : {groups}")
            res = pg.anova(data=df, dv=score_col, between=factor_col)
            st.dataframe(res)
            
            p_val = res['p-unc'].values[0]
            if p_val < 0.05:
                st.success(f"Différence significative (p < 0.05) !")
            else:
                st.warning("Pas de différence significative.")

# --- Section 3 : Corrélations entre aliments ---
st.header("3. Corrélations entre habitudes")

cols_num = [c for c in df.columns if c.endswith('_num')]
corr = df[cols_num].corr()

fig_corr = plot_correlation_heatmap(corr)
st.plotly_chart(fig_corr, use_container_width=True)
