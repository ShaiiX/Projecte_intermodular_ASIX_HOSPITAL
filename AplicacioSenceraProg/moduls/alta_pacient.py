import customtkinter as ctk
from db import connectar
import consultes
from estil import *


def menu_alta_pacient():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Alta Pacient", "480x600")
    topbar(f, "Alta Pacient", icon="👤", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Alta Pacient", None)])

    scroll = ctk.CTkScrollableFrame(f, fg_color=C["bg"], corner_radius=0)
    scroll.pack(fill="both", expand=True)

    c = mk_card(scroll)
    c.pack(fill="x", padx=20, pady=20)
    card_section(c, "Dades del pacient", icon="👤")

    camps = [
        ("Nom",              "Nom del pacient"),
        ("Cognoms",          "Cognoms complets"),
        ("Telèfon",          "Ex: 612 345 678"),
        ("Email",            "exemple@correu.cat"),
        ("DNI",              "Ex: 12345678A"),
        ("Data Naixement",   "YYYY-MM-DD"),
        ("Targeta Sanitària","Ex: XXXX1234567890"),
    ]
    entries = [field(c, lbl, ph) for lbl, ph in camps]
    sl = status_lbl(c)

    def guardar():
        vals = [e.get().strip() for e in entries]
        if any(v == "" for v in vals):
            err(sl, "Tots els camps són obligatoris"); return
        print(vals)
        try:
            conn = connectar()
            consultes.alta_pacient_db(conn, vals)
            conn.close()
            ok(sl, "✓  Pacient donat d'alta correctament")
            for e in entries: e.delete(0, "end")
        except Exception as ex:
            err(sl, str(ex))

    btn_primary(c, "💾  Guardar pacient", guardar)