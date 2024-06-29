import pandas as pd
from datetime import datetime

# Función para convertir las fechas
def convertir_fecha(fecha):
    global cambios_realizados
    formatos_fecha = ['%m/%d/%y', '%d/%m/%y', '%Y-%m-%d']
    
    # Verificar si la fecha es un valor nulo o un número
    if pd.isnull(fecha) or isinstance(fecha, (int, float)):
        return fecha

    # Convertir la fecha si es una cadena
    for formato in formatos_fecha:
        try:
            # Detectar si el año es de dos dígitos y agregar '20' al principio
            if len(fecha.split('/')[-1]) == 2:
                nueva_fecha = datetime.strptime(fecha, formato).strftime('%Y/%m/%d')
            else:
                nueva_fecha = datetime.strptime(fecha, formato).strftime('%Y/%m/%d')
            
            # Incrementar el contador si la fecha fue cambiada
            if nueva_fecha != fecha:
                cambios_realizados += 1
            return nueva_fecha
        except ValueError:
            continue
    # Manejar errores de conversión de fecha
    print(f"Error al convertir la fecha: {fecha}")
    return fecha

# Leer el archivo CSV especificando el delimitador correcto
try:
    df = pd.read_csv('NombreDelArchivo.csv', delimiter=';')
except pd.errors.ParserError:
    print("Error al leer el archivo CSV. Verifica la línea problemática.")
    raise

# Contar las ocurrencias de "SIN DATO", "SE DESCONOCE" y "NO APLICA" antes de reemplazar
sin_dato_count = (df == "SIN DATO").sum().sum()
se_desconoce_count = (df == "SE DESCONOCE").sum().sum()
no_aplica_count = (df == "NO APLICA").sum().sum()

# Reemplazar "SIN DATO", "SE DESCONOCE" y "NO APLICA" por NaN
df.replace(["SIN DATO", "SE DESCONOCE", "NO APLICA"], pd.NA, inplace=True)

# Aplicar la función de conversión a la columna de fechas
# Reemplaza 'fecha_detencion_aprehension' con el nombre real de la columna que contiene las fechas
cambios_realizados = 0
# df['fecha_detencion_aprehension'] = df['fecha_detencion_aprehension'].apply(convertir_fecha)
df['Fecha de Detención'] = df['Fecha de Detención'].apply(convertir_fecha)

# Guardar el resultado en un nuevo archivo CSV
df.to_csv('año_cleaned_converted.csv', index=False)

# Mostrar el número de datos modificados
print(f"Fechas convertidas y archivo guardado como 'año_cleaned_converted.csv'. Total de cambios realizados: {cambios_realizados}")
print(f"Número de datos 'SIN DATO' modificados: {sin_dato_count}")
print(f"Número de datos 'SE DESCONOCE' modificados: {se_desconoce_count}")
print(f"Número de datos 'NO APLICA' modificados: {no_aplica_count}")

# Inspeccionar las primeras filas para verificar el contenido
print(df.head())
