import pandas as pd
import pymysql

# Leer los archivos CSV
df_cantones = pd.read_csv('Datos_Limpios/2024_convertido.csv')
df_poblacion = pd.read_csv('Datos_Limpios/PolacionCantonClean.csv')

# Reemplazar NaN en las columnas
df_cantones['codigo_canton'] = df_cantones['codigo_canton'].fillna('-')
df_cantones['canton'] = df_cantones['canton'].fillna('-')
df_cantones['codigo_provincia'] = df_cantones['codigo_provincia'].fillna('-')

# Unir los DataFrames en la columna 'nombre_canton'
df_combined = pd.merge(df_cantones, df_poblacion, on='nombre_canton')

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='tu_usuario',
    password='tu_contraseña',
    db='IntegradorCuarto'
)

# Función para verificar si el código de provincia existe
def verificar_codigo_provincia(codigo_provincia, conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM Provincias WHERE codigo_provincia = %s", (codigo_provincia,))
    return cursor.fetchone()[0] > 0

# Función para insertar datos en la tabla Cantones
def insertar_datos_cantones(df, conexion):
    cursor = conexion.cursor()
    
    for index, row in df.iterrows():
        # Verificar si el cantón ya existe
        cursor.execute("SELECT COUNT(*) FROM Cantones WHERE codigo_canton = %s", (row['codigo_canton'],))
        if cursor.fetchone()[0] == 0:
            # Verificar si el código de provincia existe
            if verificar_codigo_provincia(row['codigo_provincia'], conexion):
                # Insertar los datos en la tabla Cantones
                sql = """
                INSERT INTO Cantones (codigo_canton, canton, codigo_provincia, superficie_canton, densidad_poblacional)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    row['codigo_canton'],
                    row['canton'],
                    row['codigo_provincia'],
                    
                    row['superficie_canton'],
                    row['densidad_poblacional']
                ))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_cantones(df_combined, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Cantones.")
