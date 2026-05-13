import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import consultes
from .estil import *


_TIPUS_CAMPS = {
    "Metge": [
        ("Especialitat", "Ex: Cardiologia"),
        ("Currículum", "Resum professional"),
        ("Núm. Col·legiat", "Ex: COL-12345"),
    ],
    "Infermer/a Planta": [
        ("Torn (M/T/N)", "M = Matí, T = Tarda, N = Nit"),
        ("Anys Experiència", "Ex: 5"),
        ("ID Planta", "Número de planta assignada"),
    ],
    "Infermer/a Metge": [
        ("Torn (M/T/N)", "M = Matí, T = Tarda, N = Nit"),
        ("Anys Experiència", "Ex: 5"),
        ("ID Metge", "ID del metge responsable"),
    ],
    "Vari / Administratiu": [
        ("Tipus Feina", "Ex: Neteja, Administració"),
        ("Horari", "Ex: Dl-Dv 08:00-15:00"),
    ],
}

_TIPUS_KEY = {
    "Metge": "metge",
    "Infermer/a Planta": "infermer_planta",
    "Infermer/a Metge": "infermer_metge",
    "Vari / Administratiu": "vari",
}


def menu_alta_personal():
    f = ctk.CTkToplevel()
    aplicar_estil_finestra(f, "Alta Personal", "780x660")

    # Capçalera
    header = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=0, height=56)
    header.pack(fill="x")
    header.pack_propagate(False)
    ctk.CTkLabel(header, text="👩‍⚕️  Alta Personal",
                 font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
                 text_color=C["text"]).pack(side="left", padx=20, pady=16)

    body = ctk.CTkScrollableFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True)

    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=1)

    # ── Columna esquerra: dades comuns ────────────────────────────────────
    card_esq = frame_card(body)
    card_esq.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

    ctk.CTkLabel(card_esq, text="Dades personals",
                 font=ctk.CTkFont(size=13, weight="bold"),
                 text_color=C["sub"]).pack(anchor="w", padx=16, pady=(14, 2))
    separator(card_esq).pack(fill="x", padx=16, pady=(0, 10))

    camps_comuns = [
        ("Nom", "Nom"),
        ("Cognom 1", "Primer cognom"),
        ("Cognom 2", "Segon cognom"),
        ("DNI", "Ex: 12345678A"),
        ("Data Naix. (YYYY-MM-DD)", "Ex: 1985-03-21"),
        ("Telèfon", "Ex: 612345678"),
        ("Email", "exemple@hospital.cat"),
        ("Adreça", "Carrer, número, pis"),
    ]
    entries_comuns = []
    for label, ph in camps_comuns:
        ctk.CTkLabel(card_esq, text=label, font=ctk.CTkFont(size=11),
                     text_color=C["sub"]).pack(anchor="w", padx=16, pady=(4, 0))
        e = entry_estilitzat(card_esq, placeholder=ph, width=310)
        e.pack(padx=16, pady=(2, 2))
        entries_comuns.append(e)

    # ── Columna dreta: tipus + camps específics ───────────────────────────
    card_drt = frame_card(body)
    card_drt.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

    ctk.CTkLabel(card_drt, text="Tipus de personal",
                 font=ctk.CTkFont(size=13, weight="bold"),
                 text_color=C["sub"]).pack(anchor="w", padx=16, pady=(14, 2))
    separator(card_drt).pack(fill="x", padx=16, pady=(0, 10))

    tipus_var = ctk.StringVar(value="Metge")
    selector = ctk.CTkOptionMenu(
        card_drt,
        values=list(_TIPUS_CAMPS.keys()),
        variable=tipus_var,
        fg_color=C["card2"],
        button_color=C["accent"],
        button_hover_color=C["accent2"],
        dropdown_fg_color=C["card"],
        text_color=C["text"],
        width=310,
        height=40,
        corner_radius=10,
    )
    selector.pack(padx=16, pady=(0, 12))

    extra_frame = ctk.CTkFrame(card_drt, fg_color="transparent")
    extra_frame.pack(fill="x", padx=16)
    extra_entries = []

    def rebuild_extra(*_):
        for w in extra_frame.winfo_children():
            w.destroy()
        extra_entries.clear()
        for label, ph in _TIPUS_CAMPS.get(tipus_var.get(), []):
            ctk.CTkLabel(extra_frame, text=label, font=ctk.CTkFont(size=11),
                         text_color=C["sub"]).pack(anchor="w", pady=(4, 0))
            e = entry_estilitzat(extra_frame, placeholder=ph, width=310)
            e.pack(pady=(2, 2))
            extra_entries.append(e)

    tipus_var.trace_add("write", rebuild_extra)
    rebuild_extra()

    # ── Missatge estat + botó ─────────────────────────────────────────────
    status = ctk.CTkLabel(body, text="", font=ctk.CTkFont(size=12), text_color=C["accent3"])
    status.grid(row=1, column=0, columnspan=2, pady=(0, 4))

    def guardar():
        comuns = [e.get().strip() for e in entries_comuns]
        extras = [e.get().strip() for e in extra_entries]
        if any(v == "" for v in comuns + extras):
            status.configure(text="⚠️  Tots els camps són obligatoris", text_color=C["accent4"])
            return
        try:
            conn = connectar()
            tipus_key = _TIPUS_KEY[tipus_var.get()]
            res = consultes.alta_personal_db(conn, comuns, tipus_key, extras, None)
            conn.close()
            status.configure(text=f"✅  Personal donat d'alta (ID {res})", text_color=C["accent3"])
        except Exception as ex:
            status.configure(text=f"❌  {ex}", text_color=C["danger"])

    btn_frame = ctk.CTkFrame(body, fg_color="transparent")
    btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
    boto_primari(btn_frame, "💾  Guardar personal", guardar, width=360).pack()