import customtkinter as ctk
from tkinter import messagebox
import funcions
import menu

# configuració visual amb customtkinter
ctk.set_appearance_mode("light")    # mode clar
ctk.set_default_color_theme("blue") # tema blau per defecte

# finestra principal de login
app = ctk.CTk()
app.title("Hospital - Login")   # titol
app.geometry("400x350") # mida

# frame principal que conté tots els elements del login
frame = ctk.CTkFrame(app, corner_radius=15) # bores arredonides
frame.pack(pady=40, padx=40, fill="both", expand=True)  # centrat i amb espai al voltant

# etiqueta del títol
titol = ctk.CTkLabel(
    frame,
    text="Hospital Login",  # text que es mostra
    font=ctk.CTkFont(size=20, weight="bold")    # font més gran i en negreta
)
titol.pack(pady=(20, 20))   # espai entre el títol i els inputs

# input usuari
entry_user = ctk.CTkEntry(
    frame,
    placeholder_text="Usuari",  # text placeholder (apareix quan no s'ha escrit res)
    width=200
)
entry_user.pack(pady=10)

# input contrasenya
entry_pass = ctk.CTkEntry(
    frame,
    placeholder_text="Contrasenya",
    show="*",   # amaga el text que s'escriu amb asteriscs
    width=200
)
entry_pass.pack(pady=10)


def login():    # funció que s'executa quan clica el botó de login
    # obtenir els valors dels inputs
    nom_usuari = entry_user.get()
    contrasenya = entry_pass.get()
    resultat = funcions.proces_login(nom_usuari, contrasenya)   # crida a la funcio per validar el login

    if resultat == "buit":  # control si els camps estan buits
        messagebox.showwarning("Error", "Camps buits")
        return

    if resultat:    # si el login és correcte
        messagebox.showinfo("OK", "Login correcte")
        funcions.guardar_login_fitxer(nom_usuari, contrasenya)  # guardar el login en un fitxer amb seguretat
        app.withdraw()  # amagar finestra login
        menu.obrir_menu(resultat)   # obrir menú segons el rol de l'usuari
    else:
        messagebox.showerror("Error", "Login incorrecte")   # si el login és incorrecte es mostra un error

# funció registre
def registre():
    # obtenir les dades dels inputs
    nom_usuari = entry_user.get()
    contrasenya = entry_pass.get()

    if funcions.proces_registre(nom_usuari, contrasenya):   # crida la funció per registrar l'usuari
        messagebox.showinfo("OK", "Usuari creat")
    else:
        messagebox.showerror("Error", "Error al registrar") # sino error al registrar

# botó per iniciar sessió
btn_login = ctk.CTkButton(
    frame,
    text="Iniciar sessió",
    command=login,  # funció que s'executa al clicar
    width=200
)
btn_login.pack(pady=(15, 5))

# botó registre
btn_register = ctk.CTkButton(   # botó per registrar el nou usuari
    frame,
    text="Registrar",
    command=registre,   # funció que s'executa al clicar
    width=200,
    fg_color="gray" # color diferent per distingirlo
)
btn_register.pack(pady=5)

# executar app
app.mainloop()