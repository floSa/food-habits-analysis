import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import prince

from utils.data_loader import load_data, clean_data
from utils import analysis as A

st.set_page_config(page_title="Population", page_icon="👥", layout="wide")
sns.set_theme(style="whitegrid", palette="muted")

st.title("👥 Population — qui sont les répondants ?")
st.markdown(
    "Avant d'interpréter *ce que les gens mangent*, il faut savoir **qui** a répondu. "
    "On en tire les **limites de représentativité** valables pour toute l'analyse."
)

df = clean_data(load_data())
if df is None:
    st.stop()
n = len(df)

# --- KPIs ---------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Répondants", f"{n:,}".replace(",", " "))
c2.metric("Femmes", f"{df['Sexe'].eq('Femme').mean()*100:.0f} %")
c3.metric("Zone rurale", f"{df['Rura'].eq('Rural').mean()*100:.0f} %")
c4.metric("Régime spécifique", f"{df['Regime_B'].eq('Oui').mean()*100:.0f} %")
st.divider()

# --- Sexe & âge ---------------------------------------------------------------
st.subheader("Sexe et âge")
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
sns.countplot(data=df, x="Sexe", ax=axes[0], order=df["Sexe"].value_counts().index)
axes[0].set_title("Sexe"); axes[0].set_xlabel(""); axes[0].set_ylabel("Effectif")
sns.countplot(data=df, x="Age", ax=axes[1], order=A.AGE_ORDER)
axes[1].set_title("Tranche d'âge"); axes[1].set_xlabel(""); axes[1].set_ylabel("Effectif")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Près de **trois répondants sur quatre sont des femmes**, et la tranche **18-34 ans "
    "concentre 64 %** de l'échantillon (95 % ont entre 18 et 60 ans). Population jeune et "
    "adulte active, pas un échantillon tous âges."
)
st.divider()

# --- Géographie ---------------------------------------------------------------
st.subheader("Répartition géographique")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
sns.countplot(data=df, x="Card", ax=axes[0]); axes[0].set_title("Zone (Nord/Sud)"); axes[0].set_xlabel(""); axes[0].set_ylabel("Effectif")
sns.countplot(data=df, x="Rura", ax=axes[1]); axes[1].set_title("Type de zone"); axes[1].set_xlabel(""); axes[1].set_ylabel("Effectif")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Collecte **fortement concentrée dans le Sud** (≈ 79 %) et plutôt **citadine** (≈ 61 %). "
    "Tout effet « géographique » est à lire avec ce déséquilibre en tête."
)
st.divider()

# --- CSP & étude --------------------------------------------------------------
st.subheader("Catégorie socio-professionnelle et niveau d'étude")
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
sns.countplot(data=df, y="pro", ax=axes[0], order=df["pro"].value_counts().index)
axes[0].set_title("CSP"); axes[0].set_xlabel("Effectif"); axes[0].set_ylabel("")
sns.countplot(data=df, x="Etud", ax=axes[1], order=[e for e in A.ETU_ORDER if e in df["Etud"].unique()])
axes[1].set_title("Niveau d'étude"); axes[1].set_xlabel(""); axes[1].set_ylabel("Effectif")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Salariés et étudiants dominent. Surtout, l'échantillon est **très diplômé** : près de "
    "**72 % ont au moins un Bac+3** — un biais qui pèse sur les connaissances et pratiques observées."
)
st.divider()

# --- Pyramide âge × sexe ------------------------------------------------------
st.subheader("Croisement âge × sexe")
col_g, col_t = st.columns([3, 2])
with col_g:
    fig, ax = plt.subplots(figsize=(8, 4.6))
    sns.countplot(data=df, x="Age", hue="Sexe", order=A.AGE_ORDER, ax=ax)
    ax.set_title("Pyramide des âges par sexe"); ax.set_xlabel(""); ax.set_ylabel("Effectif")
    fig.tight_layout(); st.pyplot(fig)
with col_t:
    st.markdown("**Effectifs**")
    st.dataframe(pd.crosstab(df["Age"], df["Sexe"]).reindex(A.AGE_ORDER), width="stretch")
st.markdown(
    "La surreprésentation féminine se vérifie **dans toutes les tranches d'âge** : un biais "
    "transversal, pas l'effet d'une classe d'âge."
)
st.divider()

# --- Régimes ------------------------------------------------------------------
st.subheader("Régimes alimentaires particuliers")
regimes = {
    "Régime spécifique": int(df["Regime_B"].eq("Oui").sum()),
    "Végétarien": int(df["végétarien"].sum()),
    "Diabétique": int(df["diabétique"].sum()),
    "Sans gluten": int(df["gluten"].sum()),
}
reg_df = pd.DataFrame({"Régime": list(regimes), "Effectif": list(regimes.values())})
reg_df["% échantillon"] = (reg_df["Effectif"] / n * 100).round(1)
col_g, col_t = st.columns([3, 2])
with col_g:
    fig, ax = plt.subplots(figsize=(8, 3.6))
    sns.barplot(data=reg_df, y="Régime", x="Effectif", ax=ax)
    ax.set_title("Régimes déclarés"); ax.set_xlabel("Effectif"); ax.set_ylabel("")
    fig.tight_layout(); st.pyplot(fig)
with col_t:
    st.dataframe(reg_df, hide_index=True, width="stretch")
st.markdown(
    "Le **végétarisme** (≈ 8 %) devance largement les contraintes médicales (~1 % chacune) — "
    "à garder en tête pour l'analyse des consommations de viande."
)
st.divider()

# --- ACM démographique --------------------------------------------------------
st.subheader("Cartographie des profils (ACM démographique)")
DEMO = ["Sexe", "Age", "Rura", "Card", "Etud", "pro"]
Xd = df[DEMO].astype(str).fillna("NR")
mca_d = prince.MCA(n_components=4, random_state=42).fit(Xd)
ben = A.benzecri_percentages(mca_d.eigenvalues_, len(DEMO))
coords_d = mca_d.column_coordinates(Xd)

fig, ax = plt.subplots(figsize=(10, 6.5))
palette = dict(zip(DEMO, sns.color_palette("tab10", len(DEMO))))
for idx in coords_d.index:
    var, mod = idx.split("__")
    ax.scatter(coords_d.loc[idx, 0], coords_d.loc[idx, 1], color=palette[var], s=35)
    ax.annotate(mod, (coords_d.loc[idx, 0], coords_d.loc[idx, 1]), fontsize=8)
ax.axhline(0, color="grey", lw=0.6); ax.axvline(0, color="grey", lw=0.6)
ax.set_xlabel(f"Axe 1 ({ben[0]:.0f} %)"); ax.set_ylabel(f"Axe 2 ({ben[1]:.0f} %)")
ax.set_title("ACM des variables socio-démographiques (inertie corrigée Benzécri)")
ax.legend(handles=[plt.Line2D([0], [0], marker="o", ls="", color=palette[v], label=v) for v in DEMO], fontsize=8)
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "L'espace socio-démographique est **fortement structuré** (plan 1-2 ≈ 89 % d'inertie "
    "corrigée) et se résume surtout à un **gradient d'âge** : retraités/+60 ans d'un côté, "
    "étudiants/18-34 de l'autre (âge et profession se confondent). À retenir : cet axe d'âge "
    "ne suffira pourtant pas à expliquer les *assiettes* (voir page Sociologie)."
)

st.info("📄 Analyse détaillée : `reports/01_population.md`")
