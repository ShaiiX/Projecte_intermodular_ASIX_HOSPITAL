--Funcio del trigger
CREATE OR REPLACE FUNCTION fn_auditoria_completa()
RETURNS TRIGGER AS $$
DECLARE
    v_query_id BIGINT; --identificador de la query que s'utilitzara per identificar la query i comprovar si es repeteix o no
    v_query_text TEXT; --la query completa
BEGIN
    -- 1. Intentar capturar la estructura de la consulta desde el motor de Postgres
    SELECT queryid, query 
    INTO v_query_id, v_query_text
    FROM pg_stat_statements
    WHERE query = current_query() 
    LIMIT 1;

    -- 2. "Plan B": Si la consulta es muy reciente y no aparece en las estadísticas, 
    -- generamos un ID basado en el hash del texto.
    IF v_query_id IS NULL THEN
        v_query_id := hashtext(current_query());
        v_query_text := current_query();
    END IF;

    -- 3. Registrar la estructura en la librería (solo si no existe ya)
    INSERT INTO QUERY_LIBRARY (query_id, query_text)
    VALUES (v_query_id, v_query_text)
    ON CONFLICT (query_id) DO NOTHING;

    -- 4. Registrar el movimiento en el log de accesos
    -- Caso DELETE: Usamos los datos viejos (OLD)
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO LOG_ACCESS (id_registre, taula_afectada, accio, query_id, detalles_datos)
        VALUES (OLD.id, TG_TABLE_NAME, TG_OP, v_query_id, 'ESBORRAT: ' || OLD::text);
    
    -- Caso UPDATE: Mostramos el cambio de OLD a NEW
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO LOG_ACCESS (id_registre, taula_afectada, accio, query_id, detalles_datos)
        VALUES (NEW.id, TG_TABLE_NAME, TG_OP, v_query_id, 'CANVI: ' || OLD::text || ' -> ' || NEW::text);
    
    -- Caso INSERT: Guardamos los datos nuevos (NEW)
    ELSE
        INSERT INTO LOG_ACCESS (id_registre, taula_afectada, accio, query_id, detalles_datos)
        VALUES (NEW.id, TG_TABLE_NAME, TG_OP, v_query_id, 'NOU: ' || NEW::text);
    END IF;

    RETURN NULL; -- Al ser un trigger AFTER, el retorno no afecta a la operación
END;
$$ LANGUAGE plpgsql;

-- exemple de incorporar el trigger a una taula en concret
CREATE TRIGGER trg_auditoria_pacientes
AFTER INSERT OR UPDATE OR DELETE ON pacientes
FOR EACH ROW EXECUTE FUNCTION fn_auditoria_completa();