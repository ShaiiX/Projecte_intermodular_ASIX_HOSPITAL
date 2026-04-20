# Esquema de Seguretat

## Rols del sistema

Hem definit els rols segons els permisos:

- Admin: control complet del sistema
- Metge: accés a dades mèdiques i gestió de pacients
- Infermer: suport en consultes i accés limitat
- Vari: personal administratiu
- Pacient: accés únic a les seves dades

## Matriu de seguretat

Els permisos que té cada rol sobre els diferents taules de la BD. Per poder gestionar l'accés segons el rol de l'usuari, separar els permisos i protegir les dades.

## Configuració SSL

L'implementem per protegir la comunicació entre l'aplicació i la BD.

Pasos del procés:
1. Generació del certificat
2. Configuració del servidor a postgresql.conf
3. Configurar pg_hba.conf que gestiona la seguretat d'accés
4. Automatitzem amb una tasca programada (Cron)

## Data Masking

Per protegir les dades sensibles, per evitar mostrar dades reals als usuaris sense permisos:

- DNI
- Adreça
- Telèfon
- Email
- Historial mèdic

## Normativa AGPD

Hem seguit una estructura per garantir el compliment de la normativa AGPD

- Dades personals: nom, email...
- Dades sensibles: diagnòstics, historial mèdic...

Per a aquestes dades s'han aplicat mesures de protecció de dades com:

- Autenticació segura com hash amb bcrypt
- Connexions SSL
- Data masking
- Control d'usuaris per rols 
- Registre d'accessos utilitzant logs

Així poder evitar l'accés no autoritzat, informació filtrada i la manipulació de les dades.

## Logs

Això comporta als logs del sistema de la base de dades amb el seu access 

Es farà la exportació dels logs en NDJSON
