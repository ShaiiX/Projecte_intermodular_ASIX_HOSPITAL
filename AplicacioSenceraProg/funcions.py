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