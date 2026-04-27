import customtkinter as ctk
from db import connectar
import consultes


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