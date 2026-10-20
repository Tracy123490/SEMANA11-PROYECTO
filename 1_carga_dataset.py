#importar librerias
from pathlib import Path
import pandas as pd
#cargar el dataset
df = pd.read_csv("Pervious_Concrete_0.csv")

#visualizar la informacion
print(df.head()) #muestra las primeras 5 filas
df.info()       #muestra columnas, tipos de datos y valores no nulos
print(df.shape) #muestra (cantidad de filas, candtidad de columnas)