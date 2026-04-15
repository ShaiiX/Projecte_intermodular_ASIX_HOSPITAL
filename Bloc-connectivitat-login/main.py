import customtkinter as ctk # interfície gràfica més moderna que tkinter
from tkinter import messagebox  # per mostrar missatges d'error o informació
import funcions # importar funcions
import menu #importar el menu per obrir despres del login
import time # per gestionar el cooldown i bloqueig de login
import config # configuració global (mode clar/oscur)

# configuració visual amb customtkinter
ctk.set_appearance_mode(config.mode_app)    # mode clar o fosc segons config
ctk.set_default_color_theme("blue") # tema blau per defecte

intents_inici_sessio = {}   # guarda intents fallits per usuari
bloqueig_inici_sessio = {}  # guarda el temps de bloqueig per usuari
timer_actiu = False         # controla si el countdown està actiu

# variable per mostrar/ocultar contrasenya
mostrar_contrasenya = False

# finestra principal de login
app = ctk.CTk()
app.title("Hospital - Login")   # titol
app.geometry("600x520") # mida

# frame principal que conté tots els elements del login
frame = ctk.CTkFrame(app, corner_radius=25) # bores arredonides
frame.pack(pady=60, padx=60, fill="both", expand=True)  # centrat i amb espai al voltant

# etiqueta del títol
titol = ctk.CTkLabel(
    frame,
    text="Hospital Login",  # text que es mostra
    font=ctk.CTkFont(size=32, weight="bold")    # font més gran i en negreta
)
titol.pack(pady=(30, 20))   # espai entre el títol i els inputs

# input usuari
entry_user = ctk.CTkEntry(
    frame,
    placeholder_text="Usuari",  # text dins del camp quan està buit
    width=320,
    height=45,
    corner_radius=12,
    font=ctk.CTkFont(size=16)
)
entry_user.pack(pady=10)

# input contrasenya
entry_pass = ctk.CTkEntry(
    frame,
    placeholder_text="Contrasenya",
    show="*",   # oculta el text amb asteriscs
    width=320,
    height=45,
    corner_radius=12,
    font=ctk.CTkFont(size=16)
)
entry_pass.pack(pady=10)

# funció per mostrar o ocultar la contrasenya
def toggle_contrasenya():
    global mostrar_contrasenya

    if not mostrar_contrasenya:
        entry_pass.configure(show="")
        btn_toggle.configure(text="Amagar")
        mostrar_contrasenya = True
    else:
        entry_pass.configure(show="*")
        btn_toggle.configure(text="Mostrar")
        mostrar_contrasenya = False

# botó per mostrar/ocultar contrasenya
btn_toggle = ctk.CTkButton(
    frame,
    text="Mostrar",
    width=90,
    height=30,
    corner_radius=8,
    command=toggle_contrasenya
)
btn_toggle.pack(pady=(0, 10))

# botó per canviar mode (clar / fosc)
def canviar_mode():
    if config.mode_app == "light":  # si el mode actual és clar canvia a fosc
        config.mode_app = "dark"    
    else:
        config.mode_app = "light"

    ctk.set_appearance_mode(config.mode_app)

btn_mode = ctk.CTkButton(   # botó per canviar el mode
    frame,
    text="Canviar mode",
    width=120,
    height=30,
    corner_radius=8,
    command=canviar_mode
)
btn_mode.pack(pady=5)

# etiqueta per mostrar missatges dins la mateixa finestra del login
status_label = ctk.CTkLabel(
    frame,
    text="",    # inicialment està buit
    font=ctk.CTkFont(size=14),
    text_color="red"
)
status_label.pack(pady=5)


# cooldown
def actualitzar_countdown(nom_usuari):
    global timer_actiu  # modifica la variable global per controlar el timer

    # si ja no hi ha bloqueig
    if nom_usuari not in bloqueig_inici_sessio:
        timer_actiu = False # es desactiva el timer
        return

    temps_restants = int(bloqueig_inici_sessio[nom_usuari] - time.time())   # calcula el temps restant del bloqueig

    if temps_restants <= 0:
        # desbloqueig automàtic
        del bloqueig_inici_sessio[nom_usuari]   # es treu el bloqueig
        intents_inici_sessio[nom_usuari] = 0    # es reinicien els intents
        status_label.configure(text="Pots tornar a intentar login", text_color="green") # missatge de desbloqueig
        timer_actiu = False # es desactiva el timer
        return

    # actualitzar text cada segon
    status_label.configure(
        text=f"Bloquejat: espera {temps_restants} segons",  # mostra el temps restant del bloqueig
        text_color="red"
    )

    # repetir cada segon
    app.after(1000, lambda: actualitzar_countdown(nom_usuari))


def login():    # funció que s'executa quan clica el botó de login
    global timer_actiu

    # obtenir els valors dels inputs
    nom_usuari = entry_user.get()
    contrasenya = entry_pass.get()

    # cooldown i bloqueig per evitar atacs de força bruta
    if nom_usuari in bloqueig_inici_sessio:
        actualitzar_countdown(nom_usuari)
        return

    resultat = funcions.proces_login(nom_usuari, contrasenya)

    if resultat == "buit":  # control si els camps estan buits
        status_label.configure(text="Camps buits", text_color="orange")
        return

    if resultat:    # si el login és correcte
        # reiniciar intents
        intents_inici_sessio[nom_usuari] = 0

        status_label.configure(text="Login correcte", text_color="green")

        funcions.guardar_login_fitxer(nom_usuari, contrasenya)
        app.withdraw()
        menu.obrir_menu(resultat)

    else:
        # sumar intent fallit
        intents_inici_sessio[nom_usuari] = intents_inici_sessio.get(nom_usuari, 0) + 1
        intents_restants = 10 - intents_inici_sessio[nom_usuari]

        # si arriba a 10 intents es bloqueja durant 2 minuts
        if intents_inici_sessio[nom_usuari] >= 10:
            bloqueig_inici_sessio[nom_usuari] = time.time() + 120
            actualitzar_countdown(nom_usuari)
        else:
            status_label.configure(
                text=f"Login incorrecte. Et queden {intents_restants} intents",
                text_color="red"
            )

# funció registre
def registre():
    # obtenir les dades dels inputs
    nom_usuari = entry_user.get()
    contrasenya = entry_pass.get()

    if funcions.proces_registre(nom_usuari, contrasenya):
        messagebox.showinfo("OK", "Usuari creat")
    else:
        messagebox.showerror("Error", "Error al registrar")

# botó per iniciar sessió
btn_login = ctk.CTkButton(
    frame,
    text="Iniciar sessió",
    command=login,
    width=320,
    height=45,
    corner_radius=12,
    font=ctk.CTkFont(size=16, weight="bold")
)
btn_login.pack(pady=10)

# executar app
app.mainloop()