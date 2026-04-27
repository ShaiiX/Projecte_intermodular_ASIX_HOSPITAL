import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import consultes  
from tkcalendar import DateEntry


def obrir_manteniment():
    # crea la finestra principal del bloc de manteniment
    app = ctk.CTk()
    app.title("Bloc de Manteniment")
    app.geometry("500x600")

    # mostra el titol superior del menu
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

    # genera un boto per a cada funcionalitat disponible
    for text, cmd in btns:
        ctk.CTkButton(app, text=text, width=300, command=cmd).pack(pady=10)

    app.mainloop()


def menu_alta_personal():
    # obre el formulari per donar d'alta nou personal
    f = ctk.CTkToplevel()
    f.title("Alta Personal")
    f.geometry("900x500")

    # separa les dades comunes de les dades especifiques
    left = ctk.CTkFrame(f)
    left.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    # allotja els camps variables segons el tipus
    right = ctk.CTkFrame(f)
    right.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    ctk.CTkLabel(left, text="Dades Personals", font=("Arial", 16, "bold")).pack(pady=10)

    labels = [
        "Nom", "Cognom1", "Cognom2", "DNI",
        "Data Nasc (YYYY-MM-DD)", "Tel", "Email", "Direcció"
    ]

    entries_comuns = []

    # crea els camps comuns per a qualsevol tipus de personal
    for l in labels:
        ctk.CTkLabel(left, text=l).pack()
        e = ctk.CTkEntry(left, width=250)
        e.pack(pady=2)
        entries_comuns.append(e)

    ctk.CTkLabel(right, text="Tipus de Personal", font=("Arial", 16, "bold")).pack(pady=10)

    # conte els camps extra que canvien dinamcament
    extra_frame = ctk.CTkFrame(right)
    extra_frame.pack(pady=10)

    extra_entries = []

    def netejar():
        # elimina els camps extra abans de regenerar-los
        for w in extra_frame.winfo_children():
            w.destroy()
        extra_entries.clear()

    def canvi_tipus(tipus):
        # adapta els camps segons el tipus de personal seleccionat
        netejar()

        if tipus == "Metge":
            # camps propis del personal medic
            camps = ["Especialitat", "Currículum", "Num Col·legiat"]
        elif tipus == "Infermer Planta":
            # camps per a infermeria de planta
            camps = ["Torn (M/T/N)", "Anys Experiència", "ID Planta"]
        elif tipus == "Infermer Metge":
            # camps per a infermeria associada a un metge
            camps = ["Torn (M/T/N)", "Anys Experiència", "ID Metge"]
        else:
            # camps per a personal administratiu o vari
            camps = ["Tipus Feina", "Horari"]

        # crea els nous camps visibles
        for c in camps:
            ctk.CTkLabel(extra_frame, text=c).pack()
            e = ctk.CTkEntry(extra_frame, width=220)
            e.pack(pady=2)
            extra_entries.append(e)

    # selector per escollir el tipus de personal
    selector = ctk.CTkOptionMenu(
        right,
        values=["Metge", "Infermer Planta","Infermer Metge", "Vari/Administratiu"],
        command=canvi_tipus
    )
    selector.set("Metge")
    selector.pack(pady=10)

    # carrega els camps inicials del primer tipus
    canvi_tipus("Metge")


    def guardar():
        # recull les dades i les envia a la consulta d'alta
        conn = connectar()

        # llegeix els valors introduits a la interfície
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

def menu_habitacio():
    # mostra la informació d'una habitacio i els seus ingressos
    f = ctk.CTkToplevel()
    f.geometry("500x400")
    # permet escriure l'identificador de l'habitacio
    ent = ctk.CTkEntry(f, placeholder_text="ID Habitació")
    ent.pack(pady=10)

    # zona on es mostren els resultats
    box = ctk.CTkTextbox(f, width=450, height=250)
    box.pack()

    def cercar():
        # neteja el resultat anterior i carrega les dades de l'habitacio
        box.delete("1.0", "end")
        # consulta les dades de l'habitacio indicada
        res = consultes.consultar_opcional_habitacio(connectar(), ent.get())
        for r in res:
            box.insert("end", f"Pacient: {r['pacient']} | Entrada: {r['data_ingres']}\n")

    ctk.CTkButton(f, text="Consultar Opcional", command=cercar).pack()


def menu_historial():
    # consulta l'historial resumit d'un pacient
    f = ctk.CTkToplevel()
    f.geometry("500x400")
    # camp per introduir l'id del pacient
    ent = ctk.CTkEntry(f, placeholder_text="ID Pacient")
    ent.pack(pady=10)

    # caixa de text amb la resposta
    box = ctk.CTkTextbox(f, width=450, height=250)
    box.pack()

    def cercar():
        # mostra el nombre de visites i diagnostics del pacient
        box.delete("1.0", "end")
        # recupera el resum de l'historial
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
    # ensenya la carrega de treball de cada metge
    f = ctk.CTkToplevel()
    f.title("Programació de Metges")
    f.geometry("600x450")

    ctk.CTkLabel(f, text="Càrrega de treball per Metge").pack(pady=10)

    # mostra el resum de visites i operacions
    box = ctk.CTkTextbox(f, width=550, height=300)
    box.pack()

    def cargar():
        # actualitza el llistat amb les dades de la base de dades
        box.delete("1.0", "end")
        conn = connectar()
        # demana les dades agregades dels metges
        dades = consultes.consultar_programacio_metge(conn)

        if not dades:
            box.insert("end", "No hi ha dades.")
        else:
            for m in dades:
                box.insert("end", f"{m['nom']} {m['cognom1']} | {m['total_visites']} | {m['total_operacions']}\n")

        conn.close()

    ctk.CTkButton(f, text="Actualitzar", command=cargar).pack()


def menu_visites():
    # consulta les visites programades per a una data concreta
    f = ctk.CTkToplevel()
    f.title("Visites")
    f.geometry("700x500")

    # selector de data per filtrar les visites
    cal = DateEntry(f, date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    # llistat de visites trobades
    box = ctk.CTkTextbox(f, width=650, height=300)
    box.pack()

    def executar():
        # carrega totes les visites del dia seleccionat
        box.delete("1.0", "end")
        conn = connectar()
        # consulta les visites del dia triat
        dades = consultes.carregar_visites_del_dia(conn, cal.get_date())

        for r in dades:
            box.insert("end", f"{r['hora_entrada']} | {r['pacient']} | {r['metge']}\n")

        conn.close()

    ctk.CTkButton(f, text="Consultar", command=executar).pack()


def menu_operacions():
    # consulta les operacions previstes per a una data concreta
    f = ctk.CTkToplevel()
    f.title("Operacions")
    f.geometry("750x500")

    # selector de data per filtrar les operacions
    cal = DateEntry(f, date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    # llistat d'operacions trobades
    box = ctk.CTkTextbox(f, width=700, height=300)
    box.pack()

    def executar():
        # carrega totes les operacions del dia seleccionat
        box.delete("1.0", "end")
        conn = connectar()
        # consulta les operacions del dia triat
        dades = consultes.carregar_operacions_dia(conn, cal.get_date())

        for r in dades:
            box.insert("end", f"{r['hora']} | {r['quirofan']} | {r['pacient']}\n")

        conn.close()

    ctk.CTkButton(f, text="Consultar", command=executar).pack()


def menu_inventari():
    # mostra l'inventari d'aparells per quirofan
    f = ctk.CTkToplevel()
    f.title("Inventari")
    f.geometry("600x400")

    # caixa on es carrega l'inventari
    box = ctk.CTkTextbox(f, width=550, height=300)
    box.pack(pady=20)

    # obté les dades directament en obrir la finestra
    conn = connectar()
    res = consultes.consultar_inventari(conn)

    # escriu cada registre dins del quadre de text
    for r in res:
        box.insert("end", f"{r['num_quirofan']} | {r['nom_aparell']} | {r['marca']} | {r['quantitat']}\n")

    conn.close()


def menu_dependencia():
    # comprova de qui depen un membre d'infermeria
    f = ctk.CTkToplevel()
    f.title("Dependència Infermeria")

    # camp per indicar l'identificador a comprovar
    e = ctk.CTkEntry(f)
    e.pack(pady=20)

    # etiqueta on es mostra el resultat
    lbl = ctk.CTkLabel(f, text="")
    lbl.pack()

    def check():
        # busca la dependencia i actualitza el text del resultat
        conn = connectar()
        res = consultes.check_dependencia_infermeria(conn, e.get())

        if res:
            lbl.configure(text=f"{res['nom']} → {'Metge' if res['es_metge'] else 'Planta'}")
        else:
            lbl.configure(text="No trobat")

        conn.close()

    ctk.CTkButton(f, text="Verificar", command=check).pack()


def menu_alta_pacient():
    # obre el formulari per donar d'alta un pacient
    f = ctk.CTkToplevel()
    f.title("Alta Pacient")
    f.geometry("400x500")

    # desa les referencies als camps del formulari
    entries = []

    labels = ["Nom", "Cognoms", "Telèfon", "Email", "DNI", "Data Naixement", "Targeta"]

    # crea tots els camps necessaris per al nou pacient
    for l in labels:
        ctk.CTkLabel(f, text=l).pack()
        e = ctk.CTkEntry(f)
        e.pack()
        entries.append(e)

    def guardar():
        # desa el pacient amb les dades introduides
        conn = connectar()
        consultes.alta_pacient(conn, [e.get() for e in entries])
        conn.close()
        messagebox.showinfo("OK", "Creat")

    ctk.CTkButton(f, text="Guardar", command=guardar).pack()
