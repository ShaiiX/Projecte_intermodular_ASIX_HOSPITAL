# Bloc de manteniment

## Funcionament

### Alta de personal dels treballadors perquè puguin estar registrats al centre
- Metges
- Personal administratiu (vari)
- Infermers

La gestió es realitza a la taula `dades_per.personal` i les seves i les seves especialitzacions (`metge`, `infermer`, `vari`).

### Alta de pacients

Es poden registrar nous pacients amb les seves dades personals i sanitàries. Aquest registre és essencial perquè permet vincular el pacient amb visites, ingressos, receptes i operacions. Cada pacient pot estar assignat a una habitació i això ho facilita.

- Dades identificadores
- Contacte
- Número de targeta sanitària

### Relació infermer - metge/planta

Es pot gestionar la relació del personal d'infermeria, per saber si un infermer està assignat a un metge o bé si treballa en una planta determinada.

Això permet poder organitzar el personal i millorar la organització.

### Gestió d'operacions

Per a un dia en concret permet consultar totes les operacions que hi ha previstes, que inclou:

- El quiròfan assignat
- El pacient a operar
- L'hora 
- Metge responsable que farà les operacions
- El personal d'infermeria que intervidrà

Evita que hi puguin haver problemes de planificació.

### Gestió de visites

Es poden consultar les visites que hi ha planificades per a un dia determinat. Mostra l'hora de la visita, el metge assignat i el pacient.

### Validació PGPLSQL

Per assegurar que les dades siguin correctes, hem implementat triggers que validen les dates dels ingressos 

