import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats as stats

def limpiar_datos(df):
    df = df.dropna()
    df['Piezas_Producidas'] = pd.to_numeric(df['Piezas_Producidas'], errors='coerce')
    df['Errores_Calidad'] = pd.to_numeric(df['Errores_Calidad'], errors='coerce')
    return df.fillna(0)

def detectar_anomalias(df):
    media = df['Errores_Calidad'].mean()
    std = df['Errores_Calidad'].std()
    df['Anomalia'] = df['Errores_Calidad'] > (media + 2 * std) if std > 0 else False
    return df

def estilo_semaforo(val, tipo='produccion'):
    if tipo == 'produccion':
        color = 'background-color: #d4edda; color: #155724' if val >= 90 else 'background-color: #f8d7da; color: #721c24'
    elif tipo == 'error':
        if val > 10: color = 'background-color: #f8d7da; color: #721c24'
        elif val == 10: color = 'background-color: #fff3cd; color: #856404'
        else: color = 'background-color: #d4edda; color: #155724'
    return color

def predecir_errores(df):
    if len(df) < 2: return 0.0
    X = df[['Piezas_Producidas']].values
    y = df['Errores_Calidad'].values
    modelo = LinearRegression().fit(X, y)
    proxima_prod = np.array([[df['Piezas_Producidas'].max() * 1.2]])
    prediccion = modelo.predict(proxima_prod)
    return round(float(prediccion[0]), 2)

def calcular_curva_gauss(df):
    errores = df['Errores_Calidad']
    mu, sigma = errores.mean(), errores.std()
    if sigma == 0: sigma = 0.1
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = stats.norm.pdf(x, mu, sigma)
    df_gauss = pd.DataFrame({'Errores': x, 'Probabilidad': y})
    return df_gauss, mu, sigma

def generar_resumen_estadistico(df):
    df_persona = df.groupby('Empleado').agg({'Piezas_Producidas':'sum', 'Errores_Calidad':'sum'}).reset_index()
    df_persona['Eficiencia'] = df_persona['Piezas_Producidas'] / (df_persona['Errores_Calidad'] + 1)
    
    top_eff = df_persona.nlargest(1, 'Eficiencia')['Empleado'].iloc[0]
    anomalias = df[df['Anomalia'] == True]['Empleado'].unique().tolist()
    
    return f"""
    - Producción Total: {df['Piezas_Producidas'].sum()}
    - Empleado más eficiente: {top_eff}
    - Predicción de errores (fatiga): {predecir_errores(df)}
    - Alertas críticas detectadas en: {', '.join(anomalias) if anomalias else 'Ninguna'}
    """