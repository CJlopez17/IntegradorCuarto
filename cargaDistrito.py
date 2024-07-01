import pandas as pd
import pymysql

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2024_convertido.csv')

# Reemplazar NaN en las columnas
df['codigo_distrito'] = df['codigo_distrito'].fillna('-')
df['nombre_distrito'] = df['nombre_distrito'].fillna('-')
df['codigo_canton'] = df['codigo_canton'].apply(lambda x: None if pd.isna(x) else int(x))

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Función para verificar si el código de cantón existe
def verificar_codigo_canton(codigo_canton, conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM Cantones WHERE codigo_canton = %s", (codigo_canton,))
    return cursor.fetchone()[0] > 0

# Función para insertar datos en la tabla Distritos
def insertar_datos_distritos(df, conexion):
    cursor = conexion.cursor()
    
    for index, row in df.iterrows():
        # Verificar si el distrito ya existe
        cursor.execute("SELECT COUNT(*) FROM Distritos WHERE codigo_distrito = %s", (row['codigo_distrito'],))
        if cursor.fetchone()[0] == 0:
            # Verificar si el código de cantón existe
            if verificar_codigo_canton(row['codigo_canton'], conexion):
                # Insertar los datos en la tabla Distritos
                sql = """
                INSERT INTO Distritos (codigo_distrito, distrito, codigo_canton)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (
                    row['codigo_distrito'],
                    row['nombre_distrito'],
                    row['codigo_canton']
                ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_distritos(df, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Distritos.")
