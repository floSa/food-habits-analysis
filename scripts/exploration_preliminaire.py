import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
import sys
import os

print(f"Executable: {sys.executable}")
print(f"Path: {sys.path}")

# Configuration pour l'affichage
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

def load_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=';')
        print(f"Dataset chargé avec succès: {df.shape}")
        return df
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return None

def basic_info(df):
    print("\n--- Informations Générales ---")
    print(df.info())
    print("\n--- Valeurs Manquantes ---")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print("\n--- Doublons ---")
    print(f"Nombre de doublons: {df.duplicated().sum()}")

def plot_univariate_dist(df, columns, output_dir="docs/analysis_outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for col in columns:
        if col not in df.columns:
            continue
            
        plt.figure(figsize=(10, 6))
        if df[col].dtype == 'object':
            sns.countplot(y=col, data=df, order=df[col].value_counts().index)
            plt.title(f'Distribution de {col}')
        else:
            sns.histplot(df[col], kde=True)
            plt.title(f'Distribution de {col}')
            
        plt.tight_layout()
        plt.savefig(f"{output_dir}/dist_{col}.png")
        plt.close()
        print(f"Graphique sauvegardé: {output_dir}/dist_{col}.png")

def main():
    filepath = '/home/florian/mes_projets/Alimentation/enquete_alimentation.csv'
    df = load_data(filepath)
    
    if df is not None:
        basic_info(df)
        
        # Variables d'intérêt initiales (basées sur Plan.md et le dict)
        cols_to_plot = ['Sexe', 'Age', 'Rura', 'Card', 'Etud', 'pro', 
                        'Regime_B', 'végétarien', 'gluten', 
                        'C_leg', 'C_frui', 'C_viaR', 'C_indu']
        
        plot_univariate_dist(df, cols_to_plot)
        
        # Exemple d'utilisation de pingouin (Corrélation ou Chi2 pour variables catégorielles)
        # On va tester le lien entre Sexe et C_viaR (Viande Rouge) - souvent significatif
        try:
            print("\n--- Test Chi2 : Sexe vs Consommation Viande Rouge ---")
            contingency = pd.crosstab(df['Sexe'], df['C_viaR'])
            expected, observed, stats = pg.chi2_independence(df, x='Sexe', y='C_viaR')
            print(stats)
        except Exception as e:
            print(f"Impossible de calculer Chi2: {e}")

if __name__ == "__main__":
    main()
