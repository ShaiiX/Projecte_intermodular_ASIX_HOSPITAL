# Esquema de Seguretat

## Rols del sistema

Hem definit els [rols](./rols-permisos/rols.sql) segons els permisos([access al la base de dades](./rols-permisos/permisos-acces-schema.sql)):

- [Admin](./rols-permisos/permisos-admin.sql): control complet del sistema
- [Metge](./rols-permisos/permisos-metge.sql): accés a dades mèdiques i gestió de pacients
- [Infermer](./rols-permisos/permisos-infermer.sql): suport en consultes i accés limitat
- [Vari](./rols-permisos/permisos-vari.sql): personal administratiu
- [Pacient](./rols-permisos/permisos-pacient.sql): accés únic a les seves dades

El rol pacient, perque hi es? 

Es coneix a hospitals que hi ha el sistema de escaneijar la tarjeta sanitaria o altres i es on et proporciona visites, proves... Son aquestes dades que podra accedir aquest pacient desde la maquina que s'incorporaran, quan arribi el cas, on es posaràn les limitacions desde l'aplicatiu a més desde la base de dades per si es el cas, no es necesari que aquest pacient pugui accedir a les dades del personal si arriba a ocurrir alguna incidencia.

## Matriu de seguretat

Els permisos que té cada rol sobre els diferents taules de la BD. Per poder gestionar l'accés segons el rol de l'usuari, separar els permisos i protegir les dades.

| Entitat / Taula | Admin | Metge | Infermer | Vari | Pacient |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Personal | All | R | - | - | - |
| Infermer | All | R | - | - | - |
| Infermer_planta | All | R | - | - | - |
| Infermer_metge | All | R | - | - | - |
| Planta | All | R | - | - | - |
| Quirofan | All | R | - | - | - |
| Aparell_medic | All | R | - | - | - |
| Tipus | All | R | - | - | - |
| Operacio | All | All | R | - | R (propi) |
| Infermer_Operacio | All | All | R | - | - |
| Metge | All | R | - | - | - |
| Visita | All | All | R | - | R (propi) |
| Prova | All | All | R | - | R (propi) |
| Expedient | All | All | R | R | R (propi) |
| Pacient | All | All | R | R | R (propi) |
| Ingres | All | All | R | - | R (propi) |
| Habitacio | All | R | R | - | - |
| Recepta | All | All | All | - | R (propi) |
| Recepta_Visita | All | All | R | - | R (propi) |
| Recepta_Ingres | All | All | All | - | R (propi) |
| Linea_Recepta | All | All | All | - | R (propi) |
| Medicament | All | R | R | - | - |
| Usuari | All | - | - | - | - |
| Rol | All | - | - | - | - |
| Usuari_Rol | All | - | - | - | - |
| Log_Access | All | - | - | - | - |
| Log_Detall | All | - | - | - | - |
| Log_Library | All | - | - | - | - |
| Empresa_Externa | All | - | - | - | - |
| Facturacio_Cantina | All | - | - | - | - |

## Schema 
S'ha separat les taules en diferents schemas, per a tenir mes control ordre i seguretat dins les dades, també facilitara feina a futur, aquests serien els schemes:

- cantina <-- Com el nom indica per a separar les dades de la cantina sobre les altres
- pacient <-- Les taules que pot accedir el pacient
- estructura <-- Sobre l'infraestructura de l'hospital
- dades_per <-- Taules restants amb dades personals
- seguretat <-- Taules per a comportar l'auditoria i seguretat de la base de dades, com els usuaris, logs...

Perque hi ha un schema per als pacients i no per a metges o altre rol? 

- Ens hem basat en un sistema per a separar dades estable, comprovem el rol amb menys permisos o que ens interesa mes tenir-ho separat, en aquest cas els pacients, per motius explicats anteriorment. Al tenir separat aquest rol es com que l'aillem de les altres dades.
- Seguidament separem les dades per seccions ja que cada rol restant pot accedir a cadascun d'elles, així es conté organització 



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

Estructura completa: 

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
### Extens
Els logs serveixen per a tenir coneixement sobre el que es fa a la base de dades.
Es separara en dues parts:

- Els logs per als backups, aquest son logs per a tenir access i coneixement el cas del que falli la base de dades,         aquestes es faran copies en altres discs durs, per si el cas de que es cremi o altre inconvenient en el servidor, aquests logs serveixen que al fer el backup inicial poguem recuperar les dades durant el temps del backup i la hora de la fallada.

Per activar aquests logs de forma que ho faci el postgres s'ha de configurar el postgresql.conf de la seguent forma:

```
#per activar els logs
logging_collector = on  

#per a guardar INSERT, UPDATE, DELETE
log_statement = 'mod' 

#posicio dels logs, la seva carpeta i el seu nom
log_directory = 'pg_log_canvis'
log_filename = 'canvis-%Y-%m-%d.log'

#cada linea per a fer-ho mes llegible
log_line_prefix = '%t [%p]: '
```
Un cop això es realitzaran els logs de forma completa per a poder utilitzarlos en cas de perdua de la base de dades.

- La segona part es sobre tenir coneixement del que es fa, per a seguretat i auditoria, es guarda dins la base de dades, per a tenir access directe i facil desde la aplicació o exportació si es el cas, si es fa un Import, Update o Delete que es repeteix molt, encomptes de guardar totes les dades hi haura una libreria per a no repetir el texte complert de la consulta.

Primerament s'ha d'activar en el postgresql.conf la seguent configuracio:
Serveix per a carregar una extensio de postgresql al iniciar el servidor que el que fa es normalitzar una query que es pot arribar a repetir sempre, com casi tots els canvis es faran desde l'aplicatiu sera mes simple de tenir un control sombre les dades desde l'aplicatiu tenint-ho de forma normalitzada aprofitant espai.
```
shared_preload_libraries = 'pg_stat_statements'
```

Un cop això ja es pot indicar el trigger, que es trova a Triggers/LOG_AUDITORIA.sql.

Perque no s'utilitza directament el pg_stat_statements? 
- Es volatil, vol dir que aquesta informacio si es reinicia el servidor o altres inconvenients pot arrivar a sobrecargar sistema si es el cas o perdre el registre de les comandes.
- No es massa organitzat i es mes complicat de trobar-ho.

Per això s'utilitzara en una taula amb aquestes matiexes dades de forma simplificada.

### Login
Quan un usuari estableix una conexió amb la base de dades sera interesant guardar-ho dins de la base de dades a log_access sense detall, ja que nomes es una conexió, per fer això s'hauria de modificar el .py ja que desde així podem indicar que sa establert la conexió i inserir-ho dins la base de dades:
```
#extreiem l'identificador de l'usuari
SELECT id_usuari
INTO usuari
FROM seguretat.USUARI
WHERE nom_usuari = usuari <--"Variable de l'usuari"

#ho afegim dins de la base de dades
INSERT INTO seguretat.LOG_ACCESS (accio, data, id_usuari) 
VALUES ('LOGIN', NOW(), usuari);
```
On cada inici obtindra l'identificador de l'usuari i ho afegira com a registre dins la base de dades.