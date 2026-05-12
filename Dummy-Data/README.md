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

La generació de dades s’ha fet amb Python utilitzant la llibreria Faker.

Aquest sistema permet crear moltes dades automàticament sense haver-les d’introduir manualment.

## Execució des de l’aplicació

La generació del dummy data es pot executar des del menú de l’aplicació. Hi ha dues opcions per facilitar les proves ràpidament:

- Generar dummy data
- Eliminar-la

Es pot eliminar les dades fictícies creades durant les proves, per poder deixar la BD neta de nou.

## Índexs

S’han creat índexs en les taules més importants per millorar el rendiment de les consultes.

### Índexs utilitzats

| Taula | Camp | Motiu |
| :--- | :--- | :--- |
| pacient.pacient | dni | Cerca ràpida de pacients |
| pacient.visita | data_visita | Consultes per dia |
| pacient.visita | id_pacient | Historials |
| pacient.visita | id_metge | Consultes de metges |

## Tecnologies utilitzades

| Tecnologia | Ús |
| :--- | :--- |
| PostgreSQL | Base de dades |
| Python | Scripts |
| Faker | Generació de dades |
| psycopg2 | Connexió amb Postgres |


---

Instal·lació de Faker: pip install faker psycopg2-binary