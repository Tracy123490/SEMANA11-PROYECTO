from pathlib import Path
import pandas as pd
import plotly.express as px

# Cargar el dataset desde la misma carpeta que este script.
df = pd.read_csv("Pervious_Concrete_0.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

columna_edad = "Age (Day)"
columna_cemento = "Cement KG/M3 (component 1)"
columna_resistencia = "Compressive Strength (Kg/m2)"
columnas_requeridas = [columna_edad, columna_cemento, columna_resistencia]
columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]

if columnas_faltantes:
    raise KeyError(f"Faltan columnas requeridas en el CSV: {columnas_faltantes}")

# Convertir a números y omitir filas con datos faltantes.
for columna in columnas_requeridas:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

df = df.dropna(subset=columnas_requeridas)
if df.empty:
    raise ValueError("No hay registros válidos para generar el gráfico.")

# Gráfico 3D: edad, cantidad de cemento y resistencia del concreto.
fig = px.scatter_3d(
    df,
    x=columna_edad,
    y=columna_cemento,
    z=columna_resistencia,
    color=columna_resistencia,
    color_continuous_scale="Viridis",
    title="Relación 3D entre edad, cemento y resistencia del concreto",
    labels={
        columna_edad: "Edad (días)",
        columna_cemento: "Cemento (kg/m³)",
        columna_resistencia: "Resistencia a la compresión (Kg/m2)",
    },
    opacity=0.75,
    hover_data=[columna_edad, columna_cemento, columna_resistencia],
)

fig.show()