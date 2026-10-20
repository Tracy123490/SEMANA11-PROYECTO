from pathlib import Path
import pandas as pd
import plotly.express as px

# Cargar el dataset y eliminar registros completamente duplicados.
df = pd.read_csv("Pervious_Concrete_0.csv")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# El dataset registra la edad de prueba, no fechas de calendario.
edad = "Age (Day)"
cemento = "Cement KG/M3 (component 1)"
resistencia = "Compressive Strength (Kg/m2)"
columnas_requeridas = [edad, cemento, resistencia]
columnas_faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]
if columnas_faltantes:
    raise KeyError(f"Faltan columnas requeridas en el CSV: {columnas_faltantes}")

# Convertir edad, cemento y resistencia a números y quitar filas incompletas.
for columna in columnas_requeridas:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

df = df.dropna(subset=columnas_requeridas)
if df.empty:
    raise ValueError("No hay registros válidos para generar el gráfico 3D.")

# Cada punto representa una muestra del concreto.
fig = px.scatter_3d(
    df,
    x=edad,
    y=cemento,
    z=resistencia,
    color=resistencia,
    color_continuous_scale="Viridis",
    opacity=0.8,
    hover_data={
        edad: True,
        cemento: ":.2f",
        resistencia: ":.2f",
    },
    title="SERIE TEMPORAL:Relación 3D entre edad, cemento y resistencia del concreto",
    labels={
        edad: "Edad del concreto (días)",
        cemento: "Cemento (kg/m³)",
        resistencia: "Resistencia a la compresión (kg/m²)",
    },
)
fig.update_layout(
    scene={
        "xaxis_title": "Edad del concreto (días)",
        "yaxis_title": "Cemento (kg/m³)",
        "zaxis_title": "Resistencia a la compresión (kg/m²)",
    }
)
fig.show()