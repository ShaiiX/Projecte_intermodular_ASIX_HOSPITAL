SELECT per.id_personal, per.nom, per.cognoms, COUNT(v.id_visita) AS total_pacients
FROM pacient.visita v
INNER JOIN dades_per.personal per
    ON per.id_personal = v.id_metge
GROUP BY per.id_personal, per.nom, per.cognoms
ORDER BY total_pacients DESC;