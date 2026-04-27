import customtkinter as ctk  # llibreria grafica principal
from tkinter import messagebox  # finestres de missatge
from db import connectar  # connexio amb la base de dades
import consultes  # funcions de consulta i insercio
from tkcalendar import DateEntry  # selector visual de dates


def obrir_manteniment():
    # crea la finestra principal del bloc de manteniment
    app = ctk.CTk()
    # assigna el titol de la finestra
    app.title("Bloc de Manteniment")
    # fixa una mida base per al menu
    app.geometry("500x600")

    # mostra el titol superior del menu
    ctk.CTkLabel(app, text="Bloc de Manteniment", font=("Arial", 24, "bold")).pack(pady=20)

    # relaciona cada boto amb la seva funcio
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
        # crea i col loca cada boto dins la finestra
        ctk.CTkButton(app, text=text, width=300, command=cmd).pack(pady=10)

    # inicia el bucle visual del menu
    app.mainloop()


def menu_alta_personal():
    # obre el formulari per donar d'alta nou personal
    f = ctk.CTkToplevel()
    # posa nom a la finestra emergent
    f.title("Alta Personal")
    # defineix l'espai disponible del formulari
    f.geometry("900x500")

    # separa les dades comunes de les dades especifiques
    left = ctk.CTkFrame(f)
    left.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    # allotja els camps variables segons el tipus
    right = ctk.CTkFrame(f)
    right.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    # titol de la seccio esquerra
    ctk.CTkLabel(left, text="Dades Personals", font=("Arial", 16, "bold")).pack(pady=10)

    # noms dels camps comuns del formulari
    labels = [
        "Nom", "Cognom1", "Cognom2", "DNI",
        "Data Nasc (YYYY-MM-DD)", "Tel", "Email", "Direcció"
    ]
    # guardara els inputs creats
    entries_comuns = []

    # crea els camps comuns per a qualsevol tipus de personal
    for l in labels:
        ctk.CTkLabel(left, text=l).pack()
        e = ctk.CTkEntry(left, width=250)
        e.pack(pady=2)
        entries_comuns.append(e)

    # titol de la seccio dreta
    ctk.CTkLabel(right, text="Tipus de Personal", font=("Arial", 16, "bold")).pack(pady=10)

    # conte els camps extra que canvien dinamcament
    extra_frame = ctk.CTkFrame(right)
    extra_frame.pack(pady=10)

    # desa els inputs extra creats
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
            # posa l'etiqueta del camp
            ctk.CTkLabel(extra_frame, text=c).pack()
            # crea l'entrada de text corresponent
            e = ctk.CTkEntry(extra_frame, width=220)
            e.pack(pady=2)
            extra_entries.append(e)

    # selector per escollir el tipus de personal
    selector = ctk.CTkOptionMenu(
        right,
        values=["Metge", "Infermer Planta","Infermer Metge", "Vari/Administratiu"],
        command=canvi_tipus
    )
    # fixa el tipus inicial visible
    selector.set("Metge")
    # col loca el selector a la dreta
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

        # intenta donar d'alta el personal
        res = consultes.alta_personal_completa(conn, tipus, comuns, extras)

        # tanca la connexio un cop acabat
        conn.close()

        if res is True:
            # informa que l'alta ha anat be
            messagebox.showinfo("Èxit", "Personal donat d'alta correctament")
            # tanca la finestra si tot es correcte
            f.destroy()
        else:
            # mostra el motiu de l'error
            messagebox.showerror("Error", str(res))

    # boto final per desar el formulari
    ctk.CTkButton(right, text="Guardar", fg_color="green", command=guardar).pack(pady=20)

def menu_habitacio():
    # mostra la informació d'una habitacio i els seus ingressos
    f = ctk.CTkToplevel()
    # defineix la mida de la finestra
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
            # escriu cada registre trobat
            box.insert("end", f"Pacient: {r['pacient']} | Entrada: {r['data_ingres']}\n")

    # boto per executar la consulta
    ctk.CTkButton(f, text="Consultar Opcional", command=cercar).pack()


def menu_historial():
    # consulta l'historial resumit d'un pacient
    f = ctk.CTkToplevel()
    # defineix la mida de la finestra
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
            # mostra el resum en diverses linies
            box.insert(
                "end",
                f"PACIENT: {r['nom']} {r['cognoms']}\n"
                f"Visites: {r['total_visites']}\n"
                f"Diagnostics: {r['diagnostics']}"
            )

    # boto per carregar l'historial
    ctk.CTkButton(f, text="Veure Historial", command=cercar).pack()


def menu_programacio_metges():
    # ensenya la carrega de treball de cada metge
    f = ctk.CTkToplevel()
    # titol de la finestra
    f.title("Programació de Metges")
    # mida de la finestra
    f.geometry("600x450")

    # text explicatiu de la consulta
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
            # missatge si la consulta no torna files
            box.insert("end", "No hi ha dades.")
        else:
            for m in dades:
                # mostra un resum per cada metge
                box.insert("end", f"{m['nom']} {m['cognom1']} | {m['total_visites']} | {m['total_operacions']}\n")

        conn.close()

    # boto per refrescar la informacio
    ctk.CTkButton(f, text="Actualitzar", command=cargar).pack()


def menu_visites():
    # consulta les visites programades per a una data concreta
    f = ctk.CTkToplevel()
    # posa el titol de la finestra
    f.title("Visites")
    # fixa la mida de la pantalla
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
            # escriu cada visita en una linia
            box.insert("end", f"{r['hora_entrada']} | {r['pacient']} | {r['metge']}\n")

        conn.close()

    # boto per carregar les visites
    ctk.CTkButton(f, text="Consultar", command=executar).pack()


def menu_operacions():
    # consulta les operacions previstes per a una data concreta
    f = ctk.CTkToplevel()
    # posa el titol de la finestra
    f.title("Operacions")
    # fixa la mida de la pantalla
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
            # escriu cada operacio en una linia
            box.insert("end", f"{r['hora']} | {r['quirofan']} | {r['pacient']}\n")

        conn.close()

    # boto per carregar les operacions
    ctk.CTkButton(f, text="Consultar", command=executar).pack()


def menu_inventari():
    # mostra l'inventari d'aparells per quirofan
    f = ctk.CTkToplevel()
    # posa el titol de la finestra
    f.title("Inventari")
    # fixa la mida de la finestra
    f.geometry("600x400")

    # caixa on es carrega l'inventari
    box = ctk.CTkTextbox(f, width=550, height=300)
    box.pack(pady=20)

    # obté les dades directament en obrir la finestra
    conn = connectar()
    res = consultes.consultar_inventari(conn)

    # escriu cada registre dins del quadre de text
    for r in res:
        # mostra les dades principals de cada aparell
        box.insert("end", f"{r['num_quirofan']} | {r['nom_aparell']} | {r['marca']} | {r['quantitat']}\n")

    # tanca la connexio quan ja no cal
    conn.close()


def menu_dependencia():
    # comprova de qui depen un membre d'infermeria
    f = ctk.CTkToplevel()
    # posa el titol de la finestra
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
            # mostra si depen d'un metge o d'una planta
            lbl.configure(text=f"{res['nom']} → {'Metge' if res['es_metge'] else 'Planta'}")
        else:
            # informa si no existeix cap resultat
            lbl.configure(text="No trobat")

        conn.close()

    # boto per llançar la comprovacio
    ctk.CTkButton(f, text="Verificar", command=check).pack()


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
