import customtkinter as ctk
from db import connectar
import consultes


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