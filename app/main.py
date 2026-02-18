import streamlit as st
import pandas as pd
import os
import plotly.express as px 
from dotenv import load_dotenv
from groq import Groq

# Importamos nuestros módulos locales
import prompts
import utils

# 1. Configuración de seguridad y API Key
load_dotenv() # Carga desde .env en local

# Intentamos obtener la clave de tres formas para evitar errores en el despliegue
api_key = os.getenv("GROQ_API_KEY") 

if not api_key:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error("⚠️ No se encontró la API Key. Por favor, configúrala en el archivo .env o en los Secrets de Streamlit.")
    st.stop()

# Inicialización del cliente de IA
client = Groq(api_key=api_key)

# 2. Configuración de la interfaz
st.set_page_config(page_title="AI Ops Mentor", page_icon="📈", layout="wide")

st.title("📈 AI Ops Mentor: Dashboard Inteligente")
st.markdown("Analizador de rendimiento industrial impulsado por Llama 3")

# Barra lateral para carga de archivos
with st.sidebar:
    st.header("Carga de Datos")
    archivo = st.file_uploader("Sube el reporte semanal (CSV)", type=["csv"])
    st.info("El archivo debe contener columnas: Empleado, Piezas_Producidas, Errores_Calidad.")

if archivo:
    # 3. Procesamiento de datos
    df = pd.read_csv(archivo)
    df = utils.limpiar_datos(df)
    
    # --- SECCIÓN DE GRÁFICOS ---
    st.subheader("📊 Análisis Visual de Rendimiento")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Gráfico 1: Producción Total por Empleado
        fig_prod = px.bar(df, x='Empleado', y='Piezas_Producidas', 
                         title="Producción Total por Empleado",
                         color='Empleado', text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_prod, use_container_width=True)

    with col_chart2:
        # Gráfico 2: Relación Producción vs Errores (Dispersión)
        fig_err = px.scatter(df, x='Piezas_Producidas', y='Errores_Calidad',
                            size='Errores_Calidad', color='Empleado',
                            title="Matriz de Calidad vs Cantidad",
                            hover_name='Empleado',
                            labels={'Piezas_Producidas': 'Producción', 'Errores_Calidad': 'Fallos'})
        st.plotly_chart(fig_err, use_container_width=True)

    # --- SECCIÓN DE RANKING Y EFICIENCIA ---
    st.divider()
    st.subheader("🏆 Cuadro de Honor y Alertas de Calidad")
    
    # Agrupación de métricas
    df_emp = df.groupby('Empleado').agg({
        'Piezas_Producidas': 'sum',
        'Errores_Calidad': 'sum'
    }).reset_index()
    
    # Cálculo de métrica de eficiencia (Producción por cada error)
    df_emp['Eficiencia'] = df_emp['Piezas_Producidas'] / (df_emp['Errores_Calidad'] + 1)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 🚀 Producción")
        max_prod = df_emp.loc[df_emp['Piezas_Producidas'].idxmax()]
        min_prod = df_emp.loc[df_emp['Piezas_Producidas'].idxmin()]
        st.success(f"🥇 **Líder:** {max_prod['Empleado']} ({int(max_prod['Piezas_Producidas'])} uds)")
        st.error(f"🥉 **Menor:** {min_prod['Empleado']} ({int(min_prod['Piezas_Producidas'])} uds)")

    with c2:
        st.markdown("#### 🛡️ Calidad (Errores)")
        max_err = df_emp.loc[df_emp['Errores_Calidad'].idxmax()]
        min_err = df_emp.loc[df_emp['Errores_Calidad'].idxmin()]
        st.error(f"⚠️ **Crítico:** {max_err['Empleado']} ({int(max_err['Errores_Calidad'])} err)")
        st.success(f"✅ **Óptimo:** {min_err['Empleado']} ({int(min_err['Errores_Calidad'])} err)")

    with c3:
        st.markdown("#### ✨ Eficiencia General")
        best_eff = df_emp.loc[df_emp['Eficiencia'].idxmax()]
        worst_eff = df_emp.loc[df_emp['Eficiencia'].idxmin()]
        st.info(f"🏆 **Mejor Perfil:** {best_eff['Empleado']}")
        st.warning(f"📉 **Bajo Rendimiento:** {worst_eff['Empleado']}")    

    # --- TABLA DE DATOS ---
    with st.expander("🔍 Ver dataset completo y detallado"):
        st.dataframe(df, use_container_width=True)

    # --- CONSULTORÍA CON IA ---
    st.divider()
    if st.button("🪄 Generar Consultoría Estratégica con IA"):
        with st.spinner("La IA está analizando los datos y patrones de producción..."):
            try:
                # Preparamos el resumen para enviárselo a la IA
                resumen = utils.generar_resumen_estadistico(df)
                
                # Llamada a Groq Cloud
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": prompts.SYSTEM_PROMPT},
                        {"role": "user", "content": prompts.generar_prompt_analisis(resumen)}
                    ]
                )
                
                # Mostramos el resultado de la IA
                st.success("### 💡 Informe de Diagnóstico y Plan de Acción")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"No se pudo completar la consultoría: {e}")
else:
    # Estado inicial cuando no hay archivo
    st.info("👋 Bienvenida/o. Por favor, sube un archivo CSV en la barra lateral para comenzar el análisis.")
    st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=1000", caption="Optimización Industrial mediante IA")