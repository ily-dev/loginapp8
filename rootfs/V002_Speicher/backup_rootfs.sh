#!/system/bin/sh
# backup_ubuntu22.sh - Backup für proot-distro ubuntu22 Container mit Fortschritt

# ============================================================
# KONFIGURATION
# ============================================================
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

OUTPUT_DIR="${OUTPUT_DIR:-/sdcard}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="ubuntu22_backup_${TIMESTAMP}.tar.gz"

# ============================================================
# FARBEN & HELPER
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

format_size() {
    local size="$1"
    if [ -z "$size" ] || [ "$size" -eq 0 ]; then
        echo "0B"
        return
    fi
    if [ "$size" -gt 1073741824 ]; then
        echo "$(echo "scale=2; $size/1073741824" | bc) GB"
    elif [ "$size" -gt 1048576 ]; then
        echo "$(echo "scale=2; $size/1048576" | bc) MB"
    elif [ "$size" -gt 1024 ]; then
        echo "$(echo "scale=2; $size/1024" | bc) KB"
    else
        echo "${size}B"
    fi
}

# ============================================================
# GRÖSSENABSCHÄTZUNG VOR DEM BACKUP
# ============================================================
estimate_backup_size() {
    log_info "Analysiere Rootfs für Größenabschätzung..."
    
    cd "$ROOTFS_DIR" || return
    
    # Berechne die Größe aller Dateien (ohne ausgeschlossene Ordner)
    local total_size=$(find . \
        -not -path "./tmp/*" \
        -not -path "./proc/*" \
        -not -path "./sys/*" \
        -not -path "./dev/*" \
        -not -path "./run/*" \
        -not -path "./vendor/*" \
        -not -path "./system/*" \
        -not -path "./apex/*" \
        -not -path "./sdcard/*" \
        -not -path "./storage/*" \
        -not -path "./mnt/*" \
        -not -path "./boot" \
        -not -path "./media/*" \
        -type f -exec du -b {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
    
    # Schätzung: Archiv wird etwa 60-80% der Originalgröße sein (durch Komprimierung)
    local estimated_archive_size=$((total_size * 70 / 100))
    
    echo ""
    echo "============================================================"
    echo "📊 ${CYAN}GRÖSSENABSCHÄTZUNG VOR DEM BACKUP${NC}"
    echo "============================================================"
    printf "%-35s %15s\n" "Ursprüngliche Rootfs-Größe" "$(format_size $total_size)"
    printf "%-35s %15s\n" "Geschätzte Archiv-Größe (ca. 70%)" "$(format_size $estimated_archive_size)"
    echo "============================================================"
    echo ""
    
    export ESTIMATED_SIZE=$estimated_archive_size
}

# ============================================================
# BACKUP MIT FORTSCHRITTSBALKEN
# ============================================================
create_backup_with_progress() {
    log_info "Starte Backup mit Fortschrittsanzeige..."
    
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
    
    # Zähle die Anzahl der Dateien für den Fortschritt
    local total_files=$(find . \
        -not -path "./tmp/*" \
        -not -path "./proc/*" \
        -not -path "./sys/*" \
        -not -path "./dev/*" \
        -not -path "./run/*" \
        -not -path "./vendor/*" \
        -not -path "./system/*" \
        -not -path "./apex/*" \
        -not -path "./sdcard/*" \
        -not -path "./storage/*" \
        -not -path "./mnt/*" \
        -not -path "./boot" \
        -not -path "./media/*" \
        -type f 2>/dev/null | wc -l)
    
    if [ "$total_files" -eq 0 ]; then
        log_warn "Keine Dateien zum Archivieren gefunden!"
        return 1
    fi
    
    # Backup mit Fortschrittsbalken
    local processed=0
    local last_percent=0
    
    # Erstelle temporäre Datei für den Fortschritt
    local progress_file="/tmp/backup_progress_$$"
    echo "0" > "$progress_file"
    
    # Starte tar im Hintergrund
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
        . 2>/dev/null &
    
    local TAR_PID=$!
    
    # Fortschrittsbalken anzeigen, während tar läuft
    echo ""
    echo -e "${CYAN}Fortschritt:${NC}"
    
    while kill -0 "$TAR_PID" 2>/dev/null; do
        # Aktuelle Dateigröße des temporären Archivs
        if [ -f "$OUTPUT_FILE" ]; then
            local current_size=$(du -b "$OUTPUT_FILE" 2>/dev/null | awk '{print $1}')
            local percent=0
            if [ "$ESTIMATED_SIZE" -gt 0 ]; then
                percent=$((current_size * 100 / ESTIMATED_SIZE))
                [ "$percent" -gt 100 ] && percent=100
            fi
            
            # Nur aktualisieren, wenn sich der Prozentwert geändert hat
            if [ "$percent" -ne "$last_percent" ]; then
                last_percent=$percent
                
                # Balken zeichnen
                local bar_length=40
                local filled=$((percent * bar_length / 100))
                local empty=$((bar_length - filled))
                
                printf "\r  ["
                printf "%${filled}s" | tr ' ' '█'
                printf "%${empty}s" | tr ' ' '░'
                printf "] %3d%%  " "$percent"
            fi
        fi
        sleep 1
    done
    
    # Warten auf tar und Exit-Code prüfen
    wait "$TAR_PID"
    local TAR_EXIT=$?
    
    echo ""  # Neue Zeile nach dem Balken
    
    if [ $TAR_EXIT -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        local SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
        log_success "Backup erfolgreich erstellt!"
        log_success "  📁 Pfad: $OUTPUT_FILE"
        log_success "  📦 Größe: $SIZE"
        
        # Optional: Kopie nach $PREFIX/files/
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
    echo "  ${MAGENTA}backup_ubuntu22.sh${NC} - Backup mit Fortschrittsbalken"
    echo "============================================================"
    echo ""
    echo "📁 Gefundenes Rootfs: $ROOTFS_DIR"
    echo "📁 Ausgabe: $OUTPUT_DIR/$BACKUP_NAME"
    echo ""
    echo "📌 Das Backup enthält NICHT:"
    echo "   - /proc, /sys, /dev, /run (gemountete Systemordner)"
    echo "   - /sdcard, /storage, /mnt (externe Speicher)"
    echo "   - Temporäre Dateien (tmp/, cache/, logs/)"
    echo ""
    echo "============================================================"
}

# ============================================================
# HAUPT-FUNKTION
# ============================================================
main() {
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
    estimate_backup_size
    create_backup_with_progress
    
    echo ""
    log_success "Backup-Vorgang abgeschlossen!"
}

main "$@"