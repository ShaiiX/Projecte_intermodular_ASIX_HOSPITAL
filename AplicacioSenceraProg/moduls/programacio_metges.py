import customtkinter as ctk
from db import connectar
import consultes


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