CREATE OR REPLACE FUNCTION pacient.validar_ingres_dates()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.data_sortida_real IS NOT NULL AND NEW.data_sortida_real < NEW.data_ingres THEN
        RAISE EXCEPTION 'Error la data de sortida real no pot ser anterior a la data d''ingrés';
    END IF;
    
    IF NEW.data_sortida_prevista IS NOT NULL AND NEW.data_sortida_prevista < NEW.data_ingres THEN
        RAISE EXCEPTION 'Error, data prevista de sortida no pot ser anterior a la data d''ingrés';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_validar_ingres
BEFORE INSERT OR UPDATE ON pacient.ingres
FOR EACH ROW
EXECUTE FUNCTION pacient.validar_ingres_dates();

-- validació de que no hi hagi dues operacions al mateix quiofan el mateix dia
CREATE OR REPLACE FUNCTION ppacient.validar_quirofan_ocu()
RETURNS TRIGGER AS $$
BEGIN
    SELECT COUNT(*) INTO existeix
    FROM pacient.operacio
    WHERE id_quirofan = NEW.id_quirofan
        AND data = NEW.data;

    IF existeix > 0 THEN
        RAISE EXCEPTION 'Error, el quiròfan està ocupat a aquesta data';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_validar_operacio
BEFORE INSERT ON pacient.operacio
FOR EACH ROW
EXECUTE FUNCTION pacient.validar_quirofan_ocu();
