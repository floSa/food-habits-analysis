import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_distribution(df, column, title=None, color=None, order=None):
    """
    Affiche la distribution d'une variable catégorielle ou numérique.
    """
    if df[column].dtype.name == 'category' or df[column].dtype == 'object':
        # Compte pour le bar chart
        if color:
            # Si on a une couleur, on doit grouper par la colonne ET la couleur
            # Si on a une couleur, on doit grouper par la colonne ET la couleur
            # FORCE string conversion to avoid Categorical issues
            df_temp = df.copy()
            df_temp[column] = df_temp[column].astype(str)
            if df_temp[color].dtype.name == 'category':
                 df_temp[color] = df_temp[color].astype(str)
                 
            counts = df_temp.groupby([column, color], observed=False, dropna=False).size().reset_index(name='Count')
        else:
            counts = df[column].value_counts().reset_index()
            counts.columns = [column, 'Count']
        
        if order:
             fig = px.bar(counts, x=column, y='Count', title=title or f"Distribution de {column}", 
                          color=color, category_orders={column: order})
        else:
             fig = px.bar(counts, x=column, y='Count', title=title or f"Distribution de {column}", color=color)
        
    else:
        # Histogramme pour numérique
        fig = px.histogram(df, x=column, title=title or f"Distribution de {column}", color=color, nbins=30)
    
    # Correction CRITIQUE : on force l'axe X à être catégoriel pour éviter que Plotly 
    # n'interprète "-18" et "+60" comme des nombres et cache "18-34".
    fig.update_xaxes(type='category')
    
    return fig

def plot_boxplot(df, x_col, y_col, title=None, color=None):
    """
    Affiche un boxplot basique.
    """
    fig = px.box(df, x=x_col, y=y_col, title=title or f"{y_col} par {x_col}", color=color)
    return fig

def plot_correlation_heatmap(corr_matrix, title="Matrice de Corrélation"):
    """
    Affiche une heatmap de corrélation.
    """
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title=title,
                    color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    return fig
