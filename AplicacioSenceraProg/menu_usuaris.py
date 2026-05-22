import customtkinter as ctk #importem el customtkinter per a la seva visualització
from db import connectar #importem la conexió amb la base de dades

import os, sys
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

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
#menu de gestio d'usuaris, esta incorporat per 
def gestio_usuaris():
    C = COLORS
    g = ctk.CTkToplevel()
    g.title("Gestió d'usuaris")
    g.geometry("460x520")
    g.configure(fg_color=C["bg_dark"])
    g.lift()
    g.focus_force()
    icon_path = resource_path(os.path.join("logo", "logo.ico"))
    g.after(201, lambda: g.iconbitmap(icon_path))
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

    # Frame del contingut on s'afegeixen i es veuen les dades
    content = ctk.CTkFrame(g, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    # això significa el boto principal que es mostrara al entrar al menu
    active_tab = [None]

    #aquesta funcio es per a generar a la del selector de pestanya cada boto, (per cada boto es truca aquesta funcio)
    def _tab_btn(text, cmd):
        b = ctk.CTkButton(tab_frame, text=text, width=0, height=34,
                        fg_color=C["bg_card"], hover_color=C["bg_card2"],
                        text_color=C["text_sub"], border_color=C["border"],
                        border_width=1, corner_radius=8,
                        font=ctk.CTkFont(size=12))
        b.pack(side="left", padx=(0, 6))
        b.configure(command=lambda: _activate(b, cmd))
        return b
    
    #aquesta funcio serveix per a canvia el boto actiu, si es que ja n'hi habia
    #basicament canvia els colors y mostra el nou contingut de la pestanya
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

    # es una funcio per a mostrar en si els errors o accions fetes malament, es veura durant el codi
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

        #primer el nom de l'usuari, amb lbl, entry
        ctk.CTkLabel(card, text="Nom d'usuari", font=ctk.CTkFont(size=11),
                    text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(16, 2))
        e_user = ctk.CTkEntry(card, placeholder_text="Nom d'usuari",
                            width=380, height=42, corner_radius=10,
                            fg_color=C["bg_card2"], border_color=C["border"],
                            text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_user.pack(padx=20, pady=(0, 8))

        #seguidament de la contrasenya de l'usuari, a l'hora de registrar-ho se l'hi aplica el hash
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

        #rols que es poden seleccionar:
        _ROLS = [
            ("admin",    "🔑  Administrador", C["accent"]),
            ("metge",    "🩺  Metge",         C["accent2"]),
            ("infermer", "👩‍⚕️  Infermer/a",   C["accent3"]),
        ]
        rol_var = ctk.StringVar(value="metge")  # rol seleccionat per defecte
        rol_frame = ctk.CTkFrame(card, fg_color="transparent")
        rol_frame.pack(anchor="w", padx=20, pady=(0, 10))
        rol_btns = {}

        #funcio per a actualitzar l'apareça del boto actualitzat.
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

        #per cada rol afegirem cada boto, amb la funció de canviar la seva aparença.
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

        #registrar un nou usuari
        def registrar():
            nom = e_user.get().strip()
            pwd = e_pass.get().strip()
            rol_sel = rol_var.get()
            if not nom or not pwd:
                sl.configure(text="⚠️  Tots els camps són obligatoris",
                            text_color=C["accent4"]); return
            try:
                import autentificacio
                # de la funcio del .py d'autentificacio crearem el hash:
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
                    
                    #rols permesos com a usuari per a afegir-lo com a create role.
                    rols_permesos = {'metge', 'infermer', 'admin'}
                    if rol_sel not in rols_permesos:
                        raise ValueError(f"Rol no permès: {rol_sel}")
                    if rol_sel == 'metge':
                        rol = 'metge_role'
                    elif rol_sel == 'admin':
                        rol = 'admin_role'
                    elif rol_sel == 'infermer':
                        rol = 'infermer_role'
                    
                    #cridem a la funcio per a poder afegir el rol dins la base de dades.
                    cur.execute("SELECT dades_per.crear_rol(%s, %s, %s)", (nom, pwd, rol))
                    conn.commit()
                conn.close()

                #indiquem a l'usuari que s'ha creat l'usuari
                sl.configure(text=f"✅  Usuari '{nom}' creat com a {rol_sel}",
                            text_color=C["accent3"])
                e_user.delete(0, "end")
                e_pass.delete(0, "end")
            except Exception as ex:
                sl.configure(text=f"❌  {ex}", text_color=C["danger"])
            
        # aquest es el boto que crea l'usuari
        ctk.CTkButton(card, text="Crear usuari", command=registrar,
                    fg_color=C["accent"], hover_color=C["accent2"],
                    width=380, height=42, corner_radius=10,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#ffffff").pack(padx=20, pady=(4, 20))

    # funcio per a canviar la contrasenya de l'usuari
    def tab_canviar_password():
        card = ctk.CTkFrame(content, fg_color=C["bg_card"], corner_radius=14,
                            border_width=1, border_color=C["border"])
        card.pack(fill="x")

        # nom de l'usuari a modificar
        ctk.CTkLabel(card, text="Nom d'usuari", font=ctk.CTkFont(size=11),
                    text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(16, 2))
        e_user = ctk.CTkEntry(card, placeholder_text="Usuari a modificar",
                            width=380, height=42, corner_radius=10,
                            fg_color=C["bg_card2"], border_color=C["border"],
                            text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_user.pack(padx=20, pady=(0, 8))

        #nova contrasenya de l'usuari
        ctk.CTkLabel(card, text="Nova contrasenya", font=ctk.CTkFont(size=11),
                    text_color=C["text_sub"]).pack(anchor="w", padx=20, pady=(0, 2))
        e_pass = ctk.CTkEntry(card, placeholder_text="Nova contrasenya", show="*",
                            width=380, height=42, corner_radius=10,
                            fg_color=C["bg_card2"], border_color=C["border"],
                            text_color=C["text_main"], font=ctk.CTkFont(size=13))
        e_pass.pack(padx=20, pady=(0, 8))

        #repetir la contrasenya de l'usuari
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

        #funcio per a canviar la contrasenya:
        def canviar():
            nom = e_user.get().strip()
            pwd = e_pass.get().strip()
            confirm = e_confirm.get().strip()

            #filtrem per assegurar les dades
            if not nom or not pwd or not confirm:
                sl.configure(text="⚠️  Tots els camps són obligatoris",
                            text_color=C["accent4"]); return
            if pwd != confirm:
                sl.configure(text="❌  Les contrasenyes no coincideixen",
                            text_color=C["danger"]); return
            try:
                import autentificacio

                #apliquem el hash a la contrasenya
                hashed = autentificacio.hash_contrasenya(pwd)
                conn = connectar()

                #apliquem les consultes necesaries
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE seguretat.usuari SET password = %s WHERE username = %s",
                        (hashed, nom)
                    )

                    #apliquem la funcio per actualitzar la contrasenya aplicada al .sql
                    cur.execute("SELECT dades_per.actualitzar_contrasenya(%s, %s)", (nom, pwd))
                    if cur.rowcount == 0:
                        sl.configure(text="❌  Usuari no trobat", text_color=C["danger"])
                    else:
                        #indiquem a l'usuari que ja s'ha canviar la contrasenya
                        conn.commit()
                        sl.configure(text="✅  Contrasenya actualitzada correctament",
                                    text_color=C["accent3"])
                        e_user.delete(0, "end")
                        e_pass.delete(0, "end")
                        e_confirm.delete(0, "end")
                conn.close()
            except Exception as ex:
                sl.configure(text=f"❌  {ex}", text_color=C["danger"])

        #boto per a canviar la contrasenya
        ctk.CTkButton(card, text="Canviar contrasenya", command=canviar,
                    fg_color=C["accent3"], hover_color="#059669",
                    width=380, height=42, corner_radius=10,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="#ffffff").pack(padx=20, pady=(4, 20))

    # Crear les pestanyes
    b1 = _tab_btn("➕  Nou usuari", tab_nou_usuari)
    b2 = _tab_btn("🔑  Canviar contrasenya", tab_canviar_password)
    # acplicar la primera pestanya
    _activate(b1, tab_nou_usuari)