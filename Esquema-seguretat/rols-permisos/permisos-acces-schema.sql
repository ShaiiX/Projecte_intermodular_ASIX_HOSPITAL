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

