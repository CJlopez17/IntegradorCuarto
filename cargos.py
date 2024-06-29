import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('Datos_Crudos/PoblacionProvincia.csv', delimiter=';')

# Contador de cambios
cambios_realizados = 0

# Función para eliminar los puntos de las cifras
def eliminar_puntos(valor):
    global cambios_realizados
    if pd.isnull(valor):
        return valor
    if isinstance(valor, str):
        nuevo_valor = valor.replace('.', '')
        if nuevo_valor != valor:
            cambios_realizados += 1
        return nuevo_valor
    return valor

# Aplicar la función a todas las columnas del DataFrame
for columna in df.columns:
    df[columna] = df[columna].apply(eliminar_puntos)

# Guardar el DataFrame limpio en un nuevo archivo CSV
df.to_csv('Datos_Limpios/PolacionProvinciaClean.csv', index=False, sep=';')

print("Datos limpiados y guardados en 'nombre_del_archivo_limpio.csv'.")
print(f"Número de datos modificados: {cambios_realizados}")
