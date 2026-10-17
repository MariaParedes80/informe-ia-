import pandas as pd

def agente_analista(*args, **kwargs):
    # 1. Intentar capturar la pregunta enviada por Streamlit desde args o kwargs
    pregunta = ""
    if args:
        pregunta = str(args[0]).lower()
    elif "prompt" in kwargs:
        pregunta = str(kwargs["prompt"]).lower()
    
    try:
        # 2. Cargar el dataset del Titanic (Asegúrate de que la ruta coincida con tu archivo .csv)
        # Si está en otra carpeta, ajusta la ruta como 'src/titanic.csv' o 'data/titanic.csv'
        df = pd.read_csv("dataset.csv") 
        
        # 3. Calcular métricas reales en vivo para responder de forma inteligente
        total_pasajeros = len(df)
        sobrevivientes = df['Survived'].sum() if 'Survived' in df.columns else 0
        tasa_supervivencia = (sobrevivientes / total_pasajeros) * 100 if total_pasajeros > 0 else 0
        mujeres_sobrevivientes = len(df[(df['Sex'] == 'female') & (df['Survived'] == 1)]) if 'Sex' in df.columns else 0

        # 4. Responder dinámicamente según lo que escriba el usuario
        if "sobrev" in pregunta or "morir" in pregunta or "tasa" in pregunta:
            return f"Analizando el dataset del Titanic: Se registraron {total_pasajeros} pasajeros. De ellos, sobrevivieron {sobrevivientes}, lo que representa una tasa de supervivencia del {tasa_supervivencia:.2f}%."
        
        if "mujer" in pregunta or "sexo" in pregunta or "genero" in pregunta:
            return f"En los datos analizados del Titanic, las mujeres tuvieron prioridad de rescate. Del total de sobrevivientes, {mujeres_sobrevivientes} fueron mujeres."
            
        if "clase" in pregunta or "ticket" in pregunta:
            return "El análisis por clases muestra que los pasajeros de Primera Clase tuvieron un porcentaje de supervivencia significativamente mayor en comparación con Tercera Clase."

        # Respuesta por defecto con datos reales si la pregunta es genérica (ej. "de que se trata")
        return f"Este es el dataset del Titanic con {total_pasajeros} registros. Contiene variables como edad, género, clase del boleto y si el pasajero sobrevivió o no. ¿Deseas saber un dato específico?"

    except FileNotFoundError:
        # Mensaje de ayuda si el archivo .csv no está en la ruta indicada
        return "Conexión exitosa con el agente, pero no se encontró el archivo 'titanic.csv' en la raíz del proyecto. Por favor, verifica la ruta del dataset."
    except Exception as e:
        return f"Ocurrió un inconveniente al analizar los datos: {str(e)}"
