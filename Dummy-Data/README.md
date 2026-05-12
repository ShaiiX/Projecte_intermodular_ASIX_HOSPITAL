# Dummy Data

Hem creat un sistema de dummy data per comprovar que el sistema funciona correctament amb moltes dades, per simular el sistema de l'hospital. Així provar el rendiment de postgres, les consultes, backups...

## Objectiu

L’objectiu és comprovar que la BD pot treballar amb molta informació sense donar errors ni perdre rendiment.

També per:

- Provar consultes grans
- Validar els índexs
- Comprovar la rèplica entre master i slave
- Fer proves de backups i restauracions
- Simular un entorn real

## Quantitat de dades

| Tipus | Quantitat |
| :--- | :--- |
| Visites | 100.000 |
| Pacients | 50.000 |
| Metges | 100 |
| Infermeres | 200 |
| Personal de neteja | 100 |
| Personal administratiu | 50 |

## Consistència de les dades

Les dades creades segueixen el mateix format que les dades reals del sistema.

- DNI simulats
- Telèfons correctes
- Emails realistes
- Dates coherents
- Pacients relacionats amb visites
- Metges relacionats amb pacients

Una petita part de la informació s’ha generat en alfabet ciríl·lic per validar compatibilitat UTF-8 i internacionalització del sistema.

## Generació de dades

La generació de dades s’ha fet amb Python des de l’aplicació, dins el mòdul:

`AplicacioSenceraProg/moduls/dummy_data.py`

El sistema crea les dades de forma automàtica i fa servir insercions massives amb `execute_values` de `psycopg2`, perquè carregar 100.000 visites i 50.000 pacients sigui més ràpid que inserir registre per registre.

També es crea un schema auxiliar anomenat `dummy_data`, on es guarden les execucions i els IDs dels registres creats. Això permet eliminar només la informació dummy sense esborrar dades reals de l’hospital.

## Execució des de l’aplicació

La generació del dummy data es pot executar des del menú de l’aplicació:

`Bloc de Manteniment > Dummy Data`

Hi ha dues opcions per facilitar les proves ràpidament:

- Generar dummy data
- Eliminar-la

L’opció d’eliminar esborra les dades segons els IDs guardats al schema `dummy_data`, respectant l’ordre de les claus foranes.

## Índexs

S’han creat índexs en les taules més importants per millorar el rendiment de les consultes.

### Índexs utilitzats

| Taula | Camp | Motiu |
| :--- | :--- | :--- |
| pacient.pacient | dni | Cerca ràpida de pacients |
| pacient.pacient | tarjeta_sanitaria | Cerca ràpida per targeta sanitària |
| dades_per.personal | dni | Cerca ràpida de personal |
| dades_per.personal | email | Cerca ràpida per correu |
| pacient.visita | data | Consultes per dia |
| pacient.visita | id_pacient | Historials |
| pacient.visita | id_metge | Consultes de metges |

## Tecnologies utilitzades

| Tecnologia | Ús |
| :--- | :--- |
| PostgreSQL | Base de dades |
| Python | Generació de dades |
| psycopg2 | Connexió amb Postgres |
| customtkinter | Opció de menú dins l'aplicació |


---

Instal·lació recomanada:

`pip install psycopg2-binary customtkinter`

Nota: el mòdul actual genera les dades amb llistes internes i funcions pròpies. Faker es pot utilitzar més endavant si es vol ampliar la varietat de noms, adreces o municipis.
