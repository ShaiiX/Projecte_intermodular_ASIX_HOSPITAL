import customtkinter as ctk  # llibreria grafica principal
from tkinter import messagebox  # finestres de missatge
from db import connectar  # connexió amb la base de dades
import consultes  # funcions de consulta i insercio


def menu_alta_pacient():
    # obre el formulari per donar d'alta un pacient
    f = ctk.CTkToplevel()
    # posa el titol de la finestra
    f.title("Alta Pacient")
    # defineix la mida del formulari
    f.geometry("400x500")

    # desa les referencies als camps del formulari
    entries = []
    # noms dels camps a omplir
    labels = ["Nom", "Cognoms", "Telèfon", "Email", "DNI", "Data Naixement", "Targeta"]

    # crea tots els camps necessaris per al nou pacient
    for l in labels:
        # crea l'etiqueta visible del camp
        ctk.CTkLabel(f, text=l).pack()
        # crea el camp editable
        e = ctk.CTkEntry(f)
        e.pack()
        entries.append(e)

    def guardar():
        # desa el pacient amb les dades introduides
        conn = connectar()
        # envia totes les dades recollides
        consultes.alta_pacient(conn, [e.get() for e in entries])
        conn.close()
        # confirma que el registre s'ha completat
        messagebox.showinfo("OK", "Creat")

    # boto per guardar el nou pacient
    ctk.CTkButton(f, text="Guardar", command=guardar).pack()