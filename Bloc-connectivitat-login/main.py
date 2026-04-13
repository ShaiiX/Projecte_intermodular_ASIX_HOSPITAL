import customtkinter as ctk
from tkinter import messagebox
import funcions
import menu

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hospital - Login")
        self.geometry("400x350")
        self.resizable(False, False)

        # principal
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.titol = ctk.CTkLabel(  # títol
            self.frame,
            text="Hospital Login",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.titol.pack(pady=(20, 20))

        self.user = ctk.CTkEntry(   # input usuari
            self.frame,
            placeholder_text="Usuari",
            width=200
        )
        self.user.pack(pady=10)

        self.password = ctk.CTkEntry(   # input contrasenya
            self.frame,
            placeholder_text="Contrasenya",
            show="*",
            width=200
        )
        self.password.pack(pady=10)

        self.btn_login = ctk.CTkButton( # botó login
            self.frame,
            text="Iniciar sessió",
            command=self.login,
            width=200
        )
        self.btn_login.pack(pady=(15, 5))

        self.btn_register = ctk.CTkButton(  # botó registre
            self.frame,
            text="Registrar",
            command=self.register,
            width=200,
            fg_color="gray"
        )
        self.btn_register.pack(pady=5)

    def login(self):
        nom_usuari = self.user.get()
        contrasenya = self.password.get()
        result = funcions.proces_login(nom_usuari, contrasenya)

        if result == "buit":
            messagebox.showwarning("Error", "Camps buits")
            return

        if result:
            messagebox.showinfo("OK", "Login correcte")
            funcions.guardar_login_fitxer(nom_usuari, contrasenya)
            menu.obrir_menu(result)
        else:
            messagebox.showerror("Error", "Login incorrecte")

    def register(self):
        nom_usuari = self.user.get()
        contrasenya = self.password.get()
        if funcions.proces_registre(nom_usuari, contrasenya):
            messagebox.showinfo("OK", "Usuari creat")
        else:
            messagebox.showerror("Error", "Error al registrar")

# executar
app = App()
app.mainloop()