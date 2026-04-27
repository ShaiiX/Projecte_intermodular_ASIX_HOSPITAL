import customtkinter as ctk
from tkcalendar import DateEntry
from db import connectar
import consultes


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