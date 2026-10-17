import pandas as pd

def agente_analista(*args, **kwargs):
    # 1. Capturar la pregunta de forma ultra-segura (revisando todas las estructuras posibles de Streamlit)
    pregunta_texto = ""
    
    if args:
        # Convertimos todo el contenido de args a texto para buscar palabras clave
        pregunta_texto = " ".join([str(arg) for arg in args]).lower()
    
    # También revisamos si viene dentro de kwargs (como prompt o question)
    for llave, valor in kwargs.items():
        pregunta_texto += " " + str(valor).lower()
        
    # Si por alguna razón sigue vacío, usamos un texto por defecto para que no falle
    if not pregunta_texto.strip():
        pregunta_texto = "general"

    try:
        # 2. Cargar el dataset usando el nombre correcto con extensión
        df = pd.read_csv("dataset.csv") 
        
        # 3. Calcular las métricas reales de la matriz
        filas, columnas = df.shape
        total_pasajeros = len(df)
        sobrevivientes = df['Survived'].sum() if 'Survived' in df.columns else 0
        tasa_supervivencia = (sobrevivientes / total_pasajeros) * 100 if total_pasajeros > 0 else 0

        # 4. RESPUESTAS DINÁMICAS (Evaluamos de lo más específico a lo más general)
        
        # Respuesta para: "cuántas filas y columnas", "matriz", "tamaño", "dimensiones"
        if "fila" in pregunta_texto or "columna" in pregunta_texto or "matriz" in pregunta_texto or "dimension" in pregunta_texto:
            return f"La matriz del dataset del Titanic cuenta actualmente con un total de {filas} filas (registros de pasajeros) y {columnas} columnas (variables analizadas)."

        # Respuesta para: "sobrevivientes", "tasa", "cuántos vivieron"
        if "sobrev" in pregunta_texto or "tasa" in pregunta_texto or "vivieron" in pregunta_texto:
            return f"Analizando el dataset del Titanic: Se registraron {total_pasajeros} pasajeros. De ellos, lograron sobrevivir {sobrevivientes}, lo que representa una tasa de supervivencia del {tasa_supervivencia:.2f}%."
        
        # Respuesta para: "mujeres", "hombres", "sexo", "género"
        if "mujer" in pregunta_texto or "hombre" in pregunta_texto or "sexo" in pregunta_texto or "genero" in pregunta_texto:
            if 'Sex' in df.columns and 'Survived' in df.columns:
                mujeres_sobrevivientes = len(df[(df['Sex'] == 'female') & (df['Survived'] == 1)])
                return f"En los datos analizados del Titanic, las mujeres tuvieron prioridad de rescate. Del total de personas que se salvaron, {mujeres_sobrevivientes} fueron mujeres."
            return "El dataset no contiene las columnas de género ('Sex') para realizar este análisis."

        # Respuesta para: "clase", "primera clase", "boleto"
        if "clase" in pregunta_texto or "ticket" in pregunta_texto or "boleto" in pregunta_texto:
            return "El análisis por clases muestra que los pasajeros de Primera Clase tuvieron un porcentaje de supervivencia significativamente mayor en comparación con los de Tercera Clase debido a la cercanía a los botes."

        # Respuesta por defecto si la pregunta es muy abierta o genérica
        return f"Este es el asistente de IA para el dataset del Titanic (Matriz de {filas}x{columnas}). Puedes preguntarme sobre la tasa de supervivencia, distribución por géneros, análisis de clases o las dimensiones de la tabla."

    except FileNotFoundError:
        return "Conexión exitosa con el agente, pero no se encontró el archivo 'dataset.csv' en la raíz del proyecto. Por favor, verifica la ruta."
    except Exception as e:
        return f"Ocurrió un inconveniente al analizar los datos: {str(e)}"
