import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import alta
import consultes
from tkcalendar import DateEntry
import tkinter as tk

# menu principal
def obrir_manteniment():
    app = ctk.CTk()
    app.title("Bloc de Manteniment")
    app.geometry("500x500")

    ctk.CTkLabel(app, text="Bloc de Manteniment", 
                 font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
    # botons a submenús
    ctk.CTkButton(app, text="Alta Personal", width=250,
                  command=menu_alta_personal).pack(pady=10)
    ctk.CTkButton(app, text="Alta Pacient", width=250,
                  command=menu_alta_pacient).pack(pady=10)
    ctk.CTkButton(app, text="Dependència Infermeria", width=250,
                  command=menu_dependencia).pack(pady=10)
    ctk.CTkButton(app, text="Operacions per dia", width=250,
                  command=menu_operacions).pack(pady=10)
    ctk.CTkButton(app, text="Visites per dia", width=250,
                  command=menu_visites).pack(pady=10)
    ctk.CTkButton(app, text="Reserves Habitació", width=250,
                  command=menu_habitacio).pack(pady=10)

    app.mainloop()

# submenus

# alta personal
def menu_alta_personal():
    f = ctk.CTkToplevel()
    f.title("Alta Personal")
    f.geometry("400x500")

    entries = []
    labels = ["Nom", "Cognom1", "Cognom2", "DNI", "Data Naixement", "Telèfon", "Email", "Direcció"]

    for l in labels:
        ctk.CTkLabel(f, text=l).pack()
        e = ctk.CTkEntry(f)
        e.pack(pady=2)
        entries.append(e)
    tipus = ctk.CTkOptionMenu(f, values=["metge", "infermer_metge", "infermer_planta", "vari"])
    tipus.pack(pady=10)

    def guardar():
        conn = connectar()
        dades = [e.get() for e in entries]
        alta.alta_personal(conn, tipus.get(), dades, (), None)
        messagebox.showinfo("OK", "Personal creat")
    ctk.CTkButton(f, text="Guardar", command=guardar).pack(pady=20)

# alta pacient
def menu_alta_pacient():
    f = ctk.CTkToplevel()
    f.title("Alta Pacient")
    f.geometry("400x500")

    entries = []
    labels = ["Nom", "Cognoms", "Telèfon", "Email", "DNI", "Data Naixement", "Targeta Sanitària"]

    for l in labels:
        ctk.CTkLabel(f, text=l).pack()
        e = ctk.CTkEntry(f)
        e.pack(pady=2)
        entries.append(e)

    def guardar():
        conn = connectar()
        dades = [e.get() for e in entries]
        alta.alta_pacient(conn, dades)
        messagebox.showinfo("OK", "Pacient creat")
    ctk.CTkButton(f, text="Guardar", command=guardar).pack(pady=20)

# dependencia infermeria
def menu_dependencia():
    f = ctk.CTkToplevel()
    f.title("Dependència Infermeria")
    f.geometry("300x200")

    entry = ctk.CTkEntry(f, placeholder_text="ID Infermer")
    entry.pack(pady=20)

    def consultar():
        conn = connectar()
        consultes.check_dependencia_infermeria(conn, entry.get())
    ctk.CTkButton(f, text="Consultar", command=consultar).pack()

# operacions
def menu_operacions():
    f = ctk.CTkToplevel()
    f.title("Operacions")
    f.geometry("500x400")

    # selecionar data
    ctk.CTkLabel(
        f,
        text="Selecciona data:",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=8)

    cal = DateEntry(f, date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)
    box = ctk.CTkTextbox(f)
    box.pack(fill="both", expand=True)

    def consultar():
        conn = connectar()
        box.delete("1.0", "end")

        data = cal.get_date()  # obtenir data seleccionada

        with conn.cursor() as cur:
            cur.execute("""
                SELECT * 
                FROM pacient.vista_operacions_detallades 
                WHERE dia = %s
            """, (data,))
            
            for r in cur.fetchall():
                box.insert("end", str(r) + "\n")

    ctk.CTkButton(f, text="Consultar", command=consultar).pack(pady=10)

# visites
def menu_visites():
    f = ctk.CTkToplevel()
    f.title("Visites")
    f.geometry("500x400")

    ctk.CTkLabel(
        f,
        text="Selecciona data:",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=8)   # seleccionar data

    cal = DateEntry(f, date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)
    box = ctk.CTkTextbox(f)
    box.pack(fill="both", expand=True)

    def consultar():
        conn = connectar()
        box.delete("1.0", "end")
        data = cal.get_date()
        dades = consultes.carregar_visites_del_dia(conn, data)

        for v in dades:
            box.insert("end", f"{v}\n")

    ctk.CTkButton(f, text="Consultar", command=consultar).pack(pady=10)

# habitacions
def menu_habitacio():
    f = ctk.CTkToplevel()
    f.title("Reserves Habitació")
    f.geometry("500x400")

    entry = ctk.CTkEntry(f, placeholder_text="ID Habitació")
    entry.pack(pady=10)
    box = ctk.CTkTextbox(f)
    box.pack(fill="both", expand=True)
