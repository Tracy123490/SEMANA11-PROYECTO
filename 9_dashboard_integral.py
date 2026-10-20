import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

CARPETA = Path(__file__).resolve().parent
DATASET = CARPETA / "Pervious_Concrete_0.csv"

# Permite iniciar el dashboard ejecutando este archivo con Python.
if os.environ.get("CONCRETE_DASHBOARD_STREAMLIT") != "1":
    entorno = os.environ.copy()
    entorno["CONCRETE_DASHBOARD_STREAMLIT"] = "1"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(Path(__file__).resolve()),
            "--server.headless",
            "true",
        ],
        cwd=CARPETA,
        env=entorno,
        check=True,
    )
    raise SystemExit

import streamlit as st

st.set_page_config(page_title="Resistencia del concreto", page_icon="🏗️", layout="wide")
st.title("Dashboard de resistencia del concreto")
st.caption("Indicadores, análisis de mezclas y comportamiento de la resistencia")

archivo = st.sidebar.file_uploader("Cargar otro archivo CSV", type="csv")
if archivo is not None:
    df = pd.read_csv(archivo)
elif DATASET.is_file():
    df = pd.read_csv(DATASET)
else:
    st.error(f"No se encontró el dataset: {DATASET.name}")
    st.stop()

df.columns = df.columns.str.strip()
for columna in df.columns:
    valores = pd.to_numeric(df[columna], errors="coerce")
    if valores.notna().any():
        df[columna] = valores


def buscar_columna(fragmento):
    return next((col for col in df.columns if fragmento in col.lower()), None)


edad_col = buscar_columna("age")
resistencia_col = buscar_columna("compressive strength") or buscar_columna("strength")

if edad_col is None or resistencia_col is None:
    st.error("El CSV debe incluir columnas de edad (Age) y resistencia (Compressive Strength).")
    st.write("Columnas encontradas:", list(df.columns))
    st.stop()

df[edad_col] = pd.to_numeric(df[edad_col], errors="coerce")
df[resistencia_col] = pd.to_numeric(df[resistencia_col], errors="coerce")
df = df.dropna(subset=[edad_col, resistencia_col])
if df.empty:
    st.error("El dataset no contiene edades y resistencias numéricas válidas.")
    st.stop()

unidad = resistencia_col.rsplit("(", 1)[-1].rstrip(")") if "(" in resistencia_col else ""
with st.sidebar:
    st.header("Filtros")
    edad_min = int(df[edad_col].min())
    edad_max = int(df[edad_col].max())
    rango = (
        st.slider("Edad del concreto (días)", edad_min, edad_max, (edad_min, edad_max))
        if edad_min < edad_max
        else (edad_min, edad_max)
    )

    componentes = {
        "Cemento": "cement",
        "Agua": "water",
        "Agregado grueso": "coarse aggregate",
        "Agregado fino": "fine aggregate",
        "Superplastificante": "superplasticizer",
        "Escoria de alto horno": "slag",
        "Ceniza volante": "fly ash",
        "Vacíos": "void",
    }
    columnas_mezcla = {
        nombre: columna
        for nombre, fragmento in componentes.items()
        if (columna := buscar_columna(fragmento)) is not None
    }

datos = df[df[edad_col].between(*rango)].copy()
if datos.empty:
    st.warning("No hay muestras para el rango de edad seleccionado.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Muestras", f"{len(datos):,}")
k2.metric("Resistencia promedio", f"{datos[resistencia_col].mean():.2f} {unidad}")
k3.metric("Resistencia máxima", f"{datos[resistencia_col].max():.2f} {unidad}")
k4.metric("Edad promedio", f"{datos[edad_col].mean():.1f} días")

izquierda, derecha = st.columns(2)
with izquierda:
    st.subheader("Resistencia promedio según edad")
    st.line_chart(datos.groupby(edad_col)[resistencia_col].mean())

with derecha:
    st.subheader("Distribución de la resistencia")
    histograma = pd.cut(datos[resistencia_col], bins=12).value_counts().sort_index()
    histograma.index = histograma.index.astype(str)
    st.bar_chart(histograma)

if columnas_mezcla:
    st.subheader("Influencia de los componentes de la mezcla")
    nombre = st.selectbox("Selecciona un componente", list(columnas_mezcla))
    st.scatter_chart(
        datos,
        x=columnas_mezcla[nombre],
        y=resistencia_col,
        x_label=f"{nombre} (kg/m³)",
        y_label=f"Resistencia ({unidad})" if unidad else "Resistencia",
    )

    st.subheader("Composición promedio de las mezclas")
    promedios = datos[list(columnas_mezcla.values())].mean()
    promedios.index = list(columnas_mezcla.keys())
    st.bar_chart(promedios)

st.subheader("Correlación entre variables")
numericas = datos.select_dtypes(include="number")
if len(numericas.columns) > 1:
    st.dataframe(numericas.corr().round(2), width="stretch")

st.subheader("Datos de las muestras")
st.dataframe(datos, width="stretch")
st.download_button(
    "Descargar datos filtrados",
    datos.to_csv(index=False).encode("utf-8"),
    file_name="muestras_concreto_filtradas.csv",
    mime="text/csv",
)
