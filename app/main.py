import streamlit as st
import pandas as pd
import os
import plotly.express as px 
import plotly.graph_objects as go
from dotenv import load_dotenv
from groq import Groq
from fpdf import FPDF
import prompts
import utils

# Configuración Inicial
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or (st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else None)

st.set_page_config(page_title="AI Ops Mentor Pro", page_icon="🏭", layout="wide")

def generar_pdf(texto_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informe de Consultoría Industrial AI Ops", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    texto_limpio = texto_ia.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, texto_limpio)
    return bytes(pdf.output())

client = None
if api_key: client = Groq(api_key=api_key)

st.title("🏭 AI Ops Mentor: Inteligencia Industrial")

archivo = st.sidebar.file_uploader("Cargar Datos de Planta (CSV)", type=["csv"])

if archivo:
    # Procesamiento inicial
    df = utils.limpiar_datos(pd.read_csv(archivo))
    df = utils.detectar_anomalias(df)
    
    # --- SEMÁFORO DE SALUD GLOBAL ---
    estado, mensaje, color_bg = utils.calcular_salud_planta(df)
    st.markdown(f"""
        <div style="background-color: {color_bg}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.1); margin-bottom: 25px; text-align: center;">
            <h2 style="margin: 0; color: #333;">{estado}</h2>
            <p style="margin: 5px 0 0 0; color: #444; font-size: 1.2em;">{mensaje}</p>
        </div>
    """, unsafe_allow_html=True)

    # Datos para Rankings
    df_p = df.groupby('Empleado').agg({'Piezas_Producidas':'sum', 'Errores_Calidad':'sum'}).reset_index()
    df_p['Eficiencia'] = df_p['Piezas_Producidas'] / (df_p['Errores_Calidad'] + 1)

    tab1, tab2 = st.tabs(["📊 Análisis Histórico", "🔮 Inteligencia Predictiva"])

    with tab1:
        st.subheader("Desempeño y Eficiencia por Operario")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.bar(df_p.nlargest(5, 'Piezas_Producidas'), x='Empleado', y='Piezas_Producidas', title="Top 5: Más Producción", color='Piezas_Producidas', color_continuous_scale='Greens'), use_container_width=True)
            st.plotly_chart(px.bar(df_p.nlargest(5, 'Eficiencia'), x='Empleado', y='Eficiencia', title="Top 5: Más Eficientes", color='Eficiencia', color_continuous_scale='Blues'), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df_p.nlargest(5, 'Errores_Calidad'), x='Empleado', y='Errores_Calidad', title="Top 5: Más Errores", color='Errores_Calidad', color_continuous_scale='Reds'), use_container_width=True)
            st.plotly_chart(px.bar(df_p.nsmallest(5, 'Eficiencia'), x='Empleado', y='Eficiencia', title="Top 5: Menos Eficientes", color='Eficiencia', color_continuous_scale='YlOrRd'), use_container_width=True)

        st.divider()
        st.subheader("Control Semafórico Detallado")
        df_styled = df.drop(columns=['Anomalia']).style.applymap(lambda x: utils.estilo_semaforo(x, 'produccion'), subset=['Piezas_Producidas']).applymap(lambda x: utils.estilo_semaforo(x, 'error'), subset=['Errores_Calidad'])
        st.dataframe(df_styled, use_container_width=True)

    with tab2:
        st.subheader("Probabilidad Estadística y Futuros Riesgos")
        
        # Campana de Gauss
        df_gauss, mu, sigma = utils.calcular_curva_gauss(df)
        fig_gauss = px.area(df_gauss, x='Errores', y='Probabilidad', title="Distribución de Probabilidad de Errores")
        fig_gauss.add_vline(x=mu, line_dash="dash", line_color="black", annotation_text="Media")
        fig_gauss.add_vrect(x0=mu + 2*sigma, x1=df_gauss['Errores'].max(), fillcolor="red", opacity=0.2, annotation_text="Zona Anómala")
        st.plotly_chart(fig_gauss, use_container_width=True)
        
        

        col_ml1, col_ml2 = st.columns(2)
        with col_ml1:
            st.metric("Predicción Errores (+20% Volumen)", f"{utils.predecir_errores(df)} uds")
            st.write("💡 *Basado en Regresión Lineal de tendencia histórica.*")
        with col_ml2:
            st.plotly_chart(px.scatter(df, x='Piezas_Producidas', y='Errores_Calidad', color='Anomalia', title="Detección de Outliers Críticos", color_discrete_map={True:'red', False:'blue'}, hover_name='Empleado'), use_container_width=True)

    # --- IA CONSULTORÍA ---
    st.divider()
    if st.button("🪄 Generar Consultoría Estratégica"):
        if client:
            with st.spinner("Analizando KPIs y modelos predictivos..."):
                resumen = utils.generar_resumen_estadistico(df)
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": prompts.SYSTEM_PROMPT}, {"role": "user", "content": prompts.generar_prompt_analisis(resumen)}])
                st.session_state.informe_ia = response.choices[0].message.content
                st.success("### 💡 Diagnóstico de la IA")
                st.markdown(st.session_state.informe_ia)
                st.download_button("📥 Descargar Reporte PDF", data=generar_pdf(st.session_state.informe_ia), file_name="informe_estrategico.pdf")
else:
    st.info("Cargue un CSV para activar el diagnóstico de salud y el motor de IA.")