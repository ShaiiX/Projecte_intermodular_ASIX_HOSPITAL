"""Paleta i helpers compartits. Importar: from moduls._estil import *"""
import customtkinter as ctk

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

def font(size=12, bold=False, mono=False):
    fam = "Courier New" if mono else "Arial"
    return (fam, size, "bold") if bold else (fam, size)

F_TITLE = ("Arial", 18, "bold")
F_CARD  = ("Arial", 13, "bold")
F_BODY  = ("Arial", 12)
F_SMALL = ("Arial", 11)
F_MONO  = ("Courier New", 12)

def setup(win, titol, mida="620x560"):
    ctk.set_appearance_mode("dark")
    win.title(titol)
    win.geometry(mida)
    win.configure(fg_color=C["bg"])

def topbar(parent, titol, icon="🏥", back_cmd=None, breadcrumbs=None):
    bar = ctk.CTkFrame(parent, fg_color=C["topbar"], corner_radius=0, height=52)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    left = ctk.CTkFrame(bar, fg_color="transparent")
    left.pack(side="left", fill="y", padx=16)
    ctk.CTkLabel(left, text=f"{icon}  {titol}", font=F_TITLE,
                 text_color=C["text"]).pack(side="left", pady=14)
    if breadcrumbs:
        ctk.CTkLabel(left, text=" › ", font=F_SMALL,
                     text_color=C["muted"]).pack(side="left")
        for i, (lbl, cmd) in enumerate(breadcrumbs):
            is_last = i == len(breadcrumbs) - 1
            color = C["text2"] if is_last else C["sub"]
            l = ctk.CTkLabel(left, text=lbl, font=F_SMALL,
                             text_color=color, cursor="arrow" if is_last else "hand2")
            l.pack(side="left")
            if cmd: l.bind("<Button-1>", lambda e, c=cmd: c())
            if not is_last:
                ctk.CTkLabel(left, text=" › ", font=F_SMALL,
                             text_color=C["muted"]).pack(side="left")
    if back_cmd:
        ctk.CTkButton(bar, text="← Enrere", command=back_cmd,
                      fg_color="transparent", hover_color=C["card2"],
                      text_color=C["sub"], border_color=C["border2"],
                      border_width=1, width=100, height=30, corner_radius=7,
                      font=F_SMALL).pack(side="right", padx=16, pady=11)
    return bar

def mk_card(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=12,
                        border_width=1, border_color=C["border"], **kw)

def card_section(parent, text, icon=""):
    inner = ctk.CTkFrame(parent, fg_color="transparent")
    inner.pack(fill="x", padx=18, pady=(14, 0))
    ctk.CTkLabel(inner, text=f"{icon}  {text}" if icon else text,
                 font=F_CARD, text_color=C["sub"]).pack(side="left")
    ctk.CTkFrame(parent, fg_color=C["border"], height=1).pack(
        fill="x", padx=18, pady=(8, 10))

def field(parent, label, placeholder="", show=None, width=380):
    ctk.CTkLabel(parent, text=label, font=F_SMALL,
                 text_color=C["muted"]).pack(anchor="w", padx=18, pady=(6,0))
    kw = dict(placeholder_text=placeholder, width=width, height=38,
              corner_radius=8, fg_color=C["bg"], border_color=C["border2"],
              text_color=C["text"], placeholder_text_color=C["muted"], font=F_BODY)
    if show: kw["show"] = show
    e = ctk.CTkEntry(parent, **kw)
    e.pack(padx=18, pady=(2,0))
    return e

def dropdown(parent, label, values, width=380):
    ctk.CTkLabel(parent, text=label, font=F_SMALL,
                 text_color=C["muted"]).pack(anchor="w", padx=18, pady=(6,0))
    v = ctk.StringVar(value=values[0])
    ctk.CTkOptionMenu(parent, values=values, variable=v, width=width, height=38,
                      corner_radius=8, fg_color=C["bg"],
                      button_color=C["accent"], button_hover_color=C["accent_h"],
                      dropdown_fg_color=C["card"], text_color=C["text"],
                      font=F_BODY).pack(padx=18, pady=(2,0))
    return v

def btn_primary(parent, text, cmd, width=380, color=None):
    b = ctk.CTkButton(parent, text=text, command=cmd,
                      fg_color=color or C["accent"], hover_color=C["accent_h"],
                      width=width, height=40, corner_radius=9,
                      font=font(13, bold=True), text_color="#ffffff")
    b.pack(padx=18, pady=(14,4))
    return b

def btn_danger(parent, text, cmd, width=380):
    b = ctk.CTkButton(parent, text=text, command=cmd,
                      fg_color=C["danger"], hover_color=C["danger_h"],
                      width=width, height=40, corner_radius=9,
                      font=font(13, bold=True), text_color="#ffffff")
    b.pack(padx=18, pady=(6,4))
    return b

def status_lbl(parent):
    l = ctk.CTkLabel(parent, text="", font=F_SMALL, text_color=C["green"])
    l.pack(padx=18, pady=(4,14))
    return l

def ok(lbl, msg="✓  Operació completada"):
    lbl.configure(text=msg, text_color=C["green"])

def err(lbl, msg):
    lbl.configure(text=f"✗  {msg}", text_color=C["danger"])

def textbox(parent, width=540, height=220):
    return ctk.CTkTextbox(parent, width=width, height=height,
                          fg_color=C["bg"], text_color=C["text2"],
                          font=F_MONO, corner_radius=8,
                          border_width=1, border_color=C["border"])

def section_lbl(parent, text):
    ctk.CTkLabel(parent, text=text.upper(),
                 font=font(10, bold=True), text_color=C["muted"]).pack(
        anchor="w", padx=24, pady=(16,4))