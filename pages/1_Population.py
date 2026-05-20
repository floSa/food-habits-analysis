import streamlit as st
import plotly.express as px
import pandas as pd
import prince
from utils.data_loader import load_data, clean_data
from utils.plotting import plot_distribution

st.set_page_config(page_title="Population", page_icon="👥", layout="wide")

st.title("👥 Qui sont les répondants ?")

# Chargement des données
df = load_data()
if df is None:
    st.error("Erreur lors du chargement des données.")
    st.stop()

df = clean_data(df)

# Sidebar filters (Global pour la page)
# Sidebar filters (Global pour la page) -> RETIRÉ sur demande
# st.sidebar.header("Filtres")
# selected_sexe = st.sidebar.multiselect("Sexe", options=df['Sexe'].unique(), default=df['Sexe'].unique())
# df_filtered = df[df['Sexe'].isin(selected_sexe)]
df_filtered = df # On garde tout le monde

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Nombre de répondants", df_filtered.shape[0])
# Calcul sécurisé du mode pour éviter le crash si df_filtered est vide
age_mode = df_filtered['Age'].mode()
val_mode_age = age_mode[0] if not age_mode.empty else "N/A"
col2.metric("Âge médian (groupe)", val_mode_age)
# Calcul sécurisé Zone Rurale
if df_filtered.shape[0] > 0:
    pct_rural = round(df_filtered[df_filtered['Rura'] == 'Rural'].shape[0] / df_filtered.shape[0] * 100, 1)
else:
    pct_rural = 0
col3.metric("Zone Rurale", f"{pct_rural} %")

st.markdown("---")

# Layout graphiques
c1, c2 = st.columns(2)

with c1:
    st.subheader("Répartition par Âge")
    fig_age = plot_distribution(df_filtered, 'Age', color='Sexe', order=['-18', '18-34', '35-60', '+60'])
    st.plotly_chart(fig_age, use_container_width=True)

with c2:
    st.subheader("Répartition Géographique (Card)")
    fig_card = plot_distribution(df_filtered, 'Card', color='Rura')
    st.plotly_chart(fig_card, use_container_width=True)

st.markdown("---")

c3, c4 = st.columns(2)

with c3:
    st.subheader("Situation Professionnelle")
    fig_pro = plot_distribution(df_filtered, 'pro')
    st.plotly_chart(fig_pro, use_container_width=True)

with c4:
    st.subheader("Niveau d'Étude")
    fig_etud = plot_distribution(df_filtered, 'Etud')
    st.plotly_chart(fig_etud, use_container_width=True)

st.markdown("---")
st.subheader("Analyse des Correspondances Multiples (ACM)")

# Variables Démographiques pour l'ACM
demo_vars = ['Sexe', 'Age', 'Rura', 'Card', 'Etud', 'pro']
available_vars = [c for c in demo_vars if c in df_filtered.columns]

if len(available_vars) > 1:
    # Préparation des données
    X = df_filtered[available_vars].astype(str).fillna("Non renseigné")
    
    try:
        # Configuration et Fit MCA
        mca = prince.MCA(
            n_components=2,
            n_iter=3,
            copy=True,
            check_input=True,
            engine='sklearn',
            random_state=42
        )
        mca = mca.fit(X)
        
        # Récupération des coordonnées des colonnes (modalités)
        coords = mca.column_coordinates(X)
        
        # Création du DataFrame pour Plotly
        coords_reset = coords.reset_index()
        coords_reset.columns = ['Variable_Modalité', 'Composante 1', 'Composante 2']
        
        # Ajout d'une colonne pour colorer selon la variable d'origine (Hack basé sur le nom généralement "Variable_Valeur")
        # Ici Prince renvoie souvent "Variable_Valeur". 
        # Si Prince renvoie juste la valeur, c'est plus dur. Prince v0.7+ fait prefix_sep='_' par defaut si je ne m'abuse ou garde le nom.
        # Vérifions : Prince concatène souvent [ColName]_[Value].
        # On va créer une colonne Groupe pour la couleur
        coords_reset['Groupe'] = coords_reset['Variable_Modalité'].apply(lambda x: x.split('_')[0] if '_' in x else 'Autre')

        # Visualisation
        fig_mca = px.scatter(
            coords_reset, 
            x='Composante 1', 
            y='Composante 2', 
            color='Groupe',
            text='Variable_Modalité',
            title="Carte des Profils (ACM - Variables Démographiques)",
            hover_data=['Variable_Modalité']
        )
        
        fig_mca.update_traces(textposition='top center', marker=dict(size=10))
        fig_mca.update_layout(height=600)
        
        st.plotly_chart(fig_mca, use_container_width=True)
        
        with st.expander("Voir l'inertie expliquée"):
             eigenvalues = mca.eigenvalues_summary
             st.dataframe(eigenvalues)

    except Exception as e:
        st.error(f"Erreur lors du calcul de l'ACM : {e}")
else:
    st.info("Pas assez de données démographiques pour l'ACM.")
