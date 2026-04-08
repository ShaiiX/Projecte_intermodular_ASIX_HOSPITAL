# Planificació inicial

# Requisits del sistema

## SO
- Utilitzarem el ubuntu 24.04 TLS, per la seva simplicitat i facilitat per a donar el servei que es vol proporcionar.

## Base de dades
- Utilitzarem PostgreSQL com a bd com a SGBD perquè és gratuït, i de codi obert, aquesta eina ja l’hem utilitzat a clase per tant tenim experiència a l’hora d’utilitzar-la.  
- S'utilitzarà el UTF-8 per als caracters cirilics  
- Té eines per realitzar la replicació  

## Seguretat
- Implementarem sistema de rols i usuaris amb permisos restrictius  
- Seguretat amb SSL  
- Sistema de logs d’accés a dades dels pacients  
- Utilització de data masking en dades importants, com contrasenyes  

## AGPD
- Seguir la normativa de AGPD  
- Documentació amb les mesures de seguretat i els tipus de dades  

## Disponibilitat
- Tindrem 2 servidors, el principal i la rèplica  
- Utilitzarem una arquitectura Actiu-Passiu, ja que sería per a un pressupost baix, que és just el que busquem  

## Dummy data
- Generar les dades amb eina Faker, que s’incorpora amb el python, el llenguatge que utilitzarem  
- 100.000 visites  
- 50.000 pacients  
- 100 metges  
- 200 infermers  
- 50 persones d’administració  

## Backups
- Farem còpies completes que inclou tota la base de dades i es farà diàriament  
- Amb aquesta còpia es podria restaurar el sistema complet  
- Es farà també un backup incremental que només guardarà els canvis des de l’últim backup, d’aquesta manera reduïm espai i temps  
- Els backups es faran automàticament  
- Es faran a les 2:00 AM per evitar impactes al rendiment del sistema  

## Integracions i visualitzacions
- Es faran exportacions de dades XML mensualment  
- Enviar les exportacions mitjançant una API a Seguretat social  
- Es farà un dashboard amb vistes per dia, relació metge-pacient etc…  
- S’utilitzarà Power BI  

# Requisits del programa

## Programació
- S’utilitzarà el llenguatge per defecte Python, per la seva simplicitat, a més que coneixem i tenim més experiència amb aquest llenguatge  

## Aplicació
- L’aplicatiu serà per entorn CLI, ja que no volem exposar a l’usuari a molta càrrega, per els pocs recursos que tenen els dispositiu  

# Requisits de documentació

## Documentació
- Totes les documentacions les farem amb MarkDown utilitzant VSCode com a eina principal de desenvolupament, tot es pujarà al repositori de GitHub (compartit)  

- Document d’instal·lació i configuració  
- Manual d’usuari detallat  
- Document de planificació  
- Enllaç al Diari de Sessions  
- Enllaç al Jira  

---

Shaila Martínez - Arnau Farreras