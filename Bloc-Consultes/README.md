# Bloc de Consultes

Informes i consultes que es realitzen dins l'hospital. Les consultes es fan directament sobre postgresql.

## Obligatori
### Informació de la planta
Donada aquesta consulta demana es proporcionara:

- El total de habitacions que n'hi ha.
- El total de quirofans disponibles.
- El total de personal que en te assignat
 
Funcionament:

Des de l'aplicatiu es seleccionara la planta a escollir i seguidament gracies a una vista dins del servidor s'extreuran aquestes dades i es mostraran dins l'aplicatiu.

Aquest informe permet:
- Conèixer els recursos disponibles de cada planta
- Controlar la distribució del personal
- Facilitar la gestió interna de l’hospital

### INFORME: Tot el personal
Es vol un informe amb les dades completes de tot el personal.

Aquestes dades poden ser sensibles, com ja es va fer datamasking anteriorment, faria falta només que es demani aquestes dades des de l'aplicatiu i mostrar-ho.

Aquest informe és útil per:
- Recursos humans
- Administració
- Gestió interna del personal

### INFORME: Nombre de visites

Aquest informe mostrarà el nombre total de visites mèdiques ateses durant el dia.

El sistema realitzarà una consulta sobre les visites registrades i agruparà la informació per data.

Permet:
- Controlar l’activitat diària de l’hospital
- Detectar moments de més càrrega assistencial
- Obtenir estadístiques de funcionament

## Opcional
### Ranking de metges

Es generarà un ranking dels metges que han atès més pacients

### Funcionament

Mitjançant les dades de les visites registrades es comptabilitzaran les atencions realitzades per cada metge i es mostrarà una classificació ordenada.

- Analitzar la càrrega de treball
- Detectar possibles saturacions
- Obtenir estadístiques internes de rendiment
