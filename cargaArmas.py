import pandas as pd
import pymysql

# Leer el archivo CSV
df = pd.read_csv('Datos_Limpios/2024_convertido.csv')

# Eliminar duplicados en las columnas 'tipo_arma' y 'arma'
df_unique = df.drop_duplicates(subset=['tipo_arma', 'arma'])

# Eliminar filas con valores NaN en las columnas 'tipo_arma' y 'arma'
df_unique = df_unique.dropna(subset=['tipo_arma', 'arma'])

# Conectar a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='Camilo$02',
    db='IntegradorCuarto'
)

# Obtener el valor máximo actual de id_arma
def obtener_max_id_arma(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT IFNULL(MAX(id_arma), 0) FROM Armas")
    max_id_arma = cursor.fetchone()[0]
    return max_id_arma

# Función para insertar datos en la tabla Armas
def insertar_datos_armas(df, conexion):
    cursor = conexion.cursor()
    max_id_arma = obtener_max_id_arma(conexion)
    
    for index, row in df.iterrows():
        # Incrementar el código de arma
        max_id_arma += 1
        
        # Verificar si el arma ya existe
        cursor.execute("SELECT COUNT(*) FROM Armas WHERE tipo_arma = %s AND arma = %s", (row['tipo_arma'], row['arma']))
        if cursor.fetchone()[0] == 0:
            sql = """
            INSERT INTO Armas (id_arma, tipo_arma, arma)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (max_id_arma, row['tipo_arma'], row['arma']))
    conexion.commit()

# Llamar a la función para insertar datos
insertar_datos_armas(df_unique, conexion)

# Cerrar la conexión
conexion.close()

print("Datos insertados correctamente en la tabla Armas.")
