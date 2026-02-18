import pandas as pd
import random
from datetime import datetime, timedelta

# Configuramos los datos de los empleados
empleados = ["Ana García", "Luis Rodríguez", "Marta Sanz", "Carlos Ruiz", "Jorge López"]
fechas = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

datos = []

for fecha in fechas:
    for nombre in empleados:
        # Generamos datos aleatorios con lógica:
        # Algunos empleados son más productivos, otros tienen más errores
        if nombre == "Luis Rodríguez":
            piezas = random.randint(70, 90)  # Producción baja
            errores = random.randint(5, 12)  # Errores altos (Caso de estudio para la IA)
        elif nombre == "Ana García":
            piezas = random.randint(130, 150) # Producción muy alta
            errores = random.randint(0, 2)    # Muy eficiente
        else:
            piezas = random.randint(100, 120)
            errores = random.randint(1, 5)

        datos.append({
            "Fecha": fecha,
            "Empleado": nombre,
            "Piezas_Producidas": piezas,
            "Errores_Calidad": errores,
            "Horas_Trabajadas": 8
        })

# Crear DataFrame y guardar
df = pd.DataFrame(datos)
df.to_csv("datos_produccion.csv", index=False)

print("✅ Archivo 'datos_produccion.csv' generado correctamente.")
print("Ahora puedes subirlo a tu aplicación de Streamlit.")