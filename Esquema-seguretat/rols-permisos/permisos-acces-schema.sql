-- revoke de tot
REVOKE ALL ON SCHEMA seguretat FROM PUBLIC;
REVOKE ALL ON SCHEMA estructura FROM PUBLIC;
REVOKE ALL ON SCHEMA dades_per FROM PUBLIC;
REVOKE ALL ON SCHEMA pacient FROM PUBLIC;
REVOKE ALL ON SCHEMA cantina FROM PUBLIC;

-- permisos schemas
GRANT USAGE ON SCHEMA seguretat TO admin_role;
GRANT USAGE ON SCHEMA estructura TO admin_role;
GRANT USAGE ON SCHEMA dades_per TO admin_role;
GRANT USAGE ON SCHEMA pacient TO admin_role;
GRANT USAGE ON SCHEMA cantina TO admin_role;

-- metge
GRANT USAGE ON SCHEMA pacient TO metge_role;
GRANT USAGE ON SCHEMA dades_per TO metge_role;
GRANT USAGE ON SCHEMA estructura TO metge_role;

-- infermer
GRANT USAGE ON SCHEMA pacient TO pacient_role;
GRANT USAGE ON SCHEMA dades_per TO pacient_role;
GRANT USAGE ON SCHEMA estructura TO pacient_role;

-- vari
GRANT USAGE ON SCHEMA pacient TO vari_role;

-- pacient
GRANT USAGE ON SCHEMA pacient TO pacient_role;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA pacient TO admin_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA dades_per TO admin_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA cantina TO admin_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA estructura TO admin_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA seguretat TO admin_role;

GRANT SELECT ON pacient.vista_operacions_detallades TO admin_role;
GRANT SELECT ON pacient.vista_visites_detallades TO admin_role;
GRANT SELECT ON estructura.vista_inventari_quirofans TO admin_role;
GRANT SELECT ON pacient.vista_ingressos_habitacio TO admin_role;
GRANT SELECT ON pacient.vista_pacient_historial TO admin_role;
GRANT SELECT ON dades_per.vista_metge_programacio TO admin_role;

ALTER ROLE admin_role CREATEROLE;

CREATE OR REPLACE FUNCTION dades_per.crear_rol(nom text, pwd text, rol text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER  -- se ejecuta como el dueño de la función (postgres)
AS $$
BEGIN
    EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', nom, pwd);
    EXECUTE format('GRANT %I TO %I', rol, nom);
END;
$$;

CREATE OR REPLACE FUNCTION dades_per.actualitzar_contrasenya(nom text, nova_pwd text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    EXECUTE format('ALTER ROLE %I WITH PASSWORD %L', nom, nova_pwd);
END;
$$;