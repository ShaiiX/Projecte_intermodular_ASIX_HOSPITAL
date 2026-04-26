def mostrar_inventari(conn, id_q=None):
    with conn.cursor() as cur:
        if id_q:
            # Inventari d'un quiròfan específic
            query = "SELECT * FROM estructura.vista_inventari_quirofans WHERE id_quirofan = %s"
            cur.execute(query, (id_q,))
        else:
            # Inventari de tots els quiròfans
            query = "SELECT * FROM estructura.vista_inventari_quirofans ORDER BY num_quirofan"
            cur.execute(query)
            
        resultats = cur.fetchall()
