SELECT p.nom_planta, COUNT(DISTINCT h.id_habitacio) AS total_habitacions,
    COUNT(DISTINCT q.id_quirofan) AS total_quirofans,
    COUNT(DISTINCT per.id_personal) AS total_infermeria
FROM hospital.planta p

LEFT JOIN hospital.habitacio h 
    ON h.id_planta = p.id_planta
LEFT JOIN hospital.quirofan q
    ON q.id_planta = p.id_planta
LEFT JOIN dades_per.personal per
    ON per.id_planta = p.id_planta
    AND per.carrec = 'Infermeria'
WHERE p.id_planta = 1
GROUP BY p.nom_planta;