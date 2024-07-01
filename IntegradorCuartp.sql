-- Drop y Create para la base de datos
DROP DATABASE IntegradorCuarto;
CREATE DATABASE IntegradorCuarto;
USE IntegradorCuarto;

-- Creacion de la tabla Detenidos
CREATE TABLE Detenidos (
    id_detenido INT PRIMARY KEY,
    sexo VARCHAR(10) NOT NULL,
    edad INT NOT NULL,
    nacionalidad VARCHAR(50),
    autoidentificacion_etnica VARCHAR(50),
    estado_civil VARCHAR(20),
    estatus_migratorio VARCHAR(20),
    nivel_instruccion VARCHAR(50),
    condicion_fisica VARCHAR(200),
    genero VARCHAR(15),
    tipo VARCHAR(20),
    nro_detenciones INT NOT NULL
);

-- Creccion de la tabla detenciones
CREATE TABLE Detenciones (
    id_detencion INT AUTO_INCREMENT PRIMARY KEY,
    id_detenido VARCHAR(10) NOT NULL,
    fecha_detencion DATE NOT NULL,
    presunta_infraccion VARCHAR(250) NOT NULL,
    presunta_subinfraccion VARCHAR(250),
    presunta_flagrancia VARCHAR(5),
    presunta_modalidad VARCHAR(250),
    hora_detencion TIME NOT NULL,
    codigo_iccs FLOAT,
    id_ubicacion VARCHAR(10) NOT NULL,
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion)
    FOREIGN KEY (id_detenido) REFERENCES Detenidos(id_detenido)
);

-- Creacion de la tabla Mobilizaciones
CREATE TABLE Movilizaciones (
    id_movilizacion VARCHAR(10) PRIMARY KEY,
    movilizacion VARCHAR(50) NOT NULL
);

-- Creacion de la tabla Armas
CREATE TABLE Armas (
    codigo_arma VARCHAR(10) PRIMARY KEY,
    tipo_arma VARCHAR(50) NOT NULL,
    arma VARCHAR(50) NOT NULL
);

-- Creacion de la tabla Detenciones_Movilizaciones
CREATE TABLE Detenciones_Movilizaciones (
    id_detencion INT,
    id_movilizacion VARCHAR(10),
    PRIMARY KEY (id_detencion, id_movilizacion),
    FOREIGN KEY (id_detencion) REFERENCES Detenciones(id_detencion),
    FOREIGN KEY (id_movilizacion) REFERENCES Movilizaciones(id_movilizacion)
);

-- Creaccion de la tabla Movilizaciones_Armas
CREATE TABLE Movilizaciones_Armas (
    id_movilizacion VARCHAR(10),
    codigo_arma VARCHAR(10),
    PRIMARY KEY (id_movilizacion, codigo_arma),
    FOREIGN KEY (id_movilizacion) REFERENCES Movilizaciones(id_movilizacion),
    FOREIGN KEY (codigo_arma) REFERENCES Armas(codigo_arma)
);

-- Creacion de la tabla Ubicaciones
CREATE TABLE Ubicaciones (
    id_ubicacion INT PRIMARY KEY,
    lugar VARCHAR(100) NOT NULL,
    tipo_lugar VARCHAR(100) NOT NULL
);

-- Creacion de la tabla Provincia
CREATE TABLE Provincias (
    codigo_provincia VARCHAR(10) PRIMARY KEY,
    provincia VARCHAR(50) NOT NULL,
    nro_pobladores INT,
    superficie_provincia FLOAT,
    densidad_poblacional FLOAT
);

-- Creaccion de la tabla Cantones
CREATE TABLE Cantones (
    codigo_canton VARCHAR(10) PRIMARY KEY,
    canton VARCHAR(50) NOT NULL,
    codigo_provincia VARCHAR(10) NOT NULL,
    superficie_canton FLOAT,
    densidad_poblacional FLOAT,
    FOREIGN KEY (codigo_provincia) REFERENCES Provincias(codigo_provincia)
);

-- Creacion de la tabla Distritos
CREATE TABLE Distritos (
    codigo_distrito VARCHAR(10) PRIMARY KEY,
    distrito VARCHAR(50) NOT NULL,
    codigo_canton INT NOT NULL,
    FOREIGN KEY (codigo_canton) REFERENCES Cantones(codigo_canton)
);

-- Creacion de la tabla Parroquias
CREATE TABLE Parroquias (
    codigo_parroquia VARCHAR(10) PRIMARY KEY,
    parroquia VARCHAR(50) NOT NULL,
    nro_pobladores int NOT NULL,
    codigo_distrito VARCHAR(10) NOT NULL,
    superficie_parroquia FLOAT,
    densidad_poblacional FLOAT,
    FOREIGN KEY (codigo_distrito) REFERENCES Distritos(codigo_distrito)
);

-- Creacion de la tabla Subcircuitos
CREATE TABLE Subcircuitos (
    codigo_subcircuito VARCHAR(15) PRIMARY KEY,
    subcircuito VARCHAR(50) NOT NULL,
    codigo_distrito VARCHAR(10) NOT NULL,
    FOREIGN KEY (codigo_distrito) REFERENCES Distritos(codigo_distrito)
);

-- Creacion de la tabla Zonas
CREATE TABLE Zonas (
    codigo_zona VARCHAR(10) PRIMARY KEY,
    zona VARCHAR(50) NOT NULL,
    subzona VARCHAR(50) NOT NULL,
    codigo_subcircuito VARCHAR(10) NOT NULL,
    FOREIGN KEY (codigo_subcircuito) REFERENCES Subcircuitos(codigo_subcircuito)
);

-- Creacion de la tabla Ubicaciones_Provincias
CREATE TABLE Ubicaciones_Provincias (
    id_ubicacion VARCHAR(10),
    codigo_provincia VARCHAR(10),
    PRIMARY KEY (id_ubicacion, codigo_provincia),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),
    FOREIGN KEY (codigo_provincia) REFERENCES Provincias(codigo_provincia)
);

-- Creacion de la tabla Ubicaciones_Cantones
CREATE TABLE Ubicaciones_Cantones (
    id_ubicacion VARCHAR(10),
    codigo_canton VARCHAR(10),
    PRIMARY KEY (id_ubicacion, codigo_canton),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),
    FOREIGN KEY (codigo_canton) REFERENCES Cantones(codigo_canton)
);

-- Creacion de la tabla Ubicaciones_Distritos
CREATE TABLE Ubicaciones_Distritos (
    id_ubicacion VARCHAR(10),
    codigo_distrito VARCHAR(10),
    PRIMARY KEY (id_ubicacion, codigo_distrito),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),
    FOREIGN KEY (codigo_distrito) REFERENCES Distritos(codigo_distrito)
);

-- Creacion de la tabla Ubicaciones_Parroquias
CREATE TABLE Ubicaciones_Parroquias (
    id_ubicacion VARCHAR(10),
    codigo_parroquia VARCHAR(10),
    PRIMARY KEY (id_ubicacion, codigo_parroquia),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),
    FOREIGN KEY (codigo_parroquia) REFERENCES Parroquias(codigo_parroquia)
);

-- Creacion de la tabla Ubicaciones_Subcircuitos
CREATE TABLE Ubicaciones_Subcircuitos (
    id_ubicacion VARCHAR(10),
    codigo_subcircuito VARCHAR(10),
    PRIMARY KEY (id_ubicacion, codigo_subcircuito),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),
    FOREIGN KEY (codigo_subcircuito) REFERENCES Subcircuitos(codigo_subcircuito)
);

-- Creacion de la tabla Ubicaciones_Zonas
CREATE TABLE Ubicaciones_Zonas (
    id_ubicacion VARCHAR(10),
    codigo_zona VARCHAR(10),
    PRIMARY KEY (id_ubicacion, codigo_zona),
    FOREIGN KEY (id_ubicacion) REFERENCES Ubicaciones(id_ubicacion),
    FOREIGN KEY (codigo_zona) REFERENCES Zonas(codigo_zona)
);

-- Creacion de Usuario todos los pivilegios
CREATE USER 'usuario1'@'localhost' IDENTIFIED BY 'mysql#DB02';
GRANT INSERT, UPDATE, DELETE, CREATE, DROP ON IntegradorCuarto.* TO 'usuario1'@'localhost';
FLUSH PRIVILEGES;

