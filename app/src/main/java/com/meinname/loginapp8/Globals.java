// app/main/java/com/meinname/loginapp8/Globals.java
package com.meinname.loginapp8;

import android.content.Context;
import org.kivy.android.PythonService;  // ★ ★ ★ IMPORT ★ ★ ★
import java.io.InputStream;
import java.util.Properties;

public class Globals {
    
    private static final String TAG = "Globals";
    
    // ============================================================
    // APP KONFIGURATION
    // ============================================================
    public static int DIALOG_DELAY = 3000;
    public static String APP_VERSION = "1.2.1";
    public static boolean DEBUG = true;
    public static int TIMEOUT = 30;
    public static int MAX_RETRIES = 3;
    public static String PYTHON_HOME = "";
    public static String LOG_DIR = "/sdcard/logs";
    
    // ============================================================
    // ROOTFS KONFIGURATION
    // ============================================================
    public static String ROOTFS_TYPE = "alpine";
    public static String ROOTFS_FILE = "alpine.tar.gz";
    public static String ROOTFS_DIR = "alpine";
    public static String INIT_SCRIPT = "alpine/init.sh";
    public static String INIT_HOST_SCRIPT = "alpine/init-host.sh";
    
    // ============================================================
    // ★ ★ ★ SHOWLOG ★ ★ ★
    // ============================================================
    public static void showLog(String tag, String message) {
        PythonService.showLog(tag, message);
    }
    
    // ============================================================
    // INITIALISIERUNG
    // ============================================================
    public static void init(Context context) {
        try {
            InputStream inputStream = context.getAssets().open("config.ini");
            Properties props = new Properties();
            props.load(inputStream);
            inputStream.close();
            
            // ============================================================
            // APP KONFIGURATION LADEN
            // ============================================================
            DIALOG_DELAY = Integer.parseInt(props.getProperty("DIALOG_DELAY", "3000"));
            APP_VERSION = props.getProperty("APP_VERSION", "1.2.1");
            DEBUG = Boolean.parseBoolean(props.getProperty("DEBUG", "true"));
            TIMEOUT = Integer.parseInt(props.getProperty("TIMEOUT", "30"));
            MAX_RETRIES = Integer.parseInt(props.getProperty("MAX_RETRIES", "3"));
            PYTHON_HOME = props.getProperty("PYTHON_HOME", "");
            LOG_DIR = props.getProperty("LOG_DIR", "/sdcard/logs");
            
            // ============================================================
            // ROOTFS KONFIGURATION LADEN
            // ============================================================
            ROOTFS_TYPE = props.getProperty("rootfs_type", "alpine").toLowerCase();
            ROOTFS_FILE = props.getProperty("rootfs_file", "alpine.tar.gz");
            ROOTFS_DIR = props.getProperty("rootfs_dir", "alpine");
            INIT_SCRIPT = props.getProperty("init_script", "alpine/init.sh");
            INIT_HOST_SCRIPT = props.getProperty("init_host_script", "alpine/init-host.sh");
            
            // ============================================================
            // LOGGING (mit showLog)
            // ============================================================
            logConfig();
            
        } catch (Exception e) {
            showLog(TAG, "❌ Fehler beim Laden der Konfiguration: " + e.getMessage());
            e.printStackTrace();
            // Fallback-Werte bleiben bestehen
        }
    }
    
    // ============================================================
    // HELPER METHODEN
    // ============================================================
    
    public static boolean isUbuntu() {
        return "ubuntu".equalsIgnoreCase(ROOTFS_TYPE);
    }
    
    public static boolean isAlpine() {
        return "alpine".equalsIgnoreCase(ROOTFS_TYPE);
    }
    
    public static String getRootfsDisplayName() {
        return isUbuntu() ? "Ubuntu Linux" : "Alpine Linux";
    }
    
    public static String getFullAssetPath(String assetName) {
        String cleanName = assetName.startsWith("assets/") ? assetName.substring(7) : assetName;
        return cleanName;
    }
    
    public static String getRootfsFileNameOnly() {
        String file = ROOTFS_FILE;
        return file.substring(file.lastIndexOf('/') + 1);
    }
    
    // ============================================================
    // LOGGING (mit showLog)
    // ============================================================
    private static void logConfig() {
        showLog(TAG, "========================================");
        showLog(TAG, "📋 APP KONFIGURATION");
        showLog(TAG, "========================================");
        showLog(TAG, "📌 DIALOG_DELAY: " + DIALOG_DELAY);
        showLog(TAG, "📌 APP_VERSION: " + APP_VERSION);
        showLog(TAG, "📌 DEBUG: " + DEBUG);
        showLog(TAG, "📌 TIMEOUT: " + TIMEOUT);
        showLog(TAG, "📌 MAX_RETRIES: " + MAX_RETRIES);
        showLog(TAG, "📌 PYTHON_HOME: " + PYTHON_HOME);
        showLog(TAG, "📌 LOG_DIR: " + LOG_DIR);
        showLog(TAG, "========================================");
        showLog(TAG, "📋 ROOTFS KONFIGURATION");
        showLog(TAG, "========================================");
        showLog(TAG, "📌 ROOTFS_TYPE: " + ROOTFS_TYPE);
        showLog(TAG, "📌 ROOTFS_FILE: " + ROOTFS_FILE);
        showLog(TAG, "📌 ROOTFS_DIR: " + ROOTFS_DIR);
        showLog(TAG, "📌 INIT_SCRIPT: " + INIT_SCRIPT);
        showLog(TAG, "📌 INIT_HOST_SCRIPT: " + INIT_HOST_SCRIPT);
        showLog(TAG, "========================================");
    }
}