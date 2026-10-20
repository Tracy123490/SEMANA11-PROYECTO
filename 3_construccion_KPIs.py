from pathlib import Path
import pandas as pd

#cargar el dataset
df = pd.read_csv("Pervious_Concrete_0.csv")
df.columns = df.columns.str.strip()

# Eliminar filas duplicadas
duplicados = int(df.duplicated().sum())
df = df.drop_duplicates()

# Columnas usadas para calcular los KPI (nombres exactos del CSV)
columna_resistencia = "Compressive Strength (Kg/m2)"
columna_edad = "Age (Day)"
columnas_requeridas = [columna_resistencia, columna_edad]
columnas_faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]

if columnas_faltantes:
    raise KeyError(f"Faltan columnas requeridas en el CSV: {columnas_faltantes}")

# Calcular KPI
resistencia_promedio = df[columna_resistencia].mean()
resistencia_maxima = df[columna_resistencia].max()
resistencia_minima = df[columna_resistencia].min()
cantidad_registros = len(df)
edad_promedio = df[columna_edad].mean()

# Mostrar resultados
print(f"Filas duplicadas eliminadas: {duplicados}")
print(f"Resistencia promedio: {resistencia_promedio:.2f} Kg/m2")
print(f"Resistencia máxima: {resistencia_maxima:.2f} Kg/m2")
print(f"Resistencia mínima: {resistencia_minima:.2f} Kg/m2")
print(f"Número de registros: {cantidad_registros}")
print(f"Edad promedio: {edad_promedio:.2f} días")
