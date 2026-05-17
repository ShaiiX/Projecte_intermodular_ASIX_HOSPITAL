import psycopg2
from psycopg2.extras import RealDictCursor

# consultes per a customtkinter

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

# altes

def alta_pacient_db(conn, d):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO pacient.PACIENT (nom, cognoms, telefon, email, dni, data_naixement, tarjeta_sanitaria) VALUES (%s,%s,%s,%s,%s,%s,%s)", d)
        conn.commit()

def alta_personal_db(conn, dades_comuns, tipus, dades_especifiques):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO dades_per.PERSONAL (nom, cognom1, cognom2, dni, data_naixement, telefon, email, direccio) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id_personal", dades_comuns)
        id_nou = cur.fetchone()[0]
        if tipus == "metge":
            dades_especifiques.insert(0, id_nou) 
            query = """
            INSERT INTO dades_per.METGE (id_personal, especialitat, curriculum, num_colegiat)
            VALUES (%s, %s, %s, %s)
            """
            cur.execute(query, dades_especifiques)
            conn.commit()

        elif tipus == "infermer_metge":
            asignat = dades_especifiques.pop()
            dades_especifiques[1] = int(dades_especifiques[1])
            dades_especifiques.insert(0, id_nou) 
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
            asignat = dades_especifiques.pop()
            dades_especifiques[1] = int(dades_especifiques[1])
            dades_especifiques.insert(0, id_nou) 
            query = """
            INSERT INTO dades_per.INFERMER (id_personal, torn, experiencia)
            VALUES (%s, %s, %s)
            """
            cur.execute(query, dades_especifiques)

            query = """
            INSERT INTO dades_per.INFERMER_PLANTA (id_infermer, id_planta)
            VALUES (%s, %s)
            """
            cur.execute(query, (id_nou, asignat))
            conn.commit()

        elif tipus == "vari":
            dades_especifiques.insert(0, id_nou) 
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
        cur.execute("SELECT * FROM pacient.vista_ingressos_habitacio WHERE id_habitacio = %s", (id_hab,))
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

# informes

def informe_planta(conn, id_planta):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
            SELECT p.num_planta,
                    COUNT(DISTINCT h.id_habitacio)  AS total_habitacions,
                    COUNT(DISTINCT q.num_quirofan)   AS total_quirofans,
                    COUNT(DISTINCT inf.id_infermer) AS total_infermeria
            FROM estructura.planta p
            LEFT JOIN estructura.habitacio h   ON h.id_planta  = p.id_planta
            LEFT JOIN estructura.quirofan q    ON q.id_planta  = p.id_planta
            LEFT JOIN dades_per.infermer_planta inf ON inf.id_planta = p.id_planta
            WHERE p.id_planta = %s
            GROUP BY p.num_planta
        """
        cur.execute(query, (id_planta,))
        return cur.fetchone()

def informe_personal(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
            SELECT id_personal, nom, cognom1, cognom2, dni, data_naixement, baixa, telefon, email, direccio
            FROM dades_per.personal
            ORDER BY cognom1, cognom2, nom
        """
        cur.execute(query)
        return cur.fetchall()

def informe_visites_dia(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
            SELECT DATE(data) AS dia, COUNT(*) AS total_visites
            FROM pacient.visita
            GROUP BY DATE(data)
            ORDER BY dia DESC
        """
        cur.execute(query)
        return cur.fetchall()

def ranking_metges(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
            SELECT per.id_personal, per.nom, per.cognom1, per.cognom2,
                    COUNT(v.id_visita) AS total_pacients
            FROM pacient.visita v
            INNER JOIN dades_per.personal per ON per.id_personal = v.id_metge
            GROUP BY per.id_personal, per.nom, per.cognom1, per.cognom2
            ORDER BY total_pacients DESC
        """
        cur.execute(query)
        return cur.fetchall()

####

def exportar_visites(conn, data_inici, data_final):

    with conn.cursor() as cur:

        query = """
        SELECT
            v.id_visita,

            DATE(v.data) AS dia,

            p.dni,
            p.nom,
            p.cognoms,
            p.tarjeta_sanitaria,

            per.nom AS nom_metge,
            per.cognom1,

            m.especialitat

        FROM pacient.visita v

        JOIN pacient.pacient p
            ON v.id_pacient = p.id_pacient

        JOIN dades_per.metge m
            ON v.id_metge = m.id_personal

        JOIN dades_per.personal per
            ON m.id_personal = per.id_personal

        WHERE DATE(v.data)
        BETWEEN %s AND %s

        ORDER BY v.data
        """

        cur.execute(query, (data_inici, data_final))

        return cur.fetchall()
    