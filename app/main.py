import streamlit as st
import pandas as pd
import os
import plotly.express as px  # <-- Nueva librería para gráficos pro
from dotenv import load_dotenv
from groq import Groq

import prompts
import utils

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Ops Mentor", page_icon="📈", layout="wide")

st.title("📈 AI Ops Mentor: Dashboard Inteligente")

archivo = st.sidebar.file_uploader("Sube el reporte (CSV)", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)
    df = utils.limpiar_datos(df)
    
    # --- SECCIÓN DE GRÁFICOS ---
    st.subheader("📊 Análisis Visual de Rendimiento")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Gráfico 1: Producción Total por Empleado
        fig_prod = px.bar(df, x='Empleado', y='Piezas_Producidas', 
                         title="Producción Total por Empleado",
                         color='Empleado', text_auto=True)
        st.plotly_chart(fig_prod, use_container_width=True)

    with col_chart2:
        # Gráfico 2: Relación Producción vs Errores (Dispersión)
        # Esto ayuda a ver quién produce mucho pero con mala calidad
        fig_err = px.scatter(df, x='Piezas_Producidas', y='Errores_Calidad',
                            size='Errores_Calidad', color='Empleado',
                            title="Calidad vs Cantidad",
                            hover_name='Empleado')
        st.plotly_chart(fig_err, use_container_width=True)
    # --- SECCIÓN DE RANKING Y EFICIENCIA ---
    st.divider()
    st.subheader("🏆 Cuadro de Honor y Alertas")
    
    # Calculamos métricas por empleado
    df_emp = df.groupby('Empleado').agg({
        'Piezas_Producidas': 'sum',
        'Errores_Calidad': 'sum'
    }).reset_index()
    
    # Calculamos una métrica de eficiencia simple: piezas por cada error
    # Usamos +1 para evitar división por cero
    df_emp['Eficiencia'] = df_emp['Piezas_Producidas'] / (df_emp['Errores_Calidad'] + 1)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.write("**🚀 Producción**")
        max_prod = df_emp.loc[df_emp['Piezas_Producidas'].idxmax()]
        min_prod = df_emp.loc[df_emp['Piezas_Producidas'].idxmin()]
        st.success(f"🥇 **Más:** {max_prod['Empleado']} ({int(max_prod['Piezas_Producidas'])} uds)")
        st.error(f"🥉 **Menos:** {min_prod['Empleado']} ({int(min_prod['Piezas_Producidas'])} uds)")

    with c2:
        st.write("**🛡️ Calidad (Errores)**")
        max_err = df_emp.loc[df_emp['Errores_Calidad'].idxmax()]
        min_err = df_emp.loc[df_emp['Errores_Calidad'].idxmin()]
        st.error(f"⚠️ **Más:** {max_err['Empleado']} ({int(max_err['Errores_Calidad'])} err)")
        st.success(f"✅ **Menos:** {min_err['Empleado']} ({int(min_err['Errores_Calidad'])} err)")

    with c3:
        st.write("**✨ Eficiencia General**")
        best_eff = df_emp.loc[df_emp['Eficiencia'].idxmax()]
        worst_eff = df_emp.loc[df_emp['Eficiencia'].idxmin()]
        st.info(f"🏆 **Mejor:** {best_eff['Empleado']}")
        st.warning(f"📉 **Peor:** {worst_eff['Empleado']}")    

    # --- TABLA DE DATOS ---
    with st.expander("Ver datos detallados"):
        st.dataframe(df, use_container_width=True)

    # --- BOTÓN DE IA ---
    st.divider()
    if st.button("🪄 Generar Consultoría Estratégica"):
        with st.spinner("La IA está analizando los gráficos y datos..."):
            try:
                resumen = utils.generar_resumen_estadistico(df)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": prompts.SYSTEM_PROMPT},
                        {"role": "user", "content": prompts.generar_prompt_analisis(resumen)}
                    ]
                )
                st.success("### 💡 Diagnóstico de la IA")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")