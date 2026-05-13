import customtkinter as ctk
from db import connectar
import consultes
from estil import *


def menu_habitacio():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Habitacions", "580x480")
    topbar(f, "Habitacions", icon="🛏️", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Habitacions", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    c = mk_card(body)
    c.pack(fill="x")
    card_section(c, "Consulta per habitació", icon="🛏️")
    e = field(c, "ID Habitació", "Introdueix l'identificador")
    sl = status_lbl(c)

    box = textbox(body, width=540, height=220)
    box.pack(pady=(12, 0))

    def cercar():
        box.delete("1.0", "end")
        try:
            res = consultes.consultar_opcional_habitacio(connectar(), e.get().strip())
            if not res:
                ok(sl, "No hi ha ingressos actius per aquesta habitació"); return
            ok(sl, f"✓  {len(res)} ingrés/os trobats")
            for r in res:
                box.insert("end", f"Pacient: {r.get('pacient','—')}  |  Entrada: {r.get('data_ingres','—')}\n")
        except Exception as ex:
            err(sl, str(ex))

    btn_primary(c, "🔍  Consultar", cercar)