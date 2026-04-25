-- schema seguretat
CREATE TABLE seguretat.ROL(
    id_rol SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL,
    descripcio TEXT
);

CREATE TABLE seguretat.USUARI (
    id_usuari SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password BYTEA NOT NULL,    -- bytea per emmagatzemar hash de contrasenya (binari) per guardarlo directament sense conversions a text
    actiu BOOLEAN DEFAULT TRUE,
    data_creacio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_activitat TIMESTAMP
);

CREATE TABLE seguretat.USUARI_ROL (
    id_usuari INT REFERENCES seguretat.USUARI(id_usuari),
    id_rol INT REFERENCES seguretat.ROL(id_rol),
    PRIMARY KEY (id_usuari, id_rol)
);

CREATE TABLE seguretat.LOG_ACCESS (
    id_log SERIAL PRIMARY KEY,
    id_usuari INT REFERENCES seguretat.USUARI(id_usuari),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accio TEXT,
    taula_afectada TEXT
);

CREATE TABLE seguretat.LOG_DETAIL(
    id_detall SERIAL PRIMARY KEY,
    id_log INT UNIQUE REFERENCES seguretat.LOG_ACCESS(id_log),
    id_library INT REFERENCES seguretat.LOG_LIBRARY(id_library),
    id_registre INT,
    taula_afectada VARCHAR(100),
    dades TEXT
);

CREATE TABLE seguretat.LOG_LIBRARY(
    id_library SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL
);


-- estructura
CREATE TABLE estructura.PLANTA(
    id_planta SERIAL PRIMARY KEY,
    num_planta INT UNIQUE,
    descripcio TEXT
);

CREATE TABLE estructura.HABITACIO (
    id_habitacio SERIAL PRIMARY KEY,
    id_planta INT REFERENCES estructura.PLANTA(id_planta),
    num_habitacio INT,
    capacitat INT,
    estat VARCHAR(50),
    CONSTRAINT unique_num_hab_pl UNIQUE (id_planta, num_habitacio)
);

CREATE TABLE estructura.QUIROFAN(
    id_planta INT REFERENCES estructura.PLANTA(id_planta),
    num_quirofan INT,
    estat VARCHAR(50),
    PRIMARY KEY (id_planta, num_quirofan)
);

CREATE TABLE estructura.TIPUS(
    id_tipus SERIAL PRIMARY KEY,
    model VARCHAR(50),
    marca VARCHAR(50),
    tipus VARCHAR(50)
);

CREATE TABLE estructura.APARELL_MEDIC(
    id_aparell SERIAL PRIMARY KEY,
    num_serie VARCHAR(100) UNIQUE,
    data_manteniment DATE,
    id_tipus INT REFERENCES estructura.TIPUS(id_tipus)
);


-- schema dades_personal
CREATE TABLE dades_per.PERSONAL(
    id_personal SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    cognom1 VARCHAR(50),
    cognom2 VARCHAR(50),
    dni VARCHAR(9) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    email VARCHAR(100),
    direccio TEXT,
    data_naixement DATE,
    baixa DATE
);

-- herència de personal
CREATE TABLE dades_per.METGE(
    id_personal INT PRIMARY KEY REFERENCES dades_per.PERSONAL(id_personal),
    especialitat VARCHAR(100),
    curriculum TEXT,
    num_colegiat VARCHAR(50)
);

CREATE TABLE dades_per.INFERMER(
    id_personal INT PRIMARY KEY REFERENCES dades_per.PERSONAL(id_personal),
    experiencia INT,
    torn VARCHAR(50)
);

CREATE TABLE dades_per.VARI(
    id_personal INT PRIMARY KEY REFERENCES dades_per.PERSONAL(id_personal),
    tipus_feina VARCHAR(100),
    horari VARCHAR(100)
);

-- relacions
CREATE TABLE dades_per.INFERMER_METGE(
    id_infermer INT REFERENCES dades_per.INFERMER(id_personal),
    id_metge INT REFERENCES dades_per.METGE(id_personal),
    PRIMARY KEY (id_infermer, id_metge)
);

CREATE TABLE dades_per.INFERMER_PLANTA(
    id_infermer INT REFERENCES dades_per.INFERMER(id_personal),
    id_planta INT REFERENCES estructura.PLANTA(id_planta),
    PRIMARY KEY (id_infermer, id_planta)
);


-- pacient
CREATE TABLE pacient.PACIENT(
    id_pacient SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    cognoms VARCHAR(100),
    dni VARCHAR(9) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    email VARCHAR(100),
    data_naixement DATE,
    tarjeta_sanitaria VARCHAR(30) UNIQUE,
    id_habitacio INT REFERENCES estructura.HABITACIO(id_habitacio)
);

CREATE TABLE pacient.EXPEDIENT(
    id_exp SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.PACIENT(id_pacient),
    historial TEXT,
    data_actualitzacio DATE,
    observacions TEXT
);

CREATE TABLE pacient.VISITA(
    id_visita SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.PACIENT(id_pacient),
    id_metge INT REFERENCES dades_per.METGE(id_personal),
    data TIMESTAMP,
    diagnostic TEXT
);

CREATE TABLE pacient.PROVA(
    id_prova SERIAL PRIMARY KEY,
    id_visita INT REFERENCES pacient.VISITA(id_visita),
    tipus VARCHAR(50),
    resultat TEXT,
    estat VARCHAR(50),
    data DATE
);

CREATE TABLE pacient.OPERACIO(
    id_operacio SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.PACIENT(id_pacient),
    tipus_operacio VARCHAR(100),
    estat VARCHAR(50),
    data TIMESTAMP,
    descripcio TEXT,
    id_metge INT REFERENCES dades_per.METGE(id_personal),
    id_planta INT,
    num_quirofan INT,
    FOREIGN KEY (id_planta, num_quirofan) 
        REFERENCES estructura.QUIROFAN(id_planta, num_quirofan)
);

CREATE TABLE pacient.INGRES(
    id_ingres SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.PACIENT(id_pacient),
    data_ingres DATE,
    data_sortida_prevista DATE,
    data_sortida_real DATE
);


-- relacions operacio - ifermer
CREATE TABLE dades_per.INFERMER_OPERACIO(
    id_infermer INT REFERENCES dades_per.INFERMER(id_personal),
    id_operacio INT REFERENCES pacient.OPERACIO(id_operacio),
    rol VARCHAR(50),
    PRIMARY KEY (id_infermer, id_operacio)
);


-- medicació
CREATE TABLE dades_per.MEDICAMENT (
    id_medicament SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    descripcio TEXT,
    preu_u NUMERIC
);

CREATE TABLE pacient.RECEPTA(
    id_recepta SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.PACIENT(id_pacient),
    id_metge INT REFERENCES dades_per.METGE(id_personal),
    data DATE,
    descripcio TEXT,
    import_total NUMERIC
);

CREATE TABLE pacient.LINIA_RECEPTA(
    id_linea SERIAL PRIMARY KEY,
    id_recepta INT REFERENCES pacient.RECEPTA(id_recepta),
    id_medicament INT REFERENCES dades_per.MEDICAMENT(id_medicament),
    quantitat INT,
    cost NUMERIC
);


-- relacions visita - ingres
CREATE TABLE pacient.RECEPTA_VISITA(
    id_recepta INT REFERENCES pacient.RECEPTA(id_recepta),
    id_visita INT REFERENCES pacient.VISITA(id_visita),
    PRIMARY KEY (id_recepta, id_visita)
);


-- cantina
CREATE TABLE cantina.EMPRESA_EXTERNA (
    id_empresa SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    direccio TEXT,
    telefon VARCHAR(20),
    correu VARCHAR(100) UNIQUE,
    persona_contacte VARCHAR(50)
);

CREATE TABLE cantina.FACTURACIO_CANTINA(
    id_tiquet SERIAL PRIMARY KEY,
    id_empresa INT REFERENCES cantina.EMPRESA_EXTERNA(id_empresa),
    data DATE,
    import_total NUMERIC,
    percentatge NUMERIC,
    import_lloguer NUMERIC
);
