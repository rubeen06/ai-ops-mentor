import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats as stats

def limpiar_datos(df):
    """Limpia los datos y asegura que las columnas sean numéricas."""
    df = df.dropna()
    df['Piezas_Producidas'] = pd.to_numeric(df['Piezas_Producidas'], errors='coerce')
    df['Errores_Calidad'] = pd.to_numeric(df['Errores_Calidad'], errors='coerce')
    return df.fillna(0)

def detectar_anomalias(df):
    """Detección estadística de anomalías usando Z-Score."""
    media = df['Errores_Calidad'].mean()
    std = df['Errores_Calidad'].std()
    df['Anomalia'] = df['Errores_Calidad'] > (media + 2 * std) if std > 0 else False
    return df

def estilo_semaforo(val, tipo='produccion'):
    """Formato condicional para la tabla de datos."""
    if tipo == 'produccion':
        color = 'background-color: #00ff3c; color: #155724' if val >= 90 else 'background-color: #f8d7da; color: #721c24'
    elif tipo == 'error':
        if val > 10: color = 'background-color: #e9091c; color: #721c24'
        elif val == 10: color = 'background-color: #ffc70e; color: #856404'
        else: color = 'background-color: #d4edda; color: #155724'
    return color

def predecir_errores(df):
    """Regresión Lineal para predecir fatiga operativa."""
    if len(df) < 2: return 0.0
    X = df[['Piezas_Producidas']].values
    y = df['Errores_Calidad'].values
    modelo = LinearRegression().fit(X, y)
    proxima_prod = np.array([[df['Piezas_Producidas'].max() * 1.2]])
    prediccion = modelo.predict(proxima_prod)
    return round(float(prediccion[0]), 2)

def calcular_salud_planta(df):
    """Calcula el estado global de la planta cruzando KPIs y ML."""
    eficiencia_media = (df['Piezas_Producidas'].sum() / (df['Errores_Calidad'].sum() + 1))
    score_eficiencia = min(100, eficiencia_media * 10) 
    num_anomalias = len(df[df['Anomalia'] == True])
    riesgo_futuro = predecir_errores(df)
    
    if score_eficiencia > 85 and num_anomalias == 0 and riesgo_futuro < 12:
        return "🟢 SALUD ÓPTIMA", "Operación estable. Alta eficiencia y riesgo controlado.", "#00ff3c"
    elif num_anomalias > 1 or riesgo_futuro > 20:
        return "🔴 RIESGO CRÍTICO", "Se detectan anomalías o alta probabilidad de fallos por fatiga.", "#e9091c"
    else:
        return "🟡 ATENCIÓN REQUERIDA", "Rendimiento moderado. Se recomienda monitoreo preventivo.", "#ffc70e"

def calcular_curva_gauss(df):
    """Genera los puntos para la campana de Gauss."""
    errores = df['Errores_Calidad']
    mu, sigma = errores.mean(), errores.std()
    if sigma == 0: sigma = 0.1
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = stats.norm.pdf(x, mu, sigma)
    df_gauss = pd.DataFrame({'Errores': x, 'Probabilidad': y})
    return df_gauss, mu, sigma

def generar_resumen_estadistico(df):
    """Resumen para el contexto de la IA."""
    df_p = df.groupby('Empleado').agg({'Piezas_Producidas':'sum', 'Errores_Calidad':'sum'}).reset_index()
    df_p['Eficiencia'] = df_p['Piezas_Producidas'] / (df_p['Errores_Calidad'] + 1)
    
    top_eff = df_p.nlargest(1, 'Eficiencia')['Empleado'].iloc[0]
    anomalias = df[df['Anomalia'] == True]['Empleado'].unique().tolist()
    
    return f"""
    - Producción Total: {df['Piezas_Producidas'].sum()}
    - Líder de Eficiencia: {top_eff}
    - Predicción Errores Futuros: {predecir_errores(df)}
    - Empleados con Anomalías: {', '.join(anomalias) if anomalias else 'Ninguno'}
    """