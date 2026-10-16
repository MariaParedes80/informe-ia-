import os
import pandas as pd


def cargar_datos(ruta_archivo="./data/dataset.csv"):
    """Carga de forma segura el archivo CSV del proyecto."""
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"El archivo '{ruta_archivo}' no existe. Por favor, colóquelo en la carpeta data/."
        )
    return pd.read_csv(ruta_archivo)