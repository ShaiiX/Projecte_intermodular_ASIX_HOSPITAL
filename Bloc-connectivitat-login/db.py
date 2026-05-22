import psycopg2  # connectar a la bd de postgres
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

# dades del .env
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')

# usuari genèric (login inicial)
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# sessió activa
sessio = {
    "usuari": None,
    "contrasenya": None
}

def iniciar_sessio(usuari, contrasenya):
    """Guarda les credencials de l'usuari."""
    sessio["usuari"] = usuari
    sessio["contrasenya"] = contrasenya

def tancar_sessio():
    """Neteja la sessió activa."""
    sessio["usuari"] = None
    sessio["contrasenya"] = None

def connectar():
    """
    Connecta a PostgreSQL utilitzant
    l'usuari de la sessió activa.
    Fa servir SSL.
    """
    try:
        usuari = sessio["usuari"] or DB_USER
        contrasenya = sessio["contrasenya"] or DB_PASSWORD
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=usuari,
            password=contrasenya,
            # SSL
            sslmode='require'
        )

        # guardar usuari actiu dins postgres
        with conn.cursor() as cur:
            cur.execute(
                "SET app.usuari_actiu TO %s",
                (usuari,)
            )
        conn.commit()
        return conn

    except Exception as e:
        messagebox.showerror(
            "Error BD",
            f"No s'ha pogut connectar:\n{e}"
        )
        return None


def connectar_generic():
    """
    Connexió inicial amb l'usuari genèric.
    També amb SSL.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            # SSL
            sslmode='require'
        )

        return conn

    except Exception as e:
        messagebox.showerror(
            "Error BD",
            f"No s'ha pogut connectar:\n{e}"
        )
        return None