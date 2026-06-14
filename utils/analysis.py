"""
Helpers d'analyse partagés entre les notebooks et l'application Streamlit.

Source unique de vérité pour les calculs non triviaux (correction de Benzécri,
grille des croyances et score de connaissance, parsing des questions à choix
multiples). Garantit que l'app présente exactement les mêmes résultats que les
notebooks / rapports.
"""
import numpy as np
import pandas as pd
from collections import Counter

# --- Constantes d'affichage ---------------------------------------------------

AGE_ORDER = ["-18", "18-34", "35-60", "+60"]
ETU_ORDER = ["Brevet", "Bac", "Bac+3", "Bac +5"]
FREQ_ORDER = ["Jamais", "Très rarement", "1 x par semaine", "3 x par semaine",
              "5 x par semaine", "1 x par jour", "A tous les repas"]

# Variables actives de l'ACM (consommations) et libellés courts
ACM_ACTIVES = ["C_leg", "C_frui", "C_fec", "C_lait", "C_viaB", "C_viaR", "C_poi", "C_indu"]
ALIMENT_FULL = {"C_leg": "Légumes", "C_frui": "Fruits", "C_fec": "Féculents",
                "C_lait": "Laitiers", "C_viaB": "Viande blanche", "C_viaR": "Viande rouge",
                "C_poi": "Poisson", "C_indu": "Industriels"}
ALIMENT_SHORT = {"C_leg": "Lég", "C_frui": "Fru", "C_fec": "Féc", "C_lait": "Lait",
                 "C_viaB": "ViaB", "C_viaR": "ViaR", "C_poi": "Poi", "C_indu": "Indu"}
FREQ_SHORT = {"Jamais": "0", "Très rarement": "TR", "1 x par semaine": "1/sem",
              "3 x par semaine": "3/sem", "5 x par semaine": "5/sem",
              "1 x par jour": "1/j", "A tous les repas": "++", "Non répondu": "NR"}


# --- ACM : correction de Benzécri --------------------------------------------

def benzecri_percentages(eigenvalues, n_active_vars):
    """Pourcentages d'inertie corrigés (Benzécri) à partir des valeurs propres.

    L'ACM brute sous-estime l'inertie des premiers axes ; on ne retient que les
    axes dont la valeur propre dépasse 1/K et on recalcule des % réalistes.
    """
    K = n_active_vars
    thr = 1 / K
    ben = np.array([((K / (K - 1)) * (l - thr)) ** 2 if l > thr else 0.0
                    for l in eigenvalues])
    return ben / ben.sum() * 100 if ben.sum() else ben


# --- Croyances (Vrai/Faux) et score de connaissance --------------------------

# Pour chaque idée reçue : (libellé, bonne réponse — "Oui" = l'affirmation est vraie)
BELIEFS = {
    "VF_saut":   ("Sauter un repas fait maigrir", "Non"),
    "VF_Eq_bon": ("Manger équilibré = pas bon", "Non"),
    "VF_Eq_Reg": ("Manger équilibré = être au régime", "Non"),
    "VF_Fec":    ("Les féculents font grossir", "Non"),
    "VF_Eq":     ("Manger équilibré coûte cher", "Non"),
    "VF_HO":     ("L'huile d'olive est meilleure", "Oui"),
    "VF_soir":   ("Manger léger le soir (recommandé)", "Oui"),
    "VF_medi":   ("Le régime méditerranéen est bénéfique", "Oui"),
    "VF_Su":     ("Le sucre roux est meilleur que le blanc", "Non"),
}


def belief_correct_rates(df):
    """Taux de bonnes réponses par idée reçue (réponses tranchées Oui/Non)."""
    rows = []
    for col, (lab, correct) in BELIEFS.items():
        clear = df[col].isin(["Oui", "Non"])
        rows.append({"Idée reçue": lab, "Bonne réponse": correct,
                     "% correct": round((df.loc[clear, col] == correct).mean() * 100, 1)})
    return pd.DataFrame(rows).sort_values("% correct").reset_index(drop=True)


def add_knowledge_score(df):
    """Ajoute Score_Connaissance (0-9) = nombre de bonnes réponses VF_*."""
    out = df.copy()
    cols = []
    for col, (_, correct) in BELIEFS.items():
        ok = col + "_ok"
        out[ok] = (out[col] == correct).astype(int)
        cols.append(ok)
    out["Score_Connaissance"] = out[cols].sum(axis=1)
    return out


def classify_5fj(s):
    """Rapport à la règle des « 5 fruits & légumes » à partir de la colonne 5fj."""
    if pd.isna(s):
        return np.nan
    if "Non je ne connais pas" in s:
        return "Ne connaît pas"
    if "J'applique" in s or "J'esaye" in s:
        return "Applique / essaie"
    if "Je n'applique pas" in s:
        return "Connaît, n'applique pas"
    if "Oui je connais" in s:
        return "Connaît seulement"
    return np.nan


# --- Questions à choix multiples ---------------------------------------------

def multi_pct(df, col):
    """Fréquence (%) de chaque option d'une question à choix multiples (split ', ')."""
    c = Counter()
    for v in df[col].dropna():
        for opt in str(v).split(", "):
            c[opt.strip()] += 1
    n = df[col].notna().sum()
    return (pd.Series(c) / n * 100).sort_values()


# Catégories de produits citées dans la question Pub (libellés à virgules internes)
PUB_OPTS = {
    "Produits industriels": "Produits industriels",
    "Produit laitier": "Produit laitier",
    "Produits frais (eau, viande, poisson…)": "Eau, viande, poisson frais, salade",
    "Autres": "Autres",
}


def add_pub_influence(df):
    """Ajoute pub_influence ∈ {Influencé, Non influencé, NaN} d'après la colonne Pub."""
    out = df.copy()
    out["pub_influence"] = out["Pub"].apply(
        lambda v: np.nan if pd.isna(v) else ("Non influencé" if v == "Non" else "Influencé"))
    return out


def pub_category_rates(df):
    """% des influencés citant chaque catégorie de produit."""
    inf = df[df["pub_influence"] == "Influencé"]
    return (pd.Series({lab: inf["Pub"].str.contains(pat, regex=False).mean() * 100
                       for lab, pat in PUB_OPTS.items()}).sort_values())
