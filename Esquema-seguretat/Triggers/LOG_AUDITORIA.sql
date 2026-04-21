--Funcio del trigger
CREATE OR REPLACE FUNCTION fn_auditoria_completa()
RETURNS TRIGGER AS $$
DECLARE
    v_query_id BIGINT; --identificador de la query que s'utilitzara per identificar la query i comprovar si es repeteix o no
    v_query_text TEXT; --la query completa
BEGIN

    SELECT queryid, query 
    INTO v_query_id, v_query_text
    FROM pg_stat_statements
    WHERE query = current_query() 
    LIMIT 1;

    IF v_query_id IS NULL THEN
        v_query_id := hashtext(current_query());
        v_query_text := current_query();
    END IF;

    INSERT INTO QUERY_LIBRARY (query_id, query_text)
    VALUES (v_query_id, v_query_text)
    ON CONFLICT (query_id) DO NOTHING;


    IF (TG_OP = 'DELETE') THEN
        INSERT INTO LOG_ACCESS (id_registre, taula_afectada, accio, query_id, detalles_datos)
        VALUES (OLD.id, TG_TABLE_NAME, TG_OP, v_query_id, 'ESBORRAT: ' || OLD::text);


    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO LOG_ACCESS (id_registre, taula_afectada, accio, query_id, detalles_datos)
        VALUES (NEW.id, TG_TABLE_NAME, TG_OP, v_query_id, 'CANVI: ' || OLD::text || ' -> ' || NEW::text);


    ELSE
        INSERT INTO LOG_ACCESS (id_registre, taula_afectada, accio, query_id, detalles_datos)
        VALUES (NEW.id, TG_TABLE_NAME, TG_OP, v_query_id, 'NOU: ' || NEW::text);
    END IF;

    RETURN NULL; 
    
$$ LANGUAGE plpgsql;

-- exemple de incorporar el trigger a una taula en concret
CREATE TRIGGER trg_auditoria_pacientes
AFTER INSERT OR UPDATE OR DELETE ON pacientes
FOR EACH ROW EXECUTE FUNCTION fn_auditoria_completa();