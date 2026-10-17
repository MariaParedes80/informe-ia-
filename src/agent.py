import pandas as pd

def agente_analista(*args, **kwargs):
    # 1. Buscador avanzado de texto dentro de CUALQUIER parámetro que envíe la interfaz
    pregunta_texto = ""
    
    # Buscar dentro de los argumentos posicionales (*args)
    if args:
        pregunta_texto += " " + " ".join([str(arg) for arg in args]).lower()
    
    # Buscar dentro de absolutamente todos los argumentos con nombre (**kwargs)
    if kwargs:
        for llave, valor in kwargs.items():
            pregunta_texto += " " + str(valor).lower()
            
    # CONTROL CRÍTICO: Si la interfaz de Streamlit está llamando a la función de manera 
    # vacía o estática (ej: agente_analista()), este bloque forzará la respuesta del Titanic.
    if not pregunta_texto.strip() or "general" in pregunta_texto:
        try:
            df = pd.read_csv("dataset.csv")
            filas, columnas = df.shape
            return f"¡Conexión lista! Tu dataset del Titanic tiene {filas} filas y {columnas} columnas. Por favor, asegúrate de pasar la variable del cuadro de texto dentro de los paréntesis al llamar a agente_analista(pregunta) en tu app.py."
        except:
            return "El agente está listo pero no se pudo leer 'dataset.csv'. Verifica el archivo."

    # 2. Procesamiento de respuestas si se detecta texto dinámico
    try:
        df = pd.read_csv("dataset.csv")
        filas, columnas = df.shape
        total_pasajeros = len(df)

        # Respuesta exacta para: Filas, Columnas o Matriz
        if "fila" in pregunta_texto or "columna" in pregunta_texto or "matriz" in pregunta_texto or "dimension" in pregunta_texto:
            return f"La matriz del dataset contiene exactamente {filas} filas (registros de pasajeros) y {columnas} columnas (variables)."

        # Respuesta exacta para: Sobrevivientes
        if "sobrev" in pregunta_texto or "tasa" in pregunta_texto or "vivieron" in pregunta_texto:
            sobrevivientes = df['Survived'].sum() if 'Survived' in df.columns else 0
            tasa = (sobrevivientes / total_pasajeros) * 100 if total_pasajeros > 0 else 0
            return f"El dataset registra {total_pasajeros} pasajeros. De ellos sobrevivieron {sobrevivientes} (Tasa: {tasa:.2f}%)."

        # Si el texto ingresado no coincide con ninguna regla anterior
        return f"Recibí tu consulta: '{pregunta_texto.strip()}'. Analizando la matriz de {filas}x{columnas}, ¿deseas conocer los sobrevivientes, género o clases?"

    except Exception as e:
        return f"Error leyendo los datos de la matriz: {str(e)}"
