// core/main/src/main/java/com/rk/terminal/Globals.java
package com.rk.terminal;

import android.content.Context;
import java.io.InputStream;
import java.util.Properties;
import java.io.File;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import android.os.Environment;

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
    // ★ ★ ★ WORKING MODE ★ ★ ★
    // ============================================================
    public static final int WORKING_MODE_ALPINE = 0;
    public static final int WORKING_MODE_UBUNTU = 1;
    public static final int WORKING_MODE_ANDROID = 2;
    
    public static int WORKING_MODE = WORKING_MODE_ALPINE;  // Default: Alpine
    
    // ============================================================
    // ★ ★ ★ SHOWLOG ★ ★ ★
    // ============================================================
    public static void showLog(String tag, String message) {
        try {
            File logFile = new File(
                Environment.getExternalStorageDirectory(),
                "main_core.log"
            );
            logFile.getParentFile().mkdirs();
            String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
                .format(new Date());
            FileWriter fw = new FileWriter(logFile, true);
            fw.write(timestamp + " - " + tag + ": " + message + "\n");
            fw.close();
        } catch (Exception e) {
            android.util.Log.d(tag, message);
        }
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
            
            // APP KONFIGURATION
            DIALOG_DELAY = Integer.parseInt(props.getProperty("DIALOG_DELAY", "3000"));
            APP_VERSION = props.getProperty("APP_VERSION", "1.2.1");
            DEBUG = Boolean.parseBoolean(props.getProperty("DEBUG", "true"));
            TIMEOUT = Integer.parseInt(props.getProperty("TIMEOUT", "30"));
            MAX_RETRIES = Integer.parseInt(props.getProperty("MAX_RETRIES", "3"));
            PYTHON_HOME = props.getProperty("PYTHON_HOME", "");
            LOG_DIR = props.getProperty("LOG_DIR", "/sdcard/logs");
            
            // ROOTFS KONFIGURATION
            ROOTFS_TYPE = props.getProperty("rootfs_type", "alpine").toLowerCase();
            ROOTFS_FILE = props.getProperty("rootfs_file", "alpine.tar.gz");
            ROOTFS_DIR = props.getProperty("rootfs_dir", "alpine");
            INIT_SCRIPT = props.getProperty("init_script", "alpine/init.sh");
            INIT_HOST_SCRIPT = props.getProperty("init_host_script", "alpine/init-host.sh");
            
            // ★ ★ ★ WORKING MODE ★ ★ ★
            String workingModeStr = props.getProperty("working_mode", "alpine").toLowerCase();
            WORKING_MODE = getWorkingModeFromString(workingModeStr);
            
            // ★ ★ ★ Logging ★ ★ ★
            logConfig();
            
        } catch (Exception e) {
            showLog(TAG, "❌ Fehler beim Laden der Konfiguration: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    // ============================================================
    // ★ ★ ★ WORKING MODE HELPER ★ ★ ★
    // ============================================================
    private static int getWorkingModeFromString(String mode) {
        return switch (mode) {
            case "ubuntu" -> WORKING_MODE_UBUNTU;
            case "android" -> WORKING_MODE_ANDROID;
            default -> WORKING_MODE_ALPINE;
        };
    }
    
    public static String getWorkingModeName() {
        return switch (WORKING_MODE) {
            case WORKING_MODE_UBUNTU -> "Ubuntu Linux";
            case WORKING_MODE_ANDROID -> "Android Shell";
            default -> "Alpine Linux";
        };
    }
    
    public static String getWorkingModeShortName() {
        return switch (WORKING_MODE) {
            case WORKING_MODE_UBUNTU -> "ubuntu";
            case WORKING_MODE_ANDROID -> "android";
            default -> "alpine";
        };
    }
    
    public static boolean isAlpine() {
        return WORKING_MODE == WORKING_MODE_ALPINE;
    }
    
    public static boolean isUbuntu() {
        return WORKING_MODE == WORKING_MODE_UBUNTU;
    }
    
    public static boolean isAndroid() {
        return WORKING_MODE == WORKING_MODE_ANDROID;
    }
    
    public static String getRootfsDisplayName() {
        return getWorkingModeName();
    }
    
    public static String getRootfsFileNameOnly() {
        String file = ROOTFS_FILE;
        return file.substring(file.lastIndexOf('/') + 1);
    }
    
    // ============================================================
    // LOGGING
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
        showLog(TAG, "📋 WORKING MODE");
        showLog(TAG, "========================================");
        showLog(TAG, "📌 WORKING_MODE: " + WORKING_MODE + " (" + getWorkingModeName() + ")");
        showLog(TAG, "========================================");
    }
}