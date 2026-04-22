# Document de Seguretat

El principal objectiu és garantitzar la protecció de dades personals tractades segons la normativa de RGPD i AGPD, definir les mesures de seguretat aplicades en el sistema de la base de dades.

El sistema gestiona informació sensible com dades mèdiques, dades personals...

## Tipus de dades tractades

- Dades identificatives: nom, cognoms, DNI
- Dades de contacte: telèfon, email, adreça
- Dades mèdiques: diagnòstics, receptes, historial mèdic
- Dades personals: empleat,s infermers, metges
- Dades administratives: facturació, ingresos

## Classificació de les dades de nivell de seguretat

- Nivell baix: nom, cognom
- Nivell mitjà: telèfon, email
- Nivell alt: historial mèdic, dades sanitàries, receptes, diagnòstics

## Tractament de les dades

Les dades seràn tractades i recollides per a les següents finalitats:
- Administració del personal
- Gestió de pacients / usuaris
- Facturació i gestió d'ingressos de l'hospital
- Controlar les visites i proves mèdiques

## Rols

S'han definit diferents rols dins del sistema:
- Admin: control total
- Metge: accés a dades mèdiques
- Infermer accés limitat
- Vari: personal administratiu o altres
- Pacient: accés només a les seves dades pròpies

## Mesures de seguretat aplicades

S'han aplicat diveres mesures com:
- Autenticacio: contrasenyes guardades com hash, no es guarden en text pla.
- Connexió segura: SSL per protegir la comunicació amb la BD
- Separació d'esquemes: seguretat, pacient, estructura, dades_per, cantina
- Control per rols: accés restringit segons l'usuari.

El control d'accés es basa en els usuaris autenticats, assignació dels rols, permisos específics sobre les taules. Es dona accés al mínim privilegi, cada usuari només accedeix al necessari.

## Datamasking

Per protegir les dades s'utilitza una extensió de PostgreSQL "Anonymizer". Les dades es veuen amb asteriscos, algunes ocultes i d'altres només parcialment per poder identificar que les dades introduïdes estàn correctas, per exemple:

DNI: *****12A

## Drets dels usuaris RGPD/ARCO

- Accés: saber quines dades es guarden
- Rectificació: modificar les dades incorrectes
- Cancel·lació: eliminar les dades
- Oposició: negar-se al tractament

També tenen dret a l'oblit i a la limitació del tractament.

## Compliment de la normativa


