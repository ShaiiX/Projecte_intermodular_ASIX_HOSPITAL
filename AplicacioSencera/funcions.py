import hashlib  # per fer hash de les contrasenyes
import base64   # per codificar la informació del login de manera segura en un fitxer
import autentificacio   # importar funcions de autentificaccio

# validacio
def validar_inputs(nom_usuari, contrasenya):    # comprova que els camps no estiguin buits
    return nom_usuari.strip() != "" and contrasenya.strip() != ""

# login
def proces_login(nom_usuari, contrasenya):  # processa el login complet
    if not validar_inputs(nom_usuari, contrasenya):
        return "buit"   # retorna error si els camps estan buits
    return autentificacio.login_usuari(nom_usuari, contrasenya) # crida a la funció de login de autentificacio.py

# registre
def proces_registre(nom_usuari, contrasenya):   # processa el registre d'un usuari
    if not validar_inputs(nom_usuari, contrasenya):
        return False
    return autentificacio.registrar_usuari(nom_usuari, contrasenya) # crida a la funció de registre

# fitxer seguretat
def guardar_login_fitxer(nom_usuari, contrasenya):  # guarda info del login en un fitxer de manera segura (hash + base64)
    try:
        hash_simple = hashlib.sha256(contrasenya.encode()).hexdigest()  # es fa un hash SHA-256 de la contrasenya
        data = f"{nom_usuari}:{hash_simple}"    # crea la linia amb usuari i hash
        encoded = base64.b64encode(data.encode()).decode()  # codifica en base64 per seguretat addicional per evitar el text pla

        with open("login_log.txt", "a") as f:   # es guarda en un fitxer
            f.write(encoded + "\n")

    except Exception as e:  # sino es pot guardar es mostra un error
        print("Error fitxer:", e)