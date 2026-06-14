import streamlit as st

from utils.data_loader import load_data, clean_data
from utils import analysis as A

st.set_page_config(page_title="Enquête Alimentation", page_icon="🍎", layout="wide")

df = clean_data(load_data())

# --- En-tête ------------------------------------------------------------------
st.title("🍎 Habitudes & dynamiques alimentaires")
st.markdown(
    "Présentation interactive de l'analyse d'une **enquête déclarative** sur les habitudes "
    "alimentaires, les croyances nutritionnelles et leurs déterminants sociologiques."
)

if df is None:
    st.error("Impossible de charger les données. Vérifiez `data/enquete_alimentation.csv`.")
    st.stop()

# --- Chiffres de cadrage ------------------------------------------------------
df_pub = A.add_pub_influence(df)
n = len(df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Répondants", f"{n:,}".replace(",", " "))
c2.metric("Femmes", f"{df['Sexe'].eq('Femme').mean()*100:.0f} %")
c3.metric("18-34 ans", f"{df['Age'].eq('18-34').mean()*100:.0f} %")
c4.metric("Bac+3 ou plus", f"{df['Etud'].isin(['Bac+3','Bac +5']).mean()*100:.0f} %")
c5.metric("Influencés par la pub", f"{df_pub['pub_influence'].eq('Influencé').mean()*100:.0f} %")

st.caption(
    "⚠️ Échantillon **non représentatif** : femmes, 18-34 ans, diplômés du supérieur et "
    "Sud sont surreprésentés. Les résultats valent d'abord *au sein de cet échantillon*."
)

st.divider()

# --- Le projet ----------------------------------------------------------------
left, right = st.columns([3, 2])

with left:
    st.subheader("Le projet")
    st.markdown(
        """
Cette application est la **vitrine interactive** d'une analyse menée en cinq volets. Chaque
page de la barre latérale correspond à un volet et présente les graphiques, les tests
statistiques et leur **interprétation**.

L'analyse de référence (avec le code) vit dans les **notebooks** du dépôt ; les **rapports**
sans code (`reports/`) en sont la version lisible et partageable.
"""
    )

    st.subheader("Les cinq analyses")
    st.markdown(
        """
| # | Page | Question |
|---|---|---|
| 1 | 👥 **Population** | Qui sont les répondants ? |
| 2 | 🍔 **Habitudes & scores** | Que mangent-ils, et qui mange le mieux ? |
| 3 | 🎓 **Sociologie (ACM)** | Les habitudes sont-elles socialement structurées ? |
| 4 | 🧠 **Croyances & pratiques** | Savoir, est-ce manger mieux ? |
| 5 | 🛒 **Marketing & choix** | Qu'est-ce qui guide l'achat ? |
"""
    )
    st.caption("👈 Naviguez via la barre latérale.")

with right:
    st.subheader("🔑 Résultats phares")
    with st.expander("L'âge, premier déterminant de la qualité alimentaire", expanded=True):
        st.markdown(
            "Ni le sexe ni le territoire ne font de différence brute sur le *Score Santé* ; "
            "une régression montre que **l'âge** est le facteur dominant (les plus jeunes ont "
            "les scores les plus bas). Le socio-démographique n'explique que **~9 %** des écarts."
        )
    with st.expander("Savoir ≠ faire : le levier est le passage à l'acte"):
        st.markdown(
            "Les connaissances nutritionnelles sont **solides et indépendantes du diplôme**, "
            "mais ne corrèlent que faiblement avec la pratique. Ceux qui **appliquent** la règle "
            "des « 5 fruits et légumes » mangent bien mieux que ceux qui la connaissent sans "
            "l'appliquer (*d* ≈ 1,0, l'effet le plus fort de l'étude)."
        )
    with st.expander("La pub pousse (discrètement) vers les produits industriels"):
        st.markdown(
            "Seuls 5 % s'avouent sensibles au marketing, mais un quart reconnaît des achats sous "
            "influence publicitaire — et ce groupe consomme significativement plus de **produits "
            "industriels** (*d* ≈ 0,5)."
        )

st.divider()

# --- Méthode & données --------------------------------------------------------
with st.expander("ℹ️ Données & méthodologie"):
    st.markdown(
        f"""
**Données** — {n} répondants, 51 variables, enquête déclarative (consommations, croyances,
socio-démographie). Nettoyage et scores : `utils/data_loader.py` ; calculs d'analyse
partagés app/notebooks : `utils/analysis.py`.

**Méthodes** — statistiques avec **pingouin** (t-test / ANOVA de Welch, tailles d'effet,
post-hoc Games-Howell), **statsmodels** (régression OLS), **prince** (ACM avec correction
de Benzécri), nuage de mots (**wordcloud**).

**Aperçu des données brutes :**
"""
    )
    st.dataframe(df.head(), width="stretch")
