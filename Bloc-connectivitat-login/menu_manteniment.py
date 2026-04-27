import customtkinter as ctk
from tkinter import messagebox
from db import connectar
import consultes  
from tkcalendar import DateEntry

def obrir_manteniment():
    app = ctk.CTk()
    app.title("Bloc de Manteniment")
    app.geometry("500x600")

    ctk.CTkLabel(app, text="Bloc de Manteniment", font=("Arial", 24, "bold")).pack(pady=20)
    
    # Botons originals
    btns = [
        ("Alta Personal", menu_alta_personal),
        ("Alta Pacient", menu_alta_pacient),
        ("Dependència Infermeria", menu_dependencia),
        ("Operacions per dia", menu_operacions),
        ("Visites per dia", menu_visites),
        ("Inventari Aparells", menu_inventari),
        ("Habitacions", menu_habitacio),
        ("Historial Pacient", menu_historial),
        ("Programació Metges", menu_programacio_metges)
    ]
    for text, cmd in btns:
        ctk.CTkButton(app, text=text, width=300, command=cmd).pack(pady=10)
    app.mainloop()

def menu_alta_personal():
    f = ctk.CTkToplevel()
    f.title("Alta Personal")
    f.geometry("500x750")

    # --- 1. Datos Comunes ---
    ctk.CTkLabel(f, text="Dades Personals", font=("Arial", 16, "bold")).pack(pady=10)
    labels = ["Nom", "Cognom1", "Cognom2", "DNI", "Data Nasc (YYYY-MM-DD)", "Tel", "Email", "Dir"]
    entries_comuns = []
    for l in labels:
        ctk.CTkLabel(f, text=l).pack()
        e = ctk.CTkEntry(f, width=350)
        e.pack()
        entries_comuns.append(e)

    # --- 2. Campos Dinámicos ---
    ctk.CTkLabel(f, text="Tipus de Personal", font=("Arial", 16, "bold")).pack(pady=15)
    
    extra_frame = ctk.CTkFrame(f)
    extra_frame.pack(pady=10, fill="x", padx=20)
    extra_entries = []

    def canvi_tipus(seleccion):
        # Limpiar campos anteriores
        for widget in extra_frame.winfo_children():
            widget.destroy()
        extra_entries.clear()
        
        if seleccion == "Metge":
            for txt in ["Especialitat", "Currículum", "Num Colegiat"]:
                ctk.CTkLabel(extra_frame, text=txt).pack()
                e = ctk.CTkEntry(extra_frame, width=300)
                e.pack()
                extra_entries.append(e)
        elif seleccion == "Infermer Planta":
            for txt in ["Torn (M/T/N)", "Anys Experiència", "ID Planta"]:
                ctk.CTkLabel(extra_frame, text=txt).pack()
                e = ctk.CTkEntry(extra_frame, width=300)
                e.pack()
                extra_entries.append(e)

    # El Selector (que faltaba en tu código)
    selector = ctk.CTkOptionMenu(f, values=["Selecciona...", "Metge", "Infermer Planta"], command=canvi_tipus)
    selector.pack(pady=10)

    # --- 3. Botón Guardar ---
    def guardar():
        if selector.get() == "Selecciona...":
            messagebox.showwarning("Atenció", "Selecciona un tipus de personal")
            return
            
        comuns = [e.get() for e in entries_comuns]
        extras = [e.get() for e in extra_entries]
        
        res = consultes.alta_personal_completa(connectar(), selector.get(), comuns, extras)
        
        if res is True:
            messagebox.showinfo("Èxit", "Personal donat d'alta correctament")
            f.destroy()
        else:
            messagebox.showerror("Error", f"No s'ha pogut realitzar l'alta: {res}")

    ctk.CTkButton(f, text="Guardar Personal", fg_color="green", command=guardar).pack(pady=20)

    selector = ctk.CTkOptionMenu(f, values=["Metge", "Infermer Planta"], command=canvi_tipus)
    selector.pack(pady=10)

    def guardar():
        res = consultes.alta_personal_completa(connectar(), selector.get(), 
                                           [e.get() for e in entries_comuns], 
                                           [e.get() for e in extra_entries])
        if res is True: messagebox.showinfo("OK", "Personal inserit!")
        else: messagebox.showerror("Error", res)

    ctk.CTkButton(f, text="Guardar tot", command=guardar).pack(pady=20)

def menu_habitacio():
    f = ctk.CTkToplevel()
    f.geometry("500x400")
    ent = ctk.CTkEntry(f, placeholder_text="ID Habitació"); ent.pack(pady=10)
    box = ctk.CTkTextbox(f, width=450, height=250); box.pack()

    def cercar():
        box.delete("1.0", "end")
        res = consultes.consultar_opcional_habitacio(connectar(), ent.get())
        for r in res:
            box.insert("end", f"Pacient: {r['pacient']} | Entrada: {r['data_ingres']}\n")
    ctk.CTkButton(f, text="Consultar Opcional", command=cercar).pack()

def menu_historial():
    f = ctk.CTkToplevel()
    f.geometry("500x400")
    ent = ctk.CTkEntry(f, placeholder_text="ID Pacient"); ent.pack(pady=10)
    box = ctk.CTkTextbox(f, width=450, height=250); box.pack()

    def cercar():
        box.delete("1.0", "end")
        r = consultes.consultar_opcional_historial(connectar(), ent.get())
        if r: box.insert("end", f"PACIENT: {r['nom']} {r['cognoms']}\nVisites: {r['total_visites']}\nDiagnostics: {r['diagnostics']}")
    ctk.CTkButton(f, text="Veure Historial", command=cercar).pack()

def menu_programacio_metges():
    f = ctk.CTkToplevel()
    f.title("Programació de Metges")
    f.geometry("600x450")

    ctk.CTkLabel(f, text="Càrrega de treball per Metge", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Cuadro de texto para mostrar los resultados
    box = ctk.CTkTextbox(f, width=550, height=300)
    box.pack(pady=10, padx=10)

    def cargar_datos():
        box.delete("1.0", "end")
        conn = connectar()
        # Llamada a la lógica del opcional 3
        dades = consultes.consultar_programacio_metge(conn)
        
        if not dades:
            box.insert("end", "No hi ha dades de programació disponibles.")
        else:
            header = f"{'METGE':<30} | {'VISITES':<10} | {'OPERACIONS':<10}\n"
            box.insert("end", header + "-"*60 + "\n")
            
            for m in dades:
                nom_complet = f"{m['nom']} {m['cognom1']}"
                linia = f"{nom_complet:<30} | {m['total_visites']:<10} | {m['total_operacions']:<10}\n"
                box.insert("end", linia)
        conn.close()

    ctk.CTkButton(f, text="Actualitzar Dades", command=cargar_datos).pack(pady=10)
    
    # Carga inicial al abrir la ventana
    cargar_datos()

def menu_visites():
    f = ctk.CTkToplevel()
    f.title("Consultar Visites")
    f.geometry("700x500")
    
    cal = DateEntry(f, date_pattern="yyyy-mm-dd"); cal.pack(pady=10)
    box = ctk.CTkTextbox(f, width=650, height=300); box.pack(padx=10)

    def executar():
        box.delete("1.0", "end")
        conn = connectar()
        dades = consultes.carregar_visites_del_dia(conn, cal.get_date())
        if not dades:
            box.insert("end", "No hi ha visites per aquest dia.")
        else:
            box.insert("end", f"{'HORA':<12} | {'PACIENT':<25} | {'METGE':<25}\n" + "-"*65 + "\n")
            for r in dades:
                box.insert("end", f"{str(r['hora_entrada']):<12} | {r['pacient']:<25} | {r['metge']:<25}\n")
        conn.close()

    ctk.CTkButton(f, text="Consultar", command=executar).pack(pady=10)

def menu_operacions():
    f = ctk.CTkToplevel()
    f.title("Consultar Operacions")
    f.geometry("750x500")
    cal = DateEntry(f, date_pattern="yyyy-mm-dd"); cal.pack(pady=10)
    box = ctk.CTkTextbox(f, width=700, height=300); box.pack()

    def executar():
        box.delete("1.0", "end")
        conn = connectar()
        dades = consultes.carregar_operacions_dia(conn, cal.get_date())
        if not dades:
            box.insert("end", "Cap operació programada.")
        else:
            header = f"{'HORA':<10} | {'QUIROFAN':<15} | {'PACIENT':<20} | {'EQUIP'}\n"
            box.insert("end", header + "-"*75 + "\n")
            for r in dades:
                box.insert("end", f"{str(r['hora']):<10} | {r['quirofan']:<15} | {r['pacient']:<20} | {r['equip_infermeria']}\n")
        conn.close()

    ctk.CTkButton(f, text="Consultar", command=executar).pack(pady=10)

def menu_inventari():
    f = ctk.CTkToplevel()
    f.title("Inventari de Quiròfans")
    f.geometry("600x400")
    box = ctk.CTkTextbox(f, width=550, height=300); box.pack(pady=20)
    
    conn = connectar()
    res = consultes.consultar_inventari(conn)
    box.insert("end", f"{'Q':<5} | {'APARELL':<25} | {'MARCA':<15} | {'QTY'}\n" + "="*55 + "\n")
    for r in res:
        box.insert("end", f"{r['num_quirofan']:<5} | {r['nom_aparell']:<25} | {r['marca']:<15} | {r['quantitat']}\n")
    conn.close()

def menu_dependencia():
    f = ctk.CTkToplevel()
    f.title("Check Infermeria")
    e_id = ctk.CTkEntry(f, placeholder_text="ID Personal Infermer"); e_id.pack(pady=20)
    lbl_res = ctk.CTkLabel(f, text=""); lbl_res.pack()

    def check():
        conn = connectar()
        res = consultes.check_dependencia_infermeria(conn, e_id.get())
        if res:
            tipus = "Metge" if res['es_metge'] else "Planta"
            lbl_res.configure(text=f"L'infermer/a {res['nom']} és de: {tipus}")
        else:
            lbl_res.configure(text="ID no trobat")
        conn.close()
    ctk.CTkButton(f, text="Verificar", command=check).pack()

# Les funcions d'alta (menu_alta_pacient, etc) segueixen la mateixa lògica d'insert

# alta personal

# alta pacient
def menu_alta_pacient():
    f = ctk.CTkToplevel()
    f.title("Alta Pacient")
    f.geometry("400x500")

    entries = []
    labels = ["Nom", "Cognoms", "Telèfon", "Email", "DNI", "Data Naixement", "Targeta Sanitària"]

    for l in labels:
        ctk.CTkLabel(f, text=l).pack()
        e = ctk.CTkEntry(f)
        e.pack(pady=2)
        entries.append(e)

    def guardar():
        conn = connectar()
        dades = [e.get() for e in entries]
        consultes.alta_pacient(conn, dades)
        messagebox.showinfo("OK", "Pacient creat")
    ctk.CTkButton(f, text="Guardar", command=guardar).pack(pady=20)

# dependencia infermeria