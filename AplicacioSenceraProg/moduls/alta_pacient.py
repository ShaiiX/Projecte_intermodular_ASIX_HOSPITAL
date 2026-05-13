import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import consultes
from .estil import *

def menu_alta_pacient():
    f = ctk.CTkToplevel()
    aplicar_estil_finestra(f, "Alta Pacient", "480x580")

    # Capçalera
    header = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=0, height=56)
    header.pack(fill="x")
    header.pack_propagate(False)
    ctk.CTkLabel(header, text="🧑‍⚕️  Alta Pacient",
                 font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
                 text_color=C["text"]).pack(side="left", padx=20, pady=16)

    # Formulari
    scroll = ctk.CTkScrollableFrame(f, fg_color=C["bg"], corner_radius=0)
    scroll.pack(fill="both", expand=True, padx=0, pady=0)

    card = frame_card(scroll)
    card.pack(fill="x", padx=24, pady=20)

    ctk.CTkLabel(card, text="Dades del pacient",
                 font=ctk.CTkFont(size=13, weight="bold"),
                 text_color=C["sub"]).pack(anchor="w", padx=20, pady=(16, 4))

    separator(card).pack(fill="x", padx=20, pady=(0, 12))

    camps = [
        ("Nom", "Nom del pacient"),
        ("Cognoms", "Cognoms complets"),
        ("Telèfon", "Ex: 612345678"),
        ("Email", "exemple@correu.cat"),
        ("DNI", "Ex: 12345678A"),
        ("Data Naixement", "YYYY-MM-DD"),
        ("Targeta Sanitària", "Ex: XXXX1234567890"),
    ]
    entries = []
    for label, placeholder in camps:
        ctk.CTkLabel(card, text=label,
                     font=ctk.CTkFont(size=12),
                     text_color=C["sub"]).pack(anchor="w", padx=20, pady=(6, 0))
        e = entry_estilitzat(card, placeholder=placeholder, width=400)
        e.pack(padx=20, pady=(2, 4))
        entries.append(e)

    # Missatge d'estat
    status = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12), text_color=C["accent3"])
    status.pack(pady=(4, 0))

    def guardar():
        dades = [e.get().strip() for e in entries]
        if any(d == "" for d in dades):
            status.configure(text="⚠️  Tots els camps són obligatoris", text_color=C["accent4"])
            return
        try:
            conn = connectar()
            consultes.alta_pacient_db(conn, dades)
            conn.close()
            status.configure(text="✅  Pacient donat d'alta correctament", text_color=C["accent3"])
            for e in entries:
                e.delete(0, "end")
        except Exception as ex:
            status.configure(text=f"❌  Error: {ex}", text_color=C["danger"])

    boto_primari(card, "💾  Guardar pacient", guardar, width=400).pack(padx=20, pady=16)