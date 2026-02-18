import pandas as pd

def limpiar_datos(df):
    """
    Limpia el DataFrame: elimina nulos y asegura formatos correctos.
    """
    # Eliminar filas completamente vacías
    df = df.dropna(how='all')
    
    # Asegurar que las columnas numéricas sean números (por si hay texto por error)
    cols_numericas = ['Piezas_Producidas', 'Errores_Calidad', 'Horas_Trabajadas']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    return df

def generar_resumen_estadistico(df):
    """
    Crea un resumen compacto para enviar a la IA sin gastar muchos tokens.
    """
    total_piezas = df['Piezas_Producidas'].sum()
    promedio_errores = df['Errores_Calidad'].mean()
    
    # Agrupamos por empleado para ver quién destaca
    rendimiento = df.groupby('Empleado').agg({
        'Piezas_Producidas': 'sum',
        'Errores_Calidad': 'sum'
    }).to_dict()

    resumen_texto = f"""
    DATOS GENERALES:
    - Total piezas: {total_piezas}
    - Promedio errores: {promedio_errores:.2f}
    
    DETALLE POR EMPLEADO:
    {rendimiento}
    """
    return resumen_texto