import pandas as pd
import pymysql
from datetime import datetime

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2024_convertido.csv')

# Imprimir los nombres de las columnas para verificar
#print("Columnas en el DataFrame:")
# print(df.columns)

# Reemplazar NaN en las columnas
df['presunta_infraccion'] = df['presunta_infraccion'].fillna('-')
df['presunta_subinfraccion'] = df['presunta_subinfraccion'].fillna('-')
df['presunta_flagrancia'] = df['presunta_flagrancia'].fillna('-')
df['presunta_modalidad'] = df['presunta_modalidad'].fillna('-')
df['codigo_iccs'] = df['codigo_iccs'].fillna(0)
df['id_detenido'] = df['id_detenido'].fillna('-')

# Convertir fechas y horas a formatos correctos
df['fecha_detencion'] = pd.to_datetime(df['fecha_detencion'], errors='coerce').dt.strftime('%Y-%m-%d')

# Asegurarse de que la hora tenga el formato correcto
df['hora_detencion'] = df['hora_detencion'].apply(lambda x: x if len(x) == 8 else x + ':00')

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Función para obtener el id_ubicacion basado en el lugar
def obtener_id_ubicacion(lugar, conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT id_ubicacion FROM Ubicaciones WHERE lugar = %s", (lugar,))
    result = cursor.fetchone()
    return result[0] if result else None

# Función para verificar si el id_detenido existe
def verificar_id_detenido(id_detenido, conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM Detenidos WHERE id_detenido = %s", (id_detenido,))
    return cursor.fetchone()[0] > 0

# Función para insertar datos en la tabla Detenciones
def insertar_datos_detenciones(df, conexion):
    cursor = conexion.cursor()
    
    for index, row in df.iterrows():
        id_ubicacion = obtener_id_ubicacion(row['lugar'], conexion)
        if id_ubicacion and verificar_id_detenido(row['id_detenido'], conexion):
            # Insertar los datos en la tabla Detenciones
            sql = """
            INSERT INTO Detenciones (id_detenido, fecha_detencion, presunta_infraccion, presunta_subinfraccion, presunta_flagrancia, presunta_modalidad, hora_detencion, codigo_iccs, id_ubicacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                row['id_detenido'],
                row['fecha_detencion'],
                row['presunta_infraccion'],
                row['presunta_subinfraccion'],
                row['presunta_flagrancia'],
                row['presunta_modalidad'],
                row['hora_detencion'],
                row['codigo_iccs'],
                id_ubicacion
            ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_detenciones(df, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Detenciones.")
