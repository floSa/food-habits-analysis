import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pingouin as pg
from scipy.stats import spearmanr

from utils.data_loader import load_data, clean_data
from utils import analysis as A

st.set_page_config(page_title="Croyances & pratiques", page_icon="🧠", layout="wide")
sns.set_theme(style="whitegrid", palette="muted")

st.title("🧠 Croyances, connaissances et pratiques")
st.markdown(
    "Les habitudes se déduisent mal du social. Reste la piste **cognitive** : les gens qui "
    "**savent** mangent-ils mieux ? Spoiler — le levier n'est pas le savoir, c'est le **faire**."
)

df = clean_data(load_data())
if df is None:
    st.stop()
df = A.add_knowledge_score(df)

# --- Idées reçues -------------------------------------------------------------
st.subheader("1. Quelles idées reçues résistent ?")
res = A.belief_correct_rates(df)
colors = ["#C44E52" if p < 50 else "#DD8452" if p < 75 else "#55A868" for p in res["% correct"]]
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.barh(res["Idée reçue"], res["% correct"], color=colors)
ax.axvline(50, color="grey", ls="--", lw=1); ax.set_xlim(0, 100); ax.set_xlabel("% de bonnes réponses")
ax.set_title("Taux de bonnes réponses par idée reçue")
for y, p in enumerate(res["% correct"]):
    ax.text(p + 1, y, f"{p:.0f}%", va="center", fontsize=9)
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Les mythes « moraux » sont déjoués (sauter un repas 95 %, équilibré = privation 90-94 %). "
    "Mais **le sucre roux** n'est rejeté que par **31 %**, et le **régime méditerranéen** (55 %) "
    "comme **manger léger le soir** (58 %) sont mal connus. Connaissances **inégales selon le sujet**."
)
st.divider()

# --- Score de connaissance ----------------------------------------------------
st.subheader("2. Score de connaissance & niveau d'étude")
aov = pg.welch_anova(df.dropna(subset=["Etud"]), dv="Score_Connaissance", between="Etud").iloc[0]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
sns.histplot(df["Score_Connaissance"], bins=range(0, 11), ax=axes[0])
axes[0].set_title("Score de connaissance (/9)"); axes[0].set_xlabel("Score")
sns.boxplot(data=df, x="Etud", y="Score_Connaissance",
            order=[e for e in A.ETU_ORDER if e in df["Etud"].unique()], ax=axes[1])
axes[1].set_title("Selon le niveau d'étude"); axes[1].set_xlabel("")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    f"Score moyen élevé (**{df['Score_Connaissance'].mean():.1f}/9**). Surtout, **le diplôme ne "
    f"fait aucune différence** (ANOVA de Welch p = {aov['p-unc']:.2f}) : la culture nutritionnelle "
    "ne se distribue pas comme le capital scolaire."
)
st.divider()

# --- Savoir vs pratique -------------------------------------------------------
st.subheader("3. Savoir, est-ce manger mieux ?")
r = spearmanr(df["Score_Connaissance"], df["Score_Sante"])
fig, ax = plt.subplots(figsize=(9, 4.4))
sns.boxplot(data=df, x="Score_Connaissance", y="Score_Sante", color="#4C72B0", ax=ax)
ax.set_title("Score Santé selon le score de connaissance"); ax.set_xlabel("Connaissance (/9)"); ax.set_ylabel("Score Santé")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    f"Relation **positive mais faible** (ρ = {r.statistic:.2f}). La connaissance n'explique "
    "presque rien des écarts de pratique : tout l'écart entre *savoir* et *faire*."
)
st.divider()

# --- Le vrai clivage : appliquer ----------------------------------------------
st.subheader("4. Le vrai clivage : appliquer, pas seulement savoir")
df["app_5fj"] = df["5fj"].apply(A.classify_5fj)
g = df.dropna(subset=["app_5fj"])
ordre = [o for o in ["Ne connaît pas", "Connaît, n'applique pas", "Connaît seulement", "Applique / essaie"]
         if o in g["app_5fj"].unique()]
a = g.loc[g["app_5fj"] == "Applique / essaie", "Score_Sante"]
b = g.loc[g["app_5fj"] == "Connaît, n'applique pas", "Score_Sante"]
tt = pg.ttest(a, b, correction=True).iloc[0]
fig, ax = plt.subplots(figsize=(9, 4.4))
sns.boxplot(data=g, x="app_5fj", y="Score_Sante", order=ordre, ax=ax)
ax.set_title("Score Santé selon le rapport à la règle des « 5 fruits et légumes »")
ax.set_xlabel(""); ax.tick_params(axis="x", rotation=15)
fig.tight_layout(); st.pyplot(fig)
st.success(
    f"**L'écart décisif** : « applique / essaie » (moy. {a.mean():.1f}) vs « connaît mais "
    f"n'applique pas » (moy. {b.mean():.1f}) → **d de Cohen = {tt['cohen-d']:.2f}** (effet large, "
    "l'un des plus forts de l'étude). Presque tout le monde *connaît* la règle ; ce qui distingue "
    "les bons mangeurs, c'est la **mise en pratique**, pas l'information."
)

# --- Conscience ---------------------------------------------------------------
col1, col2 = st.columns(2)
col1.metric("Pense que l'alimentation cause des pathologies", f"{(df['A_patho']=='Oui').mean()*100:.0f} %")
col2.metric("Pense que l'alimentation impacte la santé", f"{(df['A_sante']=='Oui').mean()*100:.0f} %")
st.caption(
    "La conscience du lien alimentation-santé est **quasi universelle**. Le problème n'est ni la "
    "sensibilisation ni l'ignorance des grands principes — c'est le passage du savoir à l'acte. "
    "**Implication** : informer ne suffit pas, il faut agir sur le passage à l'acte."
)
st.info("📄 Analyse détaillée : `reports/04_croyances_pratiques.md`")
