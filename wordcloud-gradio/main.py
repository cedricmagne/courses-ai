import gradio as gr
import pandas as pd

#Fonction pour convertir un fichier excel en json
def excel_to_json(file_path):
    df = pd.read_excel(file_path)

    #convertir le dataframe en dictionnaire
    result = df.to_dict(orient='records')

    return result

#Définir l'interface Gradio
appli = gr.Interface(
    fn=excel_to_json,
    inputs=gr.File(file_count="single", type="filepath"),
    outputs=gr.JSON(),
    title="Convertir un fichier Excel en JSON",
    description="Chargez un fichier Excel et obtenez un JSON en sortie."
)

#Initialiser l'application
appli.launch()