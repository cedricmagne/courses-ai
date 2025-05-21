"""
Module pour la visualisation de la carte
"""

import streamlit as st
import pydeck as pdk
import pandas as pd

def create_map(df: pd.DataFrame):
    """
    Crée une carte interactive des élus
    """
    try:
        # Sélectionner uniquement les colonnes nécessaires pour la carte
        needed_columns = ['Latitude_Commune', 'Longitude_Commune', 'Latitude_Dept', 'Longitude_Dept',
                         'Nom de l\'élu', 'Prénom de l\'élu', 'Libellé de la commune', 'Libellé du département']
        map_df = df[needed_columns].copy()
        
        # Permettre à l'utilisateur de choisir le type de visualisation
        viz_type = st.radio(
            "Type de visualisation",
            ["Points individuels", "Agrégation hexagonale"],
            help="Choisissez entre des points individuels ou une agrégation par zones"
        )
        
        # Filtrer les coordonnées invalides selon le type de visualisation
        if viz_type == "Points individuels":
            map_df = map_df[(map_df['Latitude_Commune'] != 0) & (map_df['Longitude_Commune'] != 0)]
        else:
            map_df = map_df[(map_df['Latitude_Dept'] != 0) & (map_df['Longitude_Dept'] != 0)]
        
        if map_df.empty:
            return None
        
        if viz_type == "Points individuels":
            # Si le dataframe est trop grand, prendre un échantillon
            if len(map_df) > 10000:
                map_df = map_df.sample(n=10000, random_state=42)
            
            # Utiliser les coordonnées des communes pour les points individuels
            map_df['position'] = map_df.apply(
                lambda row: [row['Longitude_Commune'], row['Latitude_Commune']], 
                axis=1
            )
            
            # Create a scatter plot layer
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_df,
                get_position='position',
                get_color=[200, 30, 0, 160],
                get_radius=50,
                pickable=True,
                auto_highlight=True,
                radius_scale=6,
                radius_min_pixels=3,
                radius_max_pixels=30,
                id="elected_officials"
            )
            
            # Create tooltip
            tooltip = {
                "html": "<b>Nom:</b> {Prénom de l'élu} {Nom de l'élu}<br>"
                       "<b>Commune:</b> {Libellé de la commune}<br>"
                       "<b>Département:</b> {Libellé du département}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }
            
        else:  # Agrégation hexagonale
            # Utiliser les coordonnées des départements pour l'agrégation
            hex_df = pd.DataFrame({
                'position': map_df.apply(
                    lambda row: [row['Longitude_Dept'], row['Latitude_Dept']], 
                    axis=1
                )
            })
            
            # Configuration de la couche hexagonale
            layer = pdk.Layer(
                "HexagonLayer",
                data=hex_df,
                get_position='position',
                radius=10000,
                elevation_scale=50,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                coverage=1,
                auto_highlight=True,
                colorRange=[
                    [65, 182, 196],
                    [127, 205, 187],
                    [199, 233, 180],
                    [237, 248, 177],
                    [255, 255, 204]
                ],
                id="hex_layer",
            )
            
            # Tooltip pour les hexagones
            tooltip = {
                "html": "<b>Nombre d'élus dans la zone:</b> {elevationValue}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }

        # Configuration de la vue initiale
        view_state = pdk.ViewState(
            latitude=46.603354,  # Centre de la France
            longitude=1.888334,
            zoom=5.5,  # Zoom initial ajusté
            min_zoom=4,  # Zoom minimum pour voir la France entière
            max_zoom=15,  # Zoom maximum pour le détail
            pitch=45 if viz_type == "Agrégation hexagonale" else 0,
            bearing=0
        )
        
        # Créer la carte
        deck = pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip
        )
        
        return deck
    
    except Exception as e:
        st.error(f"Erreur lors de la création de la carte: {str(e)}")
        return None

def display_map(df: pd.DataFrame):
    """
    Affiche la carte dans l'application
    """
    st.header("Carte des Élus")
    st.caption("Note: Les coordonnées sont approximatives basées sur les départements")
    deck = create_map(df)
    if deck:
        st.pydeck_chart(deck, use_container_width=True)
    else:
        st.warning("Données de localisation non disponibles pour la carte.") 