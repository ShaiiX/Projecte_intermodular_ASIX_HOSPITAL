import customtkinter as ctk
from tkinter import messagebox
import funcions
import menu

# configuració visual
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# finestra principal
app = ctk.CTk()
app.title("Hospital - Login")
app.geometry("400x350")
app.resizable(False, False)

# frame principal
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=40, padx=40, fill="both", expand=True)

# títol
titol = ctk.CTkLabel(
    frame,
    text="Hospital Login",
    font=ctk.CTkFont(size=20, weight="bold")
)
titol.pack(pady=(20, 20))

# input usuari
entry_user = ctk.CTkEntry(
    frame,
    placeholder_text="Usuari",
    width=200
)
entry_user.pack(pady=10)

# input contrasenya
entry_pass = ctk.CTkEntry(
    frame,
    placeholder_text="Contrasenya",
    show="*",
    width=200
)
entry_pass.pack(pady=10)

# funció login
def login():
    nom_usuari = entry_user.get()
    contrasenya = entry_pass.get()
    resultat = funcions.proces_login(nom_usuari, contrasenya)

    if resultat == "buit":
        messagebox.showwarning("Error", "Camps buits")
        return

    if resultat:
        messagebox.showinfo("OK", "Login correcte")
        funcions.guardar_login_fitxer(nom_usuari, contrasenya)
        app.withdraw()  # amagar login
        menu.obrir_menu(resultat)
    else:
        messagebox.showerror("Error", "Login incorrecte")

# funció registre
def registre():
    nom_usuari = entry_user.get()
    contrasenya = entry_pass.get()

    if funcions.proces_registre(nom_usuari, contrasenya):
        messagebox.showinfo("OK", "Usuari creat")
    else:
        messagebox.showerror("Error", "Error al registrar")

# botó login
btn_login = ctk.CTkButton(
    frame,
    text="Iniciar sessió",
    command=login,
    width=200
)
btn_login.pack(pady=(15, 5))

# botó registre
btn_register = ctk.CTkButton(
    frame,
    text="Registrar",
    command=registre,
    width=200,
    fg_color="gray"
)
btn_register.pack(pady=5)

# executar app
app.mainloop()