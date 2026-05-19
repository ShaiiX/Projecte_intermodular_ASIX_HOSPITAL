import customtkinter as ctk #importar la llibreria del menu grafic
from db import tancar_sessio, connectar #importem la conexió y la tancada de conexió de l'usuari
import menu_manteniment #importem el menu de manteniment del sistema 
import menu_consultes #importem el menu de consultes del sistema
import menu_usuaris # importem el menu de usuaris per a poder gestionar-los
import threading 
from datetime import date

# Paleta de color de l'aplicació
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

# Dades inicials que es mostren dins de l'aplicatiu, 
def _fetch_stats():
    # aquestes serien les dades inicials a mostrar com es vol:
    stats = {
        "pacients": "-",
        "personal": "-",
        "visites_avui": "-",
        "operacions_avui": "-",
    }
    # intentarem extreure aquestes dades 
    try:
        conn = connectar()
        if not conn:
            return stats
        with conn.cursor() as cur:
            # selector per a comptar el total de pacients
            cur.execute("SELECT COUNT(*) FROM pacient.pacient")
            stats["pacients"] = cur.fetchone()[0]
            # selector per a comptar el total del personal
            cur.execute("SELECT COUNT(*) FROM dades_per.personal WHERE baixa IS NULL OR baixa = false")
            stats["personal"] = cur.fetchone()[0]
            # selector per a comptar el total de visitas del dia d'avui
            cur.execute("SELECT COUNT(*) FROM pacient.visita WHERE DATE(data_visita) = %s", (date.today(),))
            stats["visites_avui"] = cur.fetchone()[0]
            # selector per a comptar el total d'operacions del dia d'avui
            cur.execute("SELECT COUNT(*) FROM pacient.operacio WHERE DATE(hora) = %s", (date.today(),))
            stats["operacions_avui"] = cur.fetchone()[0]
        conn.close()
    except Exception:
        pass
    return stats


# finestra del menu principal del programa
def obrir_menu(rol):
    ctk.set_appearance_mode("dark")

    f = ctk.CTkToplevel()
    f.title("Hospivibe")
    f.geometry("860x620")
    f.resizable(True, True)
    f.configure(fg_color=COLORS["bg_dark"])

    # capçelera
    header = ctk.CTkFrame(f, fg_color=COLORS["bg_card"], corner_radius=0, height=64)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    # titol principal
    ctk.CTkLabel(
        header,
        text="🏥  Hospivibe",
        font=ctk.CTkFont(family="Georgia", size=22, weight="bold"),
        text_color=COLORS["text_main"],
    ).pack(side="left", padx=28, pady=16)

    # mostra el rol de l'usuari actual
    rol_badge_color = COLORS["accent"] if rol == "admin" else COLORS["accent3"]
    ctk.CTkLabel(
        header,
        text=f"  {rol.upper()}  ",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#ffffff",
        fg_color=rol_badge_color,
        corner_radius=8,
    ).pack(side="left", pady=20)

    # tanca completament la conexió com a postgres.
    def tornar_login():
        tancar_sessio()
        f.destroy()
        f.master.deiconify()

    # afegirm el buto per si l'usuari vol tancar sessió mes tard.
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

    # cos principal del menu principal
    body = ctk.CTkScrollableFrame(f, fg_color=COLORS["bg_dark"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=0, pady=0)

    # salutació a l'usuari
    today_str = date.today().strftime("%d/%m/%Y")
    ctk.CTkLabel(
        body,
        text=f"Benvingut/da  ·  {today_str}",
        font=ctk.CTkFont(size=13),
        text_color=COLORS["text_sub"],
    ).pack(anchor="w", padx=30, pady=(20, 0))

    # resum del dia actual amb visites...
    ctk.CTkLabel(
        body,
        text="Resum del dia",
        font=ctk.CTkFont(family="Georgia", size=26, weight="bold"),
        text_color=COLORS["text_main"],
    ).pack(anchor="w", padx=30, pady=(4, 16))

    # afegim un frame per a les estadistiques.
    stats_frame = ctk.CTkFrame(body, fg_color="transparent")
    stats_frame.pack(fill="x", padx=24, pady=(0, 24))
    stats_frame.columnconfigure((0, 1, 2, 3), weight=1)

    #això son les estadistiques inicials, amb els seus colors:
    card_defs = [
        ("👥", "Pacients", "pacients",       COLORS["accent"]),
        ("🩺", "Personal", "personal",        COLORS["accent3"]),
        ("📋", "Visites avui", "visites_avui", COLORS["accent2"]),
        ("🔪", "Operacions avui", "operacions_avui", COLORS["accent4"]),
    ]

    stat_labels = {}  # per actualitzar-les un cop carregui la BD

    #ara mostrarem les estadistiques:
    for col, (icon, title, key, color) in enumerate(card_defs):
        #primer afegim el fons de cada una
        card = ctk.CTkFrame(
            stats_frame,
            fg_color=COLORS["bg_card"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew", ipady=8)

        #la icona de la estadistica
        ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=26)).pack(pady=(14, 2))

        # el texte actual de l'estadistica
        val_lbl = ctk.CTkLabel(
            card,
            text="…",
            font=ctk.CTkFont(family="Georgia", size=28, weight="bold"),
            text_color=color,
        )
        val_lbl.pack()

        #el titul de la estadistica actual
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

    # accions
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

    #aquesta funcio serveix per a crear els 3 menus, tant de consultes, usuaris i manteniment.
    def _action_btn(parent, icon, label, subtitle, color, cmd, col, row):
        # el fons
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

        # el boto per a obrir el seu propi menu
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
    
    #Retorna una versió lleugerament més fosca del color
    def _darken(hex_color):
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
            menu_usuaris.gestio_usuaris,
            col=2, row=0,
        )

    # Peu de pàgina
    ctk.CTkLabel(
        body,
        text="Sistema de gestió hospitalària",
        font=ctk.CTkFont(size=10),
        text_color=COLORS["border"],
    ).pack(pady=(10, 20))
