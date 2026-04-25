CREATE OR REPLACE VIEW pacient.vista_operacions_detallades AS
SELECT 
    o.data AS dia,              -- Usaremos este campo para filtrar en Python
    q.id_planta || ' ' ||q.num_quirofan AS quirofan,
    p.nom || ' ' || p.cognoms AS pacient,
    p.tarjeta_sanitaria AS sanitaria, 
    p_met.nom || ' ' || p_met.cognom1 || ' ' || p_met.cognom2 AS metge,
    -- Subconsulta para agrupar los enfermeros en una sola celda
    (SELECT STRING_AGG(p_inf.id_personal, ' : ', p_inf.nom, ' ', p_inf.cognom1, ' ', p_inf.cognom2,', ') 
     FROM dades_per.INFERMER_OPERACIO io 
     JOIN dades_per.INFERMER i ON io.id_infermer = i.id_personal
     JOIN dades_per.PERSONAL p_inf ON i.id_personal = p_inf.id_personal
     WHERE io.id_operacio = o.id_operacio) AS equip_infermeria
FROM pacient.OPERACIO o
JOIN estructura.QUIROFAN q ON o.id_quirofan = q.id_quirofan
JOIN pacient.PACIENT p ON o.id_planta = p.id_planta AND o.num_quirofan = p.num_quirofan
JOIN dades_per.METGE m ON o.id_metge = m.id_personal
JOIN dades_per.PERSONAL p_met ON m.id_personal = p_met.id_personal;



CREATE OR REPLACE VIEW pacient.vista_visites_detallades AS
SELECT 
    v.data::date AS dia,             -- Extraiem només la data per filtrar fàcilment
    v.data::time AS hora_entrada,    -- Extraiem l'hora per mostrar-la a la interfície
    p_met.nom || ' ' || p_met.cognom1 || ' ' || p_met.cognom2 AS metge,
    p_pac.nom || ' ' || p_pac.cognoms AS pacient,
FROM pacient.VISITA v
JOIN dades_per.METGE m ON v.id_metge = m.id_personal
JOIN dades_per.PERSONAL p_met ON m.id_personal = p_met.id_personal
JOIN pacient.PACIENT p_pac ON v.id_pacient = p_pac.id_pacient;