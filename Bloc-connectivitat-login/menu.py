import tkinter as tk
from tkinter import messagebox

def obrir_menu(rol):
    f = tk.Toplevel()
    f.title("Menú Hospital")
    f.geometry("300x200")

    if rol == "admin":
        tk.Label(f, text="Admin").pack()
        tk.Button(f, text="Gestió usuaris").pack()
        tk.Button(f, text="Consultes").pack()

    elif rol == "usuari":
        tk.Label(f, text="Usuari").pack()
        tk.Button(f, text="Veure visites").pack()

    else:
        messagebox.showerror("Error", "Rol incorrecte")