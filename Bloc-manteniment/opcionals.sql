-- opcional 1:
CREATE OR REPLACE VIEW vista_ingressos_habitacio AS
SELECT i.id_habitacio, i.data_ingres, i.data_sortida_prevista,
    CONCAT(p.nom, ' ', p.cognoms) AS pacient
FROM INGRES i
INNER JOIN PACIENT p 
    ON p.id_pacient = i.id_pacient;

-- ús de la vista
/*
SELECT *
FROM vista_ingressos_habitacio
WHERE id_habitacio = 1
ORDER BY data_ingres;
*/

-- opcional 2:
CREATE OR REPLACE VIEW vista_pacient_historial AS
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

FROM PACIENT p
LEFT JOIN VISITA v
    ON v.id_pacient = p.id_pacient
LEFT JOIN RECEPTA r
    ON r.id_visita = v.id_visita
LEFT JOIN MEDICAMENT m
    ON m.id_medicament = r.id_medicament
LEFT JOIN INGRESS i
    ON i.id_pacient = p.id_pacient
LEFT JOIN OPERACIO o
    ON o.id_pacient = p.id_pacient
GROUP BY p.id_pacient, p.nom, p.cognoms;


-- opcional3:
CREATE OR REPLACE VIEW vista_metge_programacio AS
SELECT m.id_personal AS id_metge, m.nom, m.cognom1, m.cognom2,
    -- visites
    COUNT(DISTINCT v.id_visita) AS total_visites,
    -- operacions programades
    COUNT(DISTINCT o.id_operacio) AS total_operacions
FROM METGE m
LEFT JOIN VISITA v
    ON v.id_metge = m.id_personal
LEFT JOIN OPERACIO o
    ON o.id_metge = m.id_personal
GROUP BY m.id_personal, m.nom, m.cognom1, m.cognom2;
