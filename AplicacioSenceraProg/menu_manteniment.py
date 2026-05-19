import customtkinter as ctk #importem el customtkinter per al menu grafic
from tkcalendar import DateEntry #importem la entrada de dates, un selector per a entrar coma dada la data de forma mes simple
from db import connectar #importem la conexió amb la base de dades
import consultes #importem el .py de consultes
import json #importem json per a l'exportació de dades en json

# de igual forma amb el xml, per a l'exportació de dades:
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tkinter import filedialog


# paleta de colors del menu:
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
PURPLE  = "#a78bfa"
DANGER  = "#f87171"
DANGERH = "#dc2626"
TEXT    = "#f0f4ff"
TEXT2   = "#e0e8ff"
SUB     = "#8ca0c4"
MUTED   = "#4a6080"

#funcions per a facilitar la generacio del menu:
#primer per a generar un label gracies a la funcio amb dades predefinides
def _lbl(parent, text, size=12, bold=False, color=None, **kw):
    return ctk.CTkLabel(parent, text=text, text_color=color or TEXT2,
                        font=("Arial", size, "bold" if bold else "normal"), **kw)

#generar un entry amb dades predefinides
def _entry(parent, placeholder="", show=None, width=340):
    kw = dict(placeholder_text=placeholder, width=width, height=36,
              corner_radius=7, fg_color=SIDEBAR, border_color=BORDER2,
              text_color=TEXT2, placeholder_text_color=MUTED,
              font=("Arial", 12))
    if show: kw["show"] = show
    return ctk.CTkEntry(parent, **kw)

#de igual forma amb el boto
def _btn(parent, text, cmd, color=ACCENT, hover=ACCH, width=320):
    return ctk.CTkButton(parent, text=text, command=cmd,
                         fg_color=color, hover_color=hover,
                         width=width, height=38, corner_radius=8,
                         font=("Arial", 12, "bold"), text_color="#ffffff")

#canviar el boto de color a vermell
def _btn_danger(parent, text, cmd, width=320):
    return _btn(parent, text, cmd, color=DANGER, hover=DANGERH, width=width)

#per a crear la seccio de dades, tant com mostrar o inserir-hi
def _sep(parent):
    ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=(8, 10))
def _section(parent, text, icon=""):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=16, pady=(14, 0))
    _lbl(f, f"{icon}  {text}" if icon else text, size=13, bold=True, color=SUB).pack(side="left")
    _sep(parent)

# per a crear de forma facil de forma conjunta el lbl i entry de algunes dades dels menus.
def _field(parent, label, placeholder="", show=None, width=340):
    _lbl(parent, label, size=11, color=MUTED).pack(anchor="w", padx=16, pady=(6, 0))
    e = _entry(parent, placeholder, show, width)
    e.pack(padx=16, pady=(2, 0))
    return e

#label per a mostrar errors o esdeveniments dins el programa
def _status(parent):
    l = ctk.CTkLabel(parent, text="", font=("Arial", 11),
                     text_color=GREEN, wraplength=400, justify="left")
    l.pack(anchor="w", padx=16, pady=(6, 12))
    return l

#funcio per a mostrar que s'ha fet de forma correcte
def _ok(lbl, msg="✓  Operació completada"):
    lbl.configure(text=msg, text_color=GREEN)

#funcio per a mostrar que no s'ha fet de forma correcte
def _err(lbl, msg):
    lbl.configure(text=f"✗  {msg}", text_color=DANGER)

#funcio per a generar un textbox
def _textbox(parent, width=500, height=220):
    return ctk.CTkTextbox(parent, width=width, height=height,
                          fg_color=SIDEBAR, text_color=TEXT2,
                          font=("Courier New", 11), corner_radius=8,
                          border_width=1, border_color=BORDER)

#funcio per a crear un entry de una data
def _cal(parent):
    return DateEntry(parent, date_pattern="yyyy-mm-dd",
                     background=CARD, foreground=TEXT2,
                     borderwidth=1, relief="flat",
                     selectbackground=ACCENT, font=("Arial", 11))



#panells amb continguts
#panell de alta pacient, demana dades generals dels pacients i els afegeix dins la base de dades
def _panel_alta_pacient(parent):
    scroll = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
    scroll.pack(fill="both", expand=True)

    _lbl(scroll, "Alta Pacient", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))
    _lbl(scroll, "Registra un nou pacient al sistema", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    card = ctk.CTkFrame(scroll, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16, pady=(0, 16))
    _section(card, "Dades del pacient", "👤")

    #aquests son els camps importants dels pacients
    camps = [("Nom", "Nom del pacient"), ("Cognoms", "Cognoms complets"),
             ("Telèfon", "Ex: 612 345 678"), ("Email", "exemple@correu.cat"),
             ("DNI", "Ex: 12345678A"), ("Data Naixement", "YYYY-MM-DD"),
             ("Targeta Sanitària", "Ex: XXXX1234567890")]
    entries = [_field(card, lbl, ph) for lbl, ph in camps]
    sl = _status(card)

    #guardarem les dades gracies a la alta del pacient dins de consultes.py
    def guardar():
        vals = [e.get().strip() for e in entries]
        if any(v == "" for v in vals):
            _err(sl, "Tots els camps són obligatoris"); return
        try:
            conn = connectar()
            consultes.alta_pacient_db(conn, vals)
            conn.close()
            _ok(sl, "✓  Pacient donat d'alta correctament")
            for e in entries: e.delete(0, "end")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "💾  Guardar pacient", guardar).pack(padx=16, pady=(4, 16))

#panell de alta personal
def _panel_alta_personal(parent):
    #com hi ha diferent tipus de personal, es demanaran dades diferents:
    _TIPUS_CAMPS = {
        "Metge":               [("Especialitat","Ex: Cardiologia"),("Currículum","Resum professional"),("Núm. Col·legiat","COL-12345")],
        "Infermer Planta":     [("Torn (M/T/N)","M=Matí T=Tarda N=Nit"),("Anys Experiència","Ex: 5"),("ID Planta","Num. planta")],
        "Infermer Metge":      [("Torn (M/T/N)","M=Matí T=Tarda N=Nit"),("Anys Experiència","Ex: 5"),("ID Metge","ID del metge")],
        "Vari/Administratiu":  [("Tipus Feina","Ex: Neteja"),("Horari","Ex: Dl-Dv 08-15h")],
    }
    _TIPUS_KEY = {
        "Metge":"metge","Infermer Planta":"infermer_planta",
        "Infermer Metge":"infermer_metge","Vari/Administratiu":"vari",
    }


    scroll = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
    scroll.pack(fill="both", expand=True)

    _lbl(scroll, "Alta Personal", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))
    _lbl(scroll, "Registra nou personal mèdic o administratiu", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    cols = ctk.CTkFrame(scroll, fg_color="transparent")
    cols.pack(fill="x", padx=16)
    cols.columnconfigure(0, weight=1)
    cols.columnconfigure(1, weight=1)

    #columna de l'esquerra amb les dades per defecte que tenen tots els personals
    c_esq = ctk.CTkFrame(cols, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    c_esq.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
    _section(c_esq, "Dades personals", "👤")
    comuns_defs = [
        ("Nom","Nom"),("Cognom 1","Primer cognom"),("Cognom 2","Segon cognom"),
        ("DNI","12345678A"),("Data Naix. (YYYY-MM-DD)","1985-03-21"),
        ("Telèfon","612 345 678"),("Email","correu@hospital.cat"),("Adreça","Carrer, núm..."),
    ]
    entries_comuns = [_field(c_esq, lbl, ph, width=260) for lbl, ph in comuns_defs]

    #columna de la dreta, aquesta comporta informació de les dades especifiques de cada tipus de personal
    c_drt = ctk.CTkFrame(cols, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    c_drt.grid(row=0, column=1, padx=(6, 0), sticky="nsew")
    _section(c_drt, "Tipus de personal", "🩺")

    tipus_var = ctk.StringVar(value="Metge")
    _lbl(c_drt, "Categoria", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 2))
    ctk.CTkOptionMenu(c_drt, values=list(_TIPUS_CAMPS.keys()), variable=tipus_var,
                      width=260, height=36, corner_radius=7,
                      fg_color=SIDEBAR, button_color=ACCENT, button_hover_color=ACCH,
                      dropdown_fg_color=CARD, text_color=TEXT2,
                      font=("Arial", 12)).pack(padx=16, pady=(0, 6))

    extra_frame = ctk.CTkFrame(c_drt, fg_color="transparent")
    extra_frame.pack(fill="x")
    extra_entries = []

    #funcio per a actualitzar les dades especifiques si es canvia el tipus de personal
    def rebuild(*_):
        for w in extra_frame.winfo_children(): w.destroy()
        extra_entries.clear()
        for lbl, ph in _TIPUS_CAMPS.get(tipus_var.get(), []):
            extra_entries.append(_field(extra_frame, lbl, ph, width=260))

    tipus_var.trace_add("write", rebuild)
    rebuild()

    sl = _status(scroll)

    #funcio per a guardar amb la conexió a la base de dades i la funcio de consultes.py
    def guardar():
        comuns = [e.get().strip() for e in entries_comuns]
        extras = [e.get().strip() for e in extra_entries]
        if any(v == "" for v in comuns + extras):
            _err(sl, "Tots els camps són obligatoris"); return
        try:
            conn = connectar()
            res = consultes.alta_personal_db(conn, comuns, _TIPUS_KEY[tipus_var.get()], extras)
            conn.close()
            _ok(sl, f"✓  Personal donat d'alta (ID {res})")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(scroll, "💾  Guardar personal", guardar).pack(padx=16, pady=(8, 16))


#panell per a observar la dependencia de l'infermer
def _panel_dependencia(parent):
    _lbl(parent, "Dependència Infermeria", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Comprova a quin metge o planta està assignat un infermer", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Verificar assignació", "🔗")
    e = _field(card, "ID Infermer/a", "Introdueix l'identificador")
    sl = _status(card)

    #es comprova gracies a la vista a la base de dades i depenent del resultat es mostra un o altre tipus, si es que hi ha.
    def check():
        try:
            conn = connectar()
            res = consultes.check_dependencia_infermeria(conn, e.get().strip())
            conn.close()
            if res:
                if res["es_metge"]:
                    dep = "Metge"
                elif res["es_planta"]:
                    dep = "Planta"
                else:
                    dep = "Cap Lloc"
                _ok(sl, f"✓  {res['nom']} {res['cognom1']} → assignat/da a {dep}")
            else:
                _err(sl, "No s'ha trobat cap resultat")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "🔍  Verificar", check).pack(padx=16, pady=(4, 16))


#panell de operacions, es tracta de un panell per a mostrar les operacions que hi ha hagut aquell dia.
def _panel_operacions(parent):
    _lbl(parent, "Operacions per dia", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Selecciona data", "🔪")
    _lbl(card, "Data", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 2))
    cal = _cal(card)
    cal.pack(padx=16, anchor="w", pady=(0, 4))
    sl = _status(card)

    box = _textbox(parent, height=200)
    box.pack(padx=16, pady=(8, 16), fill="x")

    #un cop s'extreuen les dades de la consulta es mostraran en el textbox indicant quirofan, pacient, hora.
    def executar():
        box.delete("1.0", "end")
        box.insert("end", f"{'Hora':<12}{'Quiròfan':<18}{'Pacient'}\n{'─'*60}\n")
        try:
            conn = connectar()
            dades = consultes.carregar_operacions_dia(conn, cal.get_date())
            conn.close()
            for r in dades:
                box.insert("end", f"{str(r.get('hora','')):<12}{str(r.get('quirofan','')):<18}{r.get('pacient','')}\n")
            _ok(sl, f"✓  {len(dades)} operacions trobades")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "🔍  Consultar operacions", executar).pack(padx=16, pady=(0, 16))


#panell de visites es tracta per a observar les visites del dia indicat
def _panel_visites(parent):
    _lbl(parent, "Visites per dia", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Selecciona data", "📋")
    _lbl(card, "Data", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 2))
    cal = _cal(card)
    cal.pack(padx=16, anchor="w", pady=(0, 4))
    sl = _status(card)

    box = _textbox(parent, height=200)
    box.pack(padx=16, pady=(8, 16), fill="x")

    #extreurem les dades gracies a la consulta dins de consultes.py i mostrarem la hora, pacient i metge.
    def executar():
        box.delete("1.0", "end")
        box.insert("end", f"{'Hora':<12}{'Pacient':<28}{'Metge'}\n{'─'*60}\n")
        try:
            conn = connectar()
            dades = consultes.carregar_visites_del_dia(conn, cal.get_date())
            conn.close()
            for r in dades:
                box.insert("end", f"{str(r.get('hora_entrada','')):<12}{str(r.get('pacient','')):<28}{r.get('metge','')}\n")
            _ok(sl, f"✓  {len(dades)} visites trobades")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "🔍  Consultar visites", executar).pack(padx=16, pady=(0, 16))


# panell de invertat, per a observar els aparells que te cada quirofan.
def _panel_inventari(parent):
    _lbl(parent, "Inventari Aparells", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))
    sl = ctk.CTkLabel(parent, text="Carregant...", font=("Arial", 11), text_color=MUTED)
    sl.pack(anchor="w", padx=16, pady=(0, 6))

    box = _textbox(parent, height=300)
    box.pack(padx=16, fill="x")
    box.insert("end", f"{'Planta':<10}{'Quiròfan':<10}{'Aparell':<26}{'Marca':<18}{'Quantitat'}\n{'─'*68}\n")

    try:
        conn = connectar()
        res = consultes.consultar_inventari(conn)
        conn.close()
        for r in res:
            box.insert("end", f"{str(r.get('id_planta','')):<10}{str(r.get('num_quirofan','')):<10}{str(r.get('nom_aparell','')):<26}{str(r.get('marca','')):<18}{r.get('quantitat','')}\n")
        _ok(sl, f"✓  {len(res)} registres carregats")
    except Exception as ex:
        _err(sl, str(ex))

# panell de habitacions, serveix per a osbervar els ingressos que hi ha i hi ha hagut 
def _panel_habitacio(parent):
    _lbl(parent, "Habitacions", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Consulta per habitació", "🛏️")
    e = _field(card, "ID Habitació", "Introdueix l'identificador")
    sl = _status(card)

    box = _textbox(parent, height=200)
    box.pack(padx=16, pady=(8, 16), fill="x")

    def cercar():
        box.delete("1.0", "end")
        try:
            res = consultes.consultar_opcional_habitacio(connectar(), e.get().strip())
            if not res:
                _ok(sl, "No hi ha ingressos actius"); return
            _ok(sl, f"✓  {len(res)} ingrés/os trobats")
            for r in res:
                box.insert("end", f"Pacient: {r.get('pacient','—')}  |  Entrada: {r.get('data_ingres','—')}  |  Sortida_prevista: {r.get('data_sortida_prevista','—')}  |  Sortida_real: {r.get('data_sortida_real','—')}\n")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "🔍  Consultar", cercar).pack(padx=16, pady=(4, 16))


#panell de historial, indicant l'identificador del pacient observarem el total de visites, 
# els seus diagnostics, medicaments, total de ingressos i el total de les seves operacions
def _panel_historial(parent):
    _lbl(parent, "Historial Pacient", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Cerca per pacient", "📂")
    e = _field(card, "ID Pacient", "Introdueix l'identificador")
    sl = _status(card)

    box = _textbox(parent, height=180)
    box.pack(padx=16, pady=(8, 16), fill="x")

    def cercar():
        box.delete("1.0", "end")
        try:
            r = consultes.consultar_opcional_historial(connectar(), e.get().strip())
            if not r:
                _err(sl, "Pacient no trobat"); return
            _ok(sl, f"✓  Historial carregat")
            box.insert("end",
                f"Pacient:     {r.get('nom','')} {r.get('cognoms','')}\n"
                f"Visites:     {r.get('total_visites','—')}\n"
                f"Diagnòstics: {r.get('diagnostics','—')}\n"
                f"Medicaments:     {r.get('medicaments_receptats','—')}\n"
                f"Ingressos:     {r.get('total_ingressos','—')}\n"
                f"Operacions:     {r.get('total_operacions','—')}\n")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "🔍  Veure historial", cercar).pack(padx=16, pady=(4, 16))


#panell de programacio, de la data d'acui segun el metge indicat es podra observar les seves visites i operacions amb l'hora i pacient
#així també facilitara la seva forma de estructurar la seva agenda
def _panel_programacio(parent):
    _lbl(parent, "Programació Metges", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Consulta les visites i operacions d'un metge per dia", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Cerca per metge", "📅")

    e = _field(card, "ID Metge", "Introdueix l'identificador del metge")
    sl = _status(card)

    box = _textbox(parent, height=280)
    box.pack(padx=16, pady=(8, 16), fill="x")

    def cercar():
        box.delete("1.0", "end")
        id_metge = e.get().strip()
        if not id_metge:
            _err(sl, "Introdueix un ID de metge"); return
        try:
            conn = connectar()
            dades = consultes.consultar_programacio_metge_id(conn, id_metge)
            conn.close()
            if not dades:
                _err(sl, "No s'han trobat dades per aquest metge"); return

            # Capçalera
            box.insert("end", f"{'Data':<14}{'Tipus':<14}{'Hora':<12}{'Pacient'}\n{'─'*60}\n")
            for r in dades:
                box.insert("end",
                    f"{str(r.get('dia','')):<14}"
                    f"{str(r.get('tipus','')):<14}"
                    f"{str(r.get('hora','')):<12}"
                    f"{r.get('pacient','')}\n"
                )
            _ok(sl, f"✓  {len(dades)} registres trobats")
        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "🔍  Cercar", cercar).pack(padx=16, pady=(4, 16))

#panell de exportacio, es un menu on es pot seleccionar de que data a data s'exportaran les visites que estan a la base de dades
# en un json o xml, com es vulgui, per a importar-ho a serveis externs.
def _panel_exportacio(parent):

    _lbl(parent, "Exportació de Dades", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))

    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )
    card.pack(fill="x", padx=16)

    _section(card, "Exportar visites", "📤")

    _lbl(card, "Data inici", size=11, color=MUTED).pack(anchor="w", padx=16)

    data_inici = _cal(card)
    data_inici.pack(anchor="w", padx=16, pady=(0, 10))

    _lbl(card, "Data final", size=11, color=MUTED).pack(anchor="w", padx=16)

    data_final = _cal(card)
    data_final.pack(anchor="w", padx=16, pady=(0, 16))

    sl = _status(card)

    def obtenir_dades():

        conn = connectar()

        dades = consultes.exportar_visites(
            conn,
            data_inici.get_date(),
            data_final.get_date()
        )

        conn.close()

        resultat = []

        for r in dades:

            #aquest seria el la seva forma en json:
            #es pot verue l'esquema a visites.schema.json
            resultat.append({
                "id_visita": r[0],
                "dia": str(r[1]),
                "pacient": {
                    "dni": r[2],
                    "nom": r[3],
                    "cognoms": r[4],
                    "tarjeta_sanitaria": r[5]
                },
                "metge": f"{r[6]} {r[7]}",
                "especialitat": r[8]
            })

        return resultat

    def exportar_json():

        try:

            dades = obtenir_dades()

            ruta = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON", "*.json")]
            )

            if not ruta:
                return

            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(dades, f, indent=4, ensure_ascii=False)

            _ok(sl, "✓  JSON exportat correctament")

        except Exception as ex:
            _err(sl, str(ex))

    #exportacio en xml
    def exportar_xml():

        try:

            dades = obtenir_dades()

            #creació del xml, amb els seus elements i subelements
            root = ET.Element("visites")

            for visita in dades:

                visita_xml = ET.SubElement(root, "visita")

                ET.SubElement(visita_xml, "id_visita").text = str(visita["id_visita"])
                ET.SubElement(visita_xml, "dia").text = visita["dia"]

                pacient = ET.SubElement(visita_xml, "pacient")

                ET.SubElement(pacient, "dni").text = visita["pacient"]["dni"]
                ET.SubElement(pacient, "nom").text = visita["pacient"]["nom"]
                ET.SubElement(pacient, "cognoms").text = visita["pacient"]["cognoms"]
                ET.SubElement(pacient, "tarjeta_sanitaria").text = visita["pacient"]["tarjeta_sanitaria"]

                ET.SubElement(visita_xml, "metge").text = visita["metge"]

            xml_str = ET.tostring(root, encoding="utf-8")

            pretty = minidom.parseString(xml_str).toprettyxml(indent="\t")

            ruta = filedialog.asksaveasfilename(
                defaultextension=".xml",
                filetypes=[("XML", "*.xml")]
            )

            if not ruta:
                return

            with open(ruta, "w", encoding="utf-8") as f:
                f.write(pretty)

            _ok(sl, "✓  XML exportat correctament")

        except Exception as ex:
            _err(sl, str(ex))

    _btn(card, "📄 Exportar JSON", exportar_json, width=420).pack(padx=16, pady=(0, 8))

    _btn(card, "📰 Exportar XML", exportar_xml, width=420).pack(padx=16, pady=(0, 16))


#panell de dummy data, per a inserir dades no reals a la base de dades per a fer proves, també es podra borrar aquestes dades per si es el cas
def _panel_dummy(parent):
    import threading

    _lbl(parent, "Dummy Data", size=18, bold=True).pack(anchor="w", padx=16, pady=(16, 2))
    _lbl(parent, "Genera o elimina les dades de prova del sistema", size=11, color=MUTED).pack(anchor="w", padx=16, pady=(0, 8))

    card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12, border_width=1, border_color=BORDER)
    card.pack(fill="x", padx=16)
    _section(card, "Gestió de dades de prova", "⚗️")

    sl = _status(card)
    bar = ctk.CTkProgressBar(card, width=460, height=6, corner_radius=4,
                              fg_color=BORDER, progress_color=ACCENT)
    bar.set(0)
    bar.pack(padx=16, pady=(0, 10))

    def executar(tasca_nom, msg):
        _ok(sl, msg)
        sl.configure(text_color=AMBER)
        bar.start()

        def worker():
            try:
                from dummy_data import generar_dummy_data, eliminar_dummy_data #improtarem les funcions del dummy data
                #generarem o eliminarem les dades com sigui el cas:
                tasca = generar_dummy_data if tasca_nom == "generar" else eliminar_dummy_data
                resultat = tasca()
                parent.after(0, lambda: bar.stop())
                parent.after(0, lambda: bar.set(1))
                parent.after(0, lambda: _ok(sl, f"✓  {resultat}"))
            except Exception as ex:
                parent.after(0, lambda: bar.stop())
                parent.after(0, lambda e=ex: _err(sl, str(e)))

        threading.Thread(target=worker, daemon=True).start()

    _btn(card, "▶  Generar dummy data", lambda: executar("generar", "Generant..."), width=440).pack(padx=16, pady=(0, 6))
    _btn_danger(card, "🗑  Eliminar dummy data", lambda: executar("eliminar", "Eliminant..."), width=440).pack(padx=16, pady=(0, 16))


# moduls ordenats que es mostraran dins l'aplicatiu
_MODULS = [
    ("Alta Pacient",        "👤", ACCENT,  _panel_alta_pacient),
    ("Alta Personal",       "🩺", TEAL,    _panel_alta_personal),
    ("Dependència",         "🔗", PURPLE,  _panel_dependencia),
    ("Operacions",          "🔪", AMBER,   _panel_operacions),
    ("Visites",             "📋", GREEN,   _panel_visites),
    ("Inventari",           "🏥", TEAL,    _panel_inventari),
    ("Habitacions",         "🛏️", ACCENT,  _panel_habitacio),
    ("Historial Pacient",   "📂", PURPLE,  _panel_historial),
    ("Prog. Metges",        "📅", AMBER,   _panel_programacio),
    ("Dummy Data",          "⚗️", DANGER,  _panel_dummy),
    ("Exportació",          "📤", TEAL,    _panel_exportacio)
]


# funcio al obrir el menude manteniment desde el menu principal
def obrir_manteniment():
    ctk.set_appearance_mode("dark")
    win = ctk.CTkToplevel()
    win.title("Bloc de Manteniment")
    win.geometry("1100x680")
    win.minsize(900, 560)
    win.configure(fg_color=BG)
    win.lift()
    win.focus_force()

    # la topbat
    topbar = ctk.CTkFrame(win, fg_color="#0a1120", corner_radius=0, height=52)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)
    _lbl(topbar, "⚙️  Bloc de Manteniment", size=17, bold=True).pack(side="left", padx=20, pady=14)
    ctk.CTkButton(topbar, text="✕  Tancar", command=win.destroy,
                  fg_color="transparent", hover_color=CARD2,
                  text_color=MUTED, border_color=BORDER2, border_width=1,
                  width=90, height=30, corner_radius=7,
                  font=("Arial", 11)).pack(side="right", padx=16, pady=11)

    #Layout principal: sidebar + contingut
    main = ctk.CTkFrame(win, fg_color="transparent")
    main.pack(fill="both", expand=True)

    # barra lateral
    sidebar = ctk.CTkFrame(main, fg_color=SIDEBAR, corner_radius=0, width=200,
                           border_width=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    ctk.CTkLabel(sidebar, text="MÒDULS", font=("Arial", 9, "bold"),
                 text_color=MUTED).pack(anchor="w", padx=16, pady=(16, 6))

    #contingut on es mostra el texte
    content_wrapper = ctk.CTkFrame(main, fg_color=BG, corner_radius=0)
    content_wrapper.pack(side="left", fill="both", expand=True)

    content_area = ctk.CTkScrollableFrame(content_wrapper, fg_color=BG, corner_radius=0)
    content_area.pack(fill="both", expand=True)

    active_btn = [None]

    #carregar el panell esquerra amb tots els panells disponibles
    def carregar_panel(build_fn, btn):
        # Ressaltar botó actiu
        if active_btn[0]:
            active_btn[0].configure(fg_color="transparent", text_color=SUB)
        btn.configure(fg_color=CARD2, text_color=TEXT)
        active_btn[0] = btn

        # Netejar contingut anterior
        for w in content_area.winfo_children():
            w.destroy()

        # Construir nou panell
        build_fn(content_area)

    # Crear botons de la sidebar
    sidebar_btns = []
    for nom, icon, color, build_fn in _MODULS:
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

    # Carregar el primer mòdul per defecte
    carregar_panel(sidebar_btns[0][1], sidebar_btns[0][0])