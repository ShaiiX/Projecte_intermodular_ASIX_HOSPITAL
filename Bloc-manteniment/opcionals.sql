CREATE OR REPLACE FUNCTION pacient.reserves_habitacio(p_id_habitacio INT)
RETURNS TABLE (
    pacient_nom TEXT,
    data_ingres DATE,
    data_sortida_prevista DATE
) 
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.nom || ' ' || p.cognoms,
        i.data_ingres,
        i.data_sortida_prevista
    FROM pacient.ingres i
    INNER JOIN pacient.pacient p ON p.id_pacient = i.id_pacient
    WHERE p.id_habitacio = p_id_habitacio
    ORDER BY i.data_ingres;
END;
$$ LANGUAGE plpgsql;