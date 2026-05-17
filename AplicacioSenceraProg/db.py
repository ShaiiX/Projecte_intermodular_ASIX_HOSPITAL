import psycopg2  # connectar a la bd de postgres
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
# usuari i password genèrics (només per al login inicial)
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# sessió activa: es guarda l'usuari i contrasenya un cop fa login
sessio = {
    "usuari": None,
    "contrasenya": None
}

def iniciar_sessio(usuari, contrasenya):
    """Guarda les credencials de l'usuari que ha fet login."""
    sessio["usuari"] = usuari
    sessio["contrasenya"] = contrasenya

def tancar_sessio():
    """Neteja les credencials en tancar sessió."""
    sessio["usuari"] = None
    sessio["contrasenya"] = None

def connectar():
    """Connecta a PostgreSQL amb l'usuari de sessió activa.
    Si no hi ha sessió, utilitza l'usuari genèric del .env."""
    try:
        usuari = sessio["usuari"] or DB_USER
        contrasenya = sessio["contrasenya"] or DB_PASSWORD

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=usuari,
            password=contrasenya
        )
        with conn.cursor() as cur:
            cur.execute("SET LOCAL app.usuari_actiu TO %s", (usuari,))
            cur.close()
        return conn
    except Exception as e:
        messagebox.showerror("Error BD", f"No s'ha pogut connectar:\n{e}")
        return None

def connectar_generic():
    """Connecta sempre amb l'usuari genèric del .env (per al login inicial)."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error BD", f"No s'ha pogut connectar:\n{e}")
        return None