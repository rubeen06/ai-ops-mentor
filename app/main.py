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

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or (st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else None)

st.set_page_config(page_title="AI Ops Mentor Pro", page_icon="🏭", layout="wide")

def generar_pdf(texto_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informe Estrategico AI Ops Mentor", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, texto_ia.encode('latin-1', 'replace').decode('latin-1'))
    return bytes(pdf.output())

client = None
if api_key: client = Groq(api_key=api_key)

st.title("🏭 AI Ops Mentor: Inteligencia Industrial")

archivo = st.sidebar.file_uploader("Cargar Reporte de Planta (CSV)", type=["csv"])

if archivo:
    df = utils.limpiar_datos(pd.read_csv(archivo))
    df = utils.detectar_anomalias(df)
    
    # Agrupación para Rankings
    df_persona = df.groupby('Empleado').agg({'Piezas_Producidas':'sum', 'Errores_Calidad':'sum'}).reset_index()
    df_persona['Eficiencia'] = df_persona['Piezas_Producidas'] / (df_persona['Errores_Calidad'] + 1)

    tab1, tab2 = st.tabs(["📊 Análisis (Histórico)", "🔮 Predictivo (Futuro)"])

    with tab1:
        st.subheader("Rankings de Desempeño")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.bar(df_persona.nlargest(5, 'Piezas_Producidas'), x='Empleado', y='Piezas_Producidas', title="Top 5: Mayor Producción", color_discrete_sequence=['#2ECC71']), use_container_width=True)
            st.plotly_chart(px.bar(df_persona.nlargest(5, 'Eficiencia'), x='Empleado', y='Eficiencia', title="Top 5: Más Eficientes", color_discrete_sequence=['#3498DB']), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df_persona.nlargest(5, 'Errores_Calidad'), x='Empleado', y='Errores_Calidad', title="Top 5: Más Errores", color_discrete_sequence=['#E74C3C']), use_container_width=True)
            st.plotly_chart(px.bar(df_persona.nsmallest(5, 'Eficiencia'), x='Empleado', y='Eficiencia', title="Top 5: Menos Eficientes", color_discrete_sequence=['#F1C40F']), use_container_width=True)

        st.subheader("Monitor de Datos (Control de Calidad)")
        st.dataframe(df.drop(columns=['Anomalia']).style.applymap(lambda x: utils.estilo_semaforo(x, 'produccion'), subset=['Piezas_Producidas']).applymap(lambda x: utils.estilo_semaforo(x, 'error'), subset=['Errores_Calidad']), use_container_width=True)

    with tab2:
        st.subheader("Probabilidad y Predicciones de Calidad")
        
        # --- CAMPANA DE GAUSS ---
        df_gauss, mu, sigma = utils.calcular_curva_gauss(df)
        fig_gauss = px.area(df_gauss, x='Errores', y='Probabilidad', title="Distribución Normal de Errores (Campana de Gauss)")
        fig_gauss.add_vline(x=mu, line_dash="dash", line_color="black", annotation_text="Media")
        fig_gauss.add_vrect(x0=mu + 2*sigma, x1=df_gauss['Errores'].max(), fillcolor="red", opacity=0.2, annotation_text="Zona de Anomalía")
        st.plotly_chart(fig_gauss, use_container_width=True)


        col_ml1, col_ml2 = st.columns(2)
        with col_ml1:
            st.metric("Predicción Errores (Carga +20%)", f"{utils.predecir_errores(df)} uds")
            st.write("💡 *La regresión lineal estima el impacto de la fatiga operativa.*")
        with col_ml2:
            st.plotly_chart(px.scatter(df, x='Piezas_Producidas', y='Errores_Calidad', color='Anomalia', title="Detección de Outliers", color_discrete_map={True:'red', False:'blue'}), use_container_width=True)

    # --- CONSULTORÍA IA ---
    if st.button("🪄 Generar Consultoría IA"):
        if client:
            with st.spinner("IA analizando la distribución y tendencias..."):
                resumen = utils.generar_resumen_estadistico(df)
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": prompts.SYSTEM_PROMPT}, {"role": "user", "content": prompts.generar_prompt_analisis(resumen)}])
                st.session_state.informe_ia = response.choices[0].message.content
                st.info(st.session_state.informe_ia)
                st.download_button("📥 Descargar Reporte PDF", data=generar_pdf(st.session_state.informe_ia), file_name="analisis_ia.pdf")
else:
    st.info("Sube un CSV para activar el motor de IA y Estadística.")