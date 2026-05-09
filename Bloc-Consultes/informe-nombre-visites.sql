SELECT DATE(data_visita) AS dia, COUNT(*) AS total_visites
FROM pacient.visita
GROUP BY DATE(data_visita);