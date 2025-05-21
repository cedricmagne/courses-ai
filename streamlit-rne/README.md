# Explorateur du Répertoire National des Élus (RNE)

Une application Streamlit pour explorer et visualiser les données du Répertoire National des Élus.

## Fonctionnalités

- Visualisation des données des élus avec filtres
- Carte interactive des élus par département et commune
- Analyses avancées (pyramide des âges, statistiques, etc.)
- Export des données filtrées

## Installation

1. Cloner le dépôt :
```bash
git clone <votre-repo>
cd <votre-repo>
```

2. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancer l'application :
```bash
streamlit run app.py
```

2. Ouvrir votre navigateur à l'adresse : http://localhost:8501

## Structure du Projet

```
.
├── app.py                  # Point d'entrée de l'application
├── config/                 # Configuration de l'application
│   ├── __init__.py
│   └── settings.py        # Paramètres globaux
├── data/                   # Gestion des données
│   ├── __init__.py
│   └── loader.py          # Chargement et prétraitement
├── utils/                  # Utilitaires
│   ├── __init__.py
│   └── helpers.py         # Fonctions auxiliaires
├── visualization/          # Composants de visualisation
│   ├── __init__.py
│   ├── advanced.py        # Visualisations avancées
│   ├── map.py            # Carte interactive
│   └── ui.py             # Interface utilisateur
├── requirements.txt       # Dépendances Python
└── README.md             # Documentation
```

## Données

Les données sont chargées directement depuis data.gouv.fr et mises en cache localement pour de meilleures performances.

## Cache

L'application utilise deux fichiers de cache pour les coordonnées :
- `dept_coords_cache.json` : Coordonnées des départements
- `commune_coords_cache.json` : Coordonnées des communes

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT.