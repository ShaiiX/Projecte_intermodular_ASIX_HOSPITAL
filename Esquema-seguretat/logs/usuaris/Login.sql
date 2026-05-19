SELECT id_usuari
INTO usuari
FROM seguretat.USUARI
WHERE nom_usuari = usuari

UPDATE seguretat.USUARI
SET ultima_activitat = NOW()
WHERE id_usuari = usuari