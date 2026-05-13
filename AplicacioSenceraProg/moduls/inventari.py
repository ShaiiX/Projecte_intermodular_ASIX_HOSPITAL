import customtkinter as ctk
from db import connectar
import consultes
from estil import *


def menu_inventari():
    f = ctk.CTkToplevel()
    f.lift()
    f.focus_force()
    f.attributes("-topmost", True)
    setup(f, "Inventari Aparells", "620x480")
    topbar(f, "Inventari", icon="🏥", back_cmd=f.destroy,
           breadcrumbs=[("Manteniment", None), ("Inventari", None)])

    body = ctk.CTkFrame(f, fg_color=C["bg"], corner_radius=0)
    body.pack(fill="both", expand=True, padx=20, pady=16)

    sl = ctk.CTkLabel(body, text="Carregant...", font=F_SMALL, text_color=C["muted"])
    sl.pack(anchor="w", pady=(0, 8))

    box = textbox(body, width=580, height=340)
    box.pack()

    # Capçalera de la taula
    box.insert("end", f"{'Quiròfan':<12}{'Aparell':<28}{'Marca':<20}{'Quantitat'}\n")
    box.insert("end", "─" * 72 + "\n")

    try:
        conn = connectar()
        res = consultes.consultar_inventari(conn)
        conn.close()
        for r in res:
            box.insert("end",
                f"{str(r.get('num_quirofan','')):<12}"
                f"{str(r.get('nom_aparell','')):<28}"
                f"{str(r.get('marca','')):<20}"
                f"{r.get('quantitat','')}\n")
        ok(sl, f"✓  {len(res)} registres carregats")
    except Exception as ex:
        err(sl, str(ex))