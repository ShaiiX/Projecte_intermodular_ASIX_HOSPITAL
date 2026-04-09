# Entitats i atributs

## Personal (generalització)
### (id_personal, nom, cognoms, DNI, telèfon, adreça)
Aquesta entitat es tractara d'una entitat jerarquica on es guardara informació de tot el personal de l'hospital
On seguidament cada subentitat incorporara informació especifica extra.

## Subentitats Personal
### Personal_Medic
### (id_personal, especialitat, estudis, curriculum)
Entitat per al personal de medic, té les mateixes dades que tots els personals més les seves dades especifiques, com els estudis.

### Personal_Infermeria
### (id_personal, )
Entitat per al personal de infermeria, amb les seves dades personals, més les especifiques.

### Personal_vari
### (id_personal, tipus_feina)
Entitat per al personal vari, que seria els zeladors, administratius, conductors d'ambulàncies...

## Planta
### (num_planta)

## Habitacio
### (id_habitacio, num_habitacio, num_planta)

## Aparell_Medic
### (id_aparell, nom, tipus)

## Quirofan
### (id_quirofan, num_quirofan, num_planta)

## Pacient
### (id_pacient, nom, cognoms, DNI, data_naixement)

## visita
### 

## Medicament
### (id_medicament, nom)

## reservacio_habitacio
###

## operacio
###