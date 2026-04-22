-- Aquest codi es de exemple, com s'incorporara dins del py a l'hora del boto de logoff.
UPDATE seguretat.USUARI SET actiu = FALSE WHERE id = idusuari;
INSERT INTO seguretat.LOG_ACCESS (accio, data, id_usuari) VALUES ('LOGOFF_VOLUNTARI', NOW(), idusuari);