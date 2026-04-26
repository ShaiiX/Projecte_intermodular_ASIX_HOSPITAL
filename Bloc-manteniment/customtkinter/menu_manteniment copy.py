import customtkinter as ctk
from tkinter import messagebox
from db import connectar

# funcions db

def obtenir_reserves_habitacio(id_habitacio):
    conn = connectar()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT i.data_ingres, i.data_sortida_prevista, p.nom
            FROM pacient.ingres i
            JOIN pacient.pacient p ON i.id_pacient = p.id_pacient
            WHERE i.id_habitacio = %s
            ORDER BY i.data_ingres;
        """, (id_habitacio,))

        dades = cur.fetchall()
        cur.close()
        conn.close()
        return dades

    except Exception as e:
        messagebox.showerror("Error BD", str(e))
        return []


def obtenir_operacions_dia(data):
    conn = connectar()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.hora, p.nom, m.nom
            FROM pacient.operacio o
            JOIN pacient.pacient p ON o.id_pacient = p.id_pacient
            JOIN dades_per.personal m ON o.id_metge = m.id_personal
            WHERE o.data = %s
            ORDER BY o.hora;
        """, (data,))

        dades = cur.fetchall()
        cur.close()
        conn.close()
        return dades

    except Exception as e:
        messagebox.showerror("Error BD", str(e))
        return []


def obtenir_visites_dia(data):
    conn = connectar()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT v.hora, p.nom, m.nom
            FROM pacient.visita v
            JOIN pacient.pacient p ON v.id_pacient = p.id_pacient
            JOIN dades_per.personal m ON v.id_metge = m.id_personal
            WHERE v.data = %s
            ORDER BY v.hora;
        """, (data,))

        dades = cur.fetchall()
        cur.close()
        conn.close()
        return dades

    except Exception as e:
        messagebox.showerror("Error BD", str(e))
        return []

# interficie

def obrir_manteniment():
    app = ctk.CTk()
    app.title("Bloc de Manteniment")
    app.geometry("700x600")

    # titol
    titol = ctk.CTkLabel(app, text="Gestió Hospital", font=ctk.CTkFont(size=26, weight="bold"))
    titol.pack(pady=20)

    # habitacio
    frame_hab = ctk.CTkFrame(app)
    frame_hab.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(frame_hab, text="Reserves per Habitació").pack(pady=5)

    entry_hab = ctk.CTkEntry(frame_hab, placeholder_text="ID Habitació")
    entry_hab.pack(pady=5)

    textbox_hab = ctk.CTkTextbox(frame_hab, height=120)
    textbox_hab.pack(pady=5, fill="x")

    def mostrar_habitacio():
        textbox_hab.delete("1.0", "end")
        dades = obtenir_reserves_habitacio(entry_hab.get())

        for d in dades:
            textbox_hab.insert("end", f"Ingrés: {d[0]} | Sortida: {d[1]} | Pacient: {d[2]}\n")

    ctk.CTkButton(frame_hab, text="Consultar", command=mostrar_habitacio).pack(pady=5)

    # operacions
    frame_op = ctk.CTkFrame(app)
    frame_op.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(frame_op, text="Operacions per Dia").pack(pady=5)

    entry_data_op = ctk.CTkEntry(frame_op, placeholder_text="YYYY-MM-DD")
    entry_data_op.pack(pady=5)

    textbox_op = ctk.CTkTextbox(frame_op, height=120)
    textbox_op.pack(pady=5, fill="x")

    def mostrar_operacions():
        textbox_op.delete("1.0", "end")
        dades = obtenir_operacions_dia(entry_data_op.get())

        for d in dades:
            textbox_op.insert("end", f"Hora: {d[0]} | Pacient: {d[1]} | Metge: {d[2]}\n")

    ctk.CTkButton(frame_op, text="Consultar", command=mostrar_operacions).pack(pady=5)

    # visites
    frame_vis = ctk.CTkFrame(app)
    frame_vis.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(frame_vis, text="Visites per Dia").pack(pady=5)

    entry_data_vis = ctk.CTkEntry(frame_vis, placeholder_text="YYYY-MM-DD")
    entry_data_vis.pack(pady=5)

    textbox_vis = ctk.CTkTextbox(frame_vis, height=120)
    textbox_vis.pack(pady=5, fill="x")

    def mostrar_visites():
        textbox_vis.delete("1.0", "end")
        dades = obtenir_visites_dia(entry_data_vis.get())

        for d in dades:
            textbox_vis.insert("end", f"Hora: {d[0]} | Pacient: {d[1]} | Metge: {d[2]}\n")

    ctk.CTkButton(frame_vis, text="Consultar", command=mostrar_visites).pack(pady=5)

    app.mainloop()