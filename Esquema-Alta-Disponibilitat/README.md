# Esquema d'alta disponibilitat

# Infraestructura de Hardware

Per garantir un sistema fiable, hem dissenyat una infraestructura d'alta disponibilitat amb redundància. Tenim dos servidors de base de dades (nodes). 

**Sistema d’emmagatzematge NAS (HP)**  
- Permet alta disponibilitat i redundància  
- Inclou suport tècnic i reemplaçament de hardware  
- Prioritza la seguretat davant la velocitat

**Sistema operatiu**  
- Linux (entorn estable i segur)  
- PostgreSQL com a SGBD  
- Suport empresarial amb Red Hat (no l'aplicarem al projcte però pensem que seria una bona pràctica)

Aquesta configuració permet evitar punts de fallada, garantir disponibilitat contínua i facilitar la recuperació ràpida davant errors.

Principalment s'ha de parlar de com s'extructura el servidor, més a dir el hardware, es necesitarà un servidor potent per a fer les consultes necesaries de forma rapida, aquesta seria la proposta:

| Component | Opció | Explicació |
| :--- | :--- | :--- |
| CPU | 
| RAM |
| Almacenament |
| Xarxa |

# Rèplica

Per la seva simplicitat i el proporcionat s'utilitzara el sistema de actiu-passiu, ja que seria per a un pressupost baix, que és just el que busquem. 

## Tipus de replicació escollida:

**Model Actiu-Passiu (Master-Slave)**

Master:
- Node principal
- Permet escriptura i modificacions

Slave:
- Node secundari
- Només lectura
- Rep dades replicades en temps real

## Funcionament

El node rep totes les operacions com Insert, update i delete, després aquestes operacions es registren al **WAL** (que és Write-Ahead Log). El slave replica aquests canvis automàticament i en cas de fallada del Master, el slave passa a ser el nou master.

Així garantir la alta disponibilitat, una recuperació ràpida de les dades i reduïr la seva pèrdua.

## Administració

Configuració del `pg_hba.conf` per permetre connexions del node secundari:
```
wal_level = replica
archive_mode = on
max_wal_senders = 10
```

# Backups

Es faran diferents tipus de còpies:

- Backup complet:
    - es realitza una vegada per setmana (els caps de setmana per la nit)

- Backup incremental:
    - 

# Restauració


