#variables
DATA_AVUI=$(date +%Y-%m-%d)
RUTA_INC="/backup/base/${DATA_AVUI}_INC"

#fem la creació de la copia incremental amb l’ajuda del incremental del pg_basebackup i la ultima completa i els WAL.
sudo -u postgres pg_basebackup -D "$RUTA_INC" --incremental=/backup/base/ULTIMA_COMPLETA/backup_manifest -Fp -Xs -v -T /var/lib/postgresql/data="${RUTA_INC}/extra_data"

