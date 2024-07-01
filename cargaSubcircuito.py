import pandas as pd
import pymysql

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2024_convertido.csv')

# Reemplazar NaN en las columnas
df['codigo_subcircuito'] = df['codigo_subcircuito'].fillna('-')
df['nombre_subcircuito'] = df['nombre_subcircuito'].fillna('-')
df['codigo_distrito'] = df['codigo_distrito'].fillna('-')

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

# Función para insertar datos en la tabla Subcircuitos
def insertar_datos_subcircuitos(df, conexion):
    cursor = conexion.cursor()
    
    for index, row in df.iterrows():
        # Verificar si el subcircuito ya existe
        cursor.execute("SELECT COUNT(*) FROM Subcircuitos WHERE codigo_subcircuito = %s", (row['codigo_subcircuito'],))
        if cursor.fetchone()[0] == 0:
            # Verificar si el código de distrito existe
            if verificar_codigo_distrito(row['codigo_distrito'], conexion):
                # Insertar los datos en la tabla Subcircuitos
                sql = """
                INSERT INTO Subcircuitos (codigo_subcircuito, subcircuito, codigo_distrito)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (
                    row['codigo_subcircuito'],
                    row['nombre_subcircuito'],
                    row['codigo_distrito']
                ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_subcircuitos(df, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Subcircuitos.")
