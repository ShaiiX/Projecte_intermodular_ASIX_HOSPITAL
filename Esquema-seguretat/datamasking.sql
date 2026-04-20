CREATE OR REPLACE VIEW pacient_mask AS    -- dades protegides pel pacient
SELECT id_pacient, nom, cognoms,
    CONCAT('***', RIGHT(dni, 3)) AS dni,    -- dni amb els ultims 3 caracters
    '***' AS telefon,   -- telefon no es mostra
    CONCAT(LEFT(email, 2), '***@***.com') AS email, data_naixement
FROM pacient;

-- expedient mèdic
CREATE OR REPLACE VIEW expedient_mask AS
SELECT id_expedient, id_pacient,
    '*** Dades protegides ***' AS historial,    -- ocultar dades sensibles
    data_actualitzacio
FROM expedient;

-- vista de vistes amb diagnòstic ocult
CREATE OR REPLACE VIEW visita_mask AS
SELECT id_visita, id_pacient, data_visita,
    '***' AS diagnostic, id_metge
FROM visita;

-- vista receptes ocultes
CREATE OR REPLACE VIEW recepta_mask AS
SELECT id_recepta, id_pacient,
    '***' AS descripcio, data_recepta
FROM recepta;
