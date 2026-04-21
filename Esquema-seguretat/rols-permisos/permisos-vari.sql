GRANT USAGE ON SCHEMA pacient TO vari_role;
GRANT USAGE ON SCHEMA estructura TO vari_role;
GRANT USAGE ON SCHEMA cantina TO vari_role;

GRANT SELECT ON pacient.PACIENT TO vari_role;
GRANT SELECT ON pacient.INGRES TO vari_role;
GRANT SELECT ON estructura.HABITACIO TO vari_role;
GRANT ALL ON cantina.EMPRESA_EXTERNA TO vari_role;
GRANT ALL ON cantina.FACTURACIO_CANTINA TO vari_role;