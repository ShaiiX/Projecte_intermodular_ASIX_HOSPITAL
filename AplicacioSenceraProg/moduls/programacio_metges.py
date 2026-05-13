import customtkinter as ctk
from db import connectar
import consultes
from estil import *


def menu_programacio_metges():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Programació Metges", "620x500")
    topbar(f, "Programació Metges", icon="📅", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Programació", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    sl = ctk.CTkLabel(body, text="", font=F_SMALL, text_color=C["muted"])
    sl.pack(anchor="w", pady=(0, 8))

    box = textbox(body, width=580, height=320)
    box.pack()

    def cargar():
        box.delete("1.0", "end")
        box.insert("end", f"{'Metge':<30}{'Visites':<12}{'Operacions'}\n")
        box.insert("end", "─" * 60 + "\n")
        try:
            conn = connectar()
            dades = consultes.consultar_programacio_metge(conn)
            conn.close()
            if not dades:
                box.insert("end", "No hi ha dades disponibles.\n")
                ok(sl, "Consulta completada — sense dades")
                return
            for m in dades:
                nom = f"{m.get('nom','')} {m.get('cognom1','')}"
                box.insert("end",
                    f"{nom:<30}{str(m.get('total_visites','0')):<12}"
                    f"{m.get('total_operacions','0')}\n")
            ok(sl, f"✓  {len(dades)} metges carregats")
        except Exception as ex:
            err(sl, str(ex))

    btn = ctk.CTkButton(body, text="🔄  Actualitzar",
                        command=cargar,
                        fg_color=C["accent"], hover_color=C["accent_h"],
                        width=200, height=38, corner_radius=9,
                        font=font(12, bold=True), text_color="#ffffff")
    btn.pack(pady=(12, 0))
    cargar()