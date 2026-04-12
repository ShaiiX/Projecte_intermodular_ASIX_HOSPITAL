# Entitats i atributs

### PERSONAL
**(`id_personal` (PK), dni, nom, cognom1, cognom2, data_naixament, adreça, telefon, horari, email, baixa)**
Entitat general per a qualsevol treballador del centre. És la superclase de Metge, Infermer i Personal Vari. L'atribut baixa es per a identificar si l'empleat esta de baixa o no.

### METGE
**(`id_personal` (PK/FK), especialitat, curriculum, num_colegiat)**
Personal mèdic especialitzat. Subentitat de Personal, amb dades dels seus estudis a més del curriculum que es un pdf.

### INFERMER
**(`id_personal` (PK/FK), torn, experiencia)**
Personal d'infermeria. Es divideix en especialitats de planta o de suport a metges.

### INFERMER_PLANTA
**(`id_personal` (PK/FK))**
Subentitat d'infermer assignada específicament a la cura d'una planta hospitalària.

### INFERMER_METGE
**(`id_personal` (PK/FK))**
Subentitat d'infermer que treballa directament col·laborant amb els metges.

### VARI
**(`id_personal` (PK/FK), tipus_feina, horari)**
Personal no sanitari del centre (manteniment, administració, etc.).

### PACIENT
**(`id_pacient` (PK), dni, nom, cognoms, data_naixament, telefon, email, targeta_sanitaria)**
Persona que rep l'atenció mèdica i que pot estar vinculat a un ingrés hospitalari.

### EXPEDIENT
**(`id_exp` (PK), data_actualitzacio, historial, observacions)**
Documentació clínica centralitzada de cada pacient.

### VISITA
**(`id_visita` (PK), data, diagnostic)**
Registre de les consultes diagnòstiques entre metges i pacients.

### PROVA
**(`id_prova` (PK), tipus, data, estat, resultat)**
Exàmens mèdics concrets realitzats als pacients per ordre mèdica.

### OPERACIO
**(`id_operacio` (PK), data, estat, tipus_operacio, descripcio)**
Intervencions quirúrgiques realitzades per l'equip mèdic amb suport de infermers a pacients.

### PLANTA
**(`id_planta` (PK), num_planta, descripcio)**
Divisió física de l'hospital que agrupa diverses habitacions.

### QUIROFAN
**(`num_quirofan` (PK), estat)**
Sala física on es duen a terme les operacions on pertanyen a una planta en especific, sent una entitat feble de planta, ja que el seu identificador necesita de la planta.

### APARELL_MEDIC
**(`id_aparell` (PK), marca, num_serie, model, tipus, data_manteniment)**
Inventari tecnològic que pertany a les sales de quirofan, es tracta de informació especifica de cada aparell.

### INGRES
**(`id_ingres` (PK), data_ingres, data_sortida_prevista, data_sortida_real, estat)**
Registre de l'estada d'un pacient al centre, sent la com la reserva d'habitacions.

### HABITACIO
**(`id_habitacio` (PK), num_habitacio, estat, capacitat)**
Es tracta de les habitacions que es reserven per a un pacient que esta en ingres.

### MEDICAMENT
**(`id_medicament` (PK), nom, descripcio)**
Es tracta de medicament amb el nom especific i descripció, només conte això ja que no es necesari guardar-ne aqui altres dades.

### FARMACIA
**(`id_sortida` (PK), data, import_total, descripcio)**
Gestió de les vendes o sortides de medicaments, a més incorporara al pacient/ingres a qui si l'hi ha subministrat aquest medicaments.

## Cantina
Apartat d'amplicació de la cantina
### EMPRESA_EXTERNA
**(`id_empresa` (PK), nom, direccio, correu, telefon, persona_contacte)**
Es tracta de les empreses que poden llogar la cantina, com no sempre serà la mateixa empresa, es necesari guardar-ne dades de les proximes empreses.

### FACTURACIO_CANTINA
**(`id_tiquet` (PK), data, import_total, import_lloguer, percentatge)**
Registre economic fet per la empresa que externa del lloguer de la cantina, es necesari fer el calcul del lloguer que es portara l'hospital.

## Seguretat
Es un apartat incoprorat que no s'indica però si seria necesari per a tenir controlada les dades i tenir-ho informat.
### USUARI
**(`id_usuari` (PK), nomusuari, contrasenya, data_creacio, actiu, ultim_login)**
Aquesta entitat es per a mantenir les dades dels usuaris que utilitzaran el sistema, funcionara per a trovar de forma més rapida aquestes dades a més d'afegir alguna capa més de seguretat dins de la aplicacio.

### ROL
**(`id_rol` (PK), nom, descripcio)**
Es tracta dels rols que poden tenir els usuaris a la base de dades, només es per a tenirlos guardats per a tenir forma més accesible de llegir-ho, incloent una descripció de que serveix, potser un usuari pot tenir mes de un rol.

### LOG_ACCESS
**(`id_log` (PK), data, accio, taula_afectada, posicio_log, id_registre)**
Auditoria que registre on es guarda que accio a fet un usuari a que a afectat i la posicio del log.txt per a observar la comanda completa que ha fet l'usuari.