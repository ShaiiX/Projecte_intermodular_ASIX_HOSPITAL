CREATE OR REPLACE FUNCTION trg_auditoria()
RETURNS TRIGGER AS $$
DECLARE
    comanda_completa TEXT := current_query(); -- comanda sql completa
BEGIN
    INSERT INTO LOG_ACCESS (
        id_registre, 
        taula_affectada, 
        accio, 
        data, 
        posicio_log
    )
    VALUES (
        NEW.id, --id del registre afectat       
        TG_TABLE_NAME, --tabla afectada      
        TG_OP, --accio del usuari
        now(), --data
        pg_backend_pid() --PID del registre del log, que servira com a identificador de la comanda completa
    );

    -- Guardem el registre de la comanda completa, s'afegeix sol el PID.
    RAISE LOG 'AUDIT_FULL_COMMAND: %', comanda_completa;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;