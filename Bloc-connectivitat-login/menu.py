import tkinter as tk
from tkinter import messagebox
import funcions

def obrir_menu(rol):    # funció per obrir el menú segons el rol de l'usuari
    f = tk.Toplevel()   # nova finestra
    f.title("Menú Hospital")    # títol de la finestra
    f.geometry("300x250")   # mida

    def tornar_login():
        f.destroy()
        f.master.deiconify()  # tornar a mostrar el login

    if rol == "admin":  # menú per Administrador
        tk.Label(f, text="Admin").pack(pady=10)
        tk.Button(f, text="Gestió usuaris", command=gestio_usuaris).pack(pady=5)
        tk.Button(f, text="Consultes").pack(pady=5)

    elif rol == "usuari":   # menú per Usuari normal
        tk.Label(f, text="Usuari").pack(pady=10)
        tk.Button(f, text="Veure visites").pack(pady=5)

    else:   # control d'error si el rol no és correcte
        messagebox.showerror("Error", "Rol incorrecte")

    tk.Button(f, text="Tornar al login", command=tornar_login).pack(pady=20)

def gestio_usuaris():
    g = tk.Toplevel()
    g.title("Registrar usuari")
    g.geometry("300x200")
    tk.Label(g, text="Nou usuari").pack(pady=10)

    entry_user = tk.Entry(g)
    entry_user.pack(pady=5)
    entry_pass = tk.Entry(g, show="*")
    entry_pass.pack(pady=5)

    def registrar():
        nom = entry_user.get()
        pwd = entry_pass.get()
        if funcions.proces_registre(nom, pwd):
            messagebox.showinfo("OK", "Usuari creat")
        else:
            messagebox.showerror("Error", "Error al registrar")
    tk.Button(g, text="Registrar", command=registrar).pack(pady=10)