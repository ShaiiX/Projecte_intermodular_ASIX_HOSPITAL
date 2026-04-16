-- 1. PERSONAL I USUARIS

CREATE TABLE PERSONAL (
    id_personal INT,
    dni VARCHAR(9) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    cognom1 VARCHAR(50) NOT NULL,
    cognom2 VARCHAR(50) NOT NULL,
    data_naixement DATE NOT NULL,
    adreca VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefon VARCHAR(20) NOT NULL,
    baixa BOOLEAN,
    CONSTRAINT pk_personal PRIMARY KEY (id_personal)
);

CREATE TABLE METGE (
    id_personal INT,
    especialitat VARCHAR(50) NOT NULL,
    curriculum TEXT,
    num_collegiat VARCHAR(50) NOT NULL,
    CONSTRAINT pk_metge PRIMARY KEY (id_personal),
    CONSTRAINT fk_metge_personal 
        FOREIGN KEY (id_personal) REFERENCES PERSONAL(id_personal)
);

CREATE TABLE INFERMER (
    id_personal INT,
    torn VARCHAR(50),
    experiencia TEXT,
    CONSTRAINT pk_infermer PRIMARY KEY (id_personal),
    CONSTRAINT fk_infermer_personal 
        FOREIGN KEY (id_personal) REFERENCES PERSONAL(id_personal)
);

CREATE TABLE VARI (
    id_personal INT,
    tipus_feina VARCHAR(50) NOT NULL,
    horari VARCHAR(50),
    CONSTRAINT pk_vari PRIMARY KEY (id_personal),
    CONSTRAINT fk_vari_personal 
        FOREIGN KEY (id_personal) REFERENCES PERSONAL(id_personal)
);

CREATE TABLE USUARI (
    id_usuari INT,
    nom_usuari VARCHAR(100) NOT NULL,
    contrasenya VARCHAR(255) NOT NULL,
    actiu BOOLEAN,
    data_creacio TIMESTAMP,
    ultim_login TIMESTAMP,
    id_personal INT,
    CONSTRAINT pk_usuari PRIMARY KEY (id_usuari),
    CONSTRAINT fk_usuari_personal 
        FOREIGN KEY (id_personal) REFERENCES PERSONAL(id_personal)
);

CREATE TABLE ROL (
    id_rol INT,
    nom VARCHAR(50) NOT NULL,
    descripcio TEXT NOT NULL,
    CONSTRAINT pk_rol PRIMARY KEY (id_rol)
);

CREATE TABLE USUARI_PERTANY_ROL (
    id_usuari INT,
    id_rol INT,
    CONSTRAINT pk_usuari_rol PRIMARY KEY (id_usuari, id_rol),
    CONSTRAINT fk_upr_usuari 
        FOREIGN KEY (id_usuari) REFERENCES USUARI(id_usuari),
    CONSTRAINT fk_upr_rol 
        FOREIGN KEY (id_rol) REFERENCES ROL(id_rol)
);

CREATE TABLE LOG_ACCES (
    id_log INT,
    data TIMESTAMP,
    accio VARCHAR(20) NOT NULL,
    id_registre INT,
    taula_afectada VARCHAR(40),
    posicio_log INT,
    id_usuari INT,
    CONSTRAINT pk_log_acces PRIMARY KEY (id_log),
    CONSTRAINT fk_log_usuari 
        FOREIGN KEY (id_usuari) REFERENCES USUARI(id_usuari)
);

-- 2. PACIENTS

CREATE TABLE PACIENT (
    id_pacient INT,
    dni VARCHAR(9) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    cognoms VARCHAR(50) NOT NULL,
    data_naixement DATE NOT NULL,
    tarjeta_sanitaria VARCHAR(50),
    email VARCHAR(100) NOT NULL,
    telefon VARCHAR(20) NOT NULL,
    CONSTRAINT pk_pacient PRIMARY KEY (id_pacient)
);

CREATE TABLE EXPEDIENT (
    id_exp INT,
    data_actualitzacio TIMESTAMP NOT NULL,
    historial TEXT NOT NULL,
    observacions TEXT NOT NULL,
    id_pacient INT,
    CONSTRAINT pk_expedient PRIMARY KEY (id_exp),
    CONSTRAINT fk_expedient_pacient 
        FOREIGN KEY (id_pacient) REFERENCES PACIENT(id_pacient)
);

CREATE TABLE VISITA (
    id_visita INT,
    data TIMESTAMP NOT NULL,
    diagnostic TEXT NOT NULL,
    id_pacient INT,
    id_metge INT,
    CONSTRAINT pk_visita PRIMARY KEY (id_visita),
    CONSTRAINT fk_visita_pacient 
        FOREIGN KEY (id_pacient) REFERENCES PACIENT(id_pacient),
    CONSTRAINT fk_visita_metge 
        FOREIGN KEY (id_metge) REFERENCES METGE(id_personal)
);

CREATE TABLE PROVA (
    id_prova INT,
    tipus VARCHAR(30) NOT NULL,
    data TIMESTAMP NOT NULL,
    resultat TEXT NOT NULL,
    estat VARCHAR(50) NOT NULL,
    id_visita INT,
    CONSTRAINT pk_prova PRIMARY KEY (id_prova),
    CONSTRAINT fk_prova_visita 
        FOREIGN KEY (id_visita) REFERENCES VISITA(id_visita)
);

-- 3. INFRAESTRUCTURA

CREATE TABLE PLANTA (
    id_planta INT,
    num_planta INT,
    descripcio TEXT,
    CONSTRAINT pk_planta PRIMARY KEY (id_planta)
);

CREATE TABLE HABITACIO (
    id_habitacio INT,
    num_habitacio VARCHAR(20) NOT NULL,
    capacitat INT NOT NULL,
    estat VARCHAR(50) NOT NULL,
    id_planta INT,
    CONSTRAINT pk_habitacio PRIMARY KEY (id_habitacio),
    CONSTRAINT fk_habitacio_planta 
        FOREIGN KEY (id_planta) REFERENCES PLANTA(id_planta)
);

CREATE TABLE QUIROFAN (
    id_planta INT,
    num_quirofan INT,
    estat VARCHAR(50) NOT NULL,
    CONSTRAINT pk_quirofan PRIMARY KEY (id_planta, num_quirofan),
    CONSTRAINT fk_quirofan_planta 
        FOREIGN KEY (id_planta) REFERENCES PLANTA(id_planta)
);

CREATE TABLE APARELL_MEDIC (
    id_aparell INT,
    num_serie VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    tipus VARCHAR(100) NOT NULL,
    data_manteniment DATE,
    id_planta INT,
    num_quirofan INT,
    CONSTRAINT pk_aparell PRIMARY KEY (id_aparell),
    CONSTRAINT fk_aparell_quirofan 
        FOREIGN KEY (id_planta, num_quirofan)
        REFERENCES QUIROFAN(id_planta, num_quirofan)
);

CREATE TABLE OPERACIO (
    id_operacio INT,
    data TIMESTAMP NOT NULL,
    tipus_operacio VARCHAR(50) NOT NULL,
    estat VARCHAR(50) NOT NULL,
    descripcio TEXT NOT NULL,
    id_pacient INT,
    id_metge INT,
    id_planta INT,
    num_quirofan INT,
    CONSTRAINT pk_operacio PRIMARY KEY (id_operacio),
    CONSTRAINT fk_operacio_pacient 
        FOREIGN KEY (id_pacient) REFERENCES PACIENT(id_pacient),
    CONSTRAINT fk_operacio_metge 
        FOREIGN KEY (id_metge) REFERENCES METGE(id_personal),
    CONSTRAINT fk_operacio_quirofan 
        FOREIGN KEY (id_planta, num_quirofan)
        REFERENCES QUIROFAN(id_planta, num_quirofan)
);

-- 4. INGRESSOS

CREATE TABLE INGRES (
    id_ingres INT,
    data_ingres DATE NOT NULL,
    data_sortida_prevista DATE NOT NULL,
    data_sortida_real DATE, 
    id_pacient INT,
    id_habitacio INT,
    CONSTRAINT pk_ingres PRIMARY KEY (id_ingres),
    CONSTRAINT fk_ingres_pacient 
        FOREIGN KEY (id_pacient) REFERENCES PACIENT(id_pacient),
    CONSTRAINT fk_ingres_habitacio 
        FOREIGN KEY (id_habitacio) REFERENCES HABITACIO(id_habitacio)
);

CREATE TABLE MEDICAMENT (
    id_medicament INT,
    nom VARCHAR(100) NOT NULL,
    descripcio TEXT NOT NULL,
    CONSTRAINT pk_medicament PRIMARY KEY (id_medicament)
);

CREATE TABLE FARMACIA (
    id_sortida INT,
    data TIMESTAMP NOT NULL,
    import_total DECIMAL(10,2) NOT NULL,
    descripcio TEXT NOT NULL,
    id_ingres INT,
    CONSTRAINT pk_farmacia PRIMARY KEY (id_sortida),
    CONSTRAINT fk_farmacia_ingres 
        FOREIGN KEY (id_ingres) REFERENCES INGRES(id_ingres)
);

-- 5. EMPRESES

CREATE TABLE EMPRESA_EXTERNA (
    id_empresa INT,
    nom VARCHAR(150) NOT NULL,
    direccio VARCHAR(255) NOT NULL, 
    correu VARCHAR(100) NOT NULL,
    telefon VARCHAR(20) NOT NULL,
    persona_contacte VARCHAR(50) NOT NULL,
    CONSTRAINT pk_empresa PRIMARY KEY (id_empresa)
);

CREATE TABLE FACTURACIO_CANTINA (
    id_tiquet INT,
    data TIMESTAMP NOT NULL,
    import_total DECIMAL(10,2) NOT NULL,
    import_lloguer DECIMAL(10,2) NOT NULL,
    percentatge DECIMAL(5,2) NOT NULL,
    id_empresa INT,
    CONSTRAINT pk_facturacio PRIMARY KEY (id_tiquet),
    CONSTRAINT fk_facturacio_empresa 
        FOREIGN KEY (id_empresa) REFERENCES EMPRESA_EXTERNA(id_empresa)
);

-- 6. RELACIONS N:M

CREATE TABLE FARMACIA_MEDICAMENT (
    id_sortida INT,
    id_medicament INT,
    quantitat INT NOT NULL,
    preu_u DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    CONSTRAINT pk_farmacia_medicament PRIMARY KEY (id_sortida, id_medicament),
    CONSTRAINT fk_fm_sortida 
        FOREIGN KEY (id_sortida) REFERENCES FARMACIA(id_sortida),
    CONSTRAINT fk_fm_medicament 
        FOREIGN KEY (id_medicament) REFERENCES MEDICAMENT(id_medicament)
);

CREATE TABLE VISITA_MEDICAMENT (
    id_visita INT,
    id_medicament INT,
    quantitat INT NOT NULL,
    descripcio TEXT NOT NULL,
    CONSTRAINT pk_visita_medicament PRIMARY KEY (id_visita, id_medicament),
    CONSTRAINT fk_vm_visita 
        FOREIGN KEY (id_visita) REFERENCES VISITA(id_visita),
    CONSTRAINT fk_vm_medicament 
        FOREIGN KEY (id_medicament) REFERENCES MEDICAMENT(id_medicament)
);

CREATE TABLE EQUIP_OPERACIO (
    id_operacio INT,
    id_infermer INT,
    rol VARCHAR(50) NOT NULL,
    CONSTRAINT pk_equip_operacio PRIMARY KEY (id_operacio, id_infermer),
    CONSTRAINT fk_eo_operacio 
        FOREIGN KEY (id_operacio) REFERENCES OPERACIO(id_operacio),
    CONSTRAINT fk_eo_infermer 
        FOREIGN KEY (id_infermer) REFERENCES INFERMER(id_personal)
);

CREATE TABLE INFERMER_PLANTA (
    id_infermer INT,
    id_planta INT,
    CONSTRAINT pk_infermer_planta PRIMARY KEY (id_infermer, id_planta),
    CONSTRAINT fk_ip_infermer 
        FOREIGN KEY (id_infermer) REFERENCES INFERMER(id_personal),
    CONSTRAINT fk_ip_planta 
        FOREIGN KEY (id_planta) REFERENCES PLANTA(id_planta)
);

CREATE TABLE INFERMER_METGE (
    id_infermer INT,
    id_metge INT,
    CONSTRAINT pk_infermer_metge PRIMARY KEY (id_infermer, id_metge),
    CONSTRAINT fk_im_infermer 
        FOREIGN KEY (id_infermer) REFERENCES INFERMER(id_personal),
    CONSTRAINT fk_im_metge 
        FOREIGN KEY (id_metge) REFERENCES METGE(id_personal)
);