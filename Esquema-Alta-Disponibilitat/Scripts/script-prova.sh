#!/bin/bash
set -euo pipefail
export PATH="/usr/lib/postgresql/18/bin:$PATH"
DB_PATH="/var/lib/postgresql/18/main"
BASE_DIR="/backup/base"
INCREMENTAL_DIR="/backup/incremental"
WAL_DIR="/var/lib/postgresql/wal_real"
COMBINED_DIR="/tmp/pg_restore_combined"
PG_USER="postgres"

error()  { echo "[ERROR] $*" >&2; exit 1; }


#  Trobar les còpies més recents 
LATEST_BASE=$(ls -td "${BASE_DIR}/"* 2>/dev/null | head -1) \
  || error "No s'ha trobat cap còpia base a $BASE_DIR"

LATEST_INC=$(ls -td "${INCREMENTAL_DIR}/"* 2>/dev/null | head -1) \
  || error "No s'ha trobat cap còpia incremental a $INCREMENTAL_DIR"

TBLSPC_BASE=$(sudo ls -la "$LATEST_BASE/pg_tblspc/" | awk '/->/{print $NF}' | head -1)
TBLSPC_INC=$(sudo ls -la "$LATEST_INC/pg_tblspc/" | awk '/->/{print $NF}' | head -1)
TBLSPC_DEST="/var/lib/postgresql/18/extra_data"

echo "Base:        $LATEST_BASE"
echo "Incremental: $LATEST_INC"
echo "WAL dir:     $WAL_DIR"


# -- Verificacions prèvies 
[[ -d "$WAL_DIR" ]] || error "Directori WAL no existeix: $WAL_DIR"
[[ -f "$LATEST_BASE/backup_manifest" ]] || error "backup_manifest no trobat a $LATEST_BASE — és una còpia vàlida de pg_basebackup?"
command -v pg_combinebackup >/dev/null 2>&1 || error "pg_combinebackup no trobat. Necessites postgresql-18."


# ── 1. Aturar PostgreSQL ─
echo "Aturant PostgreSQL..."
sudo systemctl stop postgresql || true


# ── 2. Combinar base + incremental 
echo "Combinant còpies amb pg_combinebackup..."
sudo rm -rf "$COMBINED_DIR"
sudo -u "$PG_USER" /usr/lib/postgresql/18/bin/pg_combinebackup \
  --output="$COMBINED_DIR" \
  --tablespace-map="${TBLSPC_BASE}=${TBLSPC_DEST}" \
  --tablespace-map="${TBLSPC_INC}=${TBLSPC_DEST}" \
  "$LATEST_BASE" \
  "$LATEST_INC" \
  || error "pg_combinebackup ha fallat"
echo "Còpies combinades a $COMBINED_DIR"

sudo mkdir -p "$TBLSPC_DEST"
sudo chown "$PG_USER":"$PG_USER" "$TBLSPC_DEST"


# ── 3. Substituir el directori de dades 
echo "Eliminant dades antigues de $DB_PATH..."
sudo rm -rf "${DB_PATH:?}/"*

echo "Copiant backup combinat..."
sudo cp -a "$COMBINED_DIR/." "$DB_PATH/"


# ── 4. Ajustar permisos ──
echo "Configurant permisos..."
sudo chown -R "$PG_USER":"$PG_USER" "$DB_PATH"
sudo chmod 700 "$DB_PATH"


# ── 5. Activar recovery mode 
echo "Activant recovery mode..."
sudo -u "$PG_USER" touch "$DB_PATH/recovery.signal"


# ── 6. Configurar restore_command (sense duplicats) 
echo "Configurant restore_command a postgresql.auto.conf..."
AUTOCONF="$DB_PATH/postgresql.auto.conf"

sudo sed -i \
  -e '/^restore_command[[:space:]]*=/d' \
  -e '/^recovery_target_action[[:space:]]*=/d' \
  "$AUTOCONF" 2>/dev/null || true

sudo -u "$PG_USER" bash -c "cat >> '$AUTOCONF'" <<EOF

# Restauració WAL — restore_postgresql.sh $(date '+%F %T')
restore_command = 'cp ${WAL_DIR}/%f %p'
recovery_target_action = 'promote'
EOF

# ── 7. Netejar directori temporal 
sudo rm -rf "$COMBINED_DIR"

# ── 8. Arrencar PostgreSQL 
echo "Iniciant PostgreSQL (mode recovery)..."
sudo systemctl start postgresql
sudo pg_ctlcluster 18 main start
# ── 9. Esperar que el recovery finalitzi (màx. 5 min) ─────────
echo "Esperant que el recovery WAL acabi..."
MAX=150
for i in $(seq 1 $MAX); do
  if sudo -u "$PG_USER" pg_isready -q 2>/dev/null; then
    IN_RECOVERY=$(sudo -u "$PG_USER" psql -tAq \
      -c "SELECT pg_is_in_recovery();" 2>/dev/null || echo "t")
    if [[ "$IN_RECOVERY" == "f" ]]; then
      echo "Recovery completat. PostgreSQL operatiu i en mode normal."
      echo "Restauració finalitzada correctament."
      exit 0
    fi
    echo "  Aplicant WALs... (${i}x2s)"
  else
    echo "  Esperant connexió... (${i}x2s)"
  fi
  sleep 2
done

error "Recovery no ha acabat en 5 minuts. Comprova: journalctl -u postgresql -n 50"