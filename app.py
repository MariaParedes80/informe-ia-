import streamlit as st
import os

# Configuración inicial de la interfaz gráfica de Streamlit
st.set_page_config(
    page_title="Proyecto Final - Agente IA Local", 
    page_icon="🎓", 
    layout="wide"
)

# Intentar importar los módulos de tu carpeta src/ de forma segura
try:
    from src.data_loader import cargar_datos
    from src.eda import obtener_resumen_estadistico
    from src.visualizations import generar_grafico_distribucion
    from src.agent import agente_analista
except ImportError as e:
    st.error(f"❌ Error en la estructura de archivos dentro de 'src/': {e}")
    st.stop()

st.title("🎓 Sistema Inteligente de Análisis Local (Llama 3.2:3b)")
st.markdown("---")

# --- PASO 1: CARGA RESILIENTE DE DATOS ---
try:
    df = cargar_datos()
    st.sidebar.success("✅ Dataset cargado correctamente.")
except FileNotFoundError as err:
    st.error("⚠️ **Control de Entorno (Dataset Ausente):**")
    st.info(str(err))
    st.stop()

# --- PASO 2: INTERFAZ DE ANÁLISIS DE DATOS (EDA) ---
st.header("📊 Análisis Exploratorio y Visualización")
resumen = obtener_resumen_estadistico(df)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Métricas del Archivo")
    st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    st.dataframe(df.head(5), use_container_width=True)

with col2:
    st.subheader("Visualizaciones Automáticas")
    
    # Tomamos todas las columnas disponibles del archivo
    todas_las_columnas = df.columns.tolist()
    
    if todas_las_columnas:
        col_seleccionada = st.selectbox("Seleccione columna para graficar:", todas_las_columnas)
        try:
            figura = generar_grafico_distribucion(df, col_seleccionada)
            st.pyplot(figura)
        except Exception:
            st.warning("⚠️ Esta columna contiene texto. Seleccione otra numérica (como temp_max o wind) para renderizar el gráfico.")
    else:
        st.write("No se encontraron columnas en el archivo.")

st.markdown("---")

# --- PASO 3: INTERFAZ CON AGENTE DE IA (LLM CLIENT) ---
st.header("🤖 Consulta Avanzada con Agente IA")
pregunta = st.text_input("Hazle una pregunta técnica al Agente sobre el dataset:")

if pregunta:
    with st.spinner("El Agente está analizando y procesando con Llama 3.2:3b..."):
        try:
            # Mandamos un resumen como contexto estructurado al agente
            contexto = f"Columnas del dataset: {resumen['columnas']}. Dimensiones: {resumen['dimensiones']}."
            respuesta_agente = agente_analista(contexto, pregunta)
            st.chat_message("assistant").write(respuesta_agente)
        except ConnectionError as conn_err:
            st.error("❌ **Error de Infraestructura Local:**")
            st.warning(str(conn_err))
        except FileNotFoundError as model_err:
            st.error("❌ **Error de Configuración de Modelo:**")
            st.warning(str(model_err))
        except Exception as e:
            st.error(f"❌ Error inesperado: {e}")

# 1. Creamos la caja de texto y guardamos lo que escribe el usuario en la variable 'pregunta_usuario'
pregunta_usuario = st.text_input("Hazle una pregunta técnica al Agente sobre el dataset:")

# 2. Solo si el usuario escribió algo, llamamos al agente pasándole SU pregunta
if pregunta_usuario:
    respuesta = agente_analista(pregunta_usuario) # <-- ¡Aquí debe ir la variable, SIN COMILLAS!
    st.write(respuesta)
