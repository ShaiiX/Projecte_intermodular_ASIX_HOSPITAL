import bcrypt   # hash de contrasenyes
from db import connectar

# hash
def hash_contrasenya(contrasenya):  # funció per generar un hash de la contrasenya amb bcrypt
    return bcrypt.hashpw(contrasenya.encode('utf-8'), bcrypt.gensalt())

def check_contrasenya(contrasenya, hashed): # comprova si la contrasenya coincideix amb el hash guardat a la bd
    return bcrypt.checkpw(contrasenya.encode('utf-8'), hashed)

# registre
def registrar_usuari(nom_usuari, contrasenya, rol="usuari"):    # registra un nou usuari a la bd amb el rol per defecte "usuari"
    conn = connectar()
    if not conn:
        return False

    try:
        cur = conn.cursor() # crear un cursor per executar les consultes
        hashed = hash_contrasenya(contrasenya)
        # insertar usuari a la bd
        cur.execute("""
            INSERT INTO usuaris (username, password, rol)
            VALUES (%s, %s, %s)
        """, (nom_usuari, hashed, rol))

        conn.commit()   # guardar canvis
        cur.close()
        return True

    except Exception as e:  # evitar usuaris duplicats
        print("Error registre:", e)
        return False
    
    finally:
        conn.close()    # es tanca semrpre la connexió

# login oficial (actualment no s'utilitza, es fa servir un login de prova fins que es crei la connexió amb la bd)
#def login_usuari(nom_usuari, contrasenya):  # funció per validar les credencials d'un usuari
#    conn = connectar()
#    if not conn:
#        return None
#
#    try:
#        cur = conn.cursor()
#        # consulta per obtenir hash i rol de l'usuari
#        cur.execute("""
#            SELECT password, rol FROM usuaris
#            WHERE username = %s
#        """, (nom_usuari,))
#        result = cur.fetchone()
#        cur.close()
#        conn.close()
#
#        if result:
#            db_pass, rol = result
#            if check_contrasenya(contrasenya, db_pass): # comprovació de contrasenya amb bcrypt
#                return rol  # retorna el rol si el login és correcte
#        return None
#
#    except Exception as e:
#        print("Error login:", e)
#        return None
#    
#    finally:
#        conn.close()

# aquests són usuaris de prova fins que el login funcioni amb la base de dades
def login_usuari(nom_usuari, contrasenya):  # funció per validar les credencials d'un usuari

    # --- MODE PROVA (sense BD) ---
    if nom_usuari == "prova1" and contrasenya == "1234":
        return "admin"

    if nom_usuari == "prova2" and contrasenya == "1234":
        return "usuari"

    return None
