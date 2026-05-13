import customtkinter as ctk
from db import connectar
import consultes
from estil import *


def menu_historial():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Historial Pacient", "580x460")
    topbar(f, "Historial Pacient", icon="📂", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Historial", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    c = mk_card(body)
    c.pack(fill="x")
    card_section(c, "Historial del pacient", icon="📂")
    e = field(c, "ID Pacient", "Introdueix l'identificador")
    sl = status_lbl(c)

    box = textbox(body, width=540, height=200)
    box.pack(pady=(12, 0))

    def cercar():
        box.delete("1.0", "end")
        try:
            r = consultes.consultar_opcional_historial(connectar(), e.get().strip())
            if not r:
                err(sl, "Pacient no trobat"); return
            ok(sl, f"✓  Historial de {r.get('nom','')} {r.get('cognoms','')}")
            box.insert("end",
                f"Pacient:     {r.get('nom','')} {r.get('cognoms','')}\n"
                f"Visites:     {r.get('total_visites','—')}\n"
                f"Diagnòstics: {r.get('diagnostics','—')}\n")
        except Exception as ex:
            err(sl, str(ex))

    btn_primary(c, "🔍  Veure historial", cercar)