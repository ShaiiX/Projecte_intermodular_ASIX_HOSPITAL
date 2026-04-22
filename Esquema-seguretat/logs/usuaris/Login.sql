SELECT id_usuari
INTO usuari
FROM seguretat.USUARI
WHERE nom_usuari = usuari

INSERT INTO seguretat.LOG_ACCESS (accio, data, id_usuari) 
VALUES ('LOGIN', NOW(), usuari);

UPDATE seguretat.USUARI
SET actiu = True, ultima_activitat = NOW()
WHERE id_usuari = usuari