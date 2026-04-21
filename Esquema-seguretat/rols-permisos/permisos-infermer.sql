GRANT USAGE ON SCHEMA pacient TO infermer_role;
GRANT USAGE ON SCHEMA dades_per TO infermer_role;
GRANT USAGE ON SCHEMA estructura TO infermer_role;


GRANT SELECT, INSERT, UPDATE ON pacient.VISITA TO infermer_role;
GRANT SELECT, INSERT, UPDATE ON pacient.PROVA TO infermer_role;
GRANT SELECT, INSERT, UPDATE ON pacient.OPERACIO TO infermer_role;

GRANT SELECT ON pacient.PACIENT TO infermer_role;
GRANT SELECT ON pacient.EXPEDIENT TO infermer_role;
GRANT SELECT ON pacient.INGRES TO infermer_role;

GRANT SELECT, INSERT, UPDATE ON dades_per.INFERMER_OPERACIO TO infermer_role;
GRANT SELECT, INSERT, UPDATE ON dades_per.INFERMER_PLANTA TO infermer_role;
GRANT SELECT, INSERT, UPDATE ON dades_per.INFERMER_METGE TO infermer_role;