import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pingouin as pg
from wordcloud import WordCloud

from utils.data_loader import load_data, clean_data
from utils import analysis as A

st.set_page_config(page_title="Marketing & choix", page_icon="🛒", layout="wide")
sns.set_theme(style="whitegrid", palette="muted")

st.title("🛒 Déterminants du choix & influence marketing")
st.markdown(
    "Le levier, c'est le **passage à l'acte** — et cet acte est d'abord un achat. Qu'est-ce qui "
    "guide le choix : goût, prix, santé… et la **publicité** (souvent niée) ?"
)

df = clean_data(load_data())
if df is None:
    st.stop()

# --- Critères de choix --------------------------------------------------------
st.subheader("1. Qu'est-ce qui guide le choix alimentaire ?")
c1, c2 = st.columns(2)
with c1:
    crit = A.multi_pct(df, "Crit_influe_C")
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(crit.index, crit.values, color="#55A868"); ax.set_xlim(0, 75); ax.set_xlabel("% de répondants")
    ax.set_title("Critères de choix")
    for y, p in enumerate(crit.values):
        ax.text(p + 0.5, y, f"{p:.0f}%", va="center", fontsize=9)
    fig.tight_layout(); st.pyplot(fig)
with c2:
    choix = A.multi_pct(df, "Choix")
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(choix.index, choix.values, color="#4C72B0"); ax.set_xlim(0, 75); ax.set_xlabel("% de répondants")
    ax.set_title("Arbitrage entre deux produits")
    for y, p in enumerate(choix.values):
        ax.text(p + 0.5, y, f"{p:.0f}%", va="center", fontsize=9)
    fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "Le **goût** prime (65 %) devant la santé (50 %) et le prix (40 %) ; mais **en rayon, c'est "
    "le prix qui tranche** (62 %). Seuls **5 % admettent se fier au marketing** — dénégation que "
    f"la suite met à l'épreuve. ({(df['Pd_Frais']=='Oui').mean()*100:.0f} % se disent attentifs aux produits frais.)"
)
st.divider()

# --- Publicité ----------------------------------------------------------------
st.subheader("2. L'influence de la publicité")
df = A.add_pub_influence(df)
cats = A.pub_category_rates(df)
c1, c2 = st.columns(2)
with c1:
    share = df["pub_influence"].value_counts(normalize=True) * 100
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.pie(share, labels=share.index, autopct="%.0f%%", colors=["#C44E52", "#CCCCCC"])
    ax.set_title("Achat déjà influencé par la pub ?")
    fig.tight_layout(); st.pyplot(fig)
with c2:
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.barh(cats.index, cats.values, color="#C44E52"); ax.set_xlabel("% des influencés")
    ax.set_title("Sur quels produits ?")
    for y, p in enumerate(cats.values):
        ax.text(p + 0.8, y, f"{p:.0f}%", va="center", fontsize=9)
    fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "**Un quart** reconnaît un achat sous influence pub (bien plus que les 5 % du § 1), et "
    "lorsque la pub agit, c'est massivement sur les **produits industriels** (63 %)."
)
st.divider()

# --- Hypothèse pub -> industriels --------------------------------------------
st.subheader("3. La pub pousse-t-elle vers la « malbouffe » ?")
a = df.loc[df["pub_influence"] == "Influencé", "C_indu_num"].dropna()
b = df.loc[df["pub_influence"] == "Non influencé", "C_indu_num"].dropna()
tt = pg.ttest(a, b, correction=True).iloc[0]
fig, ax = plt.subplots(figsize=(7, 4.2))
sns.boxplot(data=df.dropna(subset=["pub_influence"]), x="pub_influence", y="C_indu_num",
            order=["Non influencé", "Influencé"], ax=ax)
ax.set_title("Produits industriels selon l'influence de la pub"); ax.set_xlabel("")
ax.set_ylabel("Fréquence hebdo. industriels")
fig.tight_layout(); st.pyplot(fig)
st.success(
    f"**Hypothèse confirmée** : les personnes sensibles à la pub consomment plus de produits "
    f"industriels ({a.mean():.2f} vs {b.mean():.2f}/semaine ; **d de Cohen = {tt['cohen-d']:.2f}**, "
    f"p = {tt['p-val']:.1e}). Presque personne ne se *croit* influençable, mais l'influence se "
    "**lit dans les assiettes**."
)
st.divider()

# --- Wordcloud ----------------------------------------------------------------
st.subheader("4. Comment se représente-t-on « manger équilibré » ?")
STOP = set("""au aux avec ce ces dans de des du elle en et eux il je la le les leur lui ma mais me
meme mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur ta te tes toi
ton tu un une vos votre vous c d j l a m n s t y est plus tout tous toute toutes faire fait
manger mange plutot tres trop bien aussi sans aller etre avoir cela ca quand comme chaque
quantite produit produits aliment aliments choses chose dont peu jour""".split())
text = " ".join(df["Mangé_E"].dropna().astype(str)).lower()
wc = WordCloud(width=1000, height=420, background_color="white", stopwords=STOP,
               colormap="viridis", collocations=False).generate(text)
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.imshow(wc, interpolation="bilinear"); ax.axis("off")
fig.tight_layout(); st.pyplot(fig)
st.markdown(
    "La définition spontanée tourne autour de la **variété**, de la **modération** (quantité, "
    "raisonnable, éviter) et des **groupes d'aliments** : une définition saine, conforme aux "
    "messages de santé publique. Là encore, **le savoir n'est pas le maillon faible**."
)
st.info("📄 Analyse détaillée : `reports/05_marketing_choix.md`")
