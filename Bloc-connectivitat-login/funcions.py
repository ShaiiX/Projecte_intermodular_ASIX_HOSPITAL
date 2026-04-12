import base64
import autentificacio

# validacio
def validar_inputs(nom_usuari, contrasenya):
    return nom_usuari.strip() != "" and contrasenya.strip() != ""

# login
def proces_login(nom_usuari, contrasenya):
    if not validar_inputs(nom_usuari, contrasenya):
        return "buit"

    return autentificacio.login_usuari(nom_usuari, contrasenya)

# registre
def proces_registre(nom_usuari, contrasenya):
    if not validar_inputs(nom_usuari, contrasenya):
        return False

    return autentificacio.registrar_usuari(nom_usuari, contrasenya)

# fitxer seguretat
def guardar_login_fitxer(nom_usuari, contrasenya):
    try:
        data = f"{nom_usuari}:{contrasenya}"
        encoded = base64.b64encode(data.encode()).decode()
        with open("login_log.txt", "a") as f:
            f.write(encoded + "\n")

    except Exception as e:
        print("Error fitxer:", e)