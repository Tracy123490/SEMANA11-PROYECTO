from pathlib import Path
import pandas as pd
import plotly.express as px

# Cargar el dataset 
df = pd.read_csv("Pervious_Concrete_0.csv")
df.columns = df.columns.str.strip()

columna_resistencia = "Compressive Strength (Kg/m2)"
columna_edad = "Age (Day)"
columnas_requeridas = [columna_resistencia, columna_edad]
columnas_faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]

if columnas_faltantes:
    raise KeyError(f"Faltan columnas requeridas en el CSV: {columnas_faltantes}")

# Histograma de la distribución de la resistencia del concreto.
fig_histograma = px.histogram(
    df,
    x=columna_resistencia,
    nbins=30,
    title="Distribución de la resistencia del concreto",
    labels={columna_resistencia: "Resistencia a la compresión (Kg/m2)", "count": "Cantidad"},
)
fig_histograma.show()

# Relación entre la edad del concreto y su resistencia a la compresión.
fig_dispersion = px.scatter(
    df,
    x = columna_edad,
    y = columna_resistencia,
    title="Resistencia del concreto según su edad",
    labels={
        columna_edad: "Edad (días)",
        columna_resistencia: "Resistencia a la compresión (Kg/m2)",
    },
)
fig_dispersion.show()