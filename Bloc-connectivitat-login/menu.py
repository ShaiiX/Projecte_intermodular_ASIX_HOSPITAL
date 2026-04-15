import tkinter as tk
from tkinter import messagebox
import funcions # importar fiitxer de funcions

def obrir_menu(rol):    # funció per obrir el menú segons el rol de l'usuari
    f = tk.Toplevel()   # nova finestra
    f.title("Menú Hospital")    # títol de la finestra
    f.geometry("400x350")   # mida
    f.configure(bg="#f5f7fa")   # color de fons

    def tornar_login():
        f.destroy()
        f.master.deiconify()  # tornar a mostrar el login

    # frame principal per centrar contingut
    frame = tk.Frame(f, bg="#ffffff", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=260)

    # estil general
    font_titol = ("Segoe UI", 18, "bold")
    font_text = ("Segoe UI", 12)

    if rol == "admin":  # menú per Administrador
        tk.Label(frame, text="Panell Administrador", font=font_titol, bg="#ffffff").pack(pady=20)
        tk.Button(  # botó per gestionar els uusuaris (només ho pot veure l'admin)
            frame,
            text="Gestió usuaris",
            font=font_text,
            bg="#2563eb",
            fg="white",
            activebackground="#1e40af",
            relief="flat",
            bd=0,
            width=22,
            height=2,
            cursor="hand2",
            command=gestio_usuaris  # obre la finestra de gestió d'usuaris
        ).pack(pady=10)

        tk.Button(  # botó de consultes
            frame,
            text="Consultes",
            font=font_text,
            bg="#2563eb",
            fg="white",
            activebackground="#1e40af",
            relief="flat",
            bd=0,
            width=22,
            height=2,
            cursor="hand2"
        ).pack(pady=10)

    elif rol == "usuari":   # menú per Usuari normal
        tk.Label(frame, text="Panell Usuari", font=font_titol, bg="#ffffff").pack(pady=20)
        tk.Button(  # botó per veure les visites
            frame,
            text="Veure visites",
            font=font_text,
            bg="#16a34a",
            fg="white",
            activebackground="#166534",
            relief="flat",
            bd=0,
            width=22,
            height=2,
            cursor="hand2"
        ).pack(pady=15)

    else:   # control d'error si el rol no és correcte
        messagebox.showerror("Error", "Rol incorrecte")

    tk.Button(  # botó per tornar al login
        f,
        text="Tornar",
        command=tornar_login,
        bg="#e5e7eb",
        fg="black",
        relief="flat",
        font=("Segoe UI", 10),
        cursor="hand2"
    ).place(x=10, y=10)

def gestio_usuaris():   # finestra per gestionar els usuaris (només per admin)
    g = tk.Toplevel()   # nova finestra emergent
    g.title("Registrar usuari") # titol
    g.geometry("400x300")
    g.configure(bg="#f5f7fa")

    frame = tk.Frame(g, bg="#ffffff")   # frame per centrar contingut
    frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=200) # mida i posició del frame
    tk.Label(frame, text="Nou usuari", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=15) # etiqueta del títol

    entry_user = tk.Entry(frame, font=("Segoe UI", 11)) # input per nom d'usuari
    entry_user.pack(pady=8)

    entry_pass = tk.Entry(frame, show="*", font=("Segoe UI", 11))   # input per contrasenya, mostra asteriscs
    entry_pass.pack(pady=8)

    def registrar():    # funció que s'executa quan clica el botó de registrar
        nom = entry_user.get()
        pwd = entry_pass.get()
        if funcions.proces_registre(nom, pwd):  # crida a la funció de registre i mostra un missatge segons el resultat
            messagebox.showinfo("OK", "Usuari creat")
        else:
            messagebox.showerror("Error", "Error al registrar")

    tk.Button(  # botó per registrar el nou usuari
        frame,
        text="Registrar",
        command=registrar,
        bg="#2563eb",
        fg="white",
        activebackground="#1e40af",
        relief="flat",
        bd=0,
        width=20,
        height=2,
        cursor="hand2"
).pack(pady=15)