import tkinter as tk
from tkinter import messagebox

def obrir_menu(rol):    # funció per obrir el menú segons el rol de l'usuari
    f = tk.Toplevel()   # nova finestra
    f.title("Menú Hospital")    # títol de la finestra
    f.geometry("300x200")   # mida

    if rol == "admin":  # menú per Administrador
        tk.Label(f, text="Admin").pack()
        tk.Button(f, text="Gestió usuaris").pack()
        tk.Button(f, text="Consultes").pack()

    elif rol == "usuari":   # menú per Usuari normal
        tk.Label(f, text="Usuari").pack()
        tk.Button(f, text="Veure visites").pack()

    else:   # control d'error si el rol no és correcte
        messagebox.showerror("Error", "Rol incorrecte")