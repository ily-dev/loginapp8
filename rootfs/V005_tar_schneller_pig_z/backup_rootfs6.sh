
#!/bin/bash

# backup_ubuntu22.sh - Backup für proot-distro ubuntu22 (64-bit)

# ============================================================
# KONFIGURATION
# ============================================================
CONTAINER_NAME="ubuntu22"
PROOT_DISTRO_BASE="/data/data/com.termux/files/usr/var/lib/proot-distro/containers"

ROOTFS_DIR="${PROOT_DISTRO_BASE}/${CONTAINER_NAME}/rootfs"
if [ ! -d "$ROOTFS_DIR" ] || [ ! -d "$ROOTFS_DIR/bin" ]; then
    echo "❌ Rootfs nicht gefunden: $ROOTFS_DIR"
    exit 1
fi

OUTPUT_DIR="${OUTPUT_DIR:-/sdcard}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="ubuntu22_backup_${TIMESTAMP}.tar.gz"

# ============================================================
# FARBEN
# ============================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[⚠]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_progress() { echo -e "${CYAN}[➜]${NC} $1"; }

# ============================================================
# GRÖSSEN-FORMATIERUNG (64-BIT MIT awk)
# ============================================================
# ============================================================
# GRÖSSEN-FORMATIERUNG MIT MINDEST-EINHEIT
# ============================================================
# ============================================================
# GRÖSSEN-FORMATIERUNG (NUR MB UND GB)
# ============================================================
format_size() {
    local size="$1"
    
    # Prüfen, ob size eine gültige Zahl ist
    if [ -z "$size" ] || ! echo "$size" | grep -qE '^-?[0-9]+$'; then
        echo "0 MB"
        return
    fi
    
    # Negative Werte korrigieren
    if [ "$size" -lt 0 ] 2>/dev/null; then
        size=$((size * -1))
    fi
    
    # Wenn 0
    if [ "$size" -eq 0 ] 2>/dev/null; then
        echo "0 MB"
        return
    fi
    
    # Nur MB und GB anzeigen (alles unter 1 MB wird als 0.00 MB dargestellt)
    echo "$size" | awk '{
        size = $1
        mb = size / 1048576
        gb = size / 1073741824
        
        # Wenn größer als 0.5 GB, zeige GB an (aufgerundet)
        if (gb >= 0.5) {
            printf "%.2f GB\n", gb
        } else {
            # Sonst MB (auch wenn es 0.00 MB sind)
            printf "%.2f MB\n", mb
        }
    }'
}

# ============================================================
# SPEICHERANALYSE (ALLE VERZEICHNISSE, 64-BIT)
# ============================================================
analyze_storage() {
    log_info "Analysiere Speicherverbrauch pro Verzeichnis..."
    
    cd "$ROOTFS_DIR" || return
    
    # Hier kannst du beliebig viele Ordner hinzufügen
    local exclude_list=("root/.buildozer" "tmp" "proc" "root/login_V3/.buildozer")
    
    # Baue die Argumente für du dynamisch zusammen
    local du_args=()
    for item in "${exclude_list[@]}"; do
        du_args+=(--exclude="$item")
    done
    
    echo ""
    echo "============================================================"
    echo "📊 ${CYAN}SPEICHERANALYSE PRO VERZEICHNIS${NC}"
    echo "============================================================"
    printf "%-20s %15s\n" "Verzeichnis" "Belegter Speicher"
    echo "------------------------------------------------------------"
    
    local all_dirs="apex bin boot data dev etc home lib linkerconfig media mnt odm opt proc root run sbin sdcard storage sys system tmp usr var vendor"
    local total_size=0
    
    for dir in $all_dirs; do
        if [ -d "$dir" ]; then
            # Hier werden die du_args eingefügt
            local size=$(du -sb "${du_args[@]}" "$dir" 2>/dev/null | awk '{print $1}')
            if [ -z "$size" ]; then
                size=0
            fi
            
            printf "%-20s %15s\n" "/$dir" "$(format_size "$size")"
            total_size=$(echo "$total_size $size" | awk '{print $1 + $2}')
        fi
    done
    
    echo "------------------------------------------------------------"
    printf "${GREEN}%-20s ${CYAN}%15s${NC}\n" "GESAMT" "$(format_size "$total_size")"
    echo "============================================================"
    echo ""
    
    export TOTAL_SIZE="$total_size"
    
    # Hinweis: exit 1 beendet das gesamte Skript. 
    # Falls das Skript danach weiterlaufen soll, entferne das exit.
    # exit 1
}

# ============================================================
# BACKUP (MIT PV)
# ============================================================
create_backup() {
    log_info "Starte Backup..."
    
    cd "$ROOTFS_DIR" || return
    
    local OUTPUT_FILE="$OUTPUT_DIR/$BACKUP_NAME"
    log_progress "Erstelle: $OUTPUT_FILE"
    
    if command -v pv >/dev/null 2>&1; then
        # Gesamtgröße mit 64-Bit ermitteln
        echo "64Bit ermittelt"
        total_size=$TOTAL_SIZE
        #local total_size=$(du -sb . 2>/dev/null | awk '{print $1}')
        
        # ... in create_backup, ersetze tar -czf ...
        # NEUE VARIANTE:
        
        tar -cf - \
            --exclude=".buildozer" \
            --exclude='tmp/*' --exclude='proc/*' --exclude='proc' \
            --exclude='sys/*' --exclude='sys' --exclude='dev/*' --exclude='dev' \
            --exclude='run/*' --exclude='run' --exclude='sdcard/*' --exclude='sdcard' \
            --exclude='storage/*' --exclude='mnt/*' --exclude='mnt' --exclude='media/*' \
            --exclude='media' --exclude='var/cache/*' --exclude='var/log/*' \
            --exclude='var/tmp/*' --exclude='root/.cache/*' --exclude='home/*/.cache/*' \
            --exclude='*.log' --exclude='*.pid' --exclude='root/.bash_history' \
            --exclude='home/*/.bash_history' \
            . 2>/dev/null | pv -s "$total_size" -p -e -t -r -a | \
            pigz > "$OUTPUT_FILE"
        local tar_exit=$?
        
    else
        echo "32Bit ermittelt"
        tar -czf "$OUTPUT_FILE" \
            --exclude=".buildozer" \
            --exclude='tmp/*' --exclude='proc/*' --exclude='proc' \
            --exclude='sys/*' --exclude='sys' --exclude='dev/*' --exclude='dev' \
            --exclude='run/*' --exclude='run' --exclude='sdcard/*' --exclude='sdcard' \
            --exclude='storage/*' --exclude='mnt/*' --exclude='mnt' --exclude='media/*' \
            --exclude='media' --exclude='var/cache/*' --exclude='var/log/*' \
            --exclude='var/tmp/*' --exclude='root/.cache/*' --exclude='home/*/.cache/*' \
            --exclude='*.log' --exclude='*.pid' --exclude='root/.bash_history' \
            --exclude='home/*/.bash_history' \
            . 2>/dev/null
        local tar_exit=$?
    fi
    
    echo ""
    if [ $tar_exit -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        local SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
        log_success "✅ Backup erfolgreich erstellt!"
        log_success "  📁 Pfad: $OUTPUT_FILE"
        log_success "  📦 Größe: $SIZE"
    else
        log_error "❌ Fehler beim Erstellen des Backups!"
        return 1
    fi
}

# ============================================================
# HAUPT-FUNKTION
# ============================================================
show_info() {
    echo ""
    echo "============================================================"
    echo "  backup_ubuntu22.sh - Backup (64-Bit)"
    echo "============================================================"
    echo "📁 Rootfs: $ROOTFS_DIR"
    echo "📁 Ausgabe: $OUTPUT_DIR/$BACKUP_NAME"
    echo "============================================================"
}

main() {
    show_info
    analyze_storage
    
    if ! command -v pv >/dev/null 2>&1; then
        echo ""
        log_warn "pv nicht installiert. Installiere: pkg install pv"
        printf "Trotzdem fortfahren? (j/n) "
        read -r reply
        if [ "$reply" != "j" ] && [ "$reply" != "J" ]; then
            exit 0
        fi
    fi
    
    create_backup
    log_success "Fertig!"
}

main "$@"