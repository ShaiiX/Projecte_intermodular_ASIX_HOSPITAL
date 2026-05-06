#!/bin/bash

DB_PATH="/var/lib/postgresql/18/main"
BASE_DIR="/backup/base"
INCREMENTAL_DIR="/backup/incremental"
WAL_DIR="/var/lib/postgresql/wal_real"
LATEST_BASE=$(ls -td $BASE_DIR/* | head -1)
LATEST_INCREMENTAL=$(ls -td $INCREMENTAL_DIR/* | head -1)

echo "parant postgres"
sudo systemctl stop postgresql

echo "eliminant dades antigues”
sudo rm -rf ${DB_PATH:?}/*

echo "restaurant ultima copia completa"
sudo cp -a $LATEST_BASE/* $DB_PATH/
echo "restaurant ultima copia incremental"
sudo cp -a $LATEST_INCREMENTAL/* $DB_PATH/

echo "configurant permisos"
sudo chown -R postgres:postgres $DB_PATH

echo "activant recovery mode"
sudo -u postgres touch $DB_PATH/recovery.signal

echo "configurant restauracio wal"
sudo bash -c "cat >> $DB_PATH/postgresql.auto.conf <<EOF
restore_command = 'cp $WAL_DIR/%f %p'
EOF"

echo "iniciant postgresql"
sudo systemctl start postgresql
echo "restauracio completada"
