import customtkinter as ctk
from datetime import date
from db import connectar
import consultes
from estil import *


def menu_informes():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Informes", "680x540")
    topbar(f, "Informes", icon="📊", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Informes", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    conn = connectar()

    # ── Botons selector ───────────────────────────────────────────────────
    btn_row = ctk.CTkFrame(body, fg_color="transparent")
    btn_row.pack(fill="x", pady=(0, 12))

    active_btn = [None]

    def _selector_btn(text, cmd):
        b = ctk.CTkButton(btn_row, text=text, command=lambda: _activate(b, cmd),
                          fg_color=C["card"], hover_color=C["card2"],
                          text_color=C["sub"], border_color=C["border"],
                          border_width=1, width=0, height=34, corner_radius=8,
                          font=F_SMALL)
        b.pack(side="left", padx=(0, 6))
        return b

    def _activate(b, cmd):
        if active_btn[0]:
            active_btn[0].configure(fg_color=C["card"], text_color=C["sub"],
                                    border_color=C["border"])
        b.configure(fg_color=C["card2"], text_color=C["accent"],
                    border_color=C["accent"])
        active_btn[0] = b
        cmd()

    box = textbox(body, width=640, height=330)
    box.pack()

    def _show(lines):
        box.delete("1.0", "end")
        for k, v in lines:
            box.insert("end", f"{k:<28}{v}\n")

    def informe_planta():
        try:
            d = consultes.informe_planta(conn, 1)
            _show([
                ("Planta", d.get("nom_planta","—")),
                ("Habitacions totals", str(d.get("total_habitacions","—"))),
                ("Quiròfans totals", str(d.get("total_quirofans","—"))),
                ("Personal infermeria", str(d.get("total_infermeria","—"))),
            ])
        except Exception as ex:
            _show([("Error", str(ex))])

    def informe_personal():
        try:
            dades = consultes.informe_personal(conn)
            box.delete("1.0", "end")
            box.insert("end", f"{'ID':<8}{'Nom':<28}{'Telèfon':<18}{'Email'}\n")
            box.insert("end", "─" * 76 + "\n")
            for p in dades:
                box.insert("end",
                    f"{str(p.get('id_personal','')):<8}"
                    f"{p.get('nom','')+' '+p.get('cognom1',''):<28}"
                    f"{str(p.get('telefon','')):<18}"
                    f"{p.get('email','')}\n")
        except Exception as ex:
            _show([("Error", str(ex))])

    def informe_visites():
        try:
            d = consultes.informe_visites_dia(conn, date.today().isoformat())
            _show([("Total visites avui", str(d.get("total_visites","—")))])
        except Exception as ex:
            _show([("Error", str(ex))])

    def ranking():
        try:
            dades = consultes.ranking_metges(conn)
            box.delete("1.0", "end")
            box.insert("end", f"{'#':<5}{'Metge':<30}{'Visites'}\n")
            box.insert("end", "─" * 50 + "\n")
            for i, m in enumerate(dades, 1):
                nom = f"{m.get('nom','')} {m.get('cognom1','')}"
                box.insert("end", f"{i:<5}{nom:<30}{m.get('total_visites','0')}\n")
        except Exception as ex:
            _show([("Error", str(ex))])

    btns_def = [
        ("🏢  Informe Planta", informe_planta),
        ("👥  Personal",       informe_personal),
        ("📋  Visites avui",   informe_visites),
        ("🏆  Rànquing Metges",ranking),
    ]
    first_btn = None
    for text, cmd in btns_def:
        b = _selector_btn(text, cmd)
        if first_btn is None:
            first_btn = (b, cmd)

    # Activar el primer per defecte
    if first_btn:
        _activate(first_btn[0], first_btn[1])