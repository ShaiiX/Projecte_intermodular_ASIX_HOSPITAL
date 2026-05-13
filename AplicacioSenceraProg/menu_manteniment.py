import customtkinter as ctk
from estil import C, F_TITLE, F_CARD, F_SMALL, font, setup, topbar

from moduls.alta_personal import menu_alta_personal
from moduls.alta_pacient import menu_alta_pacient
from moduls.dependencia import menu_dependencia
from moduls.operacions import menu_operacions
from moduls.visites import menu_visites
from moduls.inventari import menu_inventari
from moduls.habitacio import menu_habitacio
from moduls.historial import menu_historial
from moduls.programacio_metges import menu_programacio_metges
from moduls.informes import menu_informes
from moduls.dummy_data import menu_dummy_data


_MODULS = [
    ("Alta Pacient",          "👤", C["accent"],  menu_alta_pacient),
    ("Alta Personal",         "🩺", C["teal"],    menu_alta_personal),
    ("Dependència",           "🔗", C["purple"],  menu_dependencia),
    ("Operacions per dia",    "🔪", C["amber"],   menu_operacions),
    ("Visites per dia",       "📋", C["green"],   menu_visites),
    ("Inventari Aparells",    "🏥", C["teal"],    menu_inventari),
    ("Habitacions",           "🛏️", C["accent"],  menu_habitacio),
    ("Historial Pacient",     "📂", C["purple"],  menu_historial),
    ("Programació Metges",    "📅", C["amber"],   menu_programacio_metges),
    ("Informes",              "📊", C["green"],   menu_informes),
    ("Dummy Data",            "⚗️",  C["danger"],  menu_dummy_data),
]


def obrir_manteniment():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Bloc de Manteniment", "620x640")

    topbar(f, "Manteniment", icon="⚙️")

    body = ctk.CTkScrollableFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=0, pady=0)

    # Títol
    ctk.CTkLabel(body, text="Selecciona una funcionalitat",
                 font=font(18, bold=True), text_color=C["text"]).pack(
        anchor="w", padx=24, pady=(20, 4))
    ctk.CTkLabel(body, text="OPCIONS DISPONIBLES",
                 font=font(10, bold=True), text_color=C["muted"]).pack(
        anchor="w", padx=24, pady=(0, 12))

    # Grid 2 columnes
    grid = ctk.CTkFrame(body, fg_color="transparent")
    grid.pack(fill="x", padx=16, pady=(0, 24))
    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)

    for i, (nom, icon, color, cmd) in enumerate(_MODULS):
        row, col = divmod(i, 2)
        _modul_card(grid, nom, icon, color, cmd, row=row, col=col)

    # Si imparell, afegir cel·la buida
    if len(_MODULS) % 2:
        empty = ctk.CTkFrame(grid, fg_color="transparent")
        empty.grid(row=len(_MODULS) // 2, column=1, padx=6, pady=6, sticky="nsew")


def _modul_card(parent, nom, icon, color, cmd, row, col):
    card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12,
                        border_width=1, border_color=C["border"], cursor="hand2")
    card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(fill="x", padx=14, pady=12)

    # icona amb fons de color
    ic_bg = ctk.CTkFrame(inner, fg_color=_alpha_color(color),
                         corner_radius=8, width=36, height=36)
    ic_bg.pack(side="left")
    ic_bg.pack_propagate(False)
    ctk.CTkLabel(ic_bg, text=icon, font=font(18)).pack(expand=True)

    ctk.CTkLabel(inner, text=nom, font=font(13, bold=True),
                 text_color=C["text2"]).pack(side="left", padx=10)

    ctk.CTkLabel(inner, text="→", font=font(14),
                 text_color=C["muted"]).pack(side="right")

    # Hover
    def _on_enter(_): card.configure(fg_color=C["card2"], border_color=C["accent"])
    def _on_leave(_): card.configure(fg_color=C["card"], border_color=C["border"])
    for w in [card, inner] + inner.winfo_children():
        w.bind("<Enter>", _on_enter)
        w.bind("<Leave>", _on_leave)
        w.bind("<Button-1>", lambda e, c=cmd: c())


def _alpha_color(hex_color):
    """Versió molt fosca d'un color per al fons de les icones."""
    r = max(0, int(hex_color[1:3], 16) // 5)
    g = max(0, int(hex_color[3:5], 16) // 5)
    b = max(0, int(hex_color[5:7], 16) // 5)
    return f"#{r:02x}{g:02x}{b:02x}"