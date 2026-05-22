# Esquema de Seguretat

## Rols del sistema

Hem definit els [rols](./rols-permisos/rols.sql) segons els permisos([access al la base de dades](./rols-permisos/permisos-acces-schema.sql)):

- [Admin](./rols-permisos/permisos-admin.sql): control complet del sistema
- [Metge](./rols-permisos/permisos-metge.sql): accés a dades mèdiques i gestió de pacients
- [Infermer](./rols-permisos/permisos-infermer.sql): suport en consultes i accés limitat
- [Vari](./rols-permisos/permisos-vari.sql): personal administratiu
- [Pacient](./rols-permisos/permisos-pacient.sql): accés únic a les seves dades

El rol pacient, perquè hi és? 

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
ssl_cert_file = '/var/lib/postgresql/server.crt'
ssl_key_file = '/var/lib/postgresql/server.key'
```

pg_hba.conf (totes les connexions amb SSL)

```
hostssl all all 192.168.0.0/24 scram-sha-256
```

Utilitzem el scram-sha-256 perquè és més segur i el md5 està obsolet.

## Automatització

Límit de validesa del certificat de 365 dies. Script manual:

```
#!/bin/bash

openssl genrsa -out /var/lib/postgresql/server.key 2048
openssl req -new -x509 -key /var/lib/postgresql/server.key \
-out /var/lib/postgresql/server.crt -days 365 -subj "/CN=localhost"

chmod 600 /var/lib/postgresql/server.key
chown postgres:postgres /var/lib/postgresql/server.key /var/lib/postgresql/server.crt

systemctl restart postgresql
```

Donar permisos:

```
chmod +x /usr/local/bin/script_ssl.sh
```

El millor seria automatitzar la renovació amb un script que reutilitzi la clau que ja existeix o que utilitzi certificats gestionats (com Let's Encrypt).

```crontab -e```

```0 0 1 1 * /ruta/script_ssl.sh```

Renovació anual automàticament

## Data Masking

Per protegir les dades sensibles i evitar mostrar informació real als usuaris sense permisos, s'ha implementat un sistema de data masking. Aquest sistema permet mostrar les dades de forma parcial o oculta (per exemple: `XXXXXX123`), garantint la privacitat.

Aquesta funcionalitat es basa en una extensió de PostgreSQL anomenada **postgresql_anonymizer (anon)**.

### Instal·lació

L'extensió s'instal·la des del repositori oficial de Dalibo:

```bash
# Afegir el repositori
curl https://apt.dalibo.org/labs/debian-dalibo.asc | sudo tee /etc/apt/trusted.gpg.d/dalibo.asc
echo "deb https://apt.dalibo.org/labs noble-dalibo main" | sudo tee /etc/apt/sources.list.d/dalibo.list
sudo apt update

# Instal·lar per a PostgreSQL 18
sudo apt install postgresql_anonymizer_18
```

> **Nota:** La versió instal·lada és la 3.x, que és la única disponible per a PostgreSQL 18. [Repositori del anon.](https://postgresql-anonymizer.readthedocs.io/en/stable/)

### Configuració

**1. Afegir l'extensió a `postgresql.conf`:**

```bash
shared_preload_libraries = 'anon'
```

**2. Reiniciar PostgreSQL:**

```bash
sudo systemctl restart postgresql
```

**3. Activar l'extensió a la base de dades:**

```sql
CREATE EXTENSION IF NOT EXISTS anon CASCADE;
SELECT anon.init();
```

**4. Activar el Dynamic Masking transparent (específic de la v3):**

```sql
ALTER DATABASE <nom_DB> SET anon.transparent_dynamic_masking TO true;
```

Tancar la sessió i reconnectar per tal que el paràmetre tingui efecte.

**5. Marcar el rol que veurà les dades enmascarades:**

```sql
SECURITY LABEL FOR anon ON ROLE infermer_role IS 'MASKED';
```

### Funcionament

L'extensió intercepta les consultes `SELECT` i substitueix les dades sensibles automàticament segons el rol de l'usuari que fa la consulta. Els rols marcats com a `MASKED` veuen les dades protegides; la resta veuen les dades reals.

Les regles es defineixen amb `SECURITY LABEL` sobre cada columna sensible.

### Regles de mascarament aplicades

> **Important:** La màscara `anon.partial` ha de respectar la longitud màxima del camp. Per a camps `varchar(9)` com el DNI, s'utilitzen 6 caràcters de màscara + 3 visibles = 9 total.

```sql
-- Usuaris: contrasenya sempre oculta
SECURITY LABEL FOR anon ON COLUMN seguretat.usuari.password
IS 'MASKED WITH VALUE ''********''';

-- Personal: DNI (6 X + 3 últims caràcters)
SECURITY LABEL FOR anon ON COLUMN dades_per.personal.dni
IS 'MASKED WITH FUNCTION anon.partial(dni, 0, ''XXXXXX'', 3)';
```
**Altres exemples dins de [datamasking.sql](./datamasking.sql)**

### Dades protegides

S'han identificat com a dades sensibles les següents columnes:

- `seguretat.usuari.password`
- `dades_per.personal.dni`
- `dades_per.personal.direccio`
- `dades_per.personal.telefon`
- `pacient.pacient.dni`
- `pacient.pacient.tarjeta_sanitaria`
- `pacient.pacient.telefon`
- `pacient.expedient.historial`
- `pacient.expedient.observacions`
- `pacient.visita.diagnostic`

### Control d'accés

El data masking s'aplica seguint el principi de **mínim privilegi**:

- `admin_role` i `metge_role` veuen les dades reals
- `infermer_role` i altres rols sense privilegis veuen les dades enmascarades

Per verificar que el masking funciona correctament, connectar-se amb el rol enmascarado i fer una consulta:

```sql
SET ROLE infermer_role;
SELECT dni FROM pacient.pacient LIMIT 1;
-- Resultat esperat: XXXXXX12A
```

>**Nomenglatura:** Ho podeu trovar dins la pàgina web 

## Normativa AGPD

[Estructura completa](https://github.com/ShaiiX/Projecte_intermodular_ASIX_HOSPITAL/tree/main/Esquema-seguretat/agpd)

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

- Els logs per als backups, aquest son logs per a tenir access i coneixement el cas del que falli la base de dades, aquestes es faran copies en altres discs durs, per si el cas de que es cremi o altre inconvenient en el servidor, aquests logs serveixen que al fer el backup inicial poguem recuperar les dades durant el temps del backup i la hora de la fallada.

Aquest logs seràn basicament WAL, es un sistema que a més de replica dades en altres servidors, que s'utilitzarà mes endavant, permet guardar les comandes i així tenir unes copies continues en cas de perdua.

- La segona part es sobre tenir coneixement del que es fa, per a seguretat i auditoria, es guarda dins la base de dades, per a tenir access directe i facil desde la aplicació o exportació si es el cas, si es fa un Import, Update o Delete que es repeteix molt, encomptes de guardar totes les dades s'haura de normalitzar aquestes mateixes consultes.

Un cop això ja es pot indicar el trigger, que es trova a [logs/LOG_AUDITORIA.sql](./logs/LOG_AUDITORIA.sql).

Perque no s'utilitza directament el pg_stat_statements, que fa la mateixa funció? 
- Es volatil, vol dir que aquesta informacio si es reinicia el servidor o altres inconvenients pot arrivar a sobrecargar sistema si es el cas o perdre el registre de les comandes.
- No es massa organitzat i es mes complicat de trobar-ho.

Per això s'utilitzara en una taula amb aquestes matiexes dades de forma simplificada.

### Login
Quan un usuari estableix una conexió amb la base de dades sera interesant guardar quan ha estat la utlima conexió, per fer això s'hauria de modificar el .py ja que desde així podem indicar que sa establert la conexió.
On cada inici obtindra l'identificador de l'usuari i modificara el registre dins la base de dades.
[login.sql](/Esquema-seguretat/logs/usuaris/Login.sql)

Per a indicar i mantenir l'activiat de l'usuari, on cada acció que faci l'usuari al sistema amb la base de dades s'haura de actualitzar el registre:
```
UPDATE usuaris SET ultima_activitat = NOW() WHERE id = idusuari;
```