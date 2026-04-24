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

