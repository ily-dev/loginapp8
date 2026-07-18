#!/system/bin/sh
# backup_ubuntu22.sh - Backup für proot-distro ubuntu22 Container

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

# ============================================================
# GRÖSSEN-FUNKTIONEN (OHNE bc)
# ============================================================
format_size() {
    local size="$1"
    if [ -z "$size" ] || [ "$size" -eq 0 ]; then
        echo "0B"
        return
    fi
    
    # Negativen Wert korrigieren
    if [ "$size" -lt 0 ]; then
        size=$((size * -1))
    fi
    
    if [ "$size" -gt 1073741824 ]; then
        local gb=$((size / 1073741824))
        local remainder=$(((size % 1073741824) * 100 / 1073741824))
        echo "${gb}.${remainder} GB"
    elif [ "$size" -gt 1048576 ]; then
        local mb=$((size / 1048576))
        local remainder=$(((size % 1048576) * 100 / 1048576))
        echo "${mb}.${remainder} MB"
    elif [ "$size" -gt 1024 ]; then
        local kb=$((size / 1024))
        local remainder=$(((size % 1024) * 100 / 1024))
        echo "${kb}.${remainder} KB"
    else
        echo "${size}B"
    fi
}

# ============================================================
# SPEICHERANALYSE PRO VERZEICHNIS
# ============================================================
# ============================================================
# SPEICHERANALYSE PRO VERZEICHNIS (MIT /root UND /opt)
# ============================================================
analyze_storage() {
    log_info "Analysiere Speicherverbrauch pro Verzeichnis..."
    
    cd "$ROOTFS_DIR" || return
    
    echo ""
    echo "============================================================"
    echo "📊 ${CYAN}SPEICHERANALYSE PRO VERZEICHNIS${NC}"
    echo "============================================================"
    printf "%-20s %15s\n" "Verzeichnis" "Belegter Speicher"
    echo "------------------------------------------------------------"
    
    local total_size=0
    
    # 🔥 Jetzt mit /root und /opt
    for dir in bin etc lib root sbin usr var home opt srv tmp; do
        if [ -d "$dir" ]; then
            local size=$(du -sb "$dir" 2>/dev/null | awk '{print $1}')
            if [ -n "$size" ] && [ "$size" -gt 0 ]; then
                printf "%-20s %15s\n" "/$dir" "$(format_size $size)"
                total_size=$((total_size + size))
            fi
        fi
    done
    
    # Zusätzlich: var/cache, var/log, var/tmp, root/.cache
    for dir in var/cache var/log var/tmp root/.cache; do
        if [ -d "$dir" ]; then
            local size=$(du -sb "$dir" 2>/dev/null | awk '{print $1}')
            if [ -n "$size" ] && [ "$size" -gt 0 ]; then
                printf "%-20s %15s\n" "/$dir" "$(format_size $size)"
                total_size=$((total_size + size))
            fi
        fi
    done
    
    echo "------------------------------------------------------------"
    printf "${GREEN}%-20s ${CYAN}%15s${NC}\n" "GESAMT" "$(format_size $total_size)"
    echo "============================================================"
    echo ""
    
    export TOTAL_SIZE=$total_size
}
# ============================================================
# BACKUP MIT FORTSCHRITTSBALKEN (0-100%)
# ============================================================
create_backup() {
    log_info "Starte Backup mit Fortschrittsbalken..."
    
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
    
    # 🔥 NEU: Fortschrittsdatei im HOME-Verzeichnis (beschreibbar!)
    local progress_file="$HOME/backup_progress_$$"
    echo "0" > "$progress_file"
    
    # Starte tar mit Fortschrittsüberwachung
    (
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
        
        echo "100" > "$progress_file"
    ) &
    
    local TAR_PID=$!
    
    # Fortschrittsbalken anzeigen
    echo ""
    echo -e "${CYAN}Fortschritt:${NC}"
    
    local last_percent=0
    local bar_length=50
    
    while kill -0 "$TAR_PID" 2>/dev/null; do
        if [ -f "$progress_file" ]; then
            local percent=$(cat "$progress_file" 2>/dev/null | tr -d '\n')
            if [ -z "$percent" ]; then
                percent=0
            fi
        else
            percent=0
        fi
        
        # Prozentzahl begrenzen
        [ "$percent" -gt 100 ] && percent=100
        
        # Nur aktualisieren, wenn sich der Wert geändert hat
        if [ "$percent" -ne "$last_percent" ]; then
            last_percent=$percent
            
            # Balken zeichnen (ohne printf-Probleme)
            local filled=$((percent * bar_length / 100))
            local empty=$((bar_length - filled))
            
            # Balken manuell zusammenbauen
            local bar="["
            local i=0
            while [ $i -lt $filled ]; do
                bar="${bar}█"
                i=$((i + 1))
            done
            i=0
            while [ $i -lt $empty ]; do
                bar="${bar}░"
                i=$((i + 1))
            done
            bar="${bar}]"
            
            # Prozentzahl mit fester Breite (3 Stellen)
            if [ $percent -lt 10 ]; then
                percent_str="  ${percent}%"
            elif [ $percent -lt 100 ]; then
                percent_str=" ${percent}%"
            else
                percent_str="${percent}%"
            fi
            
            echo -ne "\r  ${bar} ${percent_str}"
        fi
        
        sleep 1
    done
    
    # Auf tar warten und Exit-Code prüfen
    wait "$TAR_PID"
    local TAR_EXIT=$?
    
    # Aufräumen
    rm -f "$progress_file"
    echo ""  # Neue Zeile nach dem Balken
    
    if [ $TAR_EXIT -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        local SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
        echo ""
        log_success "✅ Backup erfolgreich erstellt!"
        log_success "  📁 Pfad: $OUTPUT_FILE"
        log_success "  📦 Größe: $SIZE"
        echo ""
        
        # Kopie nach $PREFIX/files/ (falls vorhanden)
        if [ -d "$PREFIX/files" ]; then
            cp "$OUTPUT_FILE" "$PREFIX/files/ubuntu22_backup_latest.tar.gz"
            log_success "📋 Kopie nach: $PREFIX/files/ubuntu22_backup_latest.tar.gz"
        fi
    else
        log_error "❌ Fehler beim Erstellen des Backups!"
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
    analyze_storage
    create_backup
    
    echo ""
    log_success "Backup-Vorgang abgeschlossen!"
}

main "$@"