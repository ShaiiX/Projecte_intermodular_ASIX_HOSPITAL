CREATE OR REPLACE FUNCTION pacient.validar_ingres_dates()   -- validar les dates d'un ingrés
RETURNS TRIGGER AS $$
BEGIN   -- comprovar que la data de sortida real no sigui abans a la data d'ingres
    IF NEW.data_sortida_real IS NOT NULL AND NEW.data_sortida_real < NEW.data_ingres THEN
        RAISE EXCEPTION 'Error la data de sortida real no pot ser anterior a la data d''ingrés';
    END IF;
        -- que la data de sortida prevista tampoc sigui abans a la data d'ingres
    IF NEW.data_sortida_prevista IS NOT NULL AND NEW.data_sortida_prevista < NEW.data_ingres THEN
        RAISE EXCEPTION 'Error, data prevista de sortida no pot ser anterior a la data d''ingrés';
    END IF;
    RETURN NEW; -- permet inserts i updates si es correcte
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_validar_ingres -- trigger que executa la validacio abans insert o update d'un ingres
BEFORE INSERT OR UPDATE ON pacient.ingres
FOR EACH ROW
EXECUTE FUNCTION pacient.validar_ingres_dates();

-- evitar duplicació d’operacions al mateix quiròfan i data
CREATE OR REPLACE FUNCTION pacient.validar_quirofan_ocu()
RETURNS TRIGGER AS $$
DECLARE
    existeix INT;   -- variable guardar nombre d'operacions
BEGIN
    SELECT COUNT(*) INTO existeix   -- comprova si existeix una operacio al mateix quiròfan el mateix dia
    FROM pacient.operacio
    WHERE id_quirofan = NEW.id_quirofan
        AND data = NEW.data;

    IF existeix > 0 THEN    -- si hi han una no es pot fer insert i surt error
        RAISE EXCEPTION 'Error, el quiròfan està ocupat a aquesta data';
    END IF;
    RETURN NEW; -- sino es pot inserir l'operacio
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_validar_operacio   -- trigger q valida abans d'inserir una operacio
BEFORE INSERT ON pacient.operacio
FOR EACH ROW
EXECUTE FUNCTION pacient.validar_quirofan_ocu();
