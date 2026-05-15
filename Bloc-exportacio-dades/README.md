# Bloc d'exportació dades

Permet consultes de dades fora de l'aplicació de Python i utilitzar externes com PowerBi.

## Exportació de visites realitzades entre dues 

El sistema ha de descarregar totes le visites realitzades entre dues dates seleccionades per l'usuari.

Les dades exportades inclouen:

- Identificador de la visita
- Data de la visita
- Metge assignat
- DNI del pacient
- Nom del pacient
- Cognoms
- Targeta sanitària

### Funcionament

Des de l'aplicació l'usuari selecciona la data inicial, la final i el format d'exportació. El sistema realitza la consulta al postgres i genera automàticament el fitxer amb les dades.

## Formats suportats

### XML

Exportar les visites en format Xml:

- Documents estructurats
- Dades jeràrquiques
- Format de tabulacions

També es crea un fitxer XSD per validar l’estructura del XML, que comprova els tipus de dades, camps obligatoris, estructura correcta del doc.

### JSON

També es permet exportar les dades en format JSON

- Format lleuger
- Fàcil de llegir
- Compatible amb PowerBI
- Compatible amb altres aplicacions

També es generen indentats per facilitar la lectura. Creació d'un JSON schema per validar l’estructura del document.

## Validació dels fitxers

Per garantir que els fitxers exportats siguin correctes. 

- XML: validació XSD
- JSON: validació amb JSON schema

---

# Dashboard PowerBI

## Objectiu

El dashboard permet visualitzar de forma gràfica la informació de les visites de l'hospital. Hem utlitzat PowerBI per representar les dades exportades. Per poder obtenir una ràpida de l’activitat de l’hospital.

## Informació mostrada

El dashboard inclou:

- Total de visites del dia actual
- Desglòs de visites per àrea medica

Exemples:

- Traumatologia
- Pediatria
- Cardiologia
- Neurologia
- Urgències

## Gràfics utilitzats

### Total de visites

Es mostra el nombre total de visites realitzades durant el dia actual.

Aquest indicador permet veure ràpidament la càrrega general de l’hospital.

### Visites per àrea

Es mostra un gràfic amb el detall de visites segons l’especialitat mèdica. Per poder identificar:

- Àrees amb més activitat
- Distribució de pacients
- Càrrega de treball per departament

## Funcionament

1. Postgres guarda les dades de les visites.
2. Les dades s’exporten des de l’aplicació.
3. Powerbi importa aquestes dades.
4. El dashboard genera els gràfics automàticament.

