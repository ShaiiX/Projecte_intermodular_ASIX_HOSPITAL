# Planificació inicial

# Requisits del sistema

## SO
- Utilitzarem el ubuntu 24.04 TLS, per la seva simplicitat i facilitat per a donar el servei que es vol proporcionar.

## Base de dades
- Utilitzarem PostgreSQL com a bd com a SGBD perquè és gratuït, i de codi obert, aquesta eina ja l’hem utilitzat a clase per tant tenim experiència a l’hora d’utilitzar-la.  
- S'utilitzarà el UTF-8 per als caracters cirilics  
- Té eines per realitzar la replicació  
- PostgreSQL en Linux però amb un partner darrera com RedHat per tenir assistència tècnica  

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
- Utilitzarem una arquitectura Actiu-passiu, ja que sería per a un pressupost baix, que és just el que busquem  
- Farem una replicació Master-Slave:
  - El master permet escriure i modificar dades  
  - El slave és només de lectura i es replica en temps real  
  - En cas de fallada del master, el slave es converteix en el nou master  
- Utilització de NAS HP:
  - Emmagatzematge centralitzat per a backups físics  
  - Permet guardar còpies sense afectar el rendiment del servidor principal  
  - Alta disponibilitat i redundància de dades  
  - Assistència tècnica en cas de fallada de hardware  

## Backups
- Estratègia general:
  - Backup complet setmanal  
  - Backup incremental diari  
  - Separació de còpies en diferents ubicacions  

- Tipus de backups:
  - Backup físic:
    - Còpia directa dels fitxers de PostgreSQL  
    - Emmagatzematge al NAS HP per seguretat i disponibilitat  
  - Backup en calent:
    - Sense aturar el servei de PostgreSQL  
    - Permet continuar treballant mentre es fa la còpia  

- Automatització:
  - Execució automàtica amb Cron a Linux (02:00 AM)  

- Funcionament:
  - Les dades es processen primer en memòria i després a disc  
  - Les transaccions es guarden en logs (WAL)  
  - En cas de fallada:
    - Es restaura la còpia des del NAS  
    - S’apliquen els logs  
    - Recuperació fins a l’últim punt possible  

## Dummy data
- Generar les dades amb eina Faker, que s’incorpora amb el python, el llenguatge que utilitzarem  
- 100.000 visites  
- 50.000 pacients  
- 100 metges  
- 200 infermers  
- 50 persones d’administració  

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