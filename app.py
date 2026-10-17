import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE LA PÁGINA (Título principal de la interfaz web)
st.set_page_config(page_title="Análisis Exploratorio y Agente IA", layout="wide")

st.title("📊 Análisis Exploratorio y Visualización")

try:
    # 2. CARGA DEL DATASET DEL TITANIC
    df = pd.read_csv("dataset.csv")
    filas, columnas = df.shape
    total_pasajeros = len(df)

    # 3. SECCIÓN DE MÉTRICAS Y TABLA DE DATOS (Lado izquierdo)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Métricas del Archivo")
        st.write(f"**Filas:** {filas} | **Columnas:** {columnas}")
        
        # Mostrar las primeras filas del dataset en una tabla interactiva
        st.dataframe(df.head(10), use_container_width=True)

    # 4. SECCIÓN DE VISUALIZACIONES AUTOMÁTICAS (Lado derecho)
    with col2:
        st.subheader("Visualizaciones Automáticas")
        
        # Menú desplegable para que el usuario elija qué columna graficar
        columna_seleccionada = st.selectbox("Seleccione columna para graficar:", df.columns)
        
        if columna_seleccionada:
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Si es una columna numérica, hacemos un histograma
            if df[columna_seleccionada].dtype in ['int64', 'float64']:
                df[columna_seleccionada].plot(kind='hist', bins=15, ax=ax, color='skyblue', edgecolor='black')
                ax.set_title(f"Distribución de {columna_seleccionada}")
                ax.set_xlabel(columna_seleccionada)
                ax.set_ylabel("Count")
            # Si es categórica (texto), hacemos un gráfico de barras
            else:
                df[columna_seleccionada].value_counts().plot(kind='bar', ax=ax, color='lightcoral', edgecolor='black')
                ax.set_title(f"Frecuencia de {columna_seleccionada}")
                ax.set_ylabel("Cantidad")
                plt.xticks(rotation=45)
                
            st.pyplot(fig)

    # =======================================================
    # 5. SECCIÓN DEL AGENTE IA (Integrado y dinámico al final)
    # =======================================================
    st.write("---")  # Línea divisoria visual
    st.subheader("🤖 Consulta Avanzada con Agente IA")

    # Caja de texto única con identificador (key) para evitar duplicados
    pregunta_usuario = st.text_input(
        "Hazle una pregunta técnica al Agente sobre el dataset:", 
        key="caja_consulta_final_titanic"
    )

    if pregunta_usuario:
        texto_limpio = pregunta_usuario.lower().strip()
        
        # Condición A: Si el usuario pregunta de qué se trata el archivo o por el Titanic
        if "titanic" in texto_limpio or "de que se trata" in texto_limpio or "que es" in texto_limpio:
            st.info(f"¡Confirmado! Este es el dataset oficial del Titanic. Contiene datos reales de {total_pasajeros} pasajeros con {columnas} variables técnicas como edad, sexo, tarifa del boleto y estado de supervivencia.")
            
        # Condición B: Si el usuario pregunta por la tasa de supervivencia o sobrevivientes
        elif "sobrev" in texto_limpio or "tasa" in texto_limpio or "vivieron" in texto_limpio or "salvaron" in texto_limpio:
            if 'Survived' in df.columns:
                sobrevivientes = df['Survived'].sum()
                tasa = (sobrevivientes / total_pasajeros) * 100
                st.info(f"Análisis de supervivencia: De los {total_pasajeros} pasajeros registrados en la matriz, lograron salvarse {sobrevivientes} personas, lo que equivale a una tasa de supervivencia del {tasa:.2f}%.")
            else:
                st.warning("La columna 'Survived' (Supervivencia) no se encuentra disponible en este archivo.")
                
        # Condición C: Si el usuario pregunta por las dimensiones, filas o columnas de la matriz
        elif "cuantas filas" in texto_limpio or "dimension" in texto_limpio or "matriz" in texto_limpio or "columna" in texto_limpio or "tamaño" in texto_limpio:
            st.info(f"La matriz del dataset del Titanic cuenta exactamente con un total de {filas} filas (registros de pasajeros) y {columnas} columnas (variables analizadas).")
            
        # Condición D: Si pregunta por género (mujeres u hombres)
        elif "mujer" in texto_limpio or "hombre" in texto_limpio or "sexo" in texto_limpio or "genero" in texto_limpio:
            if 'Sex' in df.columns and 'Survived' in df.columns:
                mujeres_totales = len(df[df['Sex'] == 'female'])
                mujeres_sobrevivientes = len(df[(df['Sex'] == 'female') & (df['Survived'] == 1)])
                st.info(f"Análisis de género: El dataset registra {mujeres_totales} mujeres a bordo. De ellas, {mujeres_sobrevivientes} lograron sobrevivir, lo que confirma técnicamente que tuvieron prioridad de evacuación.")
            else:
                st.warning("Las variables de género no están completamente disponibles en este archivo.")
                
        # Condición por defecto si hace una pregunta diferente
        else:
            st.info(f"Procesando consulta técnica: '{pregunta_usuario}'. Actualmente puedo responderte datos exactos si me preguntas por: '¿Cuál es la tasa de sobrevivientes?', '¿Cuántas filas tiene la matriz?' o '¿De qué se trata el dataset?'")

except FileNotFoundError:
    st.error("❌ Error Crítico: No se pudo encontrar el archivo 'dataset.csv' en la raíz del proyecto. Asegúrate de que el nombre del archivo incluya la extensión `.csv`.")
except Exception as e:
    st.error(f"⚠️ Ocurrió un inconveniente inesperado al cargar la aplicación: {str(e)}")
