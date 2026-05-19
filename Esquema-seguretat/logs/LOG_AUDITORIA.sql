---Funcio per a l'auditoria de UPDATE, INSERT, DELETE.
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
    --- es normalitzara la query actual, on encomptes de haver-hi VALUES(1,2) son ? VALUES(?,?)
    v_query_norm := current_query();

    v_query_norm := regexp_replace(v_query_norm,
        '''[^'']*''', '?', 'g');
    v_query_norm := regexp_replace(v_query_norm,
        '\m\d+(\.\d+)?\M', '?', 'g');
    v_query_norm := regexp_replace(v_query_norm,
        '\m(true|false|null)\M', '?', 'gi');

    --- generarem el id de la query, que sera la mateixa si es repeteix la mateixa query
    v_query_id := hashtext(v_query_norm);

    --- obtenim la key o identificador de la taula on s'ha afectat el trigger
    SELECT a.attname
    INTO v_pk_col
    FROM pg_index i
    JOIN pg_attribute a ON a.attrelid = i.indrelid
                       AND a.attnum = ANY(i.indkey)
    WHERE i.indrelid = (TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME)::regclass
      AND i.indisprimary
    LIMIT 1;

    ---S'agafara el identificador de registre afectat
    IF (TG_OP = 'DELETE') THEN
        v_registre := to_jsonb(OLD);
    ELSE
        v_registre := to_jsonb(NEW);
    END IF;

    v_pk_value := v_registre ->> v_pk_col;

    --- Obtenim l'identificador de l'usuari, gracies al usuari_actiu que funciona durant l'execució de una query
    SELECT id_usuari
    INTO v_id_usuari
    FROM seguretat.USUARI
    WHERE username = COALESCE(
        current_setting('app.usuari_actiu', true),
        current_user
    )
    LIMIT 1;

    ---Guardem la query dins la llibreria, si hi ha confictes de id no l'afegira, ja que així significa que ja estaba
    INSERT INTO seguretat.LOG_LIBRARY (id_library, query_text)
    VALUES (v_query_id, v_query_norm)
    ON CONFLICT (id_library) DO NOTHING;

    --- registrem la accio de l'usuari dins del la taula de logs
    INSERT INTO seguretat.LOG_ACCESS (id_usuari, accio, data)
    VALUES (v_id_usuari, TG_OP, now())
    RETURNING id_log INTO v_id_log;

    ---Guardem els detalls dins de la taula de detalls, les dades s'indicaran com a json, facilitant l'hora de guardar i observar les dades
    ---Si l'acció e sun delete
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

    ---Si es un udpdate es mostrara de diferent forma
    ELSIF (TG_OP = 'UPDATE') THEN
        --- Només els camps que han canviat
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
    
    --- Si es un insert, que es el que queda, afegir els canvis
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