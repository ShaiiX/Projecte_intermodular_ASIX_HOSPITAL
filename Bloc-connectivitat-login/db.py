import psycopg2
from tkinter import messagebox

def connectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="hospital",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error BD", f"No s'ha pogut connectar:\n{e}")
        return None
