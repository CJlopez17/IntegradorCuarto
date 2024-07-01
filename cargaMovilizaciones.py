import pandas as pd
import pymysql

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2024_convertido.csv')

# Eliminar duplicados en la columna 'movilizacion'
df_unique = df.drop_duplicates(subset=['movilizacion'])

# Eliminar filas con valores NaN en la columna 'movilizacion'
df_unique = df_unique.dropna(subset=['movilizacion'])

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Obtener el valor máximo actual de id_movilizacion
def obtener_max_id_movilizacion(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT IFNULL(MAX(id_movilizacion), 0) FROM Movilizaciones")
    max_id_movilizacion = cursor.fetchone()[0]
    return max_id_movilizacion

# Función para insertar datos en la tabla Movilizaciones
def insertar_datos_movilizaciones(df, conexion):
    cursor = conexion.cursor()
    max_id_movilizacion = obtener_max_id_movilizacion(conexion)
    
    for index, row in df.iterrows():
        # Incrementar el código de movilización
        max_id_movilizacion += 1
        
        # Verificar si la movilización ya existe
        cursor.execute("SELECT COUNT(*) FROM Movilizaciones WHERE movilizacion = %s", (row['movilizacion'],))
        if cursor.fetchone()[0] == 0:
            sql = """
            INSERT INTO Movilizaciones (id_movilizacion, movilizacion)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (max_id_movilizacion, row['movilizacion']))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_movilizaciones(df_unique, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Movilizaciones.")
