import pandas as pd
import pymysql

# Leer los archivos CSV con el delimitador correcto
df_2024 = pd.read_csv('Datos_Limpios/2024_convertido.csv', delimiter=',')
df_poblacion = pd.read_csv('Datos_Limpios/PolacionProvinciaClean.csv', delimiter=',')

# Renombrar columnas para que coincidan
# df_poblacion.columns = ['nombre_provincia', 'Poblacion', 'Superficie_de_provincia', 'Densidad_Poblacional']

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
        # Convertir valores a float
        nro_poblacion = int(row['Poblacion'])
        superficie_provincia = float(row['Superficie_de_provincia'])
        densidad_poblacional = float(row['Densidad_Poblacional'])
        
        # Verificar si la provincia ya existe
        cursor.execute("SELECT COUNT(*) FROM Provincias WHERE codigo_provincia = %s", (row['codigo_provincia'],))
        if cursor.fetchone()[0] == 0:
            sql = """
            INSERT INTO Provincias (codigo_provincia, provincia, nro_pobladores, superficie_provincia, densidad_poblacional)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (row['codigo_provincia'], row['nombre_provincia'], nro_poblacion, superficie_provincia, densidad_poblacional))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_provincias(df_combined, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Provincias.")
