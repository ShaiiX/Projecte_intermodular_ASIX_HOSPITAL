-- Vista per a Operacions
CREATE OR REPLACE VIEW pacient.vista_operacions_detallades AS
SELECT 
    o.data::date AS dia,
    o.data::time AS hora,
    q.id_planta || ' - ' || q.num_quirofan AS quirofan,
    p.nom || ' ' || p.cognoms AS pacient,
    p_met.nom || ' ' || p_met.cognom1 AS metge,
    (SELECT STRING_AGG(p_inf.nom || ' ' || p_inf.cognom1, ', ') 
     FROM dades_per.INFERMER_OPERACIO io 
     JOIN dades_per.PERSONAL p_inf ON io.id_infermer = p_inf.id_personal
     WHERE io.id_operacio = o.id_operacio) AS equip_infermeria
FROM pacient.OPERACIO o
JOIN estructura.QUIROFAN q ON o.num_quirofan = q.num_quirofan and o.id_planta = q.id_planta
JOIN pacient.PACIENT p ON o.id_pacient = p.id_pacient
JOIN dades_per.METGE m ON o.id_metge = m.id_personal
JOIN dades_per.PERSONAL p_met ON m.id_personal = p_met.id_personal;

-- Vista per a Visites
CREATE OR REPLACE VIEW pacient.vista_visites_detallades AS
SELECT 
    v.data::date AS dia,
    v.data::time AS hora_entrada,
    p_met.nom || ' ' || p_met.cognom1 || ' ' || p_met.cognom2 AS metge,
    p_pac.nom || ' ' || p_pac.cognoms AS pacient
FROM pacient.VISITA v
JOIN dades_per.METGE m ON v.id_personal = m.id_personal
JOIN dades_per.PERSONAL p_met ON m.id_personal = p_met.id_personal
JOIN pacient.PACIENT p_pac ON v.id_pacient = p_pac.id_pacient;

-- Vista d'Inventari
CREATE OR REPLACE VIEW estructura.vista_inventari_quirofans AS
SELECT 
    q.id_planta,
    q.num_quirofan,
    t.tipus AS nom_aparell,
    t.marca,
    COUNT(a.id_aparell) AS quantitat
FROM estructura.QUIROFAN q
JOIN estructura.APARELL_MEDIC a ON q.num_quirofan = a.num_quirofan AND q.id_planta = a.id_planta
JOIN estructura.TIPUS t ON a.id_tipus = t.id_tipus
GROUP BY q.num_quirofan, t.tipus, t.marca;

-- ==========================================================
-- 2. FUNCIONS I TRIGGERS DE VALIDACIÓ
-- ==========================================================

-- Validació de dates d'ingrés
CREATE OR REPLACE FUNCTION pacient.validar_ingres_dates() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.data_sortida_real IS NOT NULL AND NEW.data_sortida_real < NEW.data_ingres THEN
        RAISE EXCEPTION 'Error: data sortida real anterior a ingrés';
    END IF;
    IF NEW.data_sortida_prevista IS NOT NULL AND NEW.data_sortida_prevista < NEW.data_ingres THEN
        RAISE EXCEPTION 'Error: data sortida prevista anterior a ingrés';
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER t_validar_ingres 
BEFORE INSERT OR UPDATE ON pacient.INGRES
FOR EACH ROW EXECUTE FUNCTION pacient.validar_ingres_dates();

-- Validació d'ocupació de quiròfan
CREATE OR REPLACE FUNCTION pacient.validar_quirofan_ocu() RETURNS TRIGGER AS $$
DECLARE existeix INT;
BEGIN
    SELECT COUNT(*) INTO existeix 
    FROM pacient.OPERACIO
    WHERE id_quirofan = NEW.id_quirofan AND data = NEW.data;

    IF existeix > 0 THEN
        RAISE EXCEPTION 'Error: el quiròfan està ocupat a aquesta data i hora';
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER t_validar_operacio 
BEFORE INSERT ON pacient.OPERACIO
FOR EACH ROW EXECUTE FUNCTION pacient.validar_quirofan_ocu();

-- opcional 1:
CREATE OR REPLACE VIEW pacient.vista_ingressos_habitacio AS
SELECT i.id_habitacio, i.data_ingres, i.data_sortida_prevista,
    CONCAT(p.nom, ' ', p.cognoms) AS pacient, i.data_sortida_real
FROM pacient.INGRES i
INNER JOIN pacient.PACIENT p 
    ON p.id_pacient = i.id_pacient;

-- ús de la vista
/*
SELECT *
FROM vista_ingressos_habitacio
WHERE id_habitacio = 1
ORDER BY data_ingres;
*/

-- opcional 2:
CREATE OR REPLACE VIEW pacient.vista_pacient_historial AS
SELECT p.id_pacient, p.nom, p.cognoms,
    -- visites + diagnostic
    COUNT(DISTINCT v.id_visita) AS total_visites,
    STRING_AGG(DISTINCT v.diagnostic, ', ') AS diagnostics,
    -- medicaments receptats
    STRING_AGG(DISTINCT m.nom, ', ') AS medicaments_receptats,
    -- ingressos
    COUNT(DISTINCT i.id_ingres) AS total_ingressos,
    -- vegades quiròfan
    COUNT(DISTINCT o.id_operacio) AS total_operacions

FROM pacient.PACIENT p
LEFT JOIN pacient.VISITA v
    ON v.id_pacient = p.id_pacient
LEFT JOIN pacient.recepta_visita rv
    ON rv.id_visita = v.id_visita
LEFT JOIN pacient.RECEPTA r
    ON r.id_recepta = v.id_visita
LEFT JOIN pacient.linia_recepta lr
    ON lr.id_recepta = r.id_recepta
LEFT JOIN dades_per.MEDICAMENT m
    ON m.id_medicament = lr.id_medicament
LEFT JOIN pacient.INGRES i
    ON i.id_pacient = p.id_pacient
LEFT JOIN pacient.OPERACIO o
    ON o.id_pacient = p.id_pacient
GROUP BY p.id_pacient, p.nom, p.cognoms;


-- opcional3:
CREATE OR REPLACE VIEW dades_per.vista_metge_programacio AS
SELECT
    m.id_personal                                                         AS id_metge,
    p_metge.nom                                                           AS nom_metge,
    p_metge.cognom1                                                       AS cognom1_metge,
    p_metge.cognom2                                                       AS cognom2_metge,
    COALESCE(DATE(v.data), DATE(o.data))                  AS dia,
    CASE
        WHEN v.id_visita   IS NOT NULL THEN 'Visita'
        WHEN o.id_operacio IS NOT NULL THEN 'Operació'
    END                                                                   AS tipus,
    COALESCE(v.data::TIME, o.data::TIME)::time(0)                 AS hora,
    CONCAT(p_pac.nom, ' ', p_pac.cognoms)                                 AS pacient
FROM dades_per.personal p_metge
JOIN dades_per.METGE m
    ON m.id_personal = p_metge.id_personal
JOIN pacient.PACIENT p_pac
    ON p_pac.id_pacient IS NOT NULL
LEFT JOIN pacient.VISITA v
    ON v.id_pacient = p_pac.id_pacient
    AND v.id_metge = m.id_personal
LEFT JOIN pacient.OPERACIO o
    ON o.id_pacient = p_pac.id_pacient
    AND o.id_metge = m.id_personal
WHERE v.id_metge = m.id_personal
   OR o.id_metge = m.id_personal
ORDER BY m.id_personal, dia, hora;