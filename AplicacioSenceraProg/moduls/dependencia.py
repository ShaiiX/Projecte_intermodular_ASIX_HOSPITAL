import customtkinter as ctk
from db import connectar
import consultes


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