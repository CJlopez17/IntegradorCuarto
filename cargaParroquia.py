import pandas as pd
import pymysql

# Leer los archivos CSV
df_parroquias = pd.read_csv('Datos_Limpios/2024_convertido.csv')
df_poblacion = pd.read_csv('Datos_Limpios/PolacionParroquiaClean.csv')

# Reemplazar NaN en las columnas
df_parroquias['codigo_parroquia'] = df_parroquias['codigo_parroquia'].fillna('-')
df_parroquias['nombre_parroquia'] = df_parroquias['nombre_parroquia'].fillna('-')
df_parroquias['codigo_distrito'] = df_parroquias['codigo_distrito'].fillna('-')

# Unir los DataFrames en la columna 'nombre_parroquia'
df_combined = pd.merge(df_parroquias, df_poblacion, on='nombre_parroquia')

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Función para verificar si el código de distrito existe
def verificar_codigo_distrito(codigo_distrito, conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM Distritos WHERE codigo_distrito = %s", (codigo_distrito,))
    return cursor.fetchone()[0] > 0

# Función para insertar datos en la tabla Parroquias
def insertar_datos_parroquias(df, conexion):
    cursor = conexion.cursor()
    
    for index, row in df.iterrows():
        # Verificar si la parroquia ya existe
        cursor.execute("SELECT COUNT(*) FROM Parroquias WHERE codigo_parroquia = %s", (row['codigo_parroquia'],))
        if cursor.fetchone()[0] == 0:
            # Verificar si el código de distrito existe
            if verificar_codigo_distrito(row['codigo_distrito'], conexion):
                # Insertar los datos en la tabla Parroquias
                sql = """
                INSERT INTO Parroquias (codigo_parroquia, parroquia, codigo_distrito, nro_pobladores, superficie_parroquia, densidad_poblacional)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    row['codigo_parroquia'],
                    row['nombre_parroquia'],
                    row['codigo_distrito'],
                    row['nro_pobladores'],
                    row['superficie_parroquia'],
                    row['densidad_poblacional']
                ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_parroquias(df_combined, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Parroquias.")
