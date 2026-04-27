import customtkinter as ctk
from db import connectar
import consultes


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