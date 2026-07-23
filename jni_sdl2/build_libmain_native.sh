#!/system/bin/sh
# build_libmain_native.sh - libmain.so manuell mit NDK bauen
# Dieses Script kompiliert start.c mit der richtigen Python-Version

echo "============================================================"
echo "🔧 Baue libmain.so (Native Build)"
echo "============================================================"

# ============================================================
# PFADE (exakt für deine Umgebung)
# ============================================================
DIST_DIR="/root/.buildozer/android/platform/build-arm64-v8a/dists/loginapp7"
START_C="$DIST_DIR/jni/application/src/start.c"
OUTPUT_DIR="$DIST_DIR/libs/arm64-v8a"

# NDK Pfade
NDK="/opt/ndk/android-ndk-r29"
TOOLCHAIN="$NDK/toolchains/llvm/prebuilt/linux-x86_64"
TARGET="aarch64-linux-android"
API="25"

# Python Include und Library Pfade
PYTHON_INCLUDE="/root/.buildozer/android/platform/build-arm64-v8a/build/other_builds/python3/arm64-v8a__ndk_target_25/python3/android-build/android-root/include/python3.11"
PYTHON_LIB="/root/.buildozer/android/platform/build-arm64-v8a/build/other_builds/python3/arm64-v8a__ndk_target_25/python3/android-build/android-root/lib"

echo ""
echo "📁 DIST_DIR: $DIST_DIR"
echo "📁 START_C: $START_C"
echo "📁 OUTPUT_DIR: $OUTPUT_DIR"
echo "📁 NDK: $NDK"
echo "📁 PYTHON_INCLUDE: $PYTHON_INCLUDE"
echo "📁 PYTHON_LIB: $PYTHON_LIB"
echo ""

# ============================================================
# PRÜFUNGEN
# ============================================================
if [ ! -f "$START_C" ]; then
    echo "❌ start.c nicht gefunden: $START_C"
    echo "📝 Erwartete Struktur:"
    echo "   $DIST_DIR/jni/application/src/start.c"
    exit 1
fi
echo "✅ start.c gefunden"

if [ ! -d "$TOOLCHAIN" ]; then
    echo "❌ NDK Toolchain nicht gefunden: $TOOLCHAIN"
    echo "📝 Suche nach NDK..."
    NDK_FOUND=$(find /opt -name "ndk-build" 2>/dev/null | head -1)
    if [ -n "$NDK_FOUND" ]; then
        NDK=$(dirname "$(dirname "$NDK_FOUND")")
        TOOLCHAIN="$NDK/toolchains/llvm/prebuilt/linux-x86_64"
        echo "✅ NDK gefunden: $NDK"
    else
        echo "❌ NDK nicht gefunden!"
        exit 1
    fi
fi
echo "✅ NDK Toolchain: $TOOLCHAIN"

if [ ! -f "$PYTHON_INCLUDE/Python.h" ]; then
    echo "❌ Python.h nicht gefunden: $PYTHON_INCLUDE/Python.h"
    echo "📝 Suche nach Python.h..."
    PYTHON_INCLUDE_FOUND=$(find /root/.buildozer/android/platform/build-arm64-v8a -name "Python.h" 2>/dev/null | head -1)
    if [ -n "$PYTHON_INCLUDE_FOUND" ]; then
        PYTHON_INCLUDE=$(dirname "$PYTHON_INCLUDE_FOUND")
        PYTHON_LIB=$(dirname "$PYTHON_INCLUDE")/../lib
        echo "✅ Python Include gefunden: $PYTHON_INCLUDE"
        echo "✅ Python Lib gefunden: $PYTHON_LIB"
    else
        echo "❌ Python.h nicht gefunden!"
        exit 1
    fi
fi
echo "✅ Python Include: $PYTHON_INCLUDE"
echo "✅ Python Library: $PYTHON_LIB"

mkdir -p "$OUTPUT_DIR"
echo "✅ Output-Verzeichnis erstellt: $OUTPUT_DIR"

# ============================================================
# KOMPILIEREN
# ============================================================
echo ""
echo "🔧 Kompiliere start.c..."
echo "------------------------------------------------------------"
echo "📝 Befehl:"
echo "   $TOOLCHAIN/bin/${TARGET}${API}-clang \\"
echo "       -fPIC -shared \\"
echo "       -o $OUTPUT_DIR/libmain.so \\"
echo "       -I$PYTHON_INCLUDE \\"
echo "       -I$(dirname "$START_C") \\"
echo "       $START_C \\"
echo "       -llog -lm \\"
echo "       -L$PYTHON_LIB \\"
echo "       -lpython3.11"
echo "------------------------------------------------------------"

$TOOLCHAIN/bin/${TARGET}${API}-clang \
    -fPIC \
    -shared \
    -o "$OUTPUT_DIR/libmain.so" \
    -I"$PYTHON_INCLUDE" \
    -I"$(dirname "$START_C")" \
    "$START_C" \
    -llog \
    -lm \
    -L"$PYTHON_LIB" \
    -lpython3.11 2>&1

if [ $? -eq 0 ]; then
    echo "------------------------------------------------------------"
    echo "✅ libmain.so erstellt"
    echo "📁 Pfad: $OUTPUT_DIR/libmain.so"
    echo "📏 Größe: $(du -h "$OUTPUT_DIR/libmain.so" | cut -f1)"
    echo ""
    echo "🔍 Prüfe Symbole:"
    echo "------------------------------------------------------------"
    
    # Prüfe JNI_OnLoad
    if nm -D "$OUTPUT_DIR/libmain.so" 2>/dev/null | grep -q JNI_OnLoad; then
        echo "✅ JNI_OnLoad gefunden!"
        nm -D "$OUTPUT_DIR/libmain.so" | grep JNI_OnLoad
    else
        echo "⚠️ JNI_OnLoad NICHT gefunden!"
        echo "📝 Stelle sicher, dass start.c JNI_OnLoad() enthält"
    fi
    
    # Prüfe Python-Symbole
    echo ""
    echo "🔍 Prüfe Python-Symbole:"
    if nm -D "$OUTPUT_DIR/libmain.so" 2>/dev/null | grep -q "Py_Initialize"; then
        echo "✅ Py_Initialize gefunden!"
    else
        echo "⚠️ Py_Initialize NICHT gefunden!"
    fi
    
else
    echo "------------------------------------------------------------"
    echo "❌ Fehler beim Erstellen von libmain.so!"
    echo "📝 Prüfe die Fehlermeldungen oben"
    exit 1
fi

# ============================================================
# KOPIEREN
# ============================================================
echo ""
echo "📋 Kopiere libmain.so in APK-Struktur..."
#mkdir -p "$DIST_DIR/app/src/main/jniLibs/arm64-v8a"
#cp "$OUTPUT_DIR/libmain.so" "$DIST_DIR/app/src/main/jniLibs/arm64-v8a/libmain.so" 2>/dev/null
#echo "✅ Kopiert nach: $DIST_DIR/app/src/main/jniLibs/arm64-v8a/libmain.so"

# ============================================================
# PRÜFEN
# ============================================================
echo ""
echo "📋 Prüfe libmain.so:"
echo "------------------------------------------------------------"
file "$OUTPUT_DIR/libmain.so"
echo ""
echo "📋 Strings (erste 20):"
strings "$OUTPUT_DIR/libmain.so" | head -20

echo ""
echo "============================================================"
echo "✅ Fertig!"
echo "📁 libmain.so liegt in:"
echo "   $OUTPUT_DIR/libmain.so"
#echo "   $DIST_DIR/app/src/main/jniLibs/arm64-v8a/libmain.so"
echo "============================================================"