# Planificació Bloc de Connectivitat i Login

## Objectiu

Amb aquest bloc es podràn fer les següents accions:
- Connectar l'aplicació amb la BD de PostgreSQL
- Gestor de registres i inici de sessió dels usuaris al programa
- Garantir la seguretat de les dades que es guarden (credencials)
- Controlar l'accés al sistema

## Parts del programa

Es programen diferents tasques:
- Configuració de la connexió a la BD
- Creació de la taula d'usuaris
- Implementació dels registres d'usuaris
- Implementació del login
- Validar les credencial
- Implementar seguretat a les credencials (amb hash)
- Control d'errors de connexió
- Control d'errors del programa

## Disseny del programa

El programa es desenvoluparà en Python utilitzant un entorn virtual (venv) per gestionar les llibreries.

La interfície gràfica es farà amb CustomTkinter, ja que permet més personalització.

El codi estarà organitzat de forma modular, separant els fitxers segons la seva funció (connexió a BD, login, menú, etc.).

S’utilitzarà un enfocament d’anàlisi descendent, començant per les parts principals i dividint-les en funcions més petites.

També es faran servir llibreries per facilitar la connexió amb la base de dades i altres funcionalitats.

## Funcionament pas a pas

1. L'usuari inicia el programa
2. Introdueix el nom d'usuari i la contrassenya
3. El programa fa un hash de la contrasenya i consulta  la BD
4. Si existeix retorna un rol i mostra el menu segons el rol de l'usuari
5. En cas contrari es fa un control d'errors i es mostra el tipus d'error per pantalla

## Estructura

L'organització dels fitxers serà de la següent manera per mantenir l'ordpre del programa:

Directori bloc/
- db.py
- menu.py
- main.py
- funcions.py
- autenticacio.py

Al **fitxer db.py** és la connexió a la base de dades de PostgreSQL.

El **menu.py** és el menú principal, hi han 2 menus, el primer serà d'admin i el segon d'usuari.

El **main.py** és el programa principal amb l'usuari i contrasenya.

El **funcions.py** és on estan totes les funcions principals del programa que estan enllaçades amb el main.

Al **autentificacio.py** es on es troba tot el relacionat amb el login, amb el hash de contrasenya.
