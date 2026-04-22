--usuari.contrasenya
--es fara que la contrasenya cada que es fa select es mostri com a 8 caracters de *
SECURITY LABEL FOR anon ON COLUMN usuaris.contrasenya 
IS 'MASKED WITH FUNCTION anon.dummy_filled_string(8, ''*'')';

-- personal.dni 
--es mostrara els 3 ultims caracters del dni 
SECURITY LABEL FOR anon ON COLUMN personal.dni
IS 'MASKED WITH FUNCTION anon.anon.partial(0,'XXXXXXXX',3)';

-- personal.direccio
--es mostrara els 3 ultims caracters del dni 
SECURITY LABEL FOR anon ON COLUMN personal.dni
IS 'MASKED WITH FUNCTION anon.anon.partial(0,'XXXXXXXX',3)';

-- personal.telefon
-- pacient.dni 
-- pacient.tarjeta_sanitaria
-- pacient.telefon
-- expedient.historial
-- expedient.observacions
-- visita.diagnostic