#!/system/bin/sh
# backup_ubuntu22.sh - Backup für proot-distro ubuntu22 Container
# Basiert auf rem_ubuntu2.sh, aber ohne Lösch-Funktion

# ============================================================
# KONFIGURATION
# ============================================================
# 🔥 WICHTIG: Passe ggf. den Pfad an, falls dein Container anders heißt
CONTAINER_NAME="ubuntu22"
PROOT_DISTRO_BASE="/data/data/com.termux/files/usr/var/lib/proot-distro/containers"

# Automatische Erkennung des Rootfs-Pfades
find_rootfs() {
    local possible_paths="
        ${PROOT_DISTRO_BASE}/${CONTAINER_NAME}/rootfs
        ${PREFIX}/var/lib/proot-distro/containers/${CONTAINER_NAME}/rootfs
        /data/data/com.termux/files/usr/var/lib/proot-distro/containers/${CONTAINER_NAME}/rootfs
    "
    
    for path in $possible_paths; do
        if [ -d "$path" ] && [ -d "$path/bin" ]; then
            echo "$path"
            return 0
        fi
    done
    
    # Fallback: Suche in allen Containern
    for container_dir in ${PROOT_DISTRO_BASE}/*/rootfs; do
        if [ -d "$container_dir" ] && [ -d "$container_dir/bin" ]; then
            echo "$container_dir"
            return 0
        fi
    done
    
    return 1
}

ROOTFS_DIR=$(find_rootfs)
if [ -z "$ROOTFS_DIR" ]; then
    echo "❌ Rootfs für '$CONTAINER_NAME' nicht gefunden!"
    echo "📁 Erwartet unter: ${PROOT_DISTRO_BASE}/${CONTAINER_NAME}/rootfs"
    echo "📝 Prüfe mit: ls -la ${PROOT_DISTRO_BASE}/"
    exit 1
fi

# Ausgabeverzeichnis (kann per --output überschrieben werden)
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
MAGENTA='\033[0;35m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[⚠]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_progress() { echo -e "${CYAN}[➜]${NC} $1"; }

# ============================================================
# BACKUP ERSTELLEN
# ============================================================
create_backup() {
    log_info "Starte Backup von: $ROOTFS_DIR"
    
    if [ ! -d "$ROOTFS_DIR" ]; then
        log_error "Rootfs-Verzeichnis nicht gefunden!"
        return 1
    fi
    
    cd "$ROOTFS_DIR" || {
        log_error "Kann nicht in $ROOTFS_DIR wechseln"
        return 1
    }
    
    local OUTPUT_FILE="$OUTPUT_DIR/$BACKUP_NAME"
    log_progress "Erstelle Backup: $OUTPUT_FILE"
    
    # Backup mit Ausschluss von gemounteten/systemrelevanten Ordnern
    tar -czf "$OUTPUT_FILE" \
        --no-same-owner \
        --no-same-permissions \
        --exclude='tmp/*' \
        --exclude='proc/*' \
        --exclude='proc' \
        --exclude='sys/*' \
        --exclude='sys' \
        --exclude='dev/*' \
        --exclude='dev' \
        --exclude='run/*' \
        --exclude='run' \
        --exclude='vendor/*' \
        --exclude='system/*' \
        --exclude='apex/*' \
        --exclude='sdcard/*' \
        --exclude='sdcard' \
        --exclude='storage/*' \
        --exclude='mnt/*' \
        --exclude='mnt' \
        --exclude='boot' \
        --exclude='media/*' \
        --exclude='media' \
        --exclude='var/cache/*' \
        --exclude='var/log/*' \
        --exclude='var/tmp/*' \
        --exclude='root/.cache/*' \
        --exclude='home/*/.cache/*' \
        --exclude='*.log' \
        --exclude='*.pid' \
        --exclude='root/.bash_history' \
        --exclude='home/*/.bash_history' \
        . 2>/dev/null
    
    local TAR_EXIT=$?
    sync
    sleep 1
    
    if [ $TAR_EXIT -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        local SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
        log_success "Backup erfolgreich erstellt!"
        log_success "  📁 Pfad: $OUTPUT_FILE"
        log_success "  📦 Größe: $SIZE"
        
        # Optional: Kopie nach $PREFIX/files/ (falls vorhanden)
        if [ -d "$PREFIX/files" ]; then
            cp "$OUTPUT_FILE" "$PREFIX/files/ubuntu22_backup_latest.tar.gz"
            log_success "  📋 Kopie nach: $PREFIX/files/ubuntu22_backup_latest.tar.gz"
        fi
    else
        log_error "Fehler beim Erstellen des Backups!"
        return 1
    fi
}

# ============================================================
# INFO ANZEIGEN
# ============================================================
show_info() {
    echo ""
    echo "============================================================"
    echo "  ${MAGENTA}backup_ubuntu22.sh${NC} - Backup für proot-distro Container"
    echo "============================================================"
    echo ""
    echo "📁 Gefundenes Rootfs: $ROOTFS_DIR"
    echo "📁 Ausgabe: $OUTPUT_DIR/$BACKUP_NAME"
    echo ""
    echo "📌 Hinweis: Dieses Skript löscht KEINE Dateien!"
    echo "   Es erstellt nur ein Backup des Rootfs."
    echo ""
    echo "📌 Um das Backup wiederherzustellen:"
    echo "   1. Container stoppen: proot-distro stop $CONTAINER_NAME"
    echo "   2. Altes Rootfs sichern: mv $ROOTFS_DIR ${ROOTFS_DIR}.old"
    echo "   3. Backup entpacken: tar -xzf $OUTPUT_DIR/$BACKUP_NAME -C $ROOTFS_DIR"
    echo "   4. Container starten: proot-distro start $CONTAINER_NAME"
    echo ""
    echo "============================================================"
}

# ============================================================
# HAUPT-FUNKTION
# ============================================================
main() {
    # Optionen parsen
    while [ $# -gt 0 ]; do
        case "$1" in
            --output) OUTPUT_DIR="$2"; shift 2 ;;
            --help|-h) 
                echo "Verwendung: backup_ubuntu22.sh [--output /pfad] [--help]"
                echo "  --output /pfad  - Backup-Verzeichnis (Standard: /sdcard)"
                echo "  --help          - Diese Hilfe anzeigen"
                exit 0
                ;;
            *) log_error "Unbekannte Option: $1"; exit 1 ;;
        esac
    done
    
    show_info
    create_backup
    
    echo ""
    log_success "Backup-Vorgang abgeschlossen!"
}

main "$@"
