#variables
DATA=$(date +%Y-%m-%d)
RUTA_FULL="/backup/base/${DATA}_FULL"

#crear copia completa de la base de dades a la ruta indicada
sudo -u postgres pg_basebackup -D $RUTA_FULL -Fp -Xs -T /var/lib/postgresql/data=$RUTA_FULL/extra_data

#modifiquem per a que s’indiqui que aquesta copia es la ultima, així es simple per a fer les incrementals
sudo rm -f /backup/base/ULTIMA_COMPLETA
sudo ln -s $RUTA_FULL /backup/base/ULTIMA_COMPLETA
