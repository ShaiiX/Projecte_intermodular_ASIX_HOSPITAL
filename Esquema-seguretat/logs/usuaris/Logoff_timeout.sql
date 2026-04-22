CREATE OR REPLACE PROCEDURE tancar_sessions_expirades()
LANGUAGE plpgsql
AS $$
DECLARE
    minuts_inactivitat INTEGER := 15;
    hi_ha_actius BOOLEAN;
BEGIN
    SELECT EXISTS (SELECT 1 FROM seguretat.USUARI WHERE actiu = TRUE) 
    INTO hi_ha_actius;

    -- Si no hi ha ningú, sortim directament
    IF NOT hi_ha_actius THEN
        RETURN;
    END IF;

    INSERT INTO seguretat.LOG_ACCESS (accio, data, id_usuari)
    SELECT 'LOGOFF_TIMEOUT', NOW(), id
    FROM seguretat.USUARI 
    WHERE actiu = TRUE 
      AND ultima_activitat < (NOW() - (minuts_inactivitat || ' minutes')::INTERVAL);

    UPDATE seguretat.USUARI
    SET actiu = FALSE 
    WHERE actiu = TRUE 
      AND ultima_activitat < (NOW() - (minuts_inactivitat || ' minutes')::INTERVAL);
  
    COMMIT; 
END;
$$;
