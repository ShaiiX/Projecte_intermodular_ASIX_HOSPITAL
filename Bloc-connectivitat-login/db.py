import psycopg2 # connectar a la bd de postgres
from tkinter import messagebox

def connectar():    # connectar a la bd de PostgreSQL
    try:
        conn = psycopg2.connect(    # es crea la connexió
            host="localhost",
            database="hospital",
            user="postgres",
            password="postgres"
        )
        return conn # retorna la connexió
    except Exception as e:  # si hi ha error mostra un missatge
        messagebox.showerror("Error BD", f"No s'ha pogut connectar:\n{e}")
        return None
