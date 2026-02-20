# 📈 AI Ops Mentor: Intelligent Industrial Consulting

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](TU_LINK_DE_DESPLIEGUE_AQUI)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Ops Mentor** es una solución avanzada de **Business Intelligence** y **Analítica Predictiva** diseñada para transformar datos operativos en decisiones estratégicas. Esta aplicación no solo visualiza el rendimiento, sino que utiliza **Machine Learning** y **IA Generativa (Llama 3.3)** para anticipar riesgos de fatiga y detectar anomalías estadísticas en tiempo real.

---

## 🚀 Características Principales

### 📊 Análisis Descriptivo (El Pasado)
* **Dashboards de Rendimiento:** Visualización de producción total y tasas de error por operario.
* **Rankings de Eficiencia:** Algoritmo personalizado que identifica a los 5 empleados más eficientes y los 5 que requieren capacitación técnica.
* **Control Semafórico:** Tabla de datos con formato condicional automático (Verde/Amarillo/Rojo) basado en umbrales críticos de calidad (Regla: >90 piezas = Verde | >10 errores = Rojo).

### 🔮 Análisis Predictivo (El Futuro)
* **Detección de Anomalías (Z-Score):** Identificación automática de "Outliers" o puntos críticos de error que se desvían de la norma estadística.
* **Previsión de Fatiga (Regresión Lineal):** Modelo entrenado para predecir el incremento de errores basado en el aumento del volumen de producción.
* **Campana de Gauss (Distribución Normal):** Visualización de la probabilidad de fallos en planta, marcando zonas de riesgo estadístico.


### 🪄 IA Generativa & Consultoría
* **Reportes Ejecutivos:** La IA analiza las métricas y las predicciones de ML para redactar un plan de acción profesional.
* **Exportación PDF:** Generación instantánea de informes descargables con el diagnóstico de la IA.

---

## 🛠️ Stack Tecnológico

* **Interfaz:** [Streamlit](https://streamlit.io/)
* **Machine Learning:** [Scikit-Learn](https://scikit-learn.org/) (Linear Regression) & [SciPy](https://scipy.org/) (Gaussian Stats)
* **Visualización:** [Plotly Express](https://plotly.com/python/)
* **Motor de IA:** [Groq Cloud](https://groq.com/) (Llama 3.3 70B)
* **Generación de Documentos:** [FPDF2](https://github.com/fpdf2/fpdf2)

---

## 📦 Instalación Local

1.  **Clonar repositorio:**
    ```bash
    git clone [https://github.com/rubeen06/ai-ops-mentor.git](https://github.com/rubeen06/ai-ops-mentor.git)
    cd ai-ops-mentor
    ```

2.  **Configurar entorno:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Variables de Entorno:**
    Crea un archivo `.env` en la raíz y añade tu API Key:
    ```env
    GROQ_API_KEY=tu_clave_aqui
    ```

4.  **Ejecutar:**
    ```bash
    streamlit run app/main.py
    ```

---

## 📈 Impacto de Negocio
Este proyecto demuestra cómo la **IA Aplicada** puede optimizar la cadena de suministro y la gestión de talento:
1.  **Reducción del 90%** en el tiempo de análisis manual de reportes de planta.
2.  **Identificación proactiva** de cuellos de botella mediante modelos de regresión.
3.  **Digitalización total** de la consultoría de operaciones.

---
**Desarrollado por Rubén De la Nieta** 