-- schema seguretat
CREATE TABLE seguretat.rol(
    id_rol SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL,
    descripcio TEXT
);

CREATE TABLE seguretat.usuari (
    id_usuari SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password BYTEA NOT NULL,    -- bytea per emmagatzemar hash de contrasenya (binari) per guardarlo directament sense conversions a text
    actiu BOOLEAN DEFAULT TRUE,
    data_creacio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultim_login TIMESTAMP
);

CREATE TABLE seguretat.usuari_rol (
    id_usuari INT REFERENCES seguretat.usuari(id_usuari),
    id_rol INT REFERENCES seguretat.rol(id_rol),
    PRIMARY KEY (id_usuari, id_rol)
);

CREATE TABLE seguretat.log_access (
    id_log SERIAL PRIMARY KEY,
    id_usuari INT REFERENCES seguretat.usuari(id_usuari),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accio TEXT,
    taula_afectada TEXT
);


-- estructura
CREATE TABLE estructura.planta(
    id_planta SERIAL PRIMARY KEY,
    num_planta INT UNIQUE,
    descripcio TEXT
);

CREATE TABLE estructura.habitacio (
    id_habitacio SERIAL PRIMARY KEY,
    id_planta INT REFERENCES estructura.planta(id_planta),
    num_habitacio INT,
    capacitat INT,
    estat VARCHAR(50),
    CONSTRAINT unique_num_hab_pl UNIQUE (id_planta, num_habitacio)
);

CREATE TABLE estructura.quirofan(
    id_planta INT REFERENCES estructura.planta(id_planta),
    num_quirofan INT,
    estat VARCHAR(50),
    PRIMARY KEY (id_planta, num_quirofan)
);

CREATE TABLE estructura.tipus(
    id_tipus SERIAL PRIMARY KEY,
    model VARCHAR(50),
    marca VARCHAR(50),
    tipus VARCHAR(50)
);

CREATE TABLE estructura.aparell_medic(
    id_aparell SERIAL PRIMARY KEY,
    num_serie VARCHAR(100) UNIQUE,
    data_manteniment DATE,
    id_tipus INT REFERENCES estructura.tipus(id_tipus)
);


-- schema dades_personal
CREATE TABLE dades_per.personal(
    id_personal SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    cognom1 VARCHAR(50),
    cognom2 VARCHAR(50),
    dni VARCHAR(9) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    direccio TEXT,
    data_naixement DATE,
    baixa DATE
);

-- herència de personal
CREATE TABLE dades_per.metge(
    id_personal INT PRIMARY KEY REFERENCES dades_per.personal(id_personal),
    especialitat VARCHAR(100),
    curriculum TEXT,
    num_colegiat VARCHAR(50)
);

CREATE TABLE dades_per.infermer(
    id_personal INT PRIMARY KEY REFERENCES dades_per.personal(id_personal),
    experiencia INT,
    torn VARCHAR(50)
);

CREATE TABLE dades_per.vari(
    id_personal INT PRIMARY KEY REFERENCES dades_per.personal(id_personal),
    tipus_feina VARCHAR(100),
    horari VARCHAR(100)
);

-- relacions
CREATE TABLE dades_per.infermer_metge(
    id_infermer INT REFERENCES dades_per.infermer(id_personal),
    id_metge INT REFERENCES dades_per.metge(id_personal),
    PRIMARY KEY (id_infermer, id_metge)
);

CREATE TABLE dades_per.infermer_planta(
    id_infermer INT REFERENCES dades_per.infermer(id_personal),
    id_planta INT REFERENCES estructura.planta(id_planta),
    PRIMARY KEY (id_infermer, id_planta)
);


-- pacient
CREATE TABLE pacient.pacient(
    id_pacient SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    cognoms VARCHAR(100),
    dni VARCHAR(9) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    data_naixement DATE,
    tarjeta_sanitaria VARCHAR(30) UNIQUE,
    id_habitacio INT REFERENCES estructura.habitacio(id_habitacio)
);

CREATE TABLE pacient.expedient(
    id_exp SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.pacient(id_pacient),
    historial TEXT,
    data_actualitzacio DATE,
    observacions TEXT
);

CREATE TABLE pacient.visita(
    id_visita SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.pacient(id_pacient),
    id_metge INT REFERENCES dades_per.metge(id_personal),
    data DATE,
    diagnostic TEXT
);

CREATE TABLE pacient.prova(
    id_prova SERIAL PRIMARY KEY,
    id_visita INT REFERENCES pacient.visita(id_visita),
    tipus VARCHAR(50),
    resultat TEXT,
    estat VARCHAR(50),
    data DATE
);

CREATE TABLE pacient.operacio(
    id_operacio SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.pacient(id_pacient),
    tipus_operacio VARCHAR(100),
    estat VARCHAR(50),
    data DATE,
    descripcio TEXT,
    id_planta INT,
    num_quirofan INT,
    FOREIGN KEY (id_planta, num_quirofan) 
        REFERENCES estructura.quirofan(id_planta, num_quirofan)
);

CREATE TABLE pacient.ingres(
    id_ingres SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.pacient(id_pacient),
    data_ingres DATE,
    data_sortida_prevista DATE,
    data_sortida_real DATE
);


-- relacions operacio - ifermer
CREATE TABLE dades_per.infermer_operacio(
    id_infermer INT REFERENCES dades_per.infermer(id_personal),
    id_operacio INT REFERENCES pacient.operacio(id_operacio),
    rol VARCHAR(50),
    PRIMARY KEY (id_infermer, id_operacio)
);


-- medicació
CREATE TABLE dades_per.medicament (
    id_medicament SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    descripcio TEXT,
    preu_u NUMERIC
);

CREATE TABLE pacient.recepta(
    id_recepta SERIAL PRIMARY KEY,
    id_pacient INT REFERENCES pacient.pacient(id_pacient),
    id_metge INT REFERENCES dades_per.metge(id_personal),
    data DATE,
    descripcio TEXT,
    import_total NUMERIC
);

CREATE TABLE pacient.linea_recepta(
    id_linea SERIAL PRIMARY KEY,
    id_recepta INT REFERENCES pacient.recepta(id_recepta),
    id_medicament INT REFERENCES dades_per.medicament(id_medicament),
    quantitat INT,
    cost NUMERIC
);


-- relacions visita - ingres
CREATE TABLE pacient.recepta_visita(
    id_recepta INT REFERENCES pacient.recepta(id_recepta),
    id_visita INT REFERENCES pacient.visita(id_visita),
    PRIMARY KEY (id_recepta, id_visita)
);


-- cantina
CREATE TABLE cantina.empresa_externa (
    id_empresa SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    direccio TEXT,
    telefon VARCHAR(20),
    correu VARCHAR(100) UNIQUE,
    persona_contacte VARCHAR(50)
);

CREATE TABLE cantina.facturacio_cantina(
    id_tiquet SERIAL PRIMARY KEY,
    id_empresa INT REFERENCES cantina.empresa_externa(id_empresa),
    data DATE,
    import_total NUMERIC,
    percentatge NUMERIC,
    import_lloguer NUMERIC
);


