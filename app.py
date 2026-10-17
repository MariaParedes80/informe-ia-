import streamlit as st  # <-- ¡ESTA LÍNEA ES LA QUE FALTA Y REPARA EL ERROR!
import pandas as pd

# ==========================================
# CUADRO DE TEXTO INTEGRADO PARA EL AGENTE
# ==========================================
pregunta_usuario = st.text_input(
    "Hazle una pregunta técnica al Agente sobre el dataset:", 
    key="caja_consulta_final_titanic"
)

if pregunta_usuario:
    texto_limpio = pregunta_usuario.lower().strip()
    
    try:
        # Cargar los datos directamente en la interfaz
        df = pd.read_csv("dataset.csv")
        filas, columnas = df.shape
        total = len(df)
        
        # 1. Si pregunta por el Titanic o qué es
        if "titanic" in texto_limpio or "de que se trata" in texto_limpio:
            st.info(f"¡Confirmado! Este es el dataset oficial del Titanic. Contiene datos reales de {total} pasajeros con {columnas} variables técnicas como edad, sexo y supervivencia.")
            
        # 2. Si pregunta por sobrevivientes
        elif "sobrev" in texto_limpio or "tasa" in texto_limpio or "vivieron" in texto_limpio:
            sobrevivientes = df['Survived'].sum() if 'Survived' in df.columns else 0
            tasa = (sobrevivientes / total) * 100 if total > 0 else 0
            st.info(f"Análisis de supervivencia: De los {total} pasajeros, lograron salvarse {sobrevivientes} personas, lo que equivale a una tasa del {tasa:.2f}%.")
            
        # 3. Si pregunta explícitamente por filas o columnas
        elif "cuantas filas" in texto_limpio or "dimension" in texto_limpio or "matriz" in texto_limpio:
            st.info(f"La matriz del dataset contiene exactamente {filas} filas (registros de pasajeros) y {columnas} columnas (variables).")
            
        # 4. Respuesta por defecto para cualquier otra pregunta
        else:
            st.info(f"Procesando consulta: '{pregunta_usuario}'. Puedes preguntarme cosas como: '¿Cuál es la tasa de sobrevivientes?' o '¿De qué se trata el dataset?'")
            
    except Exception as e:
        st.error(f"No se pudo leer el archivo 'dataset.csv': {str(e)}")
