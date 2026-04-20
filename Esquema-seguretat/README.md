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

**Pasos del procés:**
1. Generació del certificat
2. Configuració del servidor a postgresql.conf
3. Configurar pg_hba.conf que gestiona la seguretat d'accés
4. Automatitzem amb una tasca programada (Cron)

Generar el certificat:

```
openssl genrsa -out server.key 2048
openssl req -new -x509 -key server.key -out server.crt -days 365
```

Configurar permisos perquè postgres només accepta la clau si té permisos restringits:

```chmod 600 server.key```

Configuració del Postgres:

postgresql.conf

```
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

pg_hba.conf (totes les connexions amb SSL)

```
hostssl all all 192.168.0.0/24 md5
```

## Automatitcació

Límit de validesa del certificat de 365 dies. Script manual:

```
#!/bin/bash
openssl req -new -x509 -key server.key -out server.crt -days 365
systemctl restart postgresql
```

El millor seria automatitzar la renovació amb un script que reutilitzi la clau que ja existeix o que utilitzi certificats gestionats (com Let's Encrypt).

```crontab -e```

```0 0 1 1 * /ruta/script_ssl.sh```

Renovació anual automàticament

## Data Masking

Per protegir les dades sensibles, per evitar mostrar dades reals als usuaris sense permisos. Ho hem implementat utilitzant vistes sql que oculten les dades.

- DNI
- Adreça
- Telèfon
- Email
- Historial mèdic

**Vistes creades**
- pacient_mask:
    - DNI
    - Telèfon
    - Email
- expedient_mask: contingut remplaçat per un text
- vista_mask: Oculta els diagnòstics
- recepta_mask: descripció oculta (protegeix la info de les receptes)

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
