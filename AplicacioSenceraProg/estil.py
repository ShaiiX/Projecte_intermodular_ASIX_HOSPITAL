"""paleta i helpers compartits
importar: from moduls._estil import *"""
import customtkinter as ctk

# diccionari centralitzat amb tots els colors de la interfície
# serveix per mantenir una aparença coherent a totes les finestres
C = {
    "bg":       "#0d1422", "topbar":  "#111827",
    "card":     "#131f32", "card2":   "#162236",
    "border":   "#1f2d44", "border2": "#2a3a5c",
    "accent":   "#3b82f6", "accent_h":"#2563eb",
    "teal":     "#06b6d4", "green":   "#10b981",
    "amber":    "#f59e0b", "purple":  "#a78bfa",
    "danger":   "#f87171", "danger_h":"#dc2626",
    "text":     "#f0f4ff", "text2":   "#e0e8ff",
    "sub":      "#8ca0c4", "muted":   "#4a6080",
}

# funció auxiliar per crear fonts de forma ràpida
# permet escollir mida negreta i font monoespaiada
def font(size=12, bold=False, mono=False):
    # si mono és cert s'utilitza courier new per a textos tècnics
    # si no s'utilitza arial com a font general de la interfície
    fam = "Courier New" if mono else "Arial"
    # retorna una tupla compatible amb customtkinter
    # si bold és cert afegeix el pes de negreta a la font
    return (fam, size, "bold") if bold else (fam, size)

# fonts fixes reutilitzades en diferents parts de l'aplicació
# eviten repetir configuracions i faciliten canvis visuals globals
F_TITLE = ("Arial", 18, "bold")
F_CARD  = ("Arial", 13, "bold")
F_BODY  = ("Arial", 12)
F_SMALL = ("Arial", 11)
F_MONO  = ("Courier New", 12)

# configura una finestra base amb mode fosc títol mida i color de fons
def setup(win, titol, mida="620x560"):
    # activa el tema fosc de customtkinter
    ctk.set_appearance_mode("dark")
    # posa el títol rebut a la finestra
    win.title(titol)
    # defineix la mida inicial de la finestra
    win.geometry(mida)
    # aplica el color de fons principal de la paleta
    win.configure(fg_color=C["bg"])

# crea la barra superior comuna de les pantalles
# pot incloure icona títol ruta de navegació i botó per tornar enrere
def topbar(parent, titol, icon="🏥", back_cmd=None, breadcrumbs=None):
    # marc principal de la barra superior
    bar = ctk.CTkFrame(parent, fg_color=C["topbar"], corner_radius=0, height=52)
    bar.pack(fill="x")
    # manté l'alçada fixa encara que el contingut sigui més petit
    bar.pack_propagate(False)
    # zona esquerra on van el títol i les molles de pa
    left = ctk.CTkFrame(bar, fg_color="transparent")
    left.pack(side="left", fill="y", padx=16)
    # etiqueta principal amb icona i títol de la pantalla
    ctk.CTkLabel(left, text=f"{icon}  {titol}", font=F_TITLE,
                 text_color=C["text"]).pack(side="left", pady=14)
    # si hi ha breadcrumbs es mostren com una ruta navegable
    if breadcrumbs:
        # separador visual entre el títol i la ruta
        ctk.CTkLabel(left, text=" › ", font=F_SMALL,
                     text_color=C["muted"]).pack(side="left")
        # recorre cada element de la ruta per crear-ne una etiqueta
        for i, (lbl, cmd) in enumerate(breadcrumbs):
            # detecta si és l'últim element de la ruta
            is_last = i == len(breadcrumbs) - 1
            # l'últim element es ressalta perquè representa la pantalla actual
            color = C["text2"] if is_last else C["sub"]
            # crea l'etiqueta de cada pas de navegació
            l = ctk.CTkLabel(left, text=lbl, font=F_SMALL,
                             text_color=color, cursor="arrow" if is_last else "hand2")
            l.pack(side="left")
            # si el pas té comanda queda vinculat al clic del ratolí
            if cmd: l.bind("<Button-1>", lambda e, c=cmd: c())
            # afegeix separador entre passos excepte després de l'últim
            if not is_last:
                ctk.CTkLabel(left, text=" › ", font=F_SMALL,
                             text_color=C["muted"]).pack(side="left")
    # si es rep una comanda de retorn es crea el botó enrere
    if back_cmd:
        ctk.CTkButton(bar, text="← Enrere", command=back_cmd,
                      fg_color="transparent", hover_color=C["card2"],
                      text_color=C["sub"], border_color=C["border2"],
                      border_width=1, width=100, height=30, corner_radius=7,
                      font=F_SMALL).pack(side="right", padx=16, pady=11)
    # retorna la barra per si la pantalla necessita reutilitzar-la
    return bar

# crea una targeta base amb fons i vora de la paleta
def mk_card(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12,
                        border_width=1, border_color=C["border"], **kw)

# afegeix un títol de secció dins una targeta o panell
def card_section(parent, text, icon=""):
    # contenidor transparent per al text de la secció
    inner = ctk.CTkFrame(parent, fg_color="transparent")
    inner.pack(fill="x", padx=18, pady=(14, 0))
    # mostra la icona només si s'ha passat com a paràmetre
    ctk.CTkLabel(inner, text=f"{icon}  {text}" if icon else text,
                 font=F_CARD, text_color=C["sub"]).pack(side="left")
    # línia separadora sota el títol de la secció
    ctk.CTkFrame(parent, fg_color=C["border"], height=1).pack(
        fill="x", padx=18, pady=(8, 10))

# crea un camp de text amb etiqueta i placeholder
# també permet rebre show per ocultar contrasenyes o dades sensibles
def field(parent, label, placeholder="", show=None, width=380):
    # etiqueta petita situada damunt del camp
    ctk.CTkLabel(parent, text=label, font=F_SMALL,
                 text_color=C["muted"]).pack(anchor="w", padx=18, pady=(6,0))
    # configuració comuna del camp d'entrada
    kw = dict(placeholder_text=placeholder, width=width, height=38,
              corner_radius=8, fg_color=C["bg"], border_color=C["border2"],
              text_color=C["text"], placeholder_text_color=C["muted"], font=F_BODY)
    # si es passa show s'afegeix a la configuració del camp
    if show: kw["show"] = show
    # crea el camp amb la configuració preparada
    e = ctk.CTkEntry(parent, **kw)
    e.pack(padx=18, pady=(2,0))
    # retorna el widget per poder llegir o modificar el valor
    return e

# crea un desplegable amb etiqueta i valors disponibles
def dropdown(parent, label, values, width=380):
    # etiqueta descriptiva del desplegable
    ctk.CTkLabel(parent, text=label, font=F_SMALL,
                 text_color=C["muted"]).pack(anchor="w", padx=18, pady=(6,0))
    # variable associada al desplegable amb el primer valor com a predeterminat
    v = ctk.StringVar(value=values[0])
    # menú desplegable amb colors adaptats al tema de l'aplicació
    ctk.CTkOptionMenu(parent, values=values, variable=v, width=width, height=38,
                      corner_radius=8, fg_color=C["bg"],
                      button_color=C["accent"], button_hover_color=C["accent_h"],
                      dropdown_fg_color=C["card"], text_color=C["text"],
                      font=F_BODY).pack(padx=18, pady=(2,0))
    # retorna la variable per consultar la selecció actual
    return v

# crea un botó principal per a accions positives o habituals
def btn_primary(parent, text, cmd, width=380, color=None):
    # utilitza el color rebut o el color accent de la paleta
    b = ctk.CTkButton(parent, text=text, command=cmd,
                      fg_color=color or C["accent"], hover_color=C["accent_h"],
                      width=width, height=40, corner_radius=9,
                      font=font(13, bold=True), text_color="#ffffff")
    b.pack(padx=18, pady=(14,4))
    # retorna el botó per si cal canviar-ne l'estat més endavant
    return b

# crea un botó de perill per a accions destructives o delicades
def btn_danger(parent, text, cmd, width=380):
    # aplica els colors de perill de la paleta
    b = ctk.CTkButton(parent, text=text, command=cmd,
                      fg_color=C["danger"], hover_color=C["danger_h"],
                      width=width, height=40, corner_radius=9,
                      font=font(13, bold=True), text_color="#ffffff")
    b.pack(padx=18, pady=(6,4))
    # retorna el botó per poder gestionar-lo des de la pantalla
    return b

# crea una etiqueta buida preparada per mostrar missatges d'estat
def status_lbl(parent):
    l = ctk.CTkLabel(parent, text="", font=F_SMALL, text_color=C["green"])
    l.pack(padx=18, pady=(4,14))
    return l

# mostra un missatge d'èxit dins una etiqueta d'estat
def ok(lbl, msg="✓  Operació completada"):
    lbl.configure(text=msg, text_color=C["green"])

# mostra un missatge d'error dins una etiqueta d'estat
def err(lbl, msg):
    lbl.configure(text=f"✗  {msg}", text_color=C["danger"])

# crea una caixa de text gran per mostrar o editar contingut llarg
def textbox(parent, width=540, height=220):
    return ctk.CTkTextbox(parent, width=width, height=height,
                          fg_color=C["bg"], text_color=C["text2"],
                          font=F_MONO, corner_radius=8,
                          border_width=1, border_color=C["border"])

# crea una etiqueta de secció en majúscules per separar blocs de contingut
def section_lbl(parent, text):
    ctk.CTkLabel(parent, text=text.upper(),
                 font=font(10, bold=True), text_color=C["muted"]).pack(
        anchor="w", padx=24, pady=(16,4))
