import customtkinter as ctk
from db import connectar
import consultes
from estil import *

_TIPUS_CAMPS = {
    "Metge":               [("Especialitat","Ex: Cardiologia"),("Currículum","Resum professional"),("Núm. Col·legiat","COL-12345")],
    "Infermer/a Planta":   [("Torn (M/T/N)","M=Matí T=Tarda N=Nit"),("Anys Experiència","Ex: 5"),("ID Planta","Num. planta")],
    "Infermer/a Metge":    [("Torn (M/T/N)","M=Matí T=Tarda N=Nit"),("Anys Experiència","Ex: 5"),("ID Metge","ID del metge")],
    "Vari / Administratiu":[("Tipus Feina","Ex: Neteja"),("Horari","Ex: Dl-Dv 08-15h")],
}
_TIPUS_KEY = {
    "Metge":"metge","Infermer/a Planta":"infermer_planta",
    "Infermer/a Metge":"infermer_metge","Vari / Administratiu":"vari",
}


def menu_alta_personal():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Alta Personal", "800x680")
    topbar(f, "Alta Personal", icon="🩺", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Alta Personal", None)])

    body = ctk.CTkScrollableFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True)

    cols = ctk.CTkFrame(body, fg_color="transparent")
    cols.pack(fill="both", expand=True, padx=16, pady=16)
    cols.columnconfigure(0, weight=1)
    cols.columnconfigure(1, weight=1)

    # ── Dades comuns ──────────────────────────────────────────────────────
    c_esq = mk_card(cols)
    c_esq.grid(row=0, column=0, padx=(4, 8), pady=0, sticky="nsew")
    card_section(c_esq, "Dades personals", icon="👤")

    comuns_defs = [
        ("Nom","Nom"),("Cognom 1","Primer cognom"),("Cognom 2","Segon cognom"),
        ("DNI","12345678A"),("Data Naix. (YYYY-MM-DD)","1985-03-21"),
        ("Telèfon","612 345 678"),("Email","correu@hospital.cat"),("Adreça","Carrer, núm..."),
    ]
    entries_comuns = [field(c_esq, lbl, ph, width=310) for lbl, ph in comuns_defs]

    # ── Tipus i camps específics ──────────────────────────────────────────
    c_drt = mk_card(cols)
    c_drt.grid(row=0, column=1, padx=(8, 4), pady=0, sticky="nsew")
    card_section(c_drt, "Tipus de personal", icon="🩺")

    tipus_var = dropdown(c_drt, "Categoria", list(_TIPUS_CAMPS.keys()), width=310)

    extra_frame = ctk.CTkFrame(c_drt, fg_color="transparent")
    extra_frame.pack(fill="x")
    extra_entries = []

    def rebuild(*_):
        for w in extra_frame.winfo_children(): w.destroy()
        extra_entries.clear()
        for lbl, ph in _TIPUS_CAMPS.get(tipus_var.get(), []):
            extra_entries.append(field(extra_frame, lbl, ph, width=310))

    tipus_var.trace_add("write", rebuild)
    rebuild()

    # ── Estat + botó ──────────────────────────────────────────────────────
    sl = ctk.CTkLabel(body, text="", font=F_SMALL, text_color=C["green"])
    sl.pack(pady=(4, 0))

    btn = ctk.CTkButton(body, text="💾  Guardar personal",
                        fg_color=C["accent"], hover_color=C["accent_h"],
                        width=400, height=40, corner_radius=9,
                        font=font(13, bold=True), text_color="#ffffff")
    btn.pack(pady=(8, 20))

    def guardar():
        comuns = [e.get().strip() for e in entries_comuns]
        extras = [e.get().strip() for e in extra_entries]
        if any(v == "" for v in comuns + extras):
            err(sl, "Tots els camps són obligatoris"); return
        try:
            conn = connectar()
            res = consultes.alta_personal_db(conn, comuns, _TIPUS_KEY[tipus_var.get()], extras, None)
            conn.close()
            ok(sl, f"✓  Personal donat d'alta (ID {res})")
        except Exception as ex:
            err(sl, str(ex))

    btn.configure(command=guardar)