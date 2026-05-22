import customtkinter as ctk #importem el customtkinter per al menu grafic
from db import connectar #importem la conexio amb la base de dades
from consultes import informe_planta, informe_personal, informe_visites_dia, ranking_metges #importem les consultes necesaries de consultes.py
import os, sys
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

#paleta de colors del menu
BG      = "#0d1422"
SIDEBAR = "#0a1120"
CARD    = "#131f32"
CARD2   = "#162236"
BORDER  = "#1f2d44"
BORDER2 = "#2a3a5c"
ACCENT  = "#3b82f6"
ACCH    = "#2563eb"
TEAL    = "#06b6d4"
GREEN   = "#10b981"
AMBER   = "#f59e0b"
DANGER  = "#f87171"
TEXT    = "#f0f4ff"
TEXT2   = "#e0e8ff"
SUB     = "#8ca0c4"
MUTED   = "#4a6080"

#funcio basica on es crearan els lbl de l'aplicatiu, com s'utilitza molt sera una funcio
def _lbl(parent, text, size=12, bold=False, color=None, **kw):
    return ctk.CTkLabel(parent, text=text, text_color=color or TEXT2,
                        font=("Arial", size, "bold" if bold else "normal"), **kw)

def _sep(parent):
    ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=(8, 10))

#funcio per a indicar que l'element a crear es una "seccio"
def _section(parent, text, icon=""):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=16, pady=(14, 0))
    _lbl(f, f"{icon}  {text}" if icon else text, size=13, bold=True, color=SUB).pack(side="left")
    _sep(parent)

#funcio per a indicar que un element es un textbox, es repetira bastant
def _textbox(parent, width=500, height=260):
    return ctk.CTkTextbox(parent, width=width, height=height,
                          fg_color=SIDEBAR, text_color=TEXT2,
                          font=("Courier New", 11), corner_radius=8,
                          border_width=1, border_color=BORDER)


# panells a mostrar a la part esquerra del menu:
# panel amb la informacio de la planta selecionada:
def _panel_info_planta(parent):
    _lbl(parent, "Informació de la Planta", size=18, bold=True).pack(
        anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Habitacions, quiròfans i personal assignat per planta",
         size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 10))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12,
                        border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Selecciona la planta", "🏢")

    row = ctk.CTkFrame(card, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=(0, 4))
    _lbl(row, "ID Planta:", size=11, color=MUTED).pack(side="left", padx=(0, 8))
    planta_entry = ctk.CTkEntry(row, width=80, height=34, corner_radius=7,
                                fg_color=SIDEBAR, border_color=BORDER2,
                                text_color=TEXT2, font=("Arial", 12))
    planta_entry.insert(0, "1")
    planta_entry.pack(side="left")

    sl = ctk.CTkLabel(card, text="", font=("Arial", 11), text_color=GREEN)
    sl.pack(anchor="w", padx=16, pady=(6, 0))

    # Targetes de resultat
    result_frame = ctk.CTkFrame(parent, fg_color="transparent")
    result_frame.pack(fill="x", padx=16, pady=(12, 0))
    result_frame.columnconfigure((0, 1, 2, 3), weight=1)

    stat_cards = {}

    #indiquem les dades que es volen mostrar
    defs = [
        ("num_planta",        "🏥", "Planta",       TEXT,  ACCENT),
        ("total_habitacions", "🛏️", "Habitacions",  TEXT,  TEAL),
        ("total_quirofans",   "🔪", "Quiròfans",    TEXT,  AMBER),
        ("total_infermeria",  "👩‍⚕️", "Infermers",  TEXT,  GREEN),
    ]

    #les mostrem
    for col, (key, icon, label, tc, color) in enumerate(defs):
        c = ctk.CTkFrame(result_frame, fg_color=CARD, corner_radius=12,
                         border_width=1, border_color=BORDER)
        c.grid(row=0, column=col, padx=5, pady=8, sticky="nsew", ipady=6)
        _lbl(c, icon, size=22).pack(pady=(12, 2))
        val = _lbl(c, "—", size=24, bold=True, color=color)
        val.pack()
        _lbl(c, label, size=10, color=MUTED).pack(pady=(0, 12))
        stat_cards[key] = val

    #consultem a la base de dades les dades demanades desde el consultes.py
    def consultar():
        try:
            conn = connectar()
            d = informe_planta(conn, planta_entry.get().strip())
            conn.close()
            if not d:
                sl.configure(text="✗  Planta no trobada", text_color=DANGER)
                for v in stat_cards.values(): v.configure(text="—")
                return
            for key, widget in stat_cards.items():
                widget.configure(text=str(d.get(key, "—")))
            sl.configure(text="✓  Dades carregades correctament", text_color=GREEN)
        except Exception as ex:
            sl.configure(text=f"✗  {ex}", text_color=DANGER)

    ctk.CTkButton(card, text="🔍  Consultar planta", command=consultar,
                  fg_color=ACCENT, hover_color=ACCH, width=320, height=38,
                  corner_radius=8, font=("Arial", 12, "bold"),
                  text_color="#ffffff").pack(padx=16, pady=(8, 16))

#panell per a la mostra de tot el personal
def _panel_personal(parent):
    _lbl(parent, "Tot el Personal", size=18, bold=True).pack(
        anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Llistat complet amb dades de tots els treballadors",
         size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    sl = ctk.CTkLabel(parent, text="Carregant...", font=("Arial", 11), text_color=MUTED)
    sl.pack(anchor="w", padx=16, pady=(0, 6))

    box = _textbox(parent, height=360)
    box.pack(padx=16, fill="x")
    box.insert("end", f"{'ID':<6}{'Nom':<40}{'DNI':<13}{'DATA NAIXEMENT':<18}{'Email':<18}{'Telèfon':<14}{'Direcció':<30}{'Baixa'}\n")
    box.insert("end", "─" * 200 + "\n")

    #extreurem les dades de ka base de dades amb la funcio de consultes.py
    try:
        conn = connectar()
        dades = informe_personal(conn)
        conn.close()
        for p in dades:
            nom = f"{p.get('nom','')} {p.get('cognom1','')} {p.get('cognom2','')}".strip()
            box.insert("end",
                f"{str(p.get('id_personal','')):<6}"
                f"{nom:<40}"
                f"{str(p.get('dni','')):<13}"
                f"{str(p.get('data_naixement','')):<18}"
                f"{str(p.get('email','')):<18}"
                f"{str(p.get('telefon','')):<14}"
                f"{str(p.get('direccio','')):<30}"
                f"{p.get('baixa','—')}\n")
        sl.configure(text=f"✓  {len(dades)} treballadors", text_color=GREEN)
    except Exception as ex:
        sl.configure(text=f"✗  {ex}", text_color=DANGER)

#panell per a mostrar les visites que hi han hagut cada dia, si es que n'hi ha.
def _panel_visites(parent):
    _lbl(parent, "Visites per Data", size=18, bold=True).pack(
        anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Nombre total de visites mèdiques agrupades per dia",
         size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    sl = ctk.CTkLabel(parent, text="", font=("Arial", 11), text_color=MUTED)
    sl.pack(anchor="w", padx=16, pady=(0, 4))

    box = _textbox(parent, height=360)
    box.pack(padx=16, fill="x")

    #carregarem les dades desde la base de dades i la mostrarem dins del textbox.
    def carregar():
        box.delete("1.0", "end")
        box.insert("end", f"{'Data':<18}{'Total visites'}\n{'─'*36}\n")
        try:
            conn = connectar()
            dades = informe_visites_dia(conn)
            conn.close()
            for r in dades:
                box.insert("end", f"{str(r.get('dia','')):<18}{r.get('total_visites','0')}\n")
            sl.configure(text=f"✓  {len(dades)} dies amb visites registrades", text_color=GREEN)
        except Exception as ex:
            sl.configure(text=f"✗  {ex}", text_color=DANGER)

    ctk.CTkButton(parent, text="🔄  Actualitzar", command=carregar,
                  fg_color=ACCENT, hover_color=ACCH, width=180, height=36,
                  corner_radius=8, font=("Arial", 12, "bold"),
                  text_color="#ffffff").pack(padx=16, pady=(0, 10), anchor="w")
    carregar()

#panell per a mostrar el ranking de metges, qui ha ates mes pacients:
def _panel_ranking(parent):
    _lbl(parent, "Rànquing de Metges", size=18, bold=True).pack(
        anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Metges ordenats per nombre de pacients atesos",
         size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    sl = ctk.CTkLabel(parent, text="", font=("Arial", 11), text_color=MUTED)
    sl.pack(anchor="w", padx=16, pady=(0, 4))

    box = _textbox(parent, height=360)
    box.pack(padx=16, fill="x")

    #carregarem les dades proporcionades gracies a la vista i les afegirem dins del textbox a mostrar
    def carregar():
        box.delete("1.0", "end")
        box.insert("end", f"{'#':<5}{'Metge':<32}{'Pacients atesos'}\n{'─'*52}\n")
        try:
            conn = connectar()
            dades = ranking_metges(conn)
            conn.close()
            medals = ["🥇", "🥈", "🥉"]
            for i, m in enumerate(dades, 1):
                nom = f"{m.get('nom','')} {m.get('cognom1','')} {m.get('cognom2','')}".strip()
                prefix = medals[i-1] if i <= 3 else f"{i} "
                box.insert("end", f"{prefix:<5}{nom:<32}{m.get('total_pacients','0')}\n")
            sl.configure(text=f"✓  {len(dades)} metges al rànquing", text_color=GREEN)
        except Exception as ex:
            sl.configure(text=f"✗  {ex}", text_color=DANGER)

    #boto per a actualitzar les dades, per si es necesari.
    ctk.CTkButton(parent, text="🔄  Actualitzar", command=carregar,
                  fg_color=ACCENT, hover_color=ACCH, width=180, height=36,
                  corner_radius=8, font=("Arial", 12, "bold"),
                  text_color="#ffffff").pack(padx=16, pady=(0, 10), anchor="w")
    carregar()


# consultes principals, aquestes son els menus principals del programa amb la seva funcio per a obrir el seu apartat
_CONSULTES = [
    ("Info Planta",      "🏢", _panel_info_planta),
    ("Tot el Personal",  "👥", _panel_personal),
    ("Visites per dia",  "📋", _panel_visites),
    ("Rànquing Metges",  "🏆", _panel_ranking),
]

#funcio que al menu inicial s'obrira, aquest obrira un menu extern amb les dades pertinents
def obrir_consultes():
    ctk.set_appearance_mode("dark")
    win = ctk.CTkToplevel()
    win.title("Consultes")
    win.geometry("1000x640")
    win.minsize(800, 520)
    win.configure(fg_color=BG)
    win.lift()
    win.focus_force()
    icon_path = resource_path(os.path.join("logo", "logo.ico"))
    win.after(201, lambda: win.iconbitmap(icon_path))
    # barra superior
    topbar = ctk.CTkFrame(win, fg_color=SIDEBAR, corner_radius=0, height=52)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)
    _lbl(topbar, "📊  Consultes", size=17, bold=True).pack(side="left", padx=20, pady=14)
    ctk.CTkButton(topbar, text="✕  Tancar", command=win.destroy,
                  fg_color="transparent", hover_color=CARD2,
                  text_color=MUTED, border_color=BORDER2, border_width=1,
                  width=90, height=30, corner_radius=7,
                  font=("Arial", 11)).pack(side="right", padx=16, pady=11)

    #layout, com es reparteix el menu
    main = ctk.CTkFrame(win, fg_color="transparent")
    main.pack(fill="both", expand=True)

    #barra lateral, per al selector de consultes
    sidebar = ctk.CTkFrame(main, fg_color=SIDEBAR, corner_radius=0, width=200)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    ctk.CTkLabel(sidebar, text="INFORMES", font=("Arial", 9, "bold"),
                 text_color=MUTED).pack(anchor="w", padx=16, pady=(16, 6))

    #area del contingut, on van les dades...
    content_area = ctk.CTkScrollableFrame(main, fg_color=BG, corner_radius=0)
    content_area.pack(side="left", fill="both", expand=True)

    #indiquem el boto actiu, ara es cap
    active_btn = [None]

    #funcio per a carregar el panell indicat, 
    def carregar_panel(build_fn, btn):
        if active_btn[0]:
            active_btn[0].configure(fg_color="transparent", text_color=SUB)
        btn.configure(fg_color=CARD2, text_color=TEXT)
        active_btn[0] = btn
        for w in content_area.winfo_children():
            w.destroy()
        build_fn(content_area)
    
    #per cada boto indicat a les consultes ho afegirem a un llistat que al apretar aquell boto carregara les dades de aquell panell
    sidebar_btns = []
    for nom, icon, build_fn in _CONSULTES:
        btn = ctk.CTkButton(
            sidebar, text=f"{icon}  {nom}",
            fg_color="transparent", hover_color=CARD2,
            text_color=SUB, anchor="w",
            width=184, height=38, corner_radius=8,
            font=("Arial", 12),
        )
        btn.configure(command=lambda b=btn, f=build_fn: carregar_panel(f, b))
        btn.pack(fill="x", padx=8, pady=1)
        sidebar_btns.append((btn, build_fn))

    # Carregar el primer per defecte
    carregar_panel(sidebar_btns[0][1], sidebar_btns[0][0])