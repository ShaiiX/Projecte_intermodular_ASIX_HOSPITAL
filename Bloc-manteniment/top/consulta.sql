CREATE OR REPLACE VIEW estructura.vista_inventari_quirofans AS
SELECT 
    q.id_quirofan,
    q.num_quirofan,
    t.tipus AS nom_aparell,
    t.marca,
    COUNT(a.id_aparell) AS quantitat
FROM estructura.QUIROFAN q
JOIN estructura.APARELL_MEDIC a ON q.id_planta = a.id_planta AND q.num_quirofan = a.num_quirofan
JOIN estructura.TIPUS t ON a.id_tipus = t.id_tipus
GROUP BY q.id_quirofan, q.num_quirofan, t.tipus, t.marca;