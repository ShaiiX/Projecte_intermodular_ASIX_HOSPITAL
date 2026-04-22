-- Usuaris
-- Contrasenya 8 asteriscs
SECURITY LABEL FOR anon ON COLUMN seguretat.usuari.contrasenya 
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    contrasenya,
    anon.dummy_filled_string(8, ''*'')
)';

-- Personal
-- DNI: XXXXXXXX + 3 últims
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.dni
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    dni,
    anon.partial(0, ''XXXXXXXX'', 3)
)';

-- Direcció: ocult
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.direccio
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    direccio,
    ''DADA PROTEGIDA''
)';

-- Telefon: format parcial
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.telefon
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    telefon,
    anon.partial(3, ''-XXXX'', 0)
)';

-- Pacient
-- DNI i targeta sanitària (parcial)
SECURITY LABEL FOR anon ON COLUMN pacient.pacient.dni
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    dni,
    anon.partial(0, ''XXXXXXXX'', 3)
)';

SECURITY LABEL FOR anon ON COLUMN pacient.pacient.tarjeta_sanitaria
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    tarjeta_sanitaria,
    anon.partial(4, ''-XXXX-XXXX'', 0)
)';

SECURITY LABEL FOR anon ON COLUMN pacient.pacient.telefon
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    telefon,
    anon.partial(3, ''-XXXX'', 0)
)';

-- Expedient i visita
-- Historial, observacions i diagnòstic
SECURITY LABEL FOR anon ON COLUMN pacient.expedient.historial
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    historial,
    ''ACCÉS RESTRINGIT A PERSONAL MÈDIC''
)';

SECURITY LABEL FOR anon ON COLUMN pacient.expedient.observacions
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    observacions,
    ''---''
)';

SECURITY LABEL FOR anon ON COLUMN pacient.visita.diagnostic
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    diagnostic,
    ''CONFIDENCIAL''
)';