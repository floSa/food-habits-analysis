import streamlit as st
import pandas as pd
import prince
import plotly.express as px
from utils.data_loader import load_data, clean_data, get_questions_dict

st.set_page_config(page_title="Sociologie Alimentaire", page_icon="🎓", layout="wide")

st.title("🎓 L'Espace Social Alimentaire (ACM)")

st.markdown("""
**Analyse des Correspondances Multiples (MCA)**
Cette méthode permet de cartographier les individus et les habitudes alimentaires dans un plan en 2 dimensions.
*   Les points proches partagent des profils de consommation similaires.
*   Nous projetons ensuite des variables sociologiques (Âge, Sexe) pour voir comment elles se structurent dans cet espace.
""")

df = load_data()
if df is None:
    st.stop()
df = clean_data(df)
questions = get_questions_dict()

# --- Configuration du modèle ---
st.sidebar.header("Paramètres MCA")

# Variables Actives : Ce qui construit l'espace (Les consommations)
# On prend les variables C_... originales (catégorielles)
active_candidates = [c for c in df.columns if c.startswith('C_') and not c.endswith('_num')]
default_actives = ['C_leg', 'C_frui', 'C_viaR', 'C_viaB', 'C_indu', 'C_poi']
selected_actives = st.sidebar.multiselect("Variables Actives (Consommations)", active_candidates, default=default_actives)

# Variables Illustratives : Pour colorer/interpréter (Socio-démographie)
illustrative_candidates = ['Sexe', 'Age', 'Rura', 'Card', 'pro', 'Etud', 'Regime_B']
selected_illustrative = st.sidebar.selectbox("Variable Illustrative (Couleur)", illustrative_candidates)

if len(selected_actives) < 3:
    st.warning("Veuillez sélectionner au moins 3 variables actives pour lancer l'analyse.")
    st.stop()

# --- Calcul MCA ---
with st.spinner("Calcul de l'ACM en cours avec Prince..."):
    # Préparation données : Prince n'aime pas les NaNs
    X = df[selected_actives].fillna("Non répondu")
    
    mca = prince.MCA(
        n_components=2,
        n_iter=3,
        copy=True,
        check_input=True,
        engine='sklearn',
        random_state=42
    )
    
    mca = mca.fit(X)
    
    # Coordonnées des individus
    row_coords = mca.row_coordinates(X)
    row_coords.columns = ['Axe 1', 'Axe 2']
    
    # Ajout des infos illustratives pour le plot
    plot_data = pd.concat([row_coords, df[illustrative_candidates]], axis=1)

# --- Visualisation ---

c1, c2 = st.columns([3, 1])

with c1:
    st.subheader("Plan Factoriel des Individus")
    fig = px.scatter(
        plot_data, 
        x='Axe 1', 
        y='Axe 2', 
        color=selected_illustrative,
        title=f"Projection des individus colorée par {selected_illustrative}",
        opacity=0.6,
        hover_data=illustrative_candidates
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Inertie expliquée")
    eigenvalues = mca.eigenvalues_summary
    st.dataframe(eigenvalues.head(5))
    st.info(f"Inertie totale plan 1-2 : {mca.percentage_of_variance_[0] + mca.percentage_of_variance_[1]:.1f}%")

st.markdown("---")
st.subheader("Variables dans l'Espace")

# Coordonnées des colonnes (modalités)
col_coords = mca.column_coordinates(X)
col_coords.columns = ['Axe 1', 'Axe 2']
col_coords['Variable'] = col_coords.index

fig_col = px.scatter(
    col_coords, 
    x='Axe 1', 
    y='Axe 2', 
    text='Variable', 
    title="Plan des Modalités (Réponses)",
)
fig_col.update_traces(textposition='top center')
st.plotly_chart(fig_col, use_container_width=True)
