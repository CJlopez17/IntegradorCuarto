import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2024_convertido.csv')

# Reemplazar "NINGUNA" por NaN en las columnas 'tipo_arma' y 'arma'
df['tipo_arma'].replace('NINGUNA', pd.NA, inplace=True)
df['arma'].replace('NINGUNA', pd.NA, inplace=True)

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv('2024_convertido.csv', index=False)

print("Reemplazo completado y archivo guardado como 'archivo_modificado.csv'.")
