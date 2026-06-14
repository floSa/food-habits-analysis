import streamlit as st
import plotly.express as px
from utils.data_loader import load_data, clean_data, get_questions_dict
from utils.plotting import plot_distribution

st.set_page_config(page_title="Marketing & Choix", page_icon="🛒", layout="wide")

st.title("🛒 Marketing & Déterminants d'Achat")

df = load_data()
if df is None:
    st.stop()
df = clean_data(df)
questions = get_questions_dict()

# Variables d'intérêt
marketing_vars = ['Crit_influe_C', 'Choix', 'Etiqt', 'Pub']

selected_var = st.selectbox("Variable à analyser", marketing_vars, format_func=lambda x: f"{x} - {questions.get(x, x)[:50]}...")

st.info(f"Question complète : {questions.get(selected_var)}")

# Analyse Croisée (Pivot)
c1, c2 = st.columns(2)

with c1:
    st.subheader("Distribution Globale")
    # Pour 'Crit_influe_C', c'est souvent multi-choix séparé par virgule ? Faut vérifier.
    # Dans une v1 simple, on plot tel quel.
    fig = plot_distribution(df, selected_var)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Influence du Profil")
    cross_var = st.selectbox("Croiser avec :", ['Sexe', 'Age', 'CSP (pro)', 'Rura'])
    mapping_profile = {'CSP (pro)': 'pro'}
    real_cross_var = mapping_profile.get(cross_var, cross_var)
    
    fig_cross = plot_distribution(df, selected_var, color=real_cross_var)
    st.plotly_chart(fig_cross, use_container_width=True)

st.markdown("---")

st.header("Focus Publicité")
# Focus Pub x Consommation Indus
if 'Pub' in df.columns:
    st.markdown("""
    ### L'influence de la Publicité sur la "Malbouffe"
    Ce graphique cherche à vérifier une hypothèse : **Les personnes qui admettent acheter des produits à cause de la publicité consomment-elles plus de produits industriels ?**
    
    *   **Oui** : Signifie que la personne a déclaré acheter sous influence de la pub.
    *   **Non** : Signifie que la personne déclare ne pas être influencée.
    """)
    
    # 'Pub' semble être Oui/Non ou similaire.
    if 'C_indu_num' in df.columns:
        fig_pub = px.box(df, x='Pub', y='C_indu_num', title="Niveau de consommation de Produits Industriels selon l'Influence Publicitaire", color='Pub')
        st.plotly_chart(fig_pub, use_container_width=True)
