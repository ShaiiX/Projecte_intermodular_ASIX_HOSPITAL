
SECURITY LABEL FOR anon ON COLUMN seguretat.usuari.password
IS 'MASKED WITH VALUE ''********''';

-- Personal

-- DNI: XXXXXX + 3 últims caràcters visibles
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.dni
IS 'MASKED WITH FUNCTION anon.partial(dni, 0, ''XXXXXX'', 3)';

-- Direcció: valor fix ocult
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.direccio
IS 'MASKED WITH VALUE ''DADA PROTEGIDA''';

-- Telèfon: 3 primers + màscara + res al final
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.telefon
IS 'MASKED WITH FUNCTION anon.partial(telefon, 3, ''-XXXX'', 0)';

-- Pacient

-- DNI: XXXXXX + 3 últims
SECURITY LABEL FOR anon ON COLUMN pacient.pacient.dni
IS 'MASKED WITH FUNCTION anon.partial(dni, 0, ''XXXXXX'', 3)';

-- Targeta sanitària: 4 primers + màscara
SECURITY LABEL FOR anon ON COLUMN pacient.pacient.tarjeta_sanitaria
IS 'MASKED WITH FUNCTION anon.partial(tarjeta_sanitaria, 4, ''-XXXX-XXXX'', 0)';

-- Telèfon
SECURITY LABEL FOR anon ON COLUMN pacient.pacient.telefon
IS 'MASKED WITH FUNCTION anon.partial(telefon, 3, ''-XXXX'', 0)';

-- Expedient i visita

-- Historial mèdic
SECURITY LABEL FOR anon ON COLUMN pacient.expedient.historial
IS 'MASKED WITH VALUE ''ACCÉS RESTRINGIT A PERSONAL MÈDIC''';

-- Observacions
SECURITY LABEL FOR anon ON COLUMN pacient.expedient.observacions
IS 'MASKED WITH VALUE ''---''';

-- Diagnòstic
SECURITY LABEL FOR anon ON COLUMN pacient.visita.diagnostic
IS 'MASKED WITH VALUE ''CONFIDENCIAL''';

SECURITY LABEL FOR anon ON ROLE infermer_role IS 'MASKED';
