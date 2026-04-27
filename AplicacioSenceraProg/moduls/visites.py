import customtkinter as ctk
from tkcalendar import DateEntry
from db import connectar
import consultes


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