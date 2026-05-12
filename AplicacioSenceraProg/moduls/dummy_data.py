import random
import threading
from datetime import datetime, timedelta
from tkinter import messagebox

import customtkinter as ctk
from psycopg2.extras import execute_values

from db import connectar


PACIENTS = 50000
VISITES = 100000
METGES = 100
INFERMERS = 200
NETEJA = 100
ADMINISTRACIO = 50


# llistes per generar dades coherents sense dependre sempre de Faker
NOMS = [
    "Marc", "Júlia", "Pau", "Laia", "Nil", "Aina", "Arnau", "Martina",
    "Pol", "Carla", "Biel", "Clàudia", "Jan", "Ona", "Joel", "Nora"
]
COGNOMS = [
    "Garcia", "Martínez", "López", "Sánchez", "Pérez", "González",
    "Ferrer", "Vidal", "Serra", "Rovira", "Torres", "Navarro"
]
NOMS_CIRILLICS = ["Алексей", "Мария", "Иван", "Анна", "Дмитрий", "Елена"]
COGNOMS_CIRILLICS = ["Иванов", "Петрова", "Смирнов", "Кузнецова", "Попов"]
ESPECIALITATS = [
    "Medicina interna", "Cardiologia", "Pediatria", "Traumatologia",
    "Neurologia", "Dermatologia", "Oncologia", "Urgencies"
]
DIAGNOSTICS = [
    "Revisio rutinaria", "Dolor abdominal", "Control postoperatori",
    "Febre i malestar", "Seguiment tractament", "Analitica alterada",
    "Dolor toracic", "Cefalea persistent"
]
TORNS = ["Mati", "Tarda", "Nit"]


def menu_dummy_data():
    # finestra del menú especific per generar o eliminar les dades de prova
    finestra = ctk.CTkToplevel()
    finestra.title("Dummy Data")
    finestra.geometry("520x360")

    ctk.CTkLabel(
        finestra,
        text="Dummy Data",
        font=("Arial", 24, "bold")
    ).pack(pady=(25, 10))

    ctk.CTkLabel(
        finestra,
        text=(
            "Genera les dades mínimes de prova i els índexs necessaris.\n"
            "També pots eliminar només la informació dummy creada aquí."
        )
    ).pack(pady=10)

    estat = ctk.CTkLabel(finestra, text="Preparat")
    estat.pack(pady=15)

    def executar(tasca, missatge):
        # executem la tasca en segon pla perquè la interfície no quedi congelada
        def worker():
            try:
                finestra.after(0, lambda: estat.configure(text=missatge))
                resultat = tasca()
                finestra.after(0, lambda: estat.configure(text="Acabat correctament"))
                finestra.after(0, lambda: messagebox.showinfo("Dummy Data", resultat))
            except Exception as exc:
                finestra.after(0, lambda: estat.configure(text="Error"))
                finestra.after(0, lambda error=exc: messagebox.showerror("Error", str(error)))

        threading.Thread(target=worker, daemon=True).start()

    ctk.CTkButton(
        finestra,
        text="Generar dummy data",
        width=300,
        command=lambda: executar(generar_dummy_data, "Generant dades... pot trigar uns minuts")
    ).pack(pady=10)

    ctk.CTkButton(
        finestra,
        text="Eliminar dummy data",
        width=300,
        fg_color="#b91c1c",
        hover_color="#7f1d1d",
        command=lambda: executar(eliminar_dummy_data, "Eliminant dades dummy...")
    ).pack(pady=10)


def generar_dummy_data():
    # connexio principal a Postgresl per carregar totes les dades fictícies
    conn = connectar()
    if conn is None:
        raise RuntimeError("No s'ha pogut connectar a la base de dades")

    try:
        with conn:
            with conn.cursor() as cur:
                # creem les taules auxiliars que permeten saber què s'ha generat
                _preparar_control(cur)
                cur.execute("SELECT COUNT(*) FROM dummy_data.ids")
                if cur.fetchone()[0] > 0:
                    raise RuntimeError(
                        "Ja existeix dummy data registrada. Elimina-la abans de generar-ne de nova."
                    )
                # els index ajuden a validar rendiment en consultes grans
                _crear_indexs(cur)
                run_id = _crear_execucio(cur)

                # primer es crea el personal perquè les visites necessiten metges
                metges_ids = _crear_personal(cur, run_id, "metge", METGES, 80000000)
                infermers_ids = _crear_personal(cur, run_id, "infermer", INFERMERS, 80100000)
                _crear_personal(cur, run_id, "neteja", NETEJA, 80200000)
                _crear_personal(cur, run_id, "administracio", ADMINISTRACIO, 80300000)
                # relacionem cada infermer amb un metge de forma repartida
                _crear_dependencia_infermers(cur, infermers_ids, metges_ids)
                # després es creen pacients i visites amb claus foranes vàlides
                pacients_ids = _crear_pacients(cur, run_id)
                _crear_visites(cur, run_id, pacients_ids, metges_ids)

                # marquem l'execució com finalitzada correctament
                cur.execute(
                    """
                    UPDATE dummy_data.execucio
                    SET finalitzada = TRUE, data_fi = CURRENT_TIMESTAMP
                    WHERE id_execucio = %s
                    """,
                    (run_id,)
                )

        return (
            f"S'han creat {PACIENTS} pacients, {VISITES} visites, "
            f"{METGES} metges, {INFERMERS} infermeres, "
            f"{NETEJA} persones de neteja i {ADMINISTRACIO} d'administració."
        )
    finally:
        conn.close()


def eliminar_dummy_data():
    # elimina només les dades registrades a dummy_data.ids
    conn = connectar()
    if conn is None:
        raise RuntimeError("No s'ha pogut connectar a la base de dades")

    try:
        with conn:
            with conn.cursor() as cur:
                _preparar_control(cur)
                cur.execute("SELECT COUNT(*) FROM dummy_data.ids")
                total = cur.fetchone()[0]

                # primer borrem relacions intermèdies per evitar errors de claus foranes
                cur.execute("""
                    DELETE FROM dades_per.infermer_metge
                    WHERE id_infermer IN (
                        SELECT pk_value FROM dummy_data.ids
                        WHERE table_name = 'dades_per.personal'
                    )
                    OR id_metge IN (
                        SELECT pk_value FROM dummy_data.ids
                        WHERE table_name = 'dades_per.personal'
                    )
                """)
                # l'ordre d'esborrat respecta les dependències entre taules
                _delete_by_ids(cur, "pacient.visita", "id_visita")
                _delete_by_ids(cur, "pacient.pacient", "id_pacient")
                _delete_by_ids(cur, "dades_per.metge", "id_personal")
                _delete_by_ids(cur, "dades_per.infermer", "id_personal")
                _delete_by_ids(cur, "dades_per.vari", "id_personal")
                _delete_by_ids(cur, "dades_per.personal", "id_personal")

                cur.execute("DELETE FROM dummy_data.ids")
                cur.execute("DELETE FROM dummy_data.execucio")

        return f"S'han eliminat {total} referències dummy de la base de dades."
    finally:
        conn.close()


def _preparar_control(cur):
    # schema auxiliar per guardar execucions i IDs generats
    cur.execute("CREATE SCHEMA IF NOT EXISTS dummy_data")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dummy_data.execucio (
            id_execucio SERIAL PRIMARY KEY,
            data_inici TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_fi TIMESTAMP,
            finalitzada BOOLEAN DEFAULT FALSE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dummy_data.ids (
            id_execucio INT REFERENCES dummy_data.execucio(id_execucio) ON DELETE CASCADE,
            table_name TEXT NOT NULL,
            pk_column TEXT NOT NULL,
            pk_value INT NOT NULL,
            PRIMARY KEY (table_name, pk_column, pk_value)
        )
    """)


def _crear_indexs(cur):
    # indexs escollits per camps usats en cerques, joins i filtres
    indexs = [
        "CREATE INDEX IF NOT EXISTS idx_dummy_pacient_dni ON pacient.pacient (dni)",
        "CREATE INDEX IF NOT EXISTS idx_dummy_pacient_targeta ON pacient.pacient (tarjeta_sanitaria)",
        "CREATE INDEX IF NOT EXISTS idx_dummy_visita_data ON pacient.visita (data)",
        "CREATE INDEX IF NOT EXISTS idx_dummy_visita_pacient ON pacient.visita (id_pacient)",
        "CREATE INDEX IF NOT EXISTS idx_dummy_visita_metge ON pacient.visita (id_metge)",
        "CREATE INDEX IF NOT EXISTS idx_dummy_personal_dni ON dades_per.personal (dni)",
        "CREATE INDEX IF NOT EXISTS idx_dummy_personal_email ON dades_per.personal (email)"
    ]
    for index in indexs:
        cur.execute(index)


def _crear_execucio(cur):
    # cada generació queda identificada amb un id_execucio
    cur.execute("INSERT INTO dummy_data.execucio DEFAULT VALUES RETURNING id_execucio")
    return cur.fetchone()[0]


def _crear_personal(cur, run_id, tipus, quantitat, dni_base):
    # prepara totes les files de personal abans d'inserirles per lots
    rows = []
    for i in range(quantitat):
        nom, cognom1, cognom2 = _persona(i)
        numero = dni_base + i
        rows.append((
            nom,
            cognom1,
            cognom2,
            _dni(numero),
            f"6{numero % 100000000:08d}",
            f"{tipus}.{i:05d}@dummy.hospital.local",
            f"Carrer Dummy {i + 1}, Girona",
            _data_naixement(22, 67),
            None
        ))

    # execute_values fa insercions massives molt més ràpides que inserir una a una
    ids = execute_values(
        cur,
        """
        INSERT INTO dades_per.personal
        (nom, cognom1, cognom2, dni, telefon, email, direccio, data_naixement, baixa)
        VALUES %s
        RETURNING id_personal
        """,
        rows,
        page_size=5000,
        fetch=True
    )
    ids = [row[0] for row in ids]
    # guarda els IDs per poder eliminar aquesta dummy data després
    _registrar_ids(cur, run_id, "dades_per.personal", "id_personal", ids)

    if tipus == "metge":
        # dades específiques de la taula filla METGE
        metges = [
            (id_personal, ESPECIALITATS[i % len(ESPECIALITATS)], "Curriculum dummy", f"COL-DMY-{i:05d}")
            for i, id_personal in enumerate(ids)
        ]
        execute_values(
            cur,
            """
            INSERT INTO dades_per.metge
            (id_personal, especialitat, curriculum, num_colegiat)
            VALUES %s
            """,
            metges,
            page_size=5000
        )
        _registrar_ids(cur, run_id, "dades_per.metge", "id_personal", ids)
    elif tipus == "infermer":
        # dades específiques de la taula filla INFERMER
        infermers = [
            (id_personal, (i % 25) + 1, TORNS[i % len(TORNS)])
            for i, id_personal in enumerate(ids)
        ]
        execute_values(
            cur,
            "INSERT INTO dades_per.infermer (id_personal, experiencia, torn) VALUES %s",
            infermers,
            page_size=5000
        )
        _registrar_ids(cur, run_id, "dades_per.infermer", "id_personal", ids)
    else:
        # neteja i administració es guarden dins la taula VARI
        feina = "Neteja" if tipus == "neteja" else "Administracio"
        horari = "Dilluns-Divendres 08:00-15:00" if tipus == "administracio" else "Torns rotatius"
        varis = [(id_personal, feina, horari) for id_personal in ids]
        execute_values(
            cur,
            "INSERT INTO dades_per.vari (id_personal, tipus_feina, horari) VALUES %s",
            varis,
            page_size=5000
        )
        _registrar_ids(cur, run_id, "dades_per.vari", "id_personal", ids)

    return ids


def _crear_dependencia_infermers(cur, infermers_ids, metges_ids):
    # assigna infermers a metges de manera circular i equilibrada
    relacions = [
        (id_infermer, metges_ids[i % len(metges_ids)])
        for i, id_infermer in enumerate(infermers_ids)
    ]
    execute_values(
        cur,
        "INSERT INTO dades_per.infermer_metge (id_infermer, id_metge) VALUES %s",
        relacions,
        page_size=5000
    )


def _crear_pacients(cur, run_id):
    #genera pacients amb DNI, telèfon, email i targeta sanitària únics
    rows = []
    for i in range(PACIENTS):
        nom, cognom1, cognom2 = _persona(i)
        numero = 30000000 + i
        rows.append((
            nom,
            f"{cognom1} {cognom2}",
            _dni(numero),
            f"7{numero % 100000000:08d}",
            f"pacient.{i:05d}@dummy.hospital.local",
            _data_naixement(0, 96),
            f"TS-DMY-{i:08d}",
            None
        ))

    # inserció massiva de pacients i retorn dels ids creats
    ids = execute_values(
        cur,
        """
        INSERT INTO pacient.pacient
        (nom, cognoms, dni, telefon, email, data_naixement, tarjeta_sanitaria, id_habitacio)
        VALUES %s
        RETURNING id_pacient
        """,
        rows,
        page_size=5000,
        fetch=True
    )
    ids = [row[0] for row in ids]
    _registrar_ids(cur, run_id, "pacient.pacient", "id_pacient", ids)
    return ids


def _crear_visites(cur, run_id, pacients_ids, metges_ids):
    # les visites sempre apunten a pacients i metges existents
    ara = datetime.now()
    rows = []
    for i in range(VISITES):
        # dates repartides en els últims mesos per fer proves de filtres per data
        data = ara - timedelta(days=random.randint(0, 900), hours=random.randint(0, 23))
        rows.append((
            pacients_ids[i % len(pacients_ids)],
            metges_ids[i % len(metges_ids)],
            data,
            DIAGNOSTICS[i % len(DIAGNOSTICS)]
        ))

    # inserció massiva de visites que és la taula més gran del dummy data
    ids = execute_values(
        cur,
        """
        INSERT INTO pacient.visita
        (id_pacient, id_metge, data, diagnostic)
        VALUES %s
        RETURNING id_visita
        """,
        rows,
        page_size=5000,
        fetch=True
    )
    ids = [row[0] for row in ids]
    _registrar_ids(cur, run_id, "pacient.visita", "id_visita", ids)


def _registrar_ids(cur, run_id, table_name, pk_column, ids):
    # guarda cada clau primària creada per poder fer una neteja exacta
    rows = [(run_id, table_name, pk_column, valor) for valor in ids]
    execute_values(
        cur,
        """
        INSERT INTO dummy_data.ids
        (id_execucio, table_name, pk_column, pk_value)
        VALUES %s
        """,
        rows,
        page_size=10000
    )


def _delete_by_ids(cur, table_name, pk_column):
    # borra registres d'una taula segons els IDs guardats al control dummy
    cur.execute(
        f"""
        DELETE FROM {table_name}
        WHERE {pk_column} IN (
            SELECT pk_value
            FROM dummy_data.ids
            WHERE table_name = %s AND pk_column = %s
        )
        """,
        (table_name, pk_column)
    )


def _persona(i):
    # cada 100 registres fem servir alfabet ciríl·lic per validar UTF-8
    if i % 100 == 0:
        return (
            NOMS_CIRILLICS[(i // 100) % len(NOMS_CIRILLICS)],
            COGNOMS_CIRILLICS[(i // 100) % len(COGNOMS_CIRILLICS)],
            COGNOMS_CIRILLICS[(i // 50) % len(COGNOMS_CIRILLICS)]
        )
    return (
        NOMS[i % len(NOMS)],
        COGNOMS[i % len(COGNOMS)],
        COGNOMS[(i * 3) % len(COGNOMS)]
    )


def _dni(numero):
    # calcula la lletra del DNI a partir del número
    lletres = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{numero:08d}{lletres[numero % 23]}"


def _data_naixement(edat_min, edat_max):
    # retorna una data de naixement coherent dins del rang d'edat indicat
    dies = random.randint(edat_min * 365, edat_max * 365)
    return (datetime.now() - timedelta(days=dies)).date()
