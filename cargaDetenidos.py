import pandas as pd
import pymysql

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2017_convertido.csv')

# Reemplazar NaN en la columna 'Edad' por 0
df['Edad'].fillna(0, inplace=True)

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Obtener el valor máximo actual de id_detenido
def obtener_max_id_detenido(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT IFNULL(MAX(id_detenido), 0) FROM Detenidos")
    max_id_detenido = cursor.fetchone()[0]
    return max_id_detenido

# Función para insertar datos en la tabla Detenidos
def insertar_datos_detenidos(df, conexion):
    cursor = conexion.cursor()
    max_id_detenido = obtener_max_id_detenido(conexion)
    
    for index, row in df.iterrows():
        # Incrementar el código de detenido
        max_id_detenido += 1
        
        # Preparar los datos para inserción, asignando NULL a las columnas faltantes
        sexo = row['Sexo'] if 'Sexo' in df.columns and pd.notna(row['Sexo']) else None
        edad = int(row['Edad']) if 'Edad' in df.columns and pd.notna(row['Edad']) else 0
        nacionalidad = row['Nacionalidad'] if 'Nacionalidad' in df.columns and pd.notna(row['Nacionalidad']) else None
        autoidentificacion_etnica = None  # No presente en el CSV
        estado_civil = None  # No presente en el CSV
        estatus_migratorio = None  # No presente en el CSV
        nivel_instruccion = None  # No presente en el CSV
        condicion_fisica = None  # No presente en el CSV
        genero = None  # No presente en el CSV
        tipo = None  # No presente en el CSV
        nro_detenciones = int(row['nro_detenciones']) if 'nro_detenciones' in df.columns and pd.notna(row['nro_detenciones']) else 0
        
        # Insertar los datos en la tabla Detenidos
        sql = """
        INSERT INTO Detenidos (id_detenido, sexo, edad, nacionalidad, autoidentificacion_etnica, estado_civil, 
                               estatus_migratorio, nivel_instruccion, condicion_fisica, genero, tipo, nro_detenciones)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            max_id_detenido,
            sexo,
            edad,
            nacionalidad,
            autoidentificacion_etnica,
            estado_civil,
            estatus_migratorio,
            nivel_instruccion,
            condicion_fisica,
            genero,
            tipo,
            nro_detenciones
        ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_detenidos(df, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Detenidos.")
