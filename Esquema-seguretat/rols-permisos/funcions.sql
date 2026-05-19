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

REVOKE EXECUTE ON FUNCTION dades_per.crear_rol(text, text) FROM PUBLIC;

GRANT EXECUTE ON FUNCTION dades_per.crear_rol(text, text) TO admin_role;



CREATE OR REPLACE FUNCTION dades_per.actualitzar_contrasenya(nom text, nova_pwd text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    EXECUTE format('ALTER ROLE %I WITH PASSWORD %L', nom, nova_pwd);
END;
$$;

REVOKE EXECUTE ON FUNCTION dades_per.actualitzar_contrasenya(text, text) FROM PUBLIC;

GRANT EXECUTE ON FUNCTION dades_per.actualitzar_contrasenya(text, text) TO admin_role;