import pandas as pd
from conexion import obtener_conexion
conexion = obtener_conexion()
query = "SELECT * FROM vino"
df = pd.read_sql(query, conexion)
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)
print("ESTAS SON LAS PRIMERAS 5 FILAS QUE SE MUESTRAN DE LA BASE DE DATOS")
print(df.head())
