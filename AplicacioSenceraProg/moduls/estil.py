# ── Paleta compartida per tots els mòduls ────────────────────────────────────
C = {
    "bg":        "#0f1623",
    "card":      "#1a2236",
    "card2":     "#1e2a40",
    "accent":    "#3b82f6",
    "accent2":   "#06b6d4",
    "accent3":   "#10b981",
    "accent4":   "#f59e0b",
    "danger":    "#ef4444",
    "text":      "#f0f4ff",
    "sub":       "#8ca0c4",
    "border":    "#2a3a5c",
}

FONT_TITLE  = ("Georgia", 20, "bold")
FONT_LABEL  = ("Georgia", 13)
FONT_SMALL  = ("Georgia", 11)
FONT_MONO   = ("Courier New", 12)

import customtkinter as ctk

def aplicar_estil_finestra(win, titol, mida="600x500"):
    """Configura fons i títol d'una CTkToplevel."""
    win.title(titol)
    win.geometry(mida)
    win.configure(fg_color=C["bg"])
    ctk.set_appearance_mode("dark")


def frame_card(parent, **kw):
    return ctk.CTkFrame(
        parent,
        fg_color=C["card"],
        corner_radius=14,
        border_width=1,
        border_color=C["border"],
        **kw,
    )


def label_titol(parent, text):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(family="Georgia", size=20, weight="bold"),
        text_color=C["text"],
    )


def label_sub(parent, text):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=12),
        text_color=C["sub"],
    )


def entry_estilitzat(parent, placeholder="", show=None, width=300):
    kw = dict(
        placeholder_text=placeholder,
        width=width,
        height=40,
        corner_radius=10,
        fg_color=C["card2"],
        border_color=C["border"],
        text_color=C["text"],
        placeholder_text_color=C["sub"],
    )
    if show:
        kw["show"] = show
    return ctk.CTkEntry(parent, **kw)


def boto_primari(parent, text, command, color=None, width=200):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=color or C["accent"],
        hover_color=C["accent2"],
        width=width,
        height=42,
        corner_radius=10,
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#ffffff",
    )


def boto_perill(parent, text, command, width=200):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=C["danger"],
        hover_color="#b91c1c",
        width=width,
        height=42,
        corner_radius=10,
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#ffffff",
    )


def textbox_resultat(parent, width=520, height=260):
    return ctk.CTkTextbox(
        parent,
        width=width,
        height=height,
        fg_color=C["card2"],
        text_color=C["text"],
        font=ctk.CTkFont(family="Courier New", size=12),
        corner_radius=10,
        border_width=1,
        border_color=C["border"],
    )


def separator(parent):
    return ctk.CTkFrame(parent, fg_color=C["border"], height=1)