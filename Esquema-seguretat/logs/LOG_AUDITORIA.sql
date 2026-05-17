-- ============================================================
-- FUNCIÓ DEL TRIGGER D'AUDITORIA
-- ============================================================
CREATE OR REPLACE FUNCTION fn_auditoria_completa()
RETURNS TRIGGER AS $$
DECLARE
    v_query_id     BIGINT;
    v_query_norm   TEXT;
    v_id_usuari    INT;
    v_id_log       BIGINT;
    v_pk_col       TEXT;
    v_pk_value     INT;
    v_registre     JSONB;
    v_dades_noves  JSONB;
BEGIN
    -- --------------------------------------------------------
    -- 1. Normalitzar la query: substituir valors per «?»
    -- --------------------------------------------------------
    v_query_norm := current_query();

    v_query_norm := regexp_replace(v_query_norm,
        '''[^'']*''', '?', 'g');
    v_query_norm := regexp_replace(v_query_norm,
        '\m\d+(\.\d+)?\M', '?', 'g');
    v_query_norm := regexp_replace(v_query_norm,
        '\m(true|false|null)\M', '?', 'gi');

    v_query_id := hashtext(v_query_norm);

    -- --------------------------------------------------------
    -- 2. Obtenir la PK de la taula que ha disparat el trigger
    -- --------------------------------------------------------
    SELECT a.attname
    INTO v_pk_col
    FROM pg_index i
    JOIN pg_attribute a ON a.attrelid = i.indrelid
                       AND a.attnum = ANY(i.indkey)
    WHERE i.indrelid = (TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME)::regclass
      AND i.indisprimary
    LIMIT 1;

    IF (TG_OP = 'DELETE') THEN
        v_registre := to_jsonb(OLD);
    ELSE
        v_registre := to_jsonb(NEW);
    END IF;

    v_pk_value := v_registre ->> v_pk_col;

    -- --------------------------------------------------------
    -- 3. Obtenir l'usuari de l'aplicació (passat per SET LOCAL)
    --    amb fallback al usuari de PostgreSQL
    -- --------------------------------------------------------
    SELECT id_usuari
    INTO v_id_usuari
    FROM seguretat.USUARI
    WHERE username = COALESCE(
        current_setting('app.usuari_actiu', true),
        current_user
    )
    LIMIT 1;

    -- --------------------------------------------------------
    -- 4. Guardar la query normalitzada a LOG_LIBRARY
    --    (només la primera vegada que apareix aquesta estructura)
    -- --------------------------------------------------------
    INSERT INTO seguretat.LOG_LIBRARY (id_library, query_text)
    VALUES (v_query_id, v_query_norm)
    ON CONFLICT (id_library) DO NOTHING;

    -- --------------------------------------------------------
    -- 5. Registrar l'accés a LOG_ACCESS
    -- --------------------------------------------------------
    INSERT INTO seguretat.LOG_ACCESS (id_usuari, accio, data)
    VALUES (v_id_usuari, TG_OP, now())
    RETURNING id_log INTO v_id_log;

    -- --------------------------------------------------------
    -- 6. Guardar els valors concrets a LOG_DETAIL
    -- --------------------------------------------------------
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO seguretat.LOG_DETAIL (
            id_log, id_library, taula_afectada, id_registre, dades
        )
        VALUES (
            v_id_log,
            v_query_id,
            TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME,
            v_pk_value,
            to_jsonb(OLD)
        );
        RETURN OLD;

    ELSIF (TG_OP = 'UPDATE') THEN
        -- Només els camps que han canviat
        SELECT jsonb_object_agg(
            key,
            jsonb_build_object(
                'abans',   to_jsonb(OLD) -> key,
                'despres', to_jsonb(NEW) -> key
            )
        )
        INTO v_dades_noves
        FROM jsonb_each(to_jsonb(NEW)) AS n(key, value)
        WHERE to_jsonb(OLD) -> key IS DISTINCT FROM to_jsonb(NEW) -> key;

        INSERT INTO seguretat.LOG_DETAIL (
            id_log, id_library, taula_afectada, id_registre, dades
        )
        VALUES (
            v_id_log,
            v_query_id,
            TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME,
            v_pk_value,
            v_dades_noves
        );
        RETURN NEW;

    ELSE -- INSERT
        INSERT INTO seguretat.LOG_DETAIL (
            id_log, id_library, taula_afectada, id_registre, dades
        )
        VALUES (
            v_id_log,
            v_query_id,
            TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME,
            v_pk_value,
            to_jsonb(NEW)
        );
        RETURN NEW;
    END IF;

END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- exemple de incorporar el trigger a una taula en concret
CREATE TRIGGER trg_auditoria_pacientes
AFTER INSERT OR UPDATE OR DELETE ON pacient.pacient
FOR EACH ROW EXECUTE FUNCTION fn_auditoria_completa();