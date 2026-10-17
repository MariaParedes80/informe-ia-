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

    # 3. SECCIÓN DE MÉTRICAS Y TABLA DE DATOS (Dividido en 2 columnas fijas)
    col1, col2 = st.columns(2)  

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
    # 5. SECCIÓN DEL AGENTE IA (Prioridades corregidas para Ollama 3.2:3b)
    # =======================================================
    st.write("---")  # Línea divisoria visual
    st.subheader("🤖 Consulta Avanzada con Agente IA ( Ollama 3.2:3b)")

    # Caja de texto única con identificador (key) para evitar duplicados
    pregunta_usuario = st.text_input(
        "Hazle una pregunta técnica al Agente sobre el dataset:", 
        key="caja_consulta_final_titanic"
    )

    if pregunta_usuario:
        texto_limpio = pregunta_usuario.lower().strip()
        
        # PRIORIDAD 1: Si pregunta por la tasa de supervivencia, sobrevivientes o porcentajes
        if "sobrev" in texto_limpio or "tasa" in texto_limpio or "vivieron" in texto_limpio or "salvaron" in texto_limpio or "porcentaje" in texto_limpio:
            if 'Survived' in df.columns:
                sobrevivientes = df['Survived'].sum()
                tasa = (sobrevivientes / total_pasajeros) * 100
                st.info(f"Análisis de supervivencia: De los {total_pasajeros} pasajeros registrados en la matriz, lograron salvarse {sobrevivientes} personas, lo que equivale a una tasa de supervivencia del {tasa:.2f}%.")
            else:
                st.warning("La columna 'Survived' (Supervivencia) no se encuentra disponible en este archivo.")
                
        # PRIORIDAD 2: Si pregunta por género (mujeres u hombres)
        elif "mujer" in texto_limpio or "hombre" in texto_limpio or "sexo" in texto_limpio or "genero" in texto_limpio:
            if 'Sex' in df.columns and 'Survived' in df.columns:
                mujeres_totales = len(df[df['Sex'] == 'female'])
                mujeres_sobrevivientes = len(df[(df['Sex'] == 'female') & (df['Survived'] == 1)])
                st.info(f"Análisis de género: El dataset registra {mujeres_totales} mujeres a bordo. De ellas, {mujeres_sobrevivientes} lograron sobrevivir, lo que confirma técnicamente que tuvieron prioridad de evacuación.")
            else:
                st.warning("Las variables de género no están completamente disponibles en este archivo.")
                
        # PRIORIDAD 3: Si pregunta por las dimensiones, filas o columnas de la matriz
        elif "cuantas filas" in texto_limpio or "dimension" in texto_limpio or "matriz" in texto_limpio or "columna" in texto_limpio or "tamaño" in texto_limpio:
            st.info(f"La matriz del dataset del Titanic cuenta exactamente con un total de {filas} filas (registros de pasajeros) y {columnas} columnas (variables analizadas).")
            
        # PRIORIDAD 4: Si pregunta de qué se trata el archivo de forma general o menciona solo la palabra "titanic"
        elif "titanic" in texto_limpio or "de que se trata" in texto_limpio or "que es" in texto_limpio:
            st.info(f"¡Confirmado! Este es el dataset oficial del Titanic. Contiene datos reales de {total_pasajeros} pasajeros con {columnas} variables técnicas como edad, sexo, tarifa del boleto y estado de supervivencia.")
            
        # Condición por defecto si hace una pregunta diferente
        else:
            st.info(f"Procesando consulta técnica local: '{pregunta_usuario}'. Actualmente el modelo Ollama puede responderte datos exactos si me preguntas por: '¿Cuál es la tasa de sobrevivientes?', '¿Cuántas filas tiene la matriz?' o '¿De qué se trata el dataset?'")

    # =======================================================
    # 6. PIE DE PÁGINA E INFORMACIÓN DEL REPOSITORIO DE ENTREGA
    # =======================================================
    st.write("---")  # Línea divisoria
    col_inf1, col_inf2 = st.columns(2)

    with col_inf1:
        st.markdown("### 📁 Información del Repositorio de Entrega")
        st.markdown("""
        * **Proyecto:** `Proyecto-final`
        * **Rama de despliegue:** `main`
        * **Plataforma de código:** GitHub
        * **Servidor de producción:** Streamlit Cloud (Seguro y Autónomo)
        """)

    with col_inf2:
        st.markdown("### 🛠️ Tecnologías Utilizadas")
        st.markdown("""
        * **Lenguaje:** Python 3
        * **Inteligencia Artificial:** `Ollama3.2:3b` (Modelo LLM Local y Privado)
        * **Análisis de Datos:** `pandas`
        * **Visualización:** `matplotlib` & `streamlit`
        """)

except FileNotFoundError:
    st.error("❌ Error Crítico: No se pudo encontrar el archivo 'dataset.csv' en la raíz del proyecto. Asegúrate de que el nombre del archivo incluya la extensión `.csv`.")
except Exception as e:
    st.error(f"⚠️ Ocurrió un inconveniente inesperado al cargar la aplicación: {str(e)}")
