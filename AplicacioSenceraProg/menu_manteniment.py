import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import consultes  
from tkcalendar import DateEntry


def obrir_manteniment():
    app = ctk.CTk()
    app.title("Bloc de Manteniment")
    app.geometry("500x600")

    ctk.CTkLabel(app, text="Bloc de Manteniment", font=("Arial", 24, "bold")).pack(pady=20)

    btns = [
        ("Alta Personal", menu_alta_personal),
        ("Alta Pacient", menu_alta_pacient),
        ("Dependència Infermeria", menu_dependencia),
        ("Operacions per dia", menu_operacions),
        ("Visites per dia", menu_visites),
        ("Inventari Aparells", menu_inventari),
        ("Habitacions", menu_habitacio),
        ("Historial Pacient", menu_historial),
        ("Programació Metges", menu_programacio_metges)
    ]

    for text, cmd in btns:
        ctk.CTkButton(app, text=text, width=300, command=cmd).pack(pady=10)

    app.mainloop()


# =========================
# ALTA PERSONAL (FIXED)
# =========================
def menu_alta_personal():
    f = ctk.CTkToplevel()
    f.title("Alta Personal")
    f.geometry("900x500")

    # =========================
    # CONTENEDOR PRINCIPAL
    # =========================
    left = ctk.CTkFrame(f)
    left.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    right = ctk.CTkFrame(f)
    right.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    # =========================
    # DADES PERSONALS (IZQUIERDA)
    # =========================
    ctk.CTkLabel(left, text="Dades Personals", font=("Arial", 16, "bold")).pack(pady=10)

    labels = [
        "Nom", "Cognom1", "Cognom2", "DNI",
        "Data Nasc (YYYY-MM-DD)", "Tel", "Email", "Direcció"
    ]

    entries_comuns = []

    for l in labels:
        ctk.CTkLabel(left, text=l).pack()
        e = ctk.CTkEntry(left, width=250)
        e.pack(pady=2)
        entries_comuns.append(e)

    # =========================
    # TIPUS PERSONAL (DERECHA)
    # =========================
    ctk.CTkLabel(right, text="Tipus de Personal", font=("Arial", 16, "bold")).pack(pady=10)

    extra_frame = ctk.CTkFrame(right)
    extra_frame.pack(pady=10)

    extra_entries = []

    def netejar():
        for w in extra_frame.winfo_children():
            w.destroy()
        extra_entries.clear()

    def canvi_tipus(tipus):
        netejar()

        if tipus == "Metge":
            camps = ["Especialitat", "Currículum", "Num Col·legiat"]
        else:
            camps = ["Torn (M/T/N)", "Anys Experiència", "ID Planta"]

        for c in camps:
            ctk.CTkLabel(extra_frame, text=c).pack()
            e = ctk.CTkEntry(extra_frame, width=220)
            e.pack(pady=2)
            extra_entries.append(e)

    # 🔥 SELECTOR
    selector = ctk.CTkOptionMenu(
        right,
        values=["Metge", "Infermer Planta"],
        command=canvi_tipus
    )
    selector.set("Metge")
    selector.pack(pady=10)

    canvi_tipus("Metge")

    # =========================
    # GUARDAR
    # =========================
    def guardar():
        conn = connectar()

        comuns = [e.get() for e in entries_comuns]
        extras = [e.get() for e in extra_entries]
        tipus = selector.get()

        res = consultes.alta_personal_completa(conn, tipus, comuns, extras)

        conn.close()

        if res is True:
            messagebox.showinfo("Èxit", "Personal donat d'alta correctament")
            f.destroy()
        else:
            messagebox.showerror("Error", str(res))

    ctk.CTkButton(right, text="Guardar", fg_color="green", command=guardar).pack(pady=20)

#####
def menu_habitacio():
    f = ctk.CTkToplevel()
    f.geometry("500x400")
    ent = ctk.CTkEntry(f, placeholder_text="ID Habitació")
    ent.pack(pady=10)

    box = ctk.CTkTextbox(f, width=450, height=250)
    box.pack()

    def cercar():
        box.delete("1.0", "end")
        res = consultes.consultar_opcional_habitacio(connectar(), ent.get())
        for r in res:
            box.insert("end", f"Pacient: {r['pacient']} | Entrada: {r['data_ingres']}\n")

    ctk.CTkButton(f, text="Consultar Opcional", command=cercar).pack()


def menu_historial():
    f = ctk.CTkToplevel()
    f.geometry("500x400")
    ent = ctk.CTkEntry(f, placeholder_text="ID Pacient")
    ent.pack(pady=10)

    box = ctk.CTkTextbox(f, width=450, height=250)
    box.pack()

    def cercar():
        box.delete("1.0", "end")
        r = consultes.consultar_opcional_historial(connectar(), ent.get())
        if r:
            box.insert(
                "end",
                f"PACIENT: {r['nom']} {r['cognoms']}\n"
                f"Visites: {r['total_visites']}\n"
                f"Diagnostics: {r['diagnostics']}"
            )

    ctk.CTkButton(f, text="Veure Historial", command=cercar).pack()


def menu_programacio_metges():
    f = ctk.CTkToplevel()
    f.title("Programació de Metges")
    f.geometry("600x450")

    ctk.CTkLabel(f, text="Càrrega de treball per Metge").pack(pady=10)

    box = ctk.CTkTextbox(f, width=550, height=300)
    box.pack()

    def cargar():
        box.delete("1.0", "end")
        conn = connectar()
        dades = consultes.consultar_programacio_metge(conn)

        if not dades:
            box.insert("end", "No hi ha dades.")
        else:
            for m in dades:
                box.insert("end", f"{m['nom']} {m['cognom1']} | {m['total_visites']} | {m['total_operacions']}\n")

        conn.close()

    ctk.CTkButton(f, text="Actualitzar", command=cargar).pack()


def menu_visites():
    f = ctk.CTkToplevel()
    f.title("Visites")
    f.geometry("700x500")

    cal = DateEntry(f, date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    box = ctk.CTkTextbox(f, width=650, height=300)
    box.pack()

    def executar():
        box.delete("1.0", "end")
        conn = connectar()
        dades = consultes.carregar_visites_del_dia(conn, cal.get_date())

        for r in dades:
            box.insert("end", f"{r['hora_entrada']} | {r['pacient']} | {r['metge']}\n")

        conn.close()

    ctk.CTkButton(f, text="Consultar", command=executar).pack()


def menu_operacions():
    f = ctk.CTkToplevel()
    f.title("Operacions")
    f.geometry("750x500")

    cal = DateEntry(f, date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    box = ctk.CTkTextbox(f, width=700, height=300)
    box.pack()

    def executar():
        box.delete("1.0", "end")
        conn = connectar()
        dades = consultes.carregar_operacions_dia(conn, cal.get_date())

        for r in dades:
            box.insert("end", f"{r['hora']} | {r['quirofan']} | {r['pacient']}\n")

        conn.close()

    ctk.CTkButton(f, text="Consultar", command=executar).pack()


def menu_inventari():
    f = ctk.CTkToplevel()
    f.title("Inventari")
    f.geometry("600x400")

    box = ctk.CTkTextbox(f, width=550, height=300)
    box.pack(pady=20)

    conn = connectar()
    res = consultes.consultar_inventari(conn)

    for r in res:
        box.insert("end", f"{r['num_quirofan']} | {r['nom_aparell']} | {r['marca']} | {r['quantitat']}\n")

    conn.close()


def menu_dependencia():
    f = ctk.CTkToplevel()
    f.title("Dependència Infermeria")

    e = ctk.CTkEntry(f)
    e.pack(pady=20)

    lbl = ctk.CTkLabel(f, text="")
    lbl.pack()

    def check():
        conn = connectar()
        res = consultes.check_dependencia_infermeria(conn, e.get())

        if res:
            lbl.configure(text=f"{res['nom']} → {'Metge' if res['es_metge'] else 'Planta'}")
        else:
            lbl.configure(text="No trobat")

        conn.close()

    ctk.CTkButton(f, text="Verificar", command=check).pack()


def menu_alta_pacient():
    f = ctk.CTkToplevel()
    f.title("Alta Pacient")
    f.geometry("400x500")

    entries = []

    labels = ["Nom", "Cognoms", "Telèfon", "Email", "DNI", "Data Naixement", "Targeta"]

    for l in labels:
        ctk.CTkLabel(f, text=l).pack()
        e = ctk.CTkEntry(f)
        e.pack()
        entries.append(e)

    def guardar():
        conn = connectar()
        consultes.alta_pacient(conn, [e.get() for e in entries])
        conn.close()
        messagebox.showinfo("OK", "Creat")

    ctk.CTkButton(f, text="Guardar", command=guardar).pack()