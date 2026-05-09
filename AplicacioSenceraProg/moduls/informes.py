import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import consultes

def menu_informes():
    conn = connectar()
    app = ctk.CTkToplevel()
    app.title("Informes")
    app.geometry("700x600")
    app.attributes("-topmost", True)
    conn = connectar()
    box = ctk.CTkTextbox(app, width=650, height=500)
    box.pack(pady=20)
    

    def mostrar(text):
        box.delete("1.0", "end")
        box.insert("end", text)

    def informe_planta():
        dades = consultes.informe_planta(conn, 1)
        txt = f"""
Planta: {dades['nom_planta']}
Habitacions: {dades['total_habitacions']}
Quirofans: {dades['total_quirofans']}
Infermeria: {dades['total_infermeria']}
"""
        mostrar(txt)

    def informe_personal():
        dades = consultes.informe_personal(conn)
        txt = ""

        for p in dades:
            txt += f"""
ID: {p['id_personal']}
Nom: {p['nom']} {p['cognom1']}
Telefon: {p['telefon']}
Email: {p['email']}
"""
        mostrar(txt)

    def informe_visites():
        dades = consultes.informe_visites_dia(conn, "2026-05-09")
        txt = f"Total visites del dia: {dades['total_visites']}"
        mostrar(txt)

    def ranking():
        dades = consultes.ranking_metges(conn)
        txt = ""

        for m in dades:
            txt += f"""
{m['nom']} {m['cognom1']}
Visites: {m['total_visites']}

"""
        mostrar(txt)

    ctk.CTkButton(app, text="Informe Planta", command=informe_planta).pack(pady=5)
    ctk.CTkButton(app,text="Informe Personal", command=informe_personal).pack(pady=5)
    ctk.CTkButton(app, text="Informe Visites", command=informe_visites).pack(pady=5)
    ctk.CTkButton(app, text="Ranking Metges", command=ranking).pack(pady=5)

