def alta_personal(conn, tipus, dades, dades_tipus, asignat):
    with conn.cursor() as cur:
        try:
            # Ejemplo llamando a un procedimiento o insert directo
            query = """
            INSERT INTO dades_per.PERSONAL (nom, cognom1, cognom2, dni, data_naixament, baixa, telefon, email, direccio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_personal
            """
            id_nou = cur.fetchone()[0]
            cur.execute(query, dades)
            conn.commit()
            dades_tipus = id_nou + dades_tipus
            
            if tipus == "metge":
                query = """
                INSERT INTO dades_per.METGE (id_personal, especialitat, curriculum, num_colegiat)
                VALUES (%s, %s, %s, %s)
                """
                cur.execute(query, dades_tipus)
                conn.commit()

            elif tipus == "infermer_metge":
                query = """
                INSERT INTO dades_per.INFERMER (id_personal, torn, experiencia)
                VALUES (%s, %s, %s)
                """
                cur.execute(query, dades_tipus)

                query = """
                INSERT INTO dades_per.INFERMER_METGE (id_infermer, id_metge)
                VALUES (%s, %s)
                """
                cur.execute(query, (id_nou, asignat))
                conn.commit()


            elif tipus == "infermer_planta":
                query = """
                INSERT INTO dades_per.METGE (id_personal, especialitat, curriculum, num_colegiat)
                VALUES (%s, %s, %s, %s)
                """
                
                query = """
                INSERT INTO dades_per.INFERMER_PLANTA (id_infermer, id_planta)
                VALUES (%s, %s)
                """
                cur.execute(query, (id_nou, asignat))
                conn.commit()

            elif tipus == "vari":
                query = """
                INSERT INTO dades_per.vari (id_personal, tipus_feina, horari)
                VALUES (%s, %s, %s)
                """
                cur.execute(query, dades_tipus)
                conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Error en l'alta: {e}")

def alta_pacient(conn, dades):
    with conn.cursor() as cur:
        try:
            query = """
            INSERT INTO pacient.PACIENT (nom, cognoms, telefon, email, dni, data_naixament, tarjeta_sanitaria) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(query, dades)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)