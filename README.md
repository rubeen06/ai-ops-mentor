# 📈 AI Ops Mentor: Consultoría de Operaciones con IA Generativa

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](TU_LINK_DE_DESPLIEGUE_AQUI)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Ops Mentor** es una aplicación inteligente diseñada para optimizar la toma de decisiones en entornos industriales y de producción. Utiliza **IA Generativa (Llama 3 vía Groq)** para analizar datos de rendimiento y transformar hojas de cálculo crudas en planes de acción estratégicos.



---

## 🚀 Características Principales

* **Análisis Automatizado:** Carga de reportes en formato CSV con detección inteligente de métricas.
* **Dashboard Interactivo:** Visualización en tiempo real de la relación entre producción y calidad mediante gráficos de dispersión y barras (Plotly).
* **Ranking de Eficiencia:** Identificación automática de empleados estrella y perfiles con necesidades de mejora.
* **Consultoría con IA:** Integración con LLMs para generar diagnósticos personalizados, detectando patrones de fatiga, fallos de maquinaria o necesidades de capacitación.
* **Exportación de Resultados:** Descarga de los planes de acción sugeridos por la IA en formato de texto.

## 🛠️ Stack Tecnológico

* **Frontend:** [Streamlit](https://streamlit.io/) (Interfaz de usuario rápida y reactiva).
* **Análisis de Datos:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/).
* **Visualización:** [Plotly](https://plotly.com/python/).
* **Cerebro IA:** [Groq Cloud](https://groq.com/) (Llama 3.3 70B) para inferencia de baja latencia.
* **Entorno:** Python 3.11+, Dotenv para gestión de secretos.

## 📦 Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/rubeen06/ai-ops-mentor.git](https://github.com/rubeen06/ai-ops-mentor.git)
   cd ai-ops-mentor

1. **Crear el entorno virtual**
    ```bash  
    python -m venv venv
    ./venv/Scripts/activate

2. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt

3. **Configurar variables de entorno:**
    ```bash 
    GROQ_API_KEY=aqui_va_la_clave_

4. **Lanzar la aplicación:**
    ```bash
    streamlit run app/main.py    


**IMPACTO DEL NEGOCIO**
Este proyecto demuestra cómo la IA Aplicada puede reducir el tiempo de supervisión manual en un 80%, permitiendo a los jefes de planta enfocarse en la ejecución de mejoras en lugar de en el análisis tedioso de datos dispersos.

### Desarrollado por Rubén De la Nieta 