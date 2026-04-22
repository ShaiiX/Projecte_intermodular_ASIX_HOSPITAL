CREATE OR REPLACE FUNCTION fn_tancar_sessions_expirades() 
RETURNS VOID AS $$
DECLARE
    minuts_inactivitat INTEGER := 15;
BEGIN
    INSERT INTO seguretat.LOG_ACCESS (accio, data, id_usuari)
    SELECT 'LOGOFF_TIMEOUT', NOW(), id
    FROM seguretat.USUARIS 
    WHERE is_online = TRUE 
      AND ultima_activitat < (NOW() - (minuts_inactivitat || ' minuts')::INTERVAL);

    UPDATE seguretat.USUARIS
    SET is_online = FALSE 
    WHERE is_online = TRUE 
      AND ultima_activitat < (NOW() - (minuts_inactivitat || ' minuts')::INTERVAL);
      
    RAISE NOTICE 'Sessions expirades processades correctament.';
END;
$$ LANGUAGE plpgsql;