import pandas as pd

def agente_analista(*args, **kwargs):
    # 1. Capturar el texto de la consulta de manera limpia
    pregunta_texto = ""
    
    # Prioridad 1: Si Streamlit manda el texto limpio dentro de los argumentos posicionales
    if args:
        pregunta_texto = " ".join([str(arg) for arg in args]).lower()
    
    # Prioridad 2: Buscar específicamente la caja de texto del usuario en kwargs
    # Revisamos nombres comunes como 'prompt', 'question', 'text', o 'body'
    elif kwargs:
        for llave in ['prompt', 'question', 'text', 'user_input']:
            if llave in kwargs:
                pregunta_texto = str(kwargs[llave]).lower()
                break
        if not pregunta_texto:
            # Si no encuentra las llaves comunes, junta todos los valores
            pregunta_texto = " ".join([str(valor) for valor in kwargs.values()]).lower()

    # Si todo falla o está vacío, asignamos una cadena vacía
    pregunta_texto = pregunta_texto.strip()

    try:
        # 2. Cargar la matriz de datos del Titanic
        df = pd.read_csv("dataset.csv")
        filas, columnas = df.shape
        total_pasajeros = len(df)

        # 3. EVALUACIÓN INTELIGENTE DE PALABRAS CLAVE (Sin falsos positivos)
        
        # Condición A: Si el usuario pregunta explícitamente por el tamaño, dimensiones o estructura de la matriz
        if "cuantas filas" in pregunta_texto or "cuántas filas" in pregunta_texto or "dimension" in pregunta_texto or "tamaño" in pregunta_texto or "tamañio" in pregunta_texto:
            return f"La matriz del dataset contiene exactamente {filas} filas (registros de pasajeros) y {columnas} columnas (variables)."

        # Condición B: Si el usuario pregunta por supervivencia o sobrevivientes
        if "sobrev" in pregunta_texto or "tasa" in pregunta_texto or "vivieron" in pregunta_texto or "salvaron" in pregunta_texto:
            sobrevivientes = df['Survived'].sum() if 'Survived' in df.columns else 0
            tasa = (sobrevivientes / total_pasajeros) * 100 if total_pasajeros > 0 else 0
            return f"Analizando los sobrevivientes: De los {total_pasajeros} pasajeros registrados en el dataset, sobrevivieron {sobrevivientes}, logrando una tasa de supervivencia del {tasa:.2f}%."

        # Condición C: Si el usuario pregunta por mujeres, hombres o género
        if "mujer" in pregunta_texto or "hombre" in pregunta_texto or "sexo" in pregunta_texto or "genero" in pregunta_texto:
            if 'Sex' in df.columns and 'Survived' in df.columns:
                mujeres_totales = len(df[df['Sex'] == 'female'])
                mujeres_sobrevivientes = len(df[(df['Sex'] == 'female') & (df['Survived'] == 1)])
                return f"Análisis de género: El dataset registra {mujeres_totales} mujeres a bordo. De ellas, {mujeres_sobrevivientes} sobrevivieron, demostrando que tuvieron prioridad en los botes."
            return "El archivo CSV no cuenta con las columnas de género necesarias para este cálculo."

        # Condición D: Si el usuario menciona explícitamente el nombre del dataset "titanic" o "dataset es de"
        if "titanic" in pregunta_texto or "de que se trata" in pregunta_texto or "que es" in pregunta_texto:
            return f"¡Confirmado! Este es el dataset oficial del Titanic. Contiene una matriz de {filas}x{columnas} con información de {total_pasajeros} pasajeros, incluyendo edad, sexo, tarifa del boleto y estado de supervivencia."

        # Respuesta comodín por si la pregunta es totalmente nueva o diferente
        return f"Procesé tu consulta técnica: '{pregunta_texto}'. Para esta matriz de {filas} filas, puedes consultarme específicamente sobre: 'cuántas filas y columnas tiene', 'cuál es la tasa de sobrevivientes' o 'análisis de género'."

    except Exception as e:
        return f"Error al procesar la consulta sobre el archivo: {str(e)}"
