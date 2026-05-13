import bcrypt   # hash de contrasenyes
from db import connectar_generic, iniciar_sessio

# hash
def hash_contrasenya(contrasenya):
    return bcrypt.hashpw(contrasenya.encode('utf-8'), bcrypt.gensalt())

def check_contrasenya(contrasenya, hashed):
    if isinstance(hashed, memoryview):  # psycopg2 retorna bytea com a memoryview
        hashed = bytes(hashed)
    return bcrypt.checkpw(contrasenya.encode('utf-8'), hashed)

# registre
def registrar_usuari(nom_usuari, contrasenya, rol="usuari"):
    conn = connectar_generic()  # sempre amb usuari genèric
    if not conn:
        return False

    try:
        cur = conn.cursor()
        hashed = hash_contrasenya(contrasenya)
        cur.execute("""
            INSERT INTO usuaris (username, password, rol)
            VALUES (%s, %s, %s)
        """, (nom_usuari, hashed, rol))
        conn.commit()
        cur.close()
        return True

    except Exception as e:
        print("Error registre:", e)
        return False

    finally:
        conn.close()

# login
def login_usuari(nom_usuari, contrasenya):
    conn = connectar_generic()  # login sempre amb usuari genèric
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.password, r.nom FROM seguretat.usuari u
            JOIN seguretat.usuari_rol ur ON ur.id_usuari = u.id_usuari
            JOIN seguretat.rol r ON ur.id_rol = r.id_rol
            WHERE username = %s
        """, (nom_usuari,))
        result = cur.fetchone()
        cur.close()

        if result:
            db_pass, rol = result
            if check_contrasenya(contrasenya, db_pass):
                # guarda les credencials a la sessió per a futures connexions
                iniciar_sessio(nom_usuari, contrasenya)
                return rol
        return None

    except Exception as e:
        print("Error login:", e)
        return None

    finally:
        conn.close()