import customtkinter as ctk  # llibreria grafica principal
from tkinter import messagebox  # finestres de missatge
from db import connectar  # connexió amb la base de dades
import consultes  # funcions de consulta i insercio


def menu_alta_personal():
    # obre el formulari per donar d'alta nou personal
    f = ctk.CTkToplevel()
    # posa nom a la finestra emergent
    f.title("Alta Personal")
    # defineix l'espai disponible del formulari
    f.geometry("700x600")

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
        values=["Metge", "Infermer Planta", "Infermer Metge", "Vari/Administratiu"],
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