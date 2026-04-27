import customtkinter as ctk  # llibreria grafica principal

# imports de cada módulo separado
from moduls.alta_personal import menu_alta_personal
from moduls.alta_pacient import menu_alta_pacient
from moduls.dependencia import menu_dependencia
from moduls.operacions import menu_operacions
from moduls.visites import menu_visites
from moduls.inventari import menu_inventari
from moduls.habitacio import menu_habitacio
from moduls.historial import menu_historial
from moduls.programacio_metges import menu_programacio_metges


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