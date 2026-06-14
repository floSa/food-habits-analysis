import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import prince
from scipy.stats import spearmanr

from utils.data_loader import load_data, clean_data
from utils import analysis as A

st.set_page_config(page_title="Sociologie (ACM)", page_icon="🎓", layout="wide")
sns.set_theme(style="whitegrid", palette="muted")

st.title("🎓 L'espace social alimentaire (ACM)")
st.markdown(
    "L'**Analyse des Correspondances Multiples** projette individus et habitudes dans un plan : "
    "les habitudes qui « vont ensemble » se retrouvent proches. Construit sur les **consommations**."
)

df = clean_data(load_data())
if df is None:
    st.stop()

X = df[A.ACM_ACTIVES].fillna("Non répondu")
K = len(A.ACM_ACTIVES)
mca = prince.MCA(n_components=5, n_iter=10, random_state=42).fit(X)
coords = mca.column_coordinates(X)
contr = mca.column_contributions_ * 100
ben = A.benzecri_percentages(mca.eigenvalues_, K)

# --- Inertie / Benzécri -------------------------------------------------------
st.subheader("1. Inertie : pourquoi corriger (Benzécri)")
col_l, col_r = st.columns([3, 2])
with col_l:
    bz = pd.DataFrame({
        "Axe": [f"Axe {i+1}" for i in range(len(ben))],
        "% brut": np.round(mca.percentage_of_variance_, 2),
        "% Benzécri": np.round(ben, 1),
        "% Benzécri cumulé": np.round(np.cumsum(ben), 1),
    })
    st.dataframe(bz, hide_index=True, width="stretch")
with col_r:
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.bar([f"A{i+1}" for i in range(len(ben))], ben, color="#4C72B0")
    ax.set_ylabel("% inertie (Benzécri)"); ax.set_title("Éboulis corrigé")
    fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Les % bruts (~4,9 %) sont un **artefact de l'ACM**. Après **correction de Benzécri**, le "
    "**plan 1-2 capte ≈ 62 %** de l'inertie : une lecture en deux dimensions est fiable."
)
st.divider()

# --- Plan des modalités -------------------------------------------------------
st.subheader("2. Le plan des modalités")
fig, ax = plt.subplots(figsize=(11, 7.5))
palette = dict(zip(A.ACM_ACTIVES, sns.color_palette("tab10", K)))
for idx in coords.index:
    var, mod = idx.split("__")
    ax.scatter(coords.loc[idx, 0], coords.loc[idx, 1], color=palette[var], s=30)
    ax.annotate(f"{A.ALIMENT_SHORT[var]}={A.FREQ_SHORT.get(mod, mod)}",
                (coords.loc[idx, 0], coords.loc[idx, 1]), fontsize=7, alpha=0.85)
ax.axhline(0, color="grey", lw=0.6); ax.axvline(0, color="grey", lw=0.6)
ax.set_xlabel(f"Axe 1 ({ben[0]:.0f} %)"); ax.set_ylabel(f"Axe 2 ({ben[1]:.0f} %)")
ax.set_title("Plan factoriel des modalités de consommation")
ax.legend(handles=[plt.Line2D([0], [0], marker="o", ls="", color=palette[v], label=A.ALIMENT_FULL[v])
                   for v in A.ACM_ACTIVES], fontsize=8, loc="upper right")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Toutes les modalités **« Jamais »** se regroupent à droite : l'**axe 1** isole une minorité "
    "déclarant ne (presque) rien consommer (axe de **non-consommation**). Les fréquences élevées "
    "de viande et de poisson s'étirent vers le haut : l'**axe 2** est l'**intensité carnée**."
)
st.divider()

# --- Contributions ------------------------------------------------------------
st.subheader("3. Interprétation par les contributions")
def top_contrib(ax_i, n=8):
    top = contr[ax_i].sort_values(ascending=False).head(n)
    return pd.DataFrame({
        "Modalité": [f"{A.ALIMENT_FULL[i.split('__')[0]]} = {i.split('__')[1]}" for i in top.index],
        "Contribution %": top.values.round(1),
        "Coordonnée": [round(coords.loc[i, ax_i], 2) for i in top.index],
    })
c1, c2 = st.columns(2)
c1.markdown("**Axe 1 — non-consommation**"); c1.dataframe(top_contrib(0), hide_index=True, width="stretch")
c2.markdown("**Axe 2 — intensité carnée**"); c2.dataframe(top_contrib(1), hide_index=True, width="stretch")
st.divider()

# --- Individus ----------------------------------------------------------------
st.subheader("4. Profils sociaux et Score Santé dans l'espace")
rc = mca.row_coordinates(X).rename(columns={0: "Axe1", 1: "Axe2"})
proj = pd.concat([rc[["Axe1", "Axe2"]], df[["Age", "Score_Sante"]].reset_index(drop=True)], axis=1)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
sns.scatterplot(data=proj, x="Axe1", y="Axe2", hue="Age", hue_order=A.AGE_ORDER,
                alpha=0.5, s=16, ax=axes[0]); axes[0].set_title("Coloré par âge")
sc = axes[1].scatter(proj["Axe1"], proj["Axe2"], c=proj["Score_Sante"], cmap="viridis", alpha=0.6, s=16)
axes[1].set_title("Coloré par Score Santé"); axes[1].set_xlabel("Axe1"); axes[1].set_ylabel("Axe2")
fig.colorbar(sc, ax=axes[1], label="Score Santé")
for a in axes:
    a.axhline(0, color="grey", lw=0.5); a.axvline(0, color="grey", lw=0.5)
fig.tight_layout(); st.pyplot(fig)
r1 = spearmanr(proj["Axe1"], proj["Score_Sante"]).statistic
r2 = spearmanr(proj["Axe2"], proj["Score_Sante"]).statistic
st.markdown(
    f"Les deux axes corrèlent modérément avec le Score Santé (ρ ≈ {r1:.2f} et {r2:.2f}). Mais "
    "les nuages par âge se **recouvrent largement** : aucune tranche n'occupe une région propre."
)

st.success(
    "**Point clé** : l'espace de consommation est **faiblement structuré socialement** — on ne "
    "déduit pas l'assiette de la position sociale. Cela converge avec la régression (≈ 9 %). "
    "La piste suivante n'est plus sociale mais **cognitive** → page Croyances."
)
st.info("📄 Analyse détaillée : `reports/03_sociologie_acm.md`")
