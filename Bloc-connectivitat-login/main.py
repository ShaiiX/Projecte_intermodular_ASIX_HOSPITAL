import customtkinter as ctk
from tkinter import messagebox
import funcions
import menu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hospital Login")
        self.geometry("400x300")

        self.user = ctk.CTkEntry(self, placeholder_text="Usuari")
        self.user.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Contrasenya", show="*")
        self.password.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=5)
        ctk.CTkButton(self, text="Registrar", command=self.register).pack()

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


if __name__ == "__main__":
    app = App()
    app.mainloop()