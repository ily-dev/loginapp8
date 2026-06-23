#!/bin/bash
# init-host.sh - Ubuntu Version (angepasst)

# ============================================================
# VERZEICHNISSE
# ============================================================
UBUNTU_DIR=$PREFIX/local/ubuntu
APP_FILES_DIR=$PREFIX/files
PROFILE=$PREFIX/local/ubuntu/root/.profile

mkdir -p $UBUNTU_DIR

# ============================================================
# UBUNTU ROOTFS ENTPACKEN (WENN NICHT VORHANDEN)
# ============================================================
if [ -z "$(ls -A "$UBUNTU_DIR" | grep -vE '^(root|tmp)$')" ]; then
    echo "📦 Entpacke Ubuntu Rootfs..."
    tar -xf "$PREFIX/files/ubuntu.tar.gz" -C "$UBUNTU_DIR"
    tar -xpf ubuntu.tar.gz -C ubuntu --no-same-owner --no-same-permissions 2>/dev/null
    echo "✅ Ubuntu Rootfs entpackt"
fi

# ============================================================
# PROOT BINARY KOPIEREN
# ============================================================
[ ! -e "$PREFIX/local/bin/proot" ] && cp "$PREFIX/files/proot" "$PREFIX/local/bin"

# ============================================================
# UBUNTU-BENUTZER ANLEGEN
# ============================================================
# (wird später im init.sh gemacht)

# ============================================================
# PROOT ARGUMENTE
# ============================================================
ARGS="--kill-on-exit"
ARGS="$ARGS -w /"

# System-Mounts (bleiben gleich)
for system_mnt in /apex /odm /product /system /system_ext /vendor \
 /linkerconfig/ld.config.txt \
 /linkerconfig/com.android.art/ld.config.txt \
 /plat_property_contexts /property_contexts; do

 if [ -e "$system_mnt" ]; then
  system_mnt=$(realpath "$system_mnt")
  ARGS="$ARGS -b ${system_mnt}"
 fi
done
unset system_mnt

# Standard-Mounts
ARGS="$ARGS -b /sdcard"
ARGS="$ARGS -b /storage"
ARGS="$ARGS -b /dev"
ARGS="$ARGS -b /data"
ARGS="$ARGS -b /dev/urandom:/dev/random"
ARGS="$ARGS -b /proc"
ARGS="$ARGS -b $PREFIX"
ARGS="$ARGS -b $PREFIX/local/stat:/proc/stat"
ARGS="$ARGS -b $PREFIX/local/vmstat:/proc/vmstat"

# App-Verzeichnis einbinden (für Python-Apps)
if [ -d "$APP_FILES_DIR" ]; then
    ARGS="$ARGS -b $APP_FILES_DIR:/root/app_files"
    echo -e "\e[32;1m[+] \e[0mApp-Verzeichnis eingebunden $APP_FILES_DIR --> /root/app_files \e[0m"
else
    echo "⚠️ App-Verzeichnis nicht gefunden: $APP_FILES_DIR"
fi

# FDs für Shell
if [ -e "/proc/self/fd" ]; then
  ARGS="$ARGS -b /proc/self/fd:/dev/fd"
fi
if [ -e "/proc/self/fd/0" ]; then
  ARGS="$ARGS -b /proc/self/fd/0:/dev/stdin"
fi
if [ -e "/proc/self/fd/1" ]; then
  ARGS="$ARGS -b /proc/self/fd/1:/dev/stdout"
fi
if [ -e "/proc/self/fd/2" ]; then
  ARGS="$ARGS -b /proc/self/fd/2:/dev/stderr"
fi

# Ubuntu-spezifische Mounts
ARGS="$ARGS -b $PREFIX"
ARGS="$ARGS -b /sys"

# TMP-Verzeichnis
if [ ! -d "$PREFIX/local/ubuntu/tmp" ]; then
 mkdir -p "$PREFIX/local/ubuntu/tmp"
 chmod 1777 "$PREFIX/local/ubuntu/tmp"
fi
ARGS="$ARGS -b $PREFIX/local/ubuntu/tmp:/dev/shm"

# Ubuntu Rootfs
ARGS="$ARGS -r $PREFIX/local/ubuntu"

# PROOT-Flags
ARGS="$ARGS -0"
ARGS="$ARGS --link2symlink"
ARGS="$ARGS --sysvipc"
ARGS="$ARGS -L"

# ============================================================
# STARTE INIT.SH (MIT UBUNTU SHELL)
# ============================================================
$LINKER $PREFIX/local/bin/proot $ARGS sh $PREFIX/local/bin/init "$@"