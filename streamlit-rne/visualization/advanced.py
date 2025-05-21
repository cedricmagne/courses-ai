"""
Module de visualisations avancées
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import Optional

def create_age_pyramid(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Crée une pyramide des âges par genre
    """
    if 'Age' not in df.columns or 'Code sexe' not in df.columns:
        return None
    
    # Create age bins
    bins = list(range(20, 91, 10))  # [20, 30, 40, 50, 60, 70, 80, 90]
    labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]  # Créer les labels dynamiquement
    
    # Add age group column
    df['Age_Group'] = pd.cut(
        df['Age'].astype(float),
        bins=bins,
        labels=labels,
        right=False,
        include_lowest=True
    )
    
    # Count by age group and gender
    age_gender = df.groupby(['Age_Group', 'Code sexe']).size().reset_index(name='count')
    
    # Create separate dataframes for men and women
    men = age_gender[age_gender['Code sexe'] == 'M'].set_index('Age_Group')['count']
    women = age_gender[age_gender['Code sexe'] == 'F'].set_index('Age_Group')['count']
    
    # Negate men counts for the pyramid
    men = -men
    
    # Create the figure
    fig = go.Figure()
    
    # Add men bars
    fig.add_trace(go.Bar(
        y=men.index,
        x=men.values,
        name='Hommes',
        orientation='h',
        marker=dict(color='rgba(0, 128, 255, 0.8)')
    ))
    
    # Add women bars
    fig.add_trace(go.Bar(
        y=women.index,
        x=women.values,
        name='Femmes',
        orientation='h',
        marker=dict(color='rgba(255, 0, 128, 0.8)')
    ))
    
    # Calculer les valeurs maximales pour les ticks
    max_value = max(abs(men.min()), women.max())
    tick_step = 20000  # Pas de 20 000 pour les ticks
    max_tick = ((max_value // tick_step) + 1) * tick_step  # Arrondir au multiple de tick_step supérieur
    
    # Créer les ticks
    tick_values = list(range(-max_tick, max_tick + tick_step, tick_step))
    tick_text = [f"{abs(val):,}".replace(",", " ") for val in tick_values]  # Formater avec des espaces pour les milliers
    
    # Update layout
    fig.update_layout(
        title="Pyramide des âges par genre",
        yaxis=dict(
            title='Groupe d\'âge',
            tickfont=dict(size=12)
        ),
        xaxis=dict(
            title='Nombre d\'élus',
            tickvals=tick_values,
            ticktext=tick_text,
            tickfont=dict(size=10),  # Réduire légèrement la taille de la police pour les nombres
            gridcolor='lightgray',
            showgrid=True
        ),
        barmode='overlay',
        bargap=0.1,
        height=600,  # Augmenter la hauteur pour une meilleure lisibilité
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_profession_analysis(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Analyse des professions les plus représentées
    """
    if 'Libellé de la catégorie socio-professionnelle' not in df.columns:
        return None
    
    # Get profession counts
    profession_counts = df['Libellé de la catégorie socio-professionnelle'].value_counts().head(15)
    
    # Create bar chart
    fig = px.bar(
        x=profession_counts.index,
        y=profession_counts.values,
        labels={'x': 'Catégorie socio-professionnelle', 'y': 'Nombre d\'élus'},
        title="Catégories socio-professionnelles les plus représentées",
        color=profession_counts.values,
        color_continuous_scale='Viridis'
    )
    
    # Update layout for readability
    fig.update_layout(
        xaxis={'categoryorder':'total descending'},
        xaxis_tickangle=-45
    )
    
    return fig

def plot_gender_distribution(df: pd.DataFrame):
    """
    Crée un graphique circulaire de la répartition par genre
    """
    gender_col = 'Code sexe' if 'Code sexe' in df.columns else None
    if not gender_col:
        return None
    
    gender_counts = df[gender_col].value_counts()
    fig = px.pie(
        values=gender_counts.values,
        names=gender_counts.index,
        title="Répartition par Genre",
        color_discrete_sequence=px.colors.sequential.Viridis,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def plot_mayors_by_department(df: pd.DataFrame):
    """
    Crée un graphique en barres du nombre d'élus par département
    """
    dept_col = 'Libellé du département' if 'Libellé du département' in df.columns else None
    if not dept_col:
        return None
    
    dept_counts = df[dept_col].value_counts().nlargest(20)
    fig = px.bar(
        x=dept_counts.index,
        y=dept_counts.values,
        title="Nombre d'élus par Département (Top 20)",
        labels={'x': 'Département', 'y': "Nombre d'élus"},
        color=dept_counts.values,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    return fig

def plot_age_distribution(df: pd.DataFrame):
    """
    Crée un histogramme de la distribution des âges
    """
    if 'Age' in df.columns and not df['Age'].empty:
        # Créer des tranches d'âge pour la coloration
        df_age = df[df['Age'].notna()].copy()  # Exclure les valeurs NaN
        
        # Définir les tranches d'âge (bins)
        min_age = df_age['Age'].min()
        max_age = df_age['Age'].max()
        n_bins = 20
        
        # Créer des bins égaux
        bins = np.linspace(min_age, max_age, n_bins)
        
        # Calculer l'histogramme manuellement
        hist, bin_edges = np.histogram(df_age['Age'], bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Créer un DataFrame pour l'histogramme
        hist_df = pd.DataFrame({
            'Age': bin_centers,
            'Count': hist,
            'bin_group': range(len(hist))  # Pour la coloration
        })
        
        # Créer le graphique avec des barres
        fig = px.bar(
            hist_df,
            x='Age',
            y='Count',
            color='bin_group',  # Utiliser les groupes de bins pour la coloration
            color_continuous_scale='viridis',  # Échelle de couleurs
            title="Distribution par Âge",
            labels={'Age': 'Âge', 'Count': 'Nombre d\'Élus'},
            template='plotly_white'
        )
        
        # Personnaliser le layout
        fig.update_layout(
            bargap=0.1,  # Ajouter un espace entre les barres
            showlegend=False,
            coloraxis_showscale=False,  # Masquer l'échelle de couleurs
            plot_bgcolor='white',
            xaxis=dict(
                title="Âge",
                gridcolor='lightgray',
                showgrid=True,
                tickmode='array',
                ticktext=[f"{x:.0f}" for x in bin_edges[::2]],  # Afficher un tick sur deux
                tickvals=bin_edges[::2]
            ),
            yaxis=dict(
                title="Nombre d'Élus",
                gridcolor='lightgray',
                showgrid=True
            )
        )
        
        # Ajouter des statistiques descriptives
        mean_age = df_age['Age'].mean()
        median_age = df_age['Age'].median()
        
        fig.add_annotation(
            text=f"Âge moyen: {mean_age:.1f} ans<br>Âge médian: {median_age:.1f} ans",
            xref="paper", yref="paper",
            x=0.98, y=0.98,
            showarrow=False,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=1,
            borderpad=4
        )
        
        return fig
    else:
        return px.histogram()  # Return empty figure if age data is not available

def display_advanced_visualizations(df: pd.DataFrame):
    """
    Affiche toutes les visualisations avancées
    """
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution par genre
        gender_fig = plot_gender_distribution(df)
        if gender_fig:
            st.plotly_chart(gender_fig, use_container_width=True)
        else:
            st.warning("Données de genre non disponibles pour la visualisation.")
        
        # Distribution par âge
        if 'Age' in df.columns:
            age_fig = plot_age_distribution(df)
            st.plotly_chart(age_fig, use_container_width=True)
        else:
            st.warning("Données d'âge non disponibles pour la visualisation.")
    
    with col2:
        # Élus par département
        dept_fig = plot_mayors_by_department(df)
        if dept_fig:
            st.plotly_chart(dept_fig, use_container_width=True)
        else:
            st.warning("Données de département non disponibles pour la visualisation.")

    st.header("Analyses Avancées")
    
    # Create tabs for different visualizations
    tabs = st.tabs([
        "Pyramide des âges",
        "Professions"
    ])
    
    with tabs[0]:
        st.subheader("Pyramide des âges des élus")
        age_pyramid = create_age_pyramid(df)
        if age_pyramid:
            st.plotly_chart(age_pyramid, use_container_width=True)
        else:
            st.warning("Données d'âge non disponibles pour cette visualisation.")
    
    with tabs[1]:
        st.subheader("Analyse des catégories socio-professionnelles")
        profession_chart = create_profession_analysis(df)
        if profession_chart:
            st.plotly_chart(profession_chart, use_container_width=True)
        else:
            st.warning("Données de profession non disponibles pour cette visualisation.") 