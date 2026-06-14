import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pingouin as pg
import statsmodels.formula.api as smf

from utils.data_loader import load_data, clean_data, get_questions_dict
from utils import analysis as A

st.set_page_config(page_title="Habitudes & scores", page_icon="🍔", layout="wide")
sns.set_theme(style="whitegrid", palette="muted")

st.title("🍔 Habitudes alimentaires & scores de santé")
st.markdown(
    "Que mangent les répondants, et **qui mange le mieux** ? Tests statistiques avec "
    "tailles d'effet, et une régression pour démêler les facteurs."
)

df = clean_data(load_data())
if df is None:
    st.stop()
q = get_questions_dict()

# --- Fréquences ---------------------------------------------------------------
st.subheader("1. Fréquence de consommation par aliment")
conso_cols = [c for c in df.columns if c.startswith("C_") and not c.endswith("_num")]
heat = pd.DataFrame([
    (df[c].value_counts(normalize=True).reindex(A.FREQ_ORDER) * 100).rename(q.get(c, c))
    for c in conso_cols
])
fig, ax = plt.subplots(figsize=(11, 5))
sns.heatmap(heat, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={"label": "% des répondants"}, ax=ax)
ax.set_title("Fréquence de consommation (% en ligne)"); ax.set_xlabel(""); ax.set_ylabel("")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Deux blocs : **légumes, fruits, féculents, laitiers** consommés quotidiennement ; "
    "**viande rouge, poisson, industriels, allégés** rares (45 % ne prennent *jamais* d'allégés)."
)
st.divider()

# --- Scores -------------------------------------------------------------------
st.subheader("2. Le Score Santé")
st.markdown(
    "**Score Santé** = Légumes + Fruits + Poisson − Industriels (fréquences hebdo.). "
    "*Mesure relative* pour comparer des groupes — sa valeur absolue n'a pas de sens clinique "
    "(les manquants sont remplacés par la médiane avant calcul)."
)
col_l, col_r = st.columns([2, 3])
with col_l:
    scores = (df[["Score_Sante", "Score_Carné"]]
              .describe().T[["mean", "std", "min", "50%", "max"]].round(1))
    st.dataframe(scores, width="stretch")
with col_r:
    fig, ax = plt.subplots(figsize=(8, 3.6))
    sns.histplot(df["Score_Sante"], bins=30, kde=True, ax=ax)
    ax.set_title("Distribution du Score Santé"); ax.set_xlabel("Score Santé")
    fig.tight_layout(); st.pyplot(fig)
st.divider()

# --- Tests à 2 groupes --------------------------------------------------------
st.subheader("3. Le score varie-t-il selon le sexe et le territoire ?")
def ttest_row(fac):
    g = df[fac].dropna().unique()
    x = df.loc[df[fac] == g[0], "Score_Sante"]; y = df.loc[df[fac] == g[1], "Score_Sante"]
    r = pg.ttest(x, y, correction=True).iloc[0]
    return {"Facteur": fac, f"groupe A": f"{g[0]} ({x.mean():.1f})", "groupe B": f"{g[1]} ({y.mean():.1f})",
            "p-val": round(r["p-val"], 3), "d de Cohen": round(r["cohen-d"], 3)}
st.dataframe(pd.DataFrame([ttest_row("Sexe"), ttest_row("Rura")]), hide_index=True, width="stretch")
st.markdown(
    "**Surprise : aucune différence significative** (p = 0,085 et 0,06), effets négligeables "
    "(*d* ≈ 0,09). L'idée reçue « les femmes / les ruraux mangent mieux » ne se vérifie pas brut. "
    "Le sexe ressortira *une fois l'âge contrôlé* (§ 5)."
)
st.divider()

# --- Tests à >2 groupes -------------------------------------------------------
st.subheader("4. Score selon l'éducation et la profession")
def anova_row(fac):
    sub = df[[fac, "Score_Sante"]].dropna()
    lev = pg.homoscedasticity(sub, dv="Score_Sante", group=fac)["pval"].values[0]
    wa = pg.welch_anova(sub, dv="Score_Sante", between=fac).iloc[0]
    np2 = pg.anova(sub, dv="Score_Sante", between=fac, detailed=True).loc[0, "np2"]
    return {"Facteur": fac, "Levene p": round(lev, 3), "Welch F": round(wa["F"], 2),
            "p-val": f"{wa['p-unc']:.1e}", "η² (np2)": round(np2, 3)}
st.dataframe(pd.DataFrame([anova_row("Etud"), anova_row("pro")]), hide_index=True, width="stretch")
fig, axes = plt.subplots(1, 2, figsize=(14, 4.6))
sns.boxplot(data=df, x="Etud", y="Score_Sante",
            order=[e for e in A.ETU_ORDER if e in df["Etud"].unique()], ax=axes[0])
axes[0].set_title("Selon le niveau d'étude"); axes[0].set_xlabel("")
order_pro = df.groupby("pro", observed=True)["Score_Sante"].mean().sort_values().index
sns.boxplot(data=df, x="pro", y="Score_Sante", order=order_pro, ax=axes[1])
axes[1].set_title("Selon la profession"); axes[1].set_xlabel(""); axes[1].tick_params(axis="x", rotation=45)
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Effets significatifs mais **modestes** : l'éducation explique ~1 % de la variance "
    "(seul **Bac+5** se détache), la profession 4 % — mais « retraité » (score le plus haut) "
    "est surtout un proxy de l'**âge**. D'où la régression."
)
st.divider()

# --- Corrélations -------------------------------------------------------------
st.subheader("5. Quelles consommations vont ensemble ?")
num_cols = [c for c in df.columns if c.endswith("_num")]
corr = df[num_cols].rename(columns={c: q.get(c[:-4], c) for c in num_cols}).corr(method="spearman")
fig, ax = plt.subplots(figsize=(8.5, 6.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax)
ax.set_title("Corrélations de Spearman entre fréquences")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Deux « mondes » : **fruits ↔ légumes** (ρ = 0,47) et **viandes entre elles** (ρ = 0,47). "
    "Les **industriels sont négativement corrélés aux légumes/fruits** : manger frais et "
    "manger industriel s'excluent partiellement."
)
st.divider()

# --- Régression ---------------------------------------------------------------
st.subheader("6. Régression : l'âge, premier déterminant")
model = smf.ols("Score_Sante ~ C(Sexe) + C(Age) + C(Etud) + C(Rura)", data=df).fit()
coef = pd.DataFrame({"coef.": model.params, "p-val": model.pvalues,
                     "IC 2.5%": model.conf_int()[0], "IC 97.5%": model.conf_int()[1]}).round(3)
st.dataframe(coef, width="stretch")
st.markdown(
    f"**R² = {model.rsquared:.3f}** — le socio-démographique n'explique que ~9 % des écarts. "
    "Mais il clarifie les rôles : **l'âge domine** (les 18-34 ans ~9 points sous les +60 ans), "
    "devant l'**éducation** (Bac+5 +3, Brevet −3) ; le **sexe** devient significatif une fois "
    "l'âge neutralisé (hommes −1) ; le **territoire** reste sans effet."
)

st.info("📄 Analyse détaillée : `reports/02_habitudes.md`")
