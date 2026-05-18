import customtkinter as ctk
from tkinter import messagebox
import funcions
from db import tancar_sessio, connectar
import config
import menu_manteniment
import menu_consultes
import threading
from datetime import date

# ── Paleta de colors ──────────────────────────────────────────────────────────
COLORS = {
    "bg_dark":      "#0f1623",
    "bg_card":      "#1a2236",
    "bg_card2":     "#1e2a40",
    "accent":       "#3b82f6",
    "accent2":      "#06b6d4",
    "accent3":      "#10b981",
    "accent4":      "#f59e0b",
    "text_main":    "#f0f4ff",
    "text_sub":     "#8ca0c4",
    "border":       "#2a3a5c",
    "danger":       "#ef4444",
}

# ── Helpers de BD ─────────────────────────────────────────────────────────────
def _fetch_stats():
    """Retorna un dict amb estadístiques bàsiques. Retorna zeros si falla."""
    stats = {
        "pacients": "0",
        "personal": "0",
        "visites_avui": "0",
        "operacions_avui": "0",
    }
    try:
        conn = connectar()
        if not conn:
            return stats
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM pacient.pacient")
            stats["pacients"] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM dades_per.personal WHERE baixa IS NULL OR baixa = false")
            stats["personal"] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM pacient.visita WHERE DATE(data_visita) = %s", (date.today(),))
            stats["visites_avui"] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM pacient.operacio WHERE DATE(hora) = %s", (date.today(),))
            stats["operacions_avui"] = cur.fetchone()[0]
        conn.close()
    except Exception:
        pass
    return stats


# ── Finestra principal del menú ───────────────────────────────────────────────
def obrir_menu(rol):
    ctk.set_appearance_mode("dark")

    f = ctk.CTkToplevel()
    f.title("Hospivibe")
    f.geometry("860x620")
    f.resizable(True, True)
    f.configure(fg_color=COLORS["bg_dark"])

    # ── Capçalera ──────────────────────────────────────────────────────────
    header = ctk.CTkFrame(f, fg_color=COLORS["bg_card"], corner_radius=0, height=64)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    ctk.CTkLabel(
        header,
        text="🏥  Hospivibe",
        font=ctk.CTkFont(family="Georgia", size=22, weight="bold"),
        text_color=COLORS["text_main"],
    ).pack(side="left", padx=28, pady=16)

    rol_badge_color = COLORS["accent"] if rol == "admin" else COLORS["accent3"]
    ctk.CTkLabel(
        header,
        text=f"  {rol.upper()}  ",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#ffffff",
        fg_color=rol_badge_color,
        corner_radius=8,
    ).pack(side="left", pady=20)

    def tornar_login():
        tancar_sessio()
        f.destroy()
        f.master.deiconify()

    ctk.CTkButton(
        header,
        text="⏻  Tancar sessió",
        command=tornar_login,
        fg_color="transparent",
        hover_color=COLORS["bg_card2"],
        text_color=COLORS["text_sub"],
        border_color=COLORS["border"],
        border_width=1,
        width=130,
        height=34,
        corner_radius=8,
        font=ctk.CTkFont(size=12),
    ).pack(side="right", padx=20, pady=14)

    # ── Cos principal ──────────────────────────────────────────────────────
    body = ctk.CTkScrollableFrame(f, fg_color=COLORS["bg_dark"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=0, pady=0)

    # Salutació
    today_str = date.today().strftime("%d/%m/%Y")
    ctk.CTkLabel(
        body,
        text=f"Benvingut/da  ·  {today_str}",
        font=ctk.CTkFont(size=13),
        text_color=COLORS["text_sub"],
    ).pack(anchor="w", padx=30, pady=(20, 0))

    ctk.CTkLabel(
        body,
        text="Resum del dia",
        font=ctk.CTkFont(family="Georgia", size=26, weight="bold"),
        text_color=COLORS["text_main"],
    ).pack(anchor="w", padx=30, pady=(4, 16))

    # ── Targetes d'estadístiques ───────────────────────────────────────────
    stats_frame = ctk.CTkFrame(body, fg_color="transparent")
    stats_frame.pack(fill="x", padx=24, pady=(0, 24))
    stats_frame.columnconfigure((0, 1, 2, 3), weight=1)

    card_defs = [
        ("👥", "Pacients", "pacients",       COLORS["accent"]),
        ("🩺", "Personal", "personal",        COLORS["accent3"]),
        ("📋", "Visites avui", "visites_avui", COLORS["accent2"]),
        ("🔪", "Operacions avui", "operacions_avui", COLORS["accent4"]),
    ]

    stat_labels = {}  # per actualitzar-les un cop carregui la BD

    for col, (icon, title, key, color) in enumerate(card_defs):
        card = ctk.CTkFrame(
            stats_frame,
            fg_color=COLORS["bg_card"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew", ipady=8)

        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=26)).pack(pady=(14, 2))
        val_lbl = ctk.CTkLabel(
            card,
            text="…",
            font=ctk.CTkFont(family="Georgia", size=28, weight="bold"),
            text_color=color,
        )
        val_lbl.pack()
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_sub"],
        ).pack(pady=(0, 14))
        stat_labels[key] = val_lbl

    # Carrega stats en segon pla
    def _load_stats():
        stats = _fetch_stats()
        for key, lbl in stat_labels.items():
            lbl.configure(text=str(stats.get(key, "—")))

    threading.Thread(target=_load_stats, daemon=True).start()

    # ── Secció d'accions ───────────────────────────────────────────────────
    sep = ctk.CTkFrame(body, fg_color=COLORS["border"], height=1)
    sep.pack(fill="x", padx=30, pady=(0, 20))

    ctk.CTkLabel(
        body,
        text="Accions",
        font=ctk.CTkFont(family="Georgia", size=20, weight="bold"),
        text_color=COLORS["text_main"],
    ).pack(anchor="w", padx=30, pady=(0, 12))

    actions_frame = ctk.CTkFrame(body, fg_color="transparent")
    actions_frame.pack(fill="x", padx=24, pady=(0, 20))

    def _action_btn(parent, icon, label, subtitle, color, cmd, col, row):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_card2"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
            cursor="hand2",
        )
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew", ipadx=8, ipady=6)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=icon, font=ctk.CTkFont(size=20)).pack(side="left")
        ctk.CTkLabel(
            top,
            text=label,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_main"],
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
            inner,
            text=subtitle,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_sub"],
            justify="left",
            wraplength=180,
        ).pack(anchor="w", pady=(4, 8))

        ctk.CTkButton(
            inner,
            text="Obrir →",
            command=cmd,
            fg_color=color,
            hover_color=_darken(color),
            width=90,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w")

    def _darken(hex_color):
        """Retorna una versió lleugerament més fosca del color."""
        r = max(0, int(hex_color[1:3], 16) - 30)
        g = max(0, int(hex_color[3:5], 16) - 30)
        b = max(0, int(hex_color[5:7], 16) - 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    # tots els rols veuen manteniment i consultes
    actions_frame.columnconfigure((0, 1, 2), weight=1)

    _action_btn(
        actions_frame, "🔧", "Manteniment",
        "Gestió d'altes, operacions, visites i inventari",
        COLORS["accent"],
        menu_manteniment.obrir_manteniment,
        col=0, row=0,
    )
    _action_btn(
        actions_frame, "📊", "Consultes",
        "Informes, rànquings i dades agregades",
        COLORS["accent2"],
        menu_consultes.obrir_consultes,
        col=1, row=0,
    )

    # gestió d'usuaris només visible per als administradors
    if rol == "admin":
        _action_btn(
            actions_frame, "👤", "Gestió usuaris",
            "Crear i administrar comptes d'accés al sistema",
            COLORS["accent3"],
            gestio_usuaris,
            col=2, row=0,
        )

    # Peu de pàgina
    ctk.CTkLabel(
        body,
        text="Sistema de gestió hospitalària",
        font=ctk.CTkFont(size=10),
        text_color=COLORS["border"],
    ).pack(pady=(10, 20))


# ── Gestió d'usuaris ──────────────────────────────────────────────────────────
def gestio_usuaris():
    C = COLORS
    g = ctk.CTkToplevel()
    g.title("Gestió d'usuaris")
    g.geometry("460x520")
    g.configure(fg_color=C["bg_dark"])
    g.lift()
    g.focus_force()

    # Topbar
    topbar = ctk.CTkFrame(g, fg_color=C["bg_card"], corner_radius=0, height=52)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)
    ctk.CTkLabel(topbar, text="👤  Gestió d'usuaris",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 text_color=C["text_main"]).pack(side="left", padx=20, pady=14)

    # Selector de pestanya
    tab_frame = ctk.CTkFrame(g, fg_color="transparent")
    tab_frame.pack(fill="x", padx=24, pady=(16, 0))

    content = ctk.CTkFrame(g, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    active_tab = [None]

    def _tab_btn(text, cmd):
        b = ctk.CTkButton(tab_frame, text=text, width=0, height=34,
                          fg_color=C["bg_card"], hover_color=C["bg_card2"],
                          text_color=C["text_sub"], border_color=C["border"],
                          border_width=1, corner_radius=8,
                          font=ctk.CTkFont(size=12))
        b.pack(side="left", padx=(0, 6))
        b.configure(command=lambda: _activate(b, cmd))
        return b

    def _activate(btn, cmd):
        if active_tab[0]:
            active_tab[0].configure(fg_color=C["bg_card"], text_color=C["text_sub"],
                                     border_color=C["border"])
        btn.configure(fg_color=C["bg_card2"], text_color=C["accent"],
                      border_color=C["accent"])
        active_tab[0] = btn
        for w in content.winfo_children():
            w.destroy()
        cmd()

    def _entry_field(parent, placeholder, show=None):
        kw = dict(placeholder_text=placeholder, width=380, height=42,
                  corner_radius=10, fg_color=C["bg_card2"],
                  border_color=C["border"], text_color=C["text_main"],
                  font=ctk.CTkFont(size=13))
        if show: kw["show"] = show
        e = ctk.CTkEntry(parent, **kw)
        e.pack(pady=(0, 10), padx=4)
        return e

    def _status_lbl(parent):
        l = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=12),
                         text_color=C["accent3"], wraplength=380)
        l.pack(pady=(4, 0), padx=4)
        return l

    # pestanya per crear un nou usuari amb nom, contrasenya i rol
    def tab_nou_usuari():
        card = ctk.CTkFrame(content, fg_color=C["bg_card"], corner_radius=14,
                            border_width=1, border_color=C["border"])
        card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(card, text="Nom d'usuari", font=ctk.CTkFont(size=11),
                     text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(16, 2))
        e_user = ctk.CTkEntry(card, placeholder_text="Nom d'usuari",
                              width=380, height=42, corner_radius=10,
                              fg_color=C["bg_card2"], border_color=C["border"],
                              text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_user.pack(padx=20, pady=(0, 8))

        ctk.CTkLabel(card, text="Contrasenya", font=ctk.CTkFont(size=11),
                     text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(0, 2))
        e_pass = ctk.CTkEntry(card, placeholder_text="Contrasenya", show="*",
                              width=380, height=42, corner_radius=10,
                              fg_color=C["bg_card2"], border_color=C["border"],
                              text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_pass.pack(padx=20, pady=(0, 8))

        # selector de rol amb botons visuals
        ctk.CTkLabel(card, text="Rol", font=ctk.CTkFont(size=11),
                     text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(0, 4))

        _ROLS = [
            ("admin",    "🔑  Administrador", C["accent"]),
            ("metge",    "🩺  Metge",         C["accent2"]),
            ("infermer", "👩‍⚕️  Infermer/a",   C["accent3"]),
        ]
        rol_var = ctk.StringVar(value="metge")  # rol seleccionat per defecte
        rol_frame = ctk.CTkFrame(card, fg_color="transparent")
        rol_frame.pack(anchor="w", padx=20, pady=(0, 10))
        rol_btns = {}

        def sel_rol(key):
            # actualitza l'aparença dels botons segons la selecció
            rol_var.set(key)
            for k, b in rol_btns.items():
                col = next(c for r, _, c in _ROLS if r == k)
                if k == key:
                    b.configure(fg_color=col, text_color="#ffffff", border_color=col)
                else:
                    b.configure(fg_color=C["bg_card2"], text_color=C["text_sub"],
                                border_color=C["border"])

        for key, label, color in _ROLS:
            b = ctk.CTkButton(rol_frame, text=label, width=118, height=36,
                              corner_radius=9, border_width=1,
                              fg_color=C["bg_card2"], text_color=C["text_sub"],
                              border_color=C["border"], font=ctk.CTkFont(size=12),
                              command=lambda k=key: sel_rol(k))
            b.pack(side="left", padx=(0, 6))
            rol_btns[key] = b
        sel_rol("metge")

        sl = _status_lbl(card)

        def registrar():
            nom = e_user.get().strip()
            pwd = e_pass.get().strip()
            rol_sel = rol_var.get()
            if not nom or not pwd:
                sl.configure(text="⚠️  Tots els camps són obligatoris",
                             text_color=C["accent4"]); return
            try:
                import autentificacio
                hashed = autentificacio.hash_contrasenya(pwd)
                conn = connectar()
                with conn.cursor() as cur:
                    # insereix l'usuari i obté el seu id
                    cur.execute(
                        "INSERT INTO seguretat.usuari (username, password) VALUES (%s, %s) RETURNING id_usuari",
                        (nom, hashed))
                    id_usuari = cur.fetchone()[0]
                    # busca l'id del rol seleccionat
                    cur.execute("SELECT id_rol FROM seguretat.rol WHERE nom = %s", (rol_sel,))
                    row = cur.fetchone()
                    if not row:
                        conn.rollback(); conn.close()
                        sl.configure(text=f"❌  Rol '{rol_sel}' no trobat a la BD",
                                     text_color=C["danger"]); return
                    # assigna el rol a l'usuari
                    cur.execute(
                        "INSERT INTO seguretat.usuari_rol (id_usuari, id_rol) VALUES (%s, %s)",
                        (id_usuari, row[0]))
                        # No se puede usar %s en DDL, usamos format validando antes
                    rols_permesos = {'metge', 'infermer', 'admin'}
                    if rol_sel not in rols_permesos:
                        raise ValueError(f"Rol no permès: {rol_sel}")
                    if rol_sel == 'metge':
                        rol = 'metge_role'
                    elif rol_sel == 'admin':
                        rol = 'admin_role'
                    elif rol_sel == 'infermer':
                        rol = 'infermer_role'
                    cur.execute("SELECT dades_per.crear_rol(%s, %s, %s)", (nom, pwd, rol))
                    conn.commit()
                conn.close()
                sl.configure(text=f"✅  Usuari '{nom}' creat com a {rol_sel}",
                             text_color=C["accent3"])
                e_user.delete(0, "end")
                e_pass.delete(0, "end")
            except Exception as ex:
                sl.configure(text=f"❌  {ex}", text_color=C["danger"])

        ctk.CTkButton(card, text="Crear usuari", command=registrar,
                      fg_color=C["accent"], hover_color=C["accent2"],
                      width=380, height=42, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      text_color="#ffffff").pack(padx=20, pady=(4, 20))

    # ── Pestanya: Canviar contrasenya ─────────────────────────────────────
    def tab_canviar_password():
        card = ctk.CTkFrame(content, fg_color=C["bg_card"], corner_radius=14,
                            border_width=1, border_color=C["border"])
        card.pack(fill="x")

        ctk.CTkLabel(card, text="Nom d'usuari", font=ctk.CTkFont(size=11),
                     text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(16, 2))
        e_user = ctk.CTkEntry(card, placeholder_text="Usuari a modificar",
                              width=380, height=42, corner_radius=10,
                              fg_color=C["bg_card2"], border_color=C["border"],
                              text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_user.pack(padx=20, pady=(0, 8))

        ctk.CTkLabel(card, text="Nova contrasenya", font=ctk.CTkFont(size=11),
                     text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(0, 2))
        e_pass = ctk.CTkEntry(card, placeholder_text="Nova contrasenya", show="*",
                              width=380, height=42, corner_radius=10,
                              fg_color=C["bg_card2"], border_color=C["border"],
                              text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_pass.pack(padx=20, pady=(0, 8))

        ctk.CTkLabel(card, text="Confirmar contrasenya", font=ctk.CTkFont(size=11),
                     text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(0, 2))
        e_confirm = ctk.CTkEntry(card, placeholder_text="Repeteix la contrasenya", show="*",
                                 width=380, height=42, corner_radius=10,
                                 fg_color=C["bg_card2"], border_color=C["border"],
                                 text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_confirm.pack(padx=20, pady=(0, 8))

        sl = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12),
                          text_color=C["accent3"], wraplength=380)
        sl.pack(pady=(4, 0), padx=20)

        def canviar():
            nom = e_user.get().strip()
            pwd = e_pass.get().strip()
            confirm = e_confirm.get().strip()
            if not nom or not pwd or not confirm:
                sl.configure(text="⚠️  Tots els camps són obligatoris",
                             text_color=C["accent4"]); return
            if pwd != confirm:
                sl.configure(text="❌  Les contrasenyes no coincideixen",
                             text_color=C["danger"]); return
            try:
                import autentificacio
                hashed = autentificacio.hash_contrasenya(pwd)
                conn = connectar()
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE seguretat.usuari SET password = %s WHERE username = %s",
                        (hashed, nom)
                    )
                    cur.execute("SELECT dades_per.actualitzar_contrasenya(%s, %s)", (nom, pwd))
                    if cur.rowcount == 0:
                        sl.configure(text="❌  Usuari no trobat", text_color=C["danger"])
                    else:
                        conn.commit()
                        sl.configure(text="✅  Contrasenya actualitzada correctament",
                                     text_color=C["accent3"])
                        e_user.delete(0, "end")
                        e_pass.delete(0, "end")
                        e_confirm.delete(0, "end")
                conn.close()
            except Exception as ex:
                sl.configure(text=f"❌  {ex}", text_color=C["danger"])

        ctk.CTkButton(card, text="Canviar contrasenya", command=canviar,
                      fg_color=C["accent3"], hover_color="#059669",
                      width=380, height=42, corner_radius=10,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      text_color="#ffffff").pack(padx=20, pady=(4, 20))

    # Crear les pestanyes i activar la primera
    b1 = _tab_btn("➕  Nou usuari", tab_nou_usuari)
    b2 = _tab_btn("🔑  Canviar contrasenya", tab_canviar_password)
    _activate(b1, tab_nou_usuari)