-- Corredores inscritos
CREATE TABLE IF NOT EXISTS inscritos (
    id                  SERIAL PRIMARY KEY,
    dorsal              INTEGER       NOT NULL,
    nombre              VARCHAR(50)   NOT NULL,
    apellidos           VARCHAR(100)  NOT NULL,
    sexo                CHAR(1)       NOT NULL CHECK (sexo IN ('M', 'F')),  -- M para masculino, F para femenino
    fecha_nacimiento    DATE          NOT NULL,
    telefono            VARCHAR(15),  NOT NULL,
    email               VARCHAR(100)  NOT NULL,
    tipo_documento      VARCHAR(20)   NOT NULL,  -- Podrías usar ENUM más adelante
    numero_documento    VARCHAR(30)   NOT NULL,
    direccion           VARCHAR(100)  NOT NULL,
    ccaa                VARCHAR(60)   NOT NULL,
    municipio           VARCHAR(50)   NOT NULL,
    tipo_carrera        VARCHAR(20)   NOT NULL CHECK (tipo_carrera IN ('trail', 'andarines')),  -- Tipos de carrera
    contacto_emergencia VARCHAR(100)  NOT NULL,
    telefono_emergencia VARCHAR(15)   NOT NULL,
    edicion             INTEGER       NOT NULL   -- Año de la carrera 2025, 2026, etc.
);

CREATE TABLE IF NOT EXISTS clasificacion (
    id                SERIAL      PRIMARY KEY,
    id_inscrito       INTEGER     NOT NULL REFERENCES inscritos(id) ON DELETE CASCADE,
    edicion           INTEGER     NOT NULL,        -- Año de la carrera
    tiempo_p0         TIMESTAMP,                   -- Tiempo en el inicio de la carrera
    tiempo_p1         TIMESTAMP,                   -- Tiempo en el primer punto de control     
    tiempo_final      TIMESTAMP,                   -- Tiempo final de la carrera
    finalizado        BOOLEAN     DEFAULT FALSE
);

-- Índice útil si consultas por edición
CREATE INDEX idx_clasificacion_edicion ON clasificacion(edicion);
