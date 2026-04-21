GRANT SELECT, INSERT, UPDATE ON pacient.VISITA TO infermer_role;
GRANT SELECT, INSERT, UPDATE ON pacient.PROVA TO infermer_role;
GRANT SELECT, INSERT, UPDATE ON pacient.OPERACIO TO infermer_role;

-- assignar
GRANT SELECT, INSERT, UPDATE ON dades_per.INFERMER TO infermer_role;

-- llegir dades pacient
GRANT SELECT ON pacient.PACIENT TO infermer_role;
GRANT SELECT ON pacient.INGRES TO infermer_role;
GRANT SELECT ON pacient.EXPEDIENT TO infermer_role;
