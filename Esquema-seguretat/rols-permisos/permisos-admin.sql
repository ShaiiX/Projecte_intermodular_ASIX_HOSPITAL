-- té control total
GRANT USAGE ON SCHEMA seguretat TO admin_role;
GRANT USAGE ON SCHEMA estructura TO admin_role;
GRANT USAGE ON SCHEMA dades_per TO admin_role;
GRANT USAGE ON SCHEMA pacient TO admin_role;
GRANT USAGE ON SCHEMA cantina TO admin_role;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA seguretat TO admin_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA estructura TO admin_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dades_per TO admin_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA pacient TO admin_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cantina TO admin_role;

GRANT INSERT, SELECT, UPDATE, DELETE ON seguretat.LOG_ACCESS TO admin_role;
