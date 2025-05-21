"""
Module de chargement et prétraitement des données
"""

import pandas as pd
import numpy as np
import json
import requests
from io import StringIO
import streamlit as st
from config.settings import DATA_URL, COLUMN_MAPPING, DEFAULT_DEPT_COORDS

def load_data() -> pd.DataFrame:
    """
    Charge les données depuis l'URL avec mise en cache Streamlit
    """
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP
        
        # Lire le contenu CSV avec l'encodage approprié
        content = response.content.decode('utf-8', errors='replace')
        df = pd.read_csv(StringIO(content), sep=";", low_memory=False)
        
        # Renommer les colonnes en utilisant le mapping
        df = df.rename(columns=COLUMN_MAPPING)
        
        # Calculer l'âge si la date de naissance est disponible
        if 'Date de naissance' in df.columns:
            df['Age'] = pd.to_datetime('today').year - pd.to_datetime(df['Date de naissance'], format='%d/%m/%Y', errors='coerce').dt.year
        
        return df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=86400)  # Cache pendant 24 heures
def load_coords_cache(cache_file: str) -> dict:
    """
    Charge les coordonnées depuis le fichier de cache avec mise en cache Streamlit
    """
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Erreur lors du chargement du cache {cache_file} : {str(e)}")
        if 'dept' in cache_file.lower():
            return DEFAULT_DEPT_COORDS
        return {}

def filter_data(df: pd.DataFrame, selected_departments: list, selected_gender: str, search_term: str) -> pd.DataFrame:
    """
    Filtre les données selon les critères sélectionnés
    """
    filtered_df = df.copy()
    
    # Filtre par département
    if selected_departments and 'Libellé du département' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Libellé du département'].fillna('').astype(str).isin(selected_departments)]
    
    # Filtre par genre
    if selected_gender != "Tous" and 'Code sexe' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Code sexe'].fillna('').astype(str) == selected_gender]
    
    # Filtre par terme de recherche
    if search_term:
        search_conditions = []
        if 'Nom de l\'élu' in filtered_df.columns:
            search_conditions.append(filtered_df['Nom de l\'élu'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        if 'Prénom de l\'élu' in filtered_df.columns:
            search_conditions.append(filtered_df['Prénom de l\'élu'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        if 'Libellé de la commune' in filtered_df.columns:
            search_conditions.append(filtered_df['Libellé de la commune'].fillna('').astype(str).str.contains(search_term, case=False, na=False))
        
        if search_conditions:
            search_condition = search_conditions[0]
            for cond in search_conditions[1:]:
                search_condition = search_condition | cond
            filtered_df = filtered_df[search_condition]
    
    return filtered_df

@st.cache_data
def preprocess_data(data: pd.DataFrame, commune_cache: dict, dept_cache: dict) -> pd.DataFrame:
    """
    Prétraite les données avec mise en cache Streamlit
    """
    if data.empty:
        return data
    
    # Ajouter les coordonnées des communes
    data['Latitude_Commune'] = data['Libellé de la commune'].map(lambda x: commune_cache.get(str(x), (None, None))[0] if pd.notna(x) else None)
    data['Longitude_Commune'] = data['Libellé de la commune'].map(lambda x: commune_cache.get(str(x), (None, None))[1] if pd.notna(x) else None)
    
    # Ajouter les coordonnées des départements
    data['Latitude_Dept'] = data['Libellé du département'].map(lambda x: dept_cache.get(x, (None, None))[0] if pd.notna(x) else None)
    data['Longitude_Dept'] = data['Libellé du département'].map(lambda x: dept_cache.get(x, (None, None))[1] if pd.notna(x) else None)
    
    # Ajouter un décalage aléatoire pour les coordonnées
    if 'Latitude_Dept' in data.columns and 'Longitude_Dept' in data.columns:
        data['Latitude_Dept'] = data['Latitude_Dept'] + np.random.normal(0, 0.05, size=len(data))
        data['Longitude_Dept'] = data['Longitude_Dept'] + np.random.normal(0, 0.05, size=len(data))
    
    if 'Latitude_Commune' in data.columns and 'Longitude_Commune' in data.columns:
        data['Latitude_Commune'] = data['Latitude_Commune'] + np.random.normal(0, 0.001, size=len(data))
        data['Longitude_Commune'] = data['Longitude_Commune'] + np.random.normal(0, 0.001, size=len(data))
    
    # Remplacer les valeurs manquantes par 0
    coord_cols = ['Latitude_Dept', 'Longitude_Dept', 'Latitude_Commune', 'Longitude_Commune']
    for col in coord_cols:
        if col in data.columns:
            data[col].fillna(0, inplace=True)
    
    return data 