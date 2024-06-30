import pandas as pd

# Leer los archivos CSV
df_2024 = pd.read_csv('Datos_Limpios/2024_convertido.csv')
df_poblacion = pd.read_csv('Datos_Limpios/PolacionProvinciaClean.csv')

# Imprimir los nombres de las columnas para verificar
print("Columnas en df_2024:")
print(df_2024.columns)

print("\nColumnas en df_poblacion:")
print(df_poblacion.columns)
