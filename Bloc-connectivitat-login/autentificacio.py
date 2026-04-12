import bcrypt
from db import connectar

# hash
def hash_contrasenya(contrasenya):
    return bcrypt.hashpw(contrasenya.encode('utf-8'), bcrypt.gensalt())

def check_contrasenya(contrasenya, hashed):
    return bcrypt.checkpw(contrasenya.encode('utf-8'), hashed)

# registre
def registrar_usuari(nom_usuari, contrasenya, rol="usuari"):
    conn = connectar()
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
        conn.close()
        return True

    except Exception as e:
        print("Error registre:", e)
        return False

# login
def login_usuari(nom_usuari, contrasenya):
    conn = connectar()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT password, rol FROM usuaris
            WHERE username = %s
        """, (nom_usuari,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            db_pass, rol = result
            if check_contrasenya(contrasenya, db_pass):
                return rol
        return None

    except Exception as e:
        print("Error login:", e)
        return None