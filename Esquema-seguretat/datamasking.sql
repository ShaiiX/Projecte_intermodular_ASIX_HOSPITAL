--- USUARIS ---
-- Contrasenya: 8 asteriscos
SECURITY LABEL FOR anon ON COLUMN usuaris.contrasenya 
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    contrasenya,
    anon.dummy_filled_string(8, ''*'')
)';

--- PERSONAL ---
-- DNI: XXXXXXXX + 3 últimos
SECURITY LABEL FOR anon ON COLUMN personal.dni
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    dni,
    anon.partial(0, ''XXXXXXXX'', 3)
)';

-- Direcció: Oculta con texto genérico
SECURITY LABEL FOR anon ON COLUMN personal.direccio
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    direccio,
    ''DADA PROTEGIDA''
)';

-- Telèfon: Formato parcial
SECURITY LABEL FOR anon ON COLUMN personal.telefon
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    telefon,
    anon.partial(3, ''-XXXX'', 0)
)';

--- PACIENT ---
-- DNI y Tarjeta Sanitaria
SECURITY LABEL FOR anon ON COLUMN pacient.dni
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    dni,
    anon.partial(0, ''XXXXXXXX'', 3)
)';

SECURITY LABEL FOR anon ON COLUMN pacient.tarjeta_sanitaria
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    tarjeta_sanitaria,
    anon.partial(4, ''-XXXX-XXXX'', 0)
)';

SECURITY LABEL FOR anon ON COLUMN pacient.telefon
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    telefon,
    anon.partial(3, ''-XXXX'', 0)
)';

--- EXPEDIENT I VISITA ---
-- Historial, Observacions y Diagnòstic
SECURITY LABEL FOR anon ON COLUMN expedient.historial
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    historial,
    ''ACCÉS RESTRINGIT A PERSONAL MÈDIC''
)';

SECURITY LABEL FOR anon ON COLUMN expedient.observacions
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    observacions,
    ''---''
)';

SECURITY LABEL FOR anon ON COLUMN visita.diagnostic
IS 'MASKED WITH FUNCTION anon.mask_if(
    NOT (pg_has_role(current_user, ''metge'', ''member'') OR pg_has_role(current_user, ''admin'', ''member'')),
    diagnostic,
    ''CONFIDENCIAL''
)';