def check_dependencia_infermeria(conn, id_personal_inf):
    with conn.cursor() as cur:
        query = """
        SELECT 
            p.nom, p.cognom1,
            EXISTS(SELECT 1 FROM seguretat.INFERMER_METGE WHERE id_personal = %s) as es_de_metge,
            EXISTS(SELECT 1 FROM seguretat.INFERMER_PLANTA WHERE id_personal = %s) as es_de_planta
        FROM seguretat.PERSONAL p
        WHERE p.id_personal = %s;
        """
        cur.execute(query, (id_personal_inf, id_personal_inf, id_personal_inf))
        res = cur.fetchone()
        
        if res:
            if res['es_de_metge']:
                print(f"L'infermer/a {res['nom']} depèn directament d'un Metge.")
            else:
                print(f"L'infermer/a {res['nom']} és personal de Planta.")
def consultar_operacions_quirofan(conn, data_consulta):
    with conn.cursor() as cur:
        query = "SELECT * FROM pacient.vista_operacions_detallades WHERE dia::DATE = %s ORDER BY dia ASC;"
        cur.execute(query, (data_consulta,))
        res = cur.fetchall()
        
def carregar_visites_del_dia(conn, data_usuari):
    with conn.cursor() as cur:
        query = """
            SELECT hora_entrada, metge, pacient 
            FROM pacient.vista_visites_detallades 
            WHERE dia = %s 
            ORDER BY hora_entrada ASC;
        """
        cur.execute(query, (data_usuari,))
        visites = cur.fetchall()
