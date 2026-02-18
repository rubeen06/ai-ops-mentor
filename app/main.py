import streamlit as st
import pandas as pd
import os
import plotly.express as px 
from dotenv import load_dotenv
from groq import Groq

# Importamos tus módulos locales
import prompts
import utils

# 1. Intentar cargar desde el archivo .env (solo para local)
load_dotenv()

# 2. Lógica Robusta para la API KEY
# Primero intentamos os.getenv, si falla, intentamos st.secrets
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

# 3. Solo ahora inicializamos el cliente
if api_key:
    client = Groq(api_key=api_key)
else:
    st.error("❌ No se encontró la GROQ_API_KEY. Verifica los Secrets en Streamlit Cloud.")
    st.stop() # Detiene la ejecución aquí si no hay llave

# Inicializamos el cliente oficial de Groq
client = Groq(api_key=api_key)

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="AI Ops Mentor | Dashboard", 
    page_icon="🚀", 
    layout="wide"
)

# Estilo personalizado para mejorar la visibilidad
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏭 AI Ops Mentor: Inteligencia de Planta")
st.subheader("Análisis de productividad y calidad con Llama 3")

# --- 3. CARGA DE DATOS ---
with st.sidebar:
    st.header("📥 Entrada de Datos")
    archivo = st.file_uploader("Sube tu reporte CSV", type=["csv"])
    st.divider()
    st.markdown("**Columnas requeridas:**")
    st.code("Empleado, Piezas_Producidas, Errores_Calidad")

if archivo:
    # Procesar datos con tus utilidades
    df = pd.read_csv(archivo)
    df = utils.limpiar_datos(df)
    
    # --- 4. DASHBOARD VISUAL ---
    st.subheader("📊 Visualización de Rendimiento")
    col1, col2 = st.columns(2)

    with col1:
        fig_prod = px.bar(df, x='Empleado', y='Piezas_Producidas', 
                         title="Producción Total por Operario",
                         color='Empleado', text_auto=True)
        st.plotly_chart(fig_prod, use_container_width=True)

    with col2:
        fig_err = px.scatter(df, x='Piezas_Producidas', y='Errores_Calidad',
                            size='Errores_Calidad', color='Empleado',
                            title="Matriz: Cantidad vs Calidad (Errores)",
                            hover_name='Empleado')
        st.plotly_chart(fig_err, use_container_width=True)

    # --- 5. INDICADORES CLAVE (KPIs) ---
    st.divider()
    st.subheader("🏆 Hallazgos Clave")
    
    # Cálculos rápidos
    df_emp = df.groupby('Empleado').agg({
        'Piezas_Producidas': 'sum', 
        'Errores_Calidad': 'sum'
    }).reset_index()
    df_emp['Eficiencia'] = df_emp['Piezas_Producidas'] / (df_emp['Errores_Calidad'] + 1)

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        mejor_prod = df_emp.loc[df_emp['Piezas_Producidas'].idxmax()]
        st.metric("Máxima Producción", mejor_prod['Empleado'], f"{int(mejor_prod['Piezas_Producidas'])} uds")

    with kpi2:
        peor_calidad = df_emp.loc[df_emp['Errores_Calidad'].idxmax()]
        st.metric("Alerta de Calidad", peor_calidad['Empleado'], f"{int(peor_calidad['Errores_Calidad'])} errores", delta_color="inverse")

    with kpi3:
        mejor_efi = df_emp.loc[df_emp['Eficiencia'].idxmax()]
        st.metric("Mayor Eficiencia", mejor_efi['Empleado'], "Líder")

    # --- 6. CONSULTORÍA CON IA ---
    st.divider()
    if st.button("🪄 Generar Consultoría Estratégica"):
        with st.spinner("Llama 3 analizando patrones de producción..."):
            try:
                resumen_para_ia = utils.generar_resumen_estadistico(df)
                
                # Llamada a la API de Groq
                # Usamos el modelo 8b que es más estable y rápido para el nivel gratuito
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": prompts.SYSTEM_PROMPT},
                        {"role": "user", "content": prompts.generar_prompt_analisis(resumen_para_ia)}
                    ]
                )
                
                st.success("### 💡 Diagnóstico y Plan de Acción")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error en la comunicación con la IA: {e}")

else:
    st.info("👋 Por favor, sube un archivo CSV en la barra lateral para comenzar el análisis.")
    # Imagen ilustrativa
    st.image("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=1000", caption="Análisis Industrial Inteligente")