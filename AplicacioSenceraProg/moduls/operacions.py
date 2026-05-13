import customtkinter as ctk
from tkcalendar import DateEntry
from db import connectar
import consultes
from estil import *


def _cal_entry(parent):
    """DateEntry amb estil fosc consistent."""
    return DateEntry(parent, date_pattern="yyyy-mm-dd",
                     background="#131f32", foreground="#f0f4ff",
                     borderwidth=1, relief="flat",
                     selectbackground="#3b82f6")


def menu_visites():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Visites per dia", "660x500")
    topbar(f, "Visites", icon="📋", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Visites", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    c = mk_card(body)
    c.pack(fill="x")
    card_section(c, "Visites del dia", icon="📋")

    ctk.CTkLabel(c, text="Data", font=F_SMALL, text_color=C["muted"]).pack(
        anchor="w", padx=18, pady=(6, 0))
    cal = _cal_entry(c)
    cal.pack(padx=18, pady=(2, 0), anchor="w")

    sl = status_lbl(c)
    box = textbox(body, width=620, height=240)
    box.pack(pady=(12, 0))

    def executar():
        box.delete("1.0", "end")
        box.insert("end", f"{'Hora':<10}{'Pacient':<30}{'Metge'}\n")
        box.insert("end", "─" * 60 + "\n")
        try:
            conn = connectar()
            dades = consultes.carregar_visites_del_dia(conn, cal.get_date())
            conn.close()
            for r in dades:
                box.insert("end",
                    f"{str(r.get('hora_entrada','')):<10}"
                    f"{str(r.get('pacient','')):<30}"
                    f"{r.get('metge','')}\n")
            ok(sl, f"✓  {len(dades)} visites trobades")
        except Exception as ex:
            err(sl, str(ex))

    btn_primary(c, "🔍  Consultar visites", executar)


def menu_operacions():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Operacions per dia", "680x500")
    topbar(f, "Operacions", icon="🔪", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Operacions", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    c = mk_card(body)
    c.pack(fill="x")
    card_section(c, "Operacions del dia", icon="🔪")

    ctk.CTkLabel(c, text="Data", font=F_SMALL, text_color=C["muted"]).pack(
        anchor="w", padx=18, pady=(6, 0))
    cal = _cal_entry(c)
    cal.pack(padx=18, pady=(2, 0), anchor="w")

    sl = status_lbl(c)
    box = textbox(body, width=640, height=240)
    box.pack(pady=(12, 0))

    def executar():
        box.delete("1.0", "end")
        box.insert("end", f"{'Hora':<10}{'Quiròfan':<16}{'Pacient'}\n")
        box.insert("end", "─" * 60 + "\n")
        try:
            conn = connectar()
            dades = consultes.carregar_operacions_dia(conn, cal.get_date())
            conn.close()
            for r in dades:
                box.insert("end",
                    f"{str(r.get('hora','')):<10}"
                    f"{str(r.get('quirofan','')):<16}"
                    f"{r.get('pacient','')}\n")
            ok(sl, f"✓  {len(dades)} operacions trobades")
        except Exception as ex:
            err(sl, str(ex))

    btn_primary(c, "🔍  Consultar operacions", executar)