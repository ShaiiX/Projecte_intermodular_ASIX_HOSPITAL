import psycopg2
from psycopg2.extras import RealDictCursor

# --- CONSULTES PER A CUSTOMTKINTER ---

def carregar_visites_del_dia(conn, data):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM pacient.vista_visites_detallades WHERE dia = %s ORDER BY hora_entrada", (data,))
        return cur.fetchall()

def carregar_operacions_dia(conn, data):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM pacient.vista_operacions_detallades WHERE dia = %s ORDER BY hora", (data,))
        return cur.fetchall()

def consultar_inventari(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM estructura.vista_inventari_quirofans ORDER BY num_quirofan")
        return cur.fetchall()

def check_dependencia_infermeria(conn, id_inf):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
            SELECT p.nom, p.cognom1,
            EXISTS(SELECT 1 FROM dades_per.INFERMER_METGE WHERE id_infermer = %s) as es_metge,
            EXISTS(SELECT 1 FROM dades_per.INFERMER_PLANTA WHERE id_infermer = %s) as es_planta
            FROM dades_per.PERSONAL p WHERE p.id_personal = %s
        """
        cur.execute(query, (id_inf, id_inf, id_inf))
        return cur.fetchone()

# --- ALTES ---

def alta_pacient_db(conn, d):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO pacient.PACIENT (nom, cognoms, telefon, email, dni, data_naixament, tarjeta_sanitaria) VALUES (%s,%s,%s,%s,%s,%s,%s)", d)
        conn.commit()

def alta_personal_db(conn, dades_comuns, tipus, dades_especifiques, asignat):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO dades_per.PERSONAL (nom, cognom1, cognom2, dni, data_naixament, telefon, email, direccio) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id_personal", dades_comuns)
        id_nou = cur.fetchone()[0]
        if tipus == "metge":
            query = """
            INSERT INTO dades_per.METGE (id_personal, especialitat, curriculum, num_colegiat)
            VALUES (%s, %s, %s, %s)
            """
            cur.execute(query, dades_especifiques)
            conn.commit()

        elif tipus == "infermer_metge":
            query = """
            INSERT INTO dades_per.INFERMER (id_personal, torn, experiencia)
            VALUES (%s, %s, %s)
            """
            cur.execute(query, dades_especifiques)

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
            cur.execute(query, dades_especifiques)
            conn.commit()
        conn.commit()
        return id_nou

def consultar_opcional_habitacio(conn, id_hab):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM vista_ingressos_habitacio WHERE id_habitacio = %s", (id_hab,))
        return cur.fetchall()

def consultar_opcional_historial(conn, id_pac):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM vista_pacient_historial WHERE id_pacient = %s", (id_pac,))
        return cur.fetchone()
    
def consultar_programacio_metge(conn):
    """Retorna la carga de trabajo (visitas y operaciones) de cada médico."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        query = "SELECT * FROM vista_metge_programacio ORDER BY cognom1 ASC;"
        cur.execute(query)
        return cur.fetchall()   