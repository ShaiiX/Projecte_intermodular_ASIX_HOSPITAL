# Còpies de seguretat i Extracció de dades

Aquest document defineix les mesures de seguretat aplicades en la gestió de les còpies de seguretat i en l'extracció de dades del sistema. Les dades tractades són sensibles (especialment dades personals i mèdiques), per tant és essencial garantir la seva confidencialitat, integritat i disponibilitat en tot moment.

## Seguretat en l’extracció de dades

Quan es treuen dades del sistema, es segueixen una sèrie de mesures per evitar accessos no autoritzats o usos indeguts:

- Només usuaris autoritzats poden realitzar extraccions
- Regstre d'activitat (logs) per controlar qui accedeix i què fa
- Validació de la finalitat de l’extracció (només per usos justificats)

A més, es revisa periòdicament l’ús de les dades exportades per assegurar que no es fa un ús incorrecte o fora del sistema.

## Control d'accés als backups

L'accés als backups està restringit únicament a administradors del sistema. Aquest accés requereix autenticació obligatòria i queda registrat per garantir la traçabilitat.

Els usuaris amb accés als backups segueixen el principi de mínim privilegi, és a dir, només tenen els permisos necessaris per realitzar les seves funcions, evitant accessos innecessaris o excessius.

## Xifrat de dades

El xifrat de dades és una de les mesures més importants per protegir la informació sensible. S'aplica en:

- Backups, per evitar que es puguin llegir en cas de pèrdua o robatori
- Transferència de dades, utilitzant connexions segures (SSL)
- Fitxers exportats, per protegir-los fora del sistema

Aquest xifrat garanteix que, fins i tot en cas d'accés no autoritzat, la informació no sigui comprensible.

## Restauració de les dades

La restauració de dades és un procés crític i controlat. Només el pot realitzar personal autoritzat, seguint un procediment establert.

Abans de restaurar, es verifica la integritat de la còpia de seguretat per evitar errors o corrupció de dades. També es realitzen tests periòdics de recuperació per assegurar que el sistema es pot restaurar correctament en cas d’incident.

## Compliment normativa

Amb totes aquestes mesures es busca garantir els següents principis de seguretat:

- Confidencialitat (les dades estan protegides davant accessos no autoritzats)
- Integritat (les dades no es modifiquen de forma incorrecta)
- Disponibilitat (les dades es poden recuperar quan sigui necessari)

*Aquest sistema compleix amb: RGPD i LOPDGDD*