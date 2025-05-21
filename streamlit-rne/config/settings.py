"""
Configuration globale de l'application
"""

# Paramètres de l'application
APP_TITLE = "Explorateur du Répertoire National des Élus"
APP_DESCRIPTION = "Une application pour explorer et visualiser les données du Répertoire National des Élus"
APP_ICON = "🗳️"
APP_LAYOUT = "wide"
APP_INITIAL_SIDEBAR_STATE = "expanded"

# URL des données
DATA_URL = "https://static.data.gouv.fr/resources/repertoire-national-des-elus-1/20250312-164444/elus-conseillers-municipaux-cm.csv"

# Chemins des fichiers de cache
DEPT_COORDS_CACHE = "dept_coords_cache.json"
COMMUNE_COORDS_CACHE = "commune_coords_cache.json"

# Colonnes importantes
COLONNES_PRINCIPALES = [
    'Nom de l\'élu',
    'Prénom de l\'élu',
    'Libellé de la commune',
    'Libellé du département'
]

# Paramètres de la carte
MAP_CENTER = [46.603354, 1.888334]  # Centre de la France
MAP_ZOOM = 6

# Mapping des colonnes pour correction d'encodage
COLUMN_MAPPING = {
    "Code du dÃ©partement": "Code du département",
    "LibellÃ© du dÃ©partement": "Libellé du département",
    "Code de la collectivitÃ© Ã  statut particulier": "Code de la collectivité à statut particulier",
    "LibellÃ© de la collectivitÃ© Ã  statut particulier": "Libellé de la collectivité à statut particulier",
    "Code de la commune": "Code de la commune",
    "LibellÃ© de la commune": "Libellé de la commune",
    "Nom de l'Ã©lu": "Nom de l'élu",
    "PrÃ©nom de l'Ã©lu": "Prénom de l'élu",
    "Code sexe": "Code sexe",
    "Date de naissance": "Date de naissance",
    "Code de la catÃ©gorie socio-professionnelle": "Code de la catégorie socio-professionnelle",
    "LibellÃ© de la catÃ©gorie socio-professionnelle": "Libellé de la catégorie socio-professionnelle",
    "Date de dÃ©but du mandat": "Date de début du mandat",
    "LibellÃ© de la fonction": "Libellé de la fonction",
    "Date de dÃ©but de la fonction": "Date de début de la fonction",
    "Code nationalitÃ©": "Code nationalité"
}

# Coordonnées par défaut des départements
DEFAULT_DEPT_COORDS = {
    "Ain": (46.0667, 5.3333),
    "Aisne": (49.5667, 3.6167),
    # ... (le reste des coordonnées)
} 