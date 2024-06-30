import pandas as pd
import pymysql

# Leer los archivos CSV
df_2024 = pd.read_csv('Datos_Limpios/2024_convertido.csv')
df_poblacion = pd.read_csv('Datos_Limpios/PolacionProvinciaClean.csv', delimiter=';')

# Renombrar columnas para que coincidan
# df_2024.rename(columns={'nombre_provincia': 'provincia'}, inplace=True)
# df_poblacion.rename(columns={'nombre_provincia': 'provincia', 'Población': 'poblacion', 'Superficie de la provincia (km2)': 'superficie_provincia', 'Densidad Poblacional': 'densidad_poblacional'}, inplace=True)

# Combinar los DataFrames
df_combined = pd.merge(df_2024, df_poblacion, on='nombre_provincia')

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Función para insertar datos en la tabla Provincias
def insertar_datos_provincias(df, conexion):
    cursor = conexion.cursor()
    for index, row in df.iterrows():
        # Verificar si la provincia ya existe
        cursor.execute("SELECT COUNT(*) FROM Provincias WHERE codigo_provincia = %s", (row['codigo_provincia'],))
        if cursor.fetchone()[0] == 0:
            sql = """
            INSERT INTO Provincias (codigo_provincia, provincia, superficie_provincia, densidad_poblacional)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (row['codigo_provincia'], row['provincia'], row['superficie_provincia'], row['densidad_poblacional']))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_provincias(df_combined, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Provincias.")
