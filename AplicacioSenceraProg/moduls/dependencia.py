import customtkinter as ctk
from db import connectar
import consultes
from estil import *


def menu_dependencia():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Dependència Infermeria", "460x320")
    topbar(f, "Dependència", icon="🔗", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Dependència", None)])

    c = mk_card(f)
    c.pack(fill="x", padx=20, pady=20)
    card_section(c, "Verificar dependència d'infermeria", icon="🔗")

    e = field(c, "ID Infermer/a", "Introdueix l'identificador")
    sl = status_lbl(c)

    def check():
        conn = connectar()
        res = consultes.check_dependencia_infermeria(conn, e.get().strip())
        conn.close()
        if res:
            dep = "Metge" if res["es_metge"] else "Planta"
            ok(sl, f"✓  {res['nom']} {res['cognom1']} → assignat/da a {dep}")
        else:
            err(sl, "No s'ha trobat cap resultat")

    btn_primary(c, "🔍  Verificar", check)