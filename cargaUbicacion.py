import pandas as pd
import pymysql

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2022_convertido.csv')

# Añadir la columna 'tipo_lugar' con un valor por defecto
df['tipo_lugar'] = '-'

# Reemplazar NaN en la columna 'lugar' por '-'
df['lugar'].fillna('-', inplace=True)

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Obtener el valor máximo actual de id_ubicacion
def obtener_max_id_ubicacion(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT IFNULL(MAX(id_ubicacion), 0) FROM Ubicaciones")
    max_id_ubicacion = cursor.fetchone()[0]
    return max_id_ubicacion

# Función para insertar datos en la tabla Ubicaciones
def insertar_datos_ubicaciones(df, conexion):
    cursor = conexion.cursor()
    max_id_ubicacion = obtener_max_id_ubicacion(conexion)
    
    for index, row in df.iterrows():
        # Verificar si la ubicación ya existe
        cursor.execute("SELECT COUNT(*) FROM Ubicaciones WHERE lugar = %s AND tipo_lugar = %s", (row['lugar'], row['tipo_lugar']))
        if cursor.fetchone()[0] == 0:
            # Incrementar el código de ubicación
            max_id_ubicacion += 1
            
            # Insertar los datos en la tabla Ubicaciones
            sql = """
            INSERT INTO Ubicaciones (id_ubicacion, lugar, tipo_lugar)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                max_id_ubicacion,
                row['lugar'],
                row['tipo_lugar']
            ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_ubicaciones(df, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Ubicaciones.")
