# Model Relacional
## 1. Gestió de Personal i Usuaris

* **PERSONAL** (**id_personal**, dni, nom, cognom1, cognom2, data_naixement, adreça, email, telefon, baixa)
* **METGE** (**id_personal**, especialitat, curriculum, num_collegiat)
    * FK: `id_personal` REFERENCIA `PERSONAL(id_personal)`
* **INFERMER** (**id_personal**, torn, experiencia)
    * FK: `id_personal` REFERENCIA `PERSONAL(id_personal)`
* **VARI** (**id_personal**, tipus_feina, horari)
    * FK: `id_personal` REFERENCIA `PERSONAL(id_personal)`

* **USUARI** (**id_usuari**, nom_usuari, contrasenya, actiu, data_creacio, ultim_login, **id_personal**)
    * FK: `id_personal` REFERENCIA `PERSONAL(id_personal)`
* **ROL** (**id_rol**, nom, descripcio)
* **USUARI_PERTANY_ROL** (**id_usuari**, **id_rol**)
    * FK: `id_usuari` REFERENCIA `USUARI(id_usuari)`
    * FK: `id_rol` REFERENCIA `ROL(id_rol)`
* **LOG_ACCES** (**id_log**, data, accio, id_registre, taula_afectada, posicio_log, **id_usuari**)
    * FK: `id_usuari` REFERENCIA `USUARI(id_usuari)`

## 2. Gestió de Pacients i Activitat Clínica

* **PACIENT** (**id_pacient**, dni, nom, cognoms, data_naixement, tarjeta_sanitaria, email, telefon)
* **EXPEDIENT** (**id_exp**, data_actualitzacio, historial, observacions, **id_pacient**)
    * FK: `id_pacient` REFERENCIA `PACIENT(id_pacient)`
* **VISITA** (**id_visita**, data, diagnostic, **id_pacient**, **id_metge**)
    * FK: `id_pacient` REFERENCIA `PACIENT(id_pacient)`
    * FK: `id_metge` REFERENCIA `METGE(id_personal)`
* **PROVA** (**id_prova**, tipus, data, resultat, estat, **id_visita**)
    * FK: `id_visita` REFERENCIA `VISITA(id_visita)`


## 3. Infraestructura i Equipament

* **PLANTA** (**id_planta**, num_planta, descripcio)
* **HABITACIO** (**id_habitacio**, num_habitacio, capacitat, estat, **id_planta**)
    * FK: `id_planta` REFERENCIA `PLANTA(id_planta)`
* **QUIROFAN** (**id_planta** **num_quirofan**, estat)
    * FK: `id_planta` REFERENCIA `PLANTA(id_planta)`
* **APARELL_MEDIC** (**id_aparell**, num_serie, marca, model, tipus, data_manteniment, **id_planta** **num_quirofan**)
    * FK: `(id_planta, num_quirofan)` REFERENCIA `QUIROFAN(id_planta, num_quirofan)`
* **OPERACIO** (**id_operacio**, data, tipus_operacio, estat, descripcio, **id_pacient**, **id_metge**, **id_planta** **num_quirofan**)
    * FK: `id_pacient` REFERENCIA `PACIENT(id_pacient)`
    * FK: `id_metge` REFERENCIA `METGE(id_personal)`
    * FK: `(id_planta, num_quirofan)` REFERENCIA `QUIROFAN(id_planta, num_quirofan)`

## 4. Ingressos i Farmàcia

* **INGRES** (**id_ingres**, data_ingres, data_sortida_prevista, data_sortida_real, **id_pacient**, **id_habitacio**)
    * FK: `id_pacient` REFERENCIA `PACIENT(id_pacient)`
    * FK: `id_habitacio` REFERENCIA `HABITACIO(id_habitacio)`
* **MEDICAMENT** (**id_medicament**, nom, descripcio)
* **FARMACIA** (**id_sortida**, data, import_total, descripcio, **id_ingres**)
    * FK: `id_ingres` REFERENCIA `INGRES(id_ingres)`


## 5. Serveis Externs i Altres

* **EMPRESA_EXTERNA** (**id_empresa**, nom, direccio, correu, telefon, persona_contacte)
* **FACTURACIO_CANTINA** (**id_tiquet**, data, import_total, import_lloguer, percentatge, **id_empresa**)
    * FK: `id_empresa` REFERENCIA `EMPRESA_EXTERNA(id_empresa)`


## 6. Taules Auxiliars de Relació (N:M)
* **FARMACIA_MEDICAMENT** (**id_sortida**, **id_medicament**, quantitat, preu_u, cost)
    * FK: `id_sortida` REFERENCIA `FARMACIA(id_sortida)`
    * FK: `id_medicament` REFERENCIA `MEDICAMENT(id_medicament)`
* **VISITA_MEDICAMENT** (**id_visita**, **id_medicament**, quantitat, descripcio)
    * FK: `id_visita` REFERENCIA `VISITA(id_visita)`
    * FK: `id_medicament` REFERENCIA `MEDICAMENT(id_medicament)`
* **EQUIP_OPERACIO** (**id_operacio**, **id_infermer**, rol)
    * FK: `id_operacio` REFERENCIA `OPERACIO(id_operacio)`
    * FK: `id_infermer` REFERENCIA `INFERMER(id_personal)`
* **INFERMER_PLANTA** (**id_infermer**, **id_planta**)
    * FK: `id_infermer` REFERENCIA `INFERMER(id_personal)`
    * FK: `id_planta` REFERENCIA `PLANTA(id_planta)`
* **INFERMER_METGE** (**id_infermer**, **id_metge**)
    * FK: `id_infermer` REFERENCIA `INFERMER(id_personal)`
    * FK: `id_metge` REFERENCIA `METGE(id_personal)`