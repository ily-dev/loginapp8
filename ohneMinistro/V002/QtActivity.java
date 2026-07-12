/*
    Copyright (c) 2012-2013, BogDan Vatra <bogdan@kde.org>
    Contact: http://www.qt-project.org/legal

    Commercial License Usage
    Licensees holding valid commercial Qt licenses may use this file in
    accordance with the commercial license agreement provided with the
    Software or, alternatively, in accordance with the terms contained in
    a written agreement between you and Digia.  For licensing terms and
    conditions see http://qt.digia.com/licensing.  For further information
    use the contact form at http://qt.digia.com/contact-us.

    BSD License Usage
    Alternatively, this file may be used under the BSD license as follows:
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

package org.qtproject.qt5.android.bindings;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.DataOutputStream;
import java.io.DataInputStream;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.pm.PackageInfo;
import android.content.res.Configuration;
import android.content.res.Resources.Theme;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.drawable.ColorDrawable;
import android.os.Build;
import android.os.Bundle;
import android.util.AttributeSet;
import android.util.Log;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager.LayoutParams;
import android.view.accessibility.AccessibilityEvent;
import dalvik.system.DexClassLoader;

// ★ ★ ★ SHOWLOG IMPORT ★ ★ ★
import org.kivy.android.PythonService;

//@ANDROID-11
import android.app.Fragment;
import android.view.ActionMode;
import android.view.ActionMode.Callback;
//@ANDROID-11
import java.lang.reflect.InvocationTargetException;


public class QtActivity extends Activity
{
    // ============================================================
    // ★ KEINE MINISTRO-KONSTANTEN MEHR ★
    // ============================================================
    private static final String ERROR_CODE_KEY = "error.code";
    private static final String ERROR_MESSAGE_KEY = "error.message";
    private static final String DEX_PATH_KEY = "dex.path";
    private static final String LIB_PATH_KEY = "lib.path";
    private static final String LOADER_CLASS_NAME_KEY = "loader.class.name";
    private static final String NATIVE_LIBRARIES_KEY = "native.libraries";
    private static final String ENVIRONMENT_VARIABLES_KEY = "environment.variables";
    private static final String APPLICATION_PARAMETERS_KEY = "application.parameters";
    private static final String BUNDLED_LIBRARIES_KEY = "bundled.libraries";
    private static final String BUNDLED_IN_LIB_RESOURCE_ID_KEY = "android.app.bundled_in_lib_resource_id";
    private static final String BUNDLED_IN_ASSETS_RESOURCE_ID_KEY = "android.app.bundled_in_assets_resource_id";
    private static final String MAIN_LIBRARY_KEY = "main.library";
    private static final String STATIC_INIT_CLASSES_KEY = "static.init.classes";
    private static final String NECESSITAS_API_LEVEL_KEY = "necessitas.api.level";
    private static final String EXTRACT_STYLE_KEY = "extract.android.style";

    public String APPLICATION_PARAMETERS = null;
    public String ENVIRONMENT_VARIABLES = "QT_USE_ANDROID_NATIVE_STYLE=1\tQT_USE_ANDROID_NATIVE_DIALOGS=1\t";
    public String[] QT_ANDROID_THEMES = null;
    public String QT_ANDROID_DEFAULT_THEME = null;

    private static final int BUFFER_SIZE = 1024;

    private ActivityInfo m_activityInfo = null;
    private DexClassLoader m_classLoader = null;
    private String[] m_sources = null;
    private String[] m_qtLibs = null;
    private int m_displayDensity = -1;

    // ============================================================
    // ★ ★ ★ SHOWLOG (VERWENDET PythonService.showLog) ★ ★ ★
    // ============================================================
    private static void showLog(String title, String message) {
        Log.d("QtActivity", "📌 " + title + ": " + message);
        PythonService.showLog("QtActivity", title + ": " + message);
    }

    public QtActivity()
    {
        showLog("QtActivity", "🏗️ Konstruktor aufgerufen");
        
        if (Build.VERSION.SDK_INT <= 10) {
            QT_ANDROID_THEMES = new String[] {"Theme_Light"};
            QT_ANDROID_DEFAULT_THEME = "Theme_Light";
        }
        else if ((Build.VERSION.SDK_INT >= 11 && Build.VERSION.SDK_INT <= 13) || Build.VERSION.SDK_INT == 21){
            QT_ANDROID_THEMES = new String[] {"Theme_Holo_Light"};
            QT_ANDROID_DEFAULT_THEME = "Theme_Holo_Light";
        } else {
            QT_ANDROID_THEMES = new String[] {"Theme_DeviceDefault_Light"};
            QT_ANDROID_DEFAULT_THEME = "Theme_DeviceDefault_Light";
        }
        
        showLog("QtActivity", "📱 Android API: " + Build.VERSION.SDK_INT + ", Theme: " + QT_ANDROID_DEFAULT_THEME);
    }

    // ============================================================
    // ★ LOAD APPLICATION (OHNE MINISTRO) ★
    // ============================================================
    private void loadApplication(Bundle loaderParams)
    {
        showLog("loadApplication", "📦 Lade Application...");
        
        try {
            final int errorCode = loaderParams.getInt(ERROR_CODE_KEY, 0);
            showLog("loadApplication", "📊 Error Code: " + errorCode);
            
            if (errorCode != 0) {
                showLog("loadApplication", "❌ Fehler beim Laden: " + loaderParams.getString(ERROR_MESSAGE_KEY));
                AlertDialog errorDialog = new AlertDialog.Builder(QtActivity.this).create();
                errorDialog.setMessage(loaderParams.getString(ERROR_MESSAGE_KEY));
                errorDialog.setButton(getResources().getString(android.R.string.ok), new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        showLog("loadApplication", "🗑️ Dialog geschlossen, beende App");
                        finish();
                    }
                });
                errorDialog.show();
                return;
            }

            // Bundled Libs hinzufügen
            ArrayList<String> libs = new ArrayList<String>();
            if (m_activityInfo.metaData.containsKey("android.app.bundled_libs_resource_id")) {
                libs.addAll(Arrays.asList(getResources().getStringArray(m_activityInfo.metaData.getInt("android.app.bundled_libs_resource_id"))));
                showLog("loadApplication", "📚 Bundled Libs: " + libs.size());
            }

            String libName = null;
            if (m_activityInfo.metaData.containsKey("android.app.lib_name")) {
                libName = m_activityInfo.metaData.getString("android.app.lib_name");
                loaderParams.putString(MAIN_LIBRARY_KEY, libName);
                showLog("loadApplication", "📚 Main Library (lib_name): " + libName);
            } else {
                showLog("loadApplication", "⚠️ Kein android.app.lib_name im Manifest gefunden!");
            }

            loaderParams.putStringArrayList(BUNDLED_LIBRARIES_KEY, libs);
            loaderParams.putInt(NECESSITAS_API_LEVEL_KEY, 2);

            // QtLoader laden und starten
            showLog("loadApplication", "🔧 Lade QtLoader...");
            String loaderClassName = loaderParams.getString(LOADER_CLASS_NAME_KEY);
            showLog("loadApplication", "📚 Loader Class Name: " + loaderClassName);
            
            m_classLoader = new DexClassLoader(
                loaderParams.getString(DEX_PATH_KEY),
                getDir("outdex", Context.MODE_PRIVATE).getAbsolutePath(),
                loaderParams.containsKey(LIB_PATH_KEY) ? loaderParams.getString(LIB_PATH_KEY) : null,
                getClassLoader()
            );

            @SuppressWarnings("rawtypes")
            Class loaderClass = m_classLoader.loadClass(loaderClassName);
            showLog("loadApplication", "✅ QtLoader Klasse geladen: " + loaderClassName);
            
            Object qtLoader = null;
            
            try {
                qtLoader = loaderClass.getDeclaredConstructor().newInstance();
                showLog("loadApplication", "✅ QtLoader Instanz erstellt");
            } catch (NoSuchMethodException e) {
                showLog("loadApplication", "❌ Kein parameterloser Konstruktor gefunden!");
                throw e;
            } catch (IllegalAccessException e) {
                showLog("loadApplication", "❌ Konstruktor ist nicht öffentlich!");
                throw e;
            } catch (InstantiationException e) {
                showLog("loadApplication", "❌ Klasse ist abstrakt oder hat keinen Konstruktor!");
                throw e;
            } catch (InvocationTargetException e) {
                showLog("loadApplication", "❌ Konstruktor hat eine Exception geworfen!");
                throw e;
            }
            
            Method prepareAppMethod = qtLoader.getClass().getMethod("loadApplication",
                                                                    Activity.class,
                                                                    ClassLoader.class,
                                                                    Bundle.class);
            showLog("loadApplication", "🔧 Rufe loadApplication() auf...");
            if (!(Boolean)prepareAppMethod.invoke(qtLoader, this, m_classLoader, loaderParams)) {
                showLog("loadApplication", "❌ loadApplication fehlgeschlagen");
                throw new Exception("");
            }

            showLog("loadApplication", "✅ QtLoader geladen");
            QtApplication.setQtActivityDelegate(qtLoader);

            // Native Bibliothek laden
            if (libName != null) {
                showLog("loadApplication", "📚 Lade native Bibliothek: " + libName);
                System.loadLibrary(libName);
                showLog("loadApplication", "✅ System.loadLibrary(" + libName + ") erfolgreich!");
            } else {
                showLog("loadApplication", "⚠️ Kein lib_name gesetzt – überspringe System.loadLibrary()");
            }

            Method startAppMethod = qtLoader.getClass().getMethod("startApplication");
            showLog("loadApplication", "🔧 Rufe startApplication() auf...");
            if (!(Boolean)startAppMethod.invoke(qtLoader)) {
                showLog("loadApplication", "❌ startApplication fehlgeschlagen");
                throw new Exception("");
            }
            
            showLog("loadApplication", "✅ Application erfolgreich geladen und gestartet");

        } catch (Exception e) {
            showLog("loadApplication", "❌ Fehler: " + e.getMessage());
            e.printStackTrace();
            AlertDialog errorDialog = new AlertDialog.Builder(QtActivity.this).create();
            if (m_activityInfo.metaData.containsKey("android.app.fatal_error_msg"))
                errorDialog.setMessage(m_activityInfo.metaData.getString("android.app.fatal_error_msg"));
            else
                errorDialog.setMessage("Fatal error, your application can't be started.");

            errorDialog.setButton(getResources().getString(android.R.string.ok), new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    showLog("loadApplication", "🗑️ Fehlerdialog geschlossen");
                    finish();
                }
            });
            errorDialog.show();
        }
    }

    // ============================================================
    // ★ STATISCHE HELFER ★
    // ============================================================
    static private void copyFile(InputStream inputStream, OutputStream outputStream)
        throws IOException
    {
        byte[] buffer = new byte[BUFFER_SIZE];
        int count;
        while ((count = inputStream.read(buffer)) > 0)
            outputStream.write(buffer, 0, count);
    }

    private void copyAsset(String source, String destination)
        throws IOException
    {
        showLog("copyAsset", "📁 Kopiere: " + source + " → " + destination);
        
        File destinationFile = new File(destination);
        if (destinationFile.exists()) {
            showLog("copyAsset", "⏭️ Datei existiert bereits");
            return;
        }

        File parentDirectory = destinationFile.getParentFile();
        if (!parentDirectory.exists()) {
            showLog("copyAsset", "📁 Erstelle Verzeichnis: " + parentDirectory.getAbsolutePath());
            parentDirectory.mkdirs();
        }

        destinationFile.createNewFile();

        AssetManager assetsManager = getAssets();
        InputStream inputStream = assetsManager.open(source);
        OutputStream outputStream = new FileOutputStream(destinationFile);
        copyFile(inputStream, outputStream);

        inputStream.close();
        outputStream.close();
        showLog("copyAsset", "✅ Kopiert");
    }

    private static void createBundledBinary(String source, String destination)
        throws IOException
    {
        File destinationFile = new File(destination);
        if (destinationFile.exists())
            return;

        File parentDirectory = destinationFile.getParentFile();
        if (!parentDirectory.exists())
            parentDirectory.mkdirs();

        destinationFile.createNewFile();

        InputStream inputStream = new FileInputStream(source);
        OutputStream outputStream = new FileOutputStream(destinationFile);
        copyFile(inputStream, outputStream);

        inputStream.close();
        outputStream.close();
    }

    private boolean cleanCacheIfNecessary(String pluginsPrefix, long packageVersion)
    {
        File versionFile = new File(pluginsPrefix + "cache.version");

        long cacheVersion = 0;
        if (versionFile.exists() && versionFile.canRead()) {
            try {
                DataInputStream inputStream = new DataInputStream(new FileInputStream(versionFile));
                cacheVersion = inputStream.readLong();
                inputStream.close();
             } catch (Exception e) {
                showLog("cleanCacheIfNecessary", "❌ Fehler beim Lesen der Cache-Version: " + e.getMessage());
                e.printStackTrace();
             }
        }

        if (cacheVersion != packageVersion) {
            showLog("cleanCacheIfNecessary", "🗑️ Lösche Cache (Version unterschiedlich)");
            deleteRecursively(new File(pluginsPrefix));
            return true;
        } else {
            showLog("cleanCacheIfNecessary", "⏭️ Cache ist aktuell");
            return false;
        }
    }

    private void extractBundledPluginsAndImports(String pluginsPrefix)
        throws IOException
    {
        showLog("extractBundledPluginsAndImports", "📦 Extrahiere Plugins nach: " + pluginsPrefix);
        
        String dataDir = getApplicationInfo().dataDir + "/";

        long packageVersion = -1;
        try {
            PackageInfo packageInfo = getPackageManager().getPackageInfo(getPackageName(), 0);
            packageVersion = packageInfo.lastUpdateTime;
            showLog("extractBundledPluginsAndImports", "📦 Package Version: " + packageVersion);
        } catch (Exception e) {
            showLog("extractBundledPluginsAndImports", "❌ Fehler beim Lesen der Package Info");
            e.printStackTrace();
        }

        if (!cleanCacheIfNecessary(pluginsPrefix, packageVersion))
            return;

        {
            File versionFile = new File(pluginsPrefix + "cache.version");
            File parentDirectory = versionFile.getParentFile();
            if (!parentDirectory.exists())
                parentDirectory.mkdirs();

            versionFile.createNewFile();

            DataOutputStream outputStream = new DataOutputStream(new FileOutputStream(versionFile));
            outputStream.writeLong(packageVersion);
            outputStream.close();
            showLog("extractBundledPluginsAndImports", "✅ Version-Datei geschrieben");
        }

        {
            if (m_activityInfo.metaData.containsKey(BUNDLED_IN_LIB_RESOURCE_ID_KEY)) {
                String[] list = getResources().getStringArray(m_activityInfo.metaData.getInt(BUNDLED_IN_LIB_RESOURCE_ID_KEY));
                for (String bundledImportBinary : list) {
                    String[] split = bundledImportBinary.split(":");
                    String sourceFileName = dataDir + "lib/" + split[0];
                    String destinationFileName = pluginsPrefix + split[1];
                    createBundledBinary(sourceFileName, destinationFileName);
                    showLog("extractBundledPluginsAndImports", "📁 Extrahiere: " + sourceFileName + " → " + destinationFileName);
                }
            }
        }

        {
            if (m_activityInfo.metaData.containsKey(BUNDLED_IN_ASSETS_RESOURCE_ID_KEY)) {
                String[] list = getResources().getStringArray(m_activityInfo.metaData.getInt(BUNDLED_IN_ASSETS_RESOURCE_ID_KEY));
                for (String fileName : list) {
                    String[] split = fileName.split(":");
                    String sourceFileName = split[0];
                    String destinationFileName = pluginsPrefix + split[1];
                    copyAsset(sourceFileName, destinationFileName);
                    showLog("extractBundledPluginsAndImports", "📁 Kopiere Asset: " + sourceFileName + " → " + destinationFileName);
                }
            }
        }
        
        showLog("extractBundledPluginsAndImports", "✅ Plugins extrahiert");
    }

    private void deleteRecursively(File directory)
    {
        showLog("deleteRecursively", "🗑️ Lösche: " + directory.getAbsolutePath());
        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory())
                    deleteRecursively(file);
                else
                    file.delete();
            }
            directory.delete();
        }
        showLog("deleteRecursively", "✅ Gelöscht");
    }

    private void cleanOldCacheIfNecessary(String oldLocalPrefix, String localPrefix)
    {
        showLog("cleanOldCacheIfNecessary", "🧹 Bereinige alten Cache...");
        File newCache = new File(localPrefix);
        if (!newCache.exists()) {
            File oldPluginsCache = new File(oldLocalPrefix + "plugins/");
            if (oldPluginsCache.exists() && oldPluginsCache.isDirectory())
                deleteRecursively(oldPluginsCache);

            File oldImportsCache = new File(oldLocalPrefix + "imports/");
            if (oldImportsCache.exists() && oldImportsCache.isDirectory())
                deleteRecursively(oldImportsCache);

            File oldQmlCache = new File(oldLocalPrefix + "qml/");
            if (oldQmlCache.exists() && oldQmlCache.isDirectory())
                deleteRecursively(oldQmlCache);
            
            showLog("cleanOldCacheIfNecessary", "✅ Alter Cache bereinigt");
        } else {
            showLog("cleanOldCacheIfNecessary", "⏭️ Neuer Cache existiert bereits");
        }
    }

    // ============================================================
    // ★ START APP (OHNE MINISTRO) ★
    // ============================================================
    private void startApp(final boolean firstStart)
    {
        showLog("startApp", "🚀 Starte App (firstStart: " + firstStart + ")");
        
        try {
            // 1. Qt-Quellen laden
            if (m_activityInfo.metaData.containsKey("android.app.qt_sources_resource_id")) {
                int resourceId = m_activityInfo.metaData.getInt("android.app.qt_sources_resource_id");
                m_sources = getResources().getStringArray(resourceId);
                showLog("startApp", "📦 Qt Sources: " + m_sources.length);
            }

            // 2. Qt-Bibliotheken laden
            if (m_activityInfo.metaData.containsKey("android.app.qt_libs_resource_id")) {
                int resourceId = m_activityInfo.metaData.getInt("android.app.qt_libs_resource_id");
                m_qtLibs = getResources().getStringArray(resourceId);
                showLog("startApp", "📚 Qt Libs: " + m_qtLibs.length);
            }

            // 3. DIREKT LOKALE QT-INITIALISIERUNG (ohne Ministro!)
            if (m_activityInfo.metaData.containsKey("android.app.use_local_qt_libs")
                    && m_activityInfo.metaData.getInt("android.app.use_local_qt_libs") == 1) {
                showLog("startApp", "📚 Verwende lokale Qt Libs");
                ArrayList<String> libraryList = new ArrayList<String>();

                String localPrefix = "/data/local/tmp/qt/";
                if (m_activityInfo.metaData.containsKey("android.app.libs_prefix"))
                    localPrefix = m_activityInfo.metaData.getString("android.app.libs_prefix");

                String pluginsPrefix = localPrefix;

                boolean bundlingQtLibs = false;
                if (m_activityInfo.metaData.containsKey("android.app.bundle_local_qt_libs")
                    && m_activityInfo.metaData.getInt("android.app.bundle_local_qt_libs") == 1) {
                    showLog("startApp", "📦 Bündle lokale Qt Libs");
                    localPrefix = getApplicationInfo().dataDir + "/";
                    pluginsPrefix = localPrefix + "qt-reserved-files/";
                    cleanOldCacheIfNecessary(localPrefix, pluginsPrefix);
                    extractBundledPluginsAndImports(pluginsPrefix);
                    bundlingQtLibs = true;
                }

                // Library-Liste aufbauen
                if (m_qtLibs != null) {
                    for (int i = 0; i < m_qtLibs.length; i++) {
                        libraryList.add(localPrefix + "lib/lib" + m_qtLibs[i] + ".so");
                        showLog("startApp", "📚 Qt Lib: " + m_qtLibs[i]);
                    }
                }

                // ★ ★ ★ FIX: load_local_libs mit Null-Check ★ ★ ★
                String loadLocalLibs = m_activityInfo.metaData.getString("android.app.load_local_libs");
                if (loadLocalLibs != null && !loadLocalLibs.isEmpty()) {
                    String[] extraLibs = loadLocalLibs.split(":");
                    for (String lib : extraLibs) {
                        if (lib != null && lib.length() > 0) {
                            if (lib.startsWith("lib/"))
                                libraryList.add(localPrefix + lib);
                            else
                                libraryList.add(pluginsPrefix + lib);
                            showLog("startApp", "📚 Extra Lib: " + lib);
                        }
                    }
                } else {
                    showLog("startApp", "⏭️ Keine load_local_libs definiert");
                }

                // Dex-Pfade
                String dexPaths = new String();
                String pathSeparator = System.getProperty("path.separator", ":");
                if (!bundlingQtLibs && m_activityInfo.metaData.containsKey("android.app.load_local_jars")) {
                    String[] jarFiles = m_activityInfo.metaData.getString("android.app.load_local_jars").split(":");
                    for (String jar : jarFiles) {
                        if (jar.length() > 0) {
                            if (dexPaths.length() > 0)
                                dexPaths += pathSeparator;
                            dexPaths += localPrefix + jar;
                            showLog("startApp", "📦 JAR: " + jar);
                        }
                    }
                }

                // Loader-Parameter zusammenstellen
                Bundle loaderParams = new Bundle();
                loaderParams.putInt(ERROR_CODE_KEY, 0);
                loaderParams.putString(DEX_PATH_KEY, dexPaths);
                loaderParams.putString(LOADER_CLASS_NAME_KEY, "org.qtproject.qt5.android.QtActivityDelegate");
                
                if (m_activityInfo.metaData.containsKey("android.app.static_init_classes")) {
                    loaderParams.putStringArray(STATIC_INIT_CLASSES_KEY,
                                                m_activityInfo.metaData.getString("android.app.static_init_classes").split(":"));
                    showLog("startApp", "📚 Static Init Classes: " + m_activityInfo.metaData.getString("android.app.static_init_classes"));
                }
                loaderParams.putStringArrayList(NATIVE_LIBRARIES_KEY, libraryList);

                // Theme-Pfad
                String themePath = getApplicationInfo().dataDir + "/qt-reserved-files/android-style/";
                String stylePath = themePath + m_displayDensity + "/";
                if (!(new File(stylePath)).exists())
                    loaderParams.putString(EXTRACT_STYLE_KEY, stylePath);
                ENVIRONMENT_VARIABLES += "\tMINISTRO_ANDROID_STYLE_PATH=" + stylePath
                                       + "\tQT_ANDROID_THEMES_ROOT_PATH=" + themePath;

                loaderParams.putString(ENVIRONMENT_VARIABLES_KEY, ENVIRONMENT_VARIABLES
                                                                  + "\tQML2_IMPORT_PATH=" + pluginsPrefix + "/qml"
                                                                  + "\tQML_IMPORT_PATH=" + pluginsPrefix + "/imports"
                                                                  + "\tQT_PLUGIN_PATH=" + pluginsPrefix + "/plugins");

                if (APPLICATION_PARAMETERS != null) {
                    loaderParams.putString(APPLICATION_PARAMETERS_KEY, APPLICATION_PARAMETERS);
                    showLog("startApp", "📚 Application Parameters: " + APPLICATION_PARAMETERS);
                } else {
                    Intent intent = getIntent();
                    if (intent != null) {
                        String parameters = intent.getStringExtra("applicationArguments");
                        if (parameters != null) {
                            loaderParams.putString(APPLICATION_PARAMETERS_KEY, parameters.replace(' ', '\t'));
                            showLog("startApp", "📚 Application Arguments: " + parameters);
                        }
                    }
                }

                // Direkt loadApplication() aufrufen (OHNE Ministro!)
                loadApplication(loaderParams);
                return;
            }

            // Fallback: Keine lokalen Qt-Libs
            showLog("startApp", "❌ Keine lokalen Qt-Libs konfiguriert!");
            AlertDialog errorDialog = new AlertDialog.Builder(QtActivity.this).create();
            errorDialog.setMessage("Keine Qt-Bibliotheken gefunden!");
            errorDialog.setButton(getResources().getString(android.R.string.ok), new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    finish();
                }
            });
            errorDialog.show();

        } catch (Exception e) {
            showLog("startApp", "❌ Fehler: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // ============================================================
    // ★ ACTIVITY LIFECYCLE ★
    // ============================================================
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        showLog("onCreate", "🚀 QtActivity onCreate");
        
        if (savedInstanceState == null) {
            savedInstanceState = new Bundle();
            showLog("onCreate", "📦 Bundle erstellt (war null)");
        }
        
        super.onCreate(savedInstanceState);
        showLog("onCreate", "✅ super.onCreate() abgeschlossen");

        try {
            m_activityInfo = getPackageManager().getActivityInfo(getComponentName(), PackageManager.GET_META_DATA);
            showLog("onCreate", "📋 Activity Info geladen");
            
            for (Field f : Class.forName("android.R$style").getDeclaredFields()) {
                if (f.getInt(null) == m_activityInfo.getThemeResource()) {
                    QT_ANDROID_THEMES = new String[] {f.getName()};
                    QT_ANDROID_DEFAULT_THEME = f.getName();
                    showLog("onCreate", "🎨 Theme: " + f.getName());
                }
            }
        } catch (Exception e) {
            showLog("onCreate", "❌ Fehler beim Laden der Activity Info: " + e.getMessage());
            e.printStackTrace();
            finish();
            return;
        }

        try {
            setTheme(Class.forName("android.R$style").getDeclaredField(QT_ANDROID_DEFAULT_THEME).getInt(null));
            showLog("onCreate", "🎨 Theme gesetzt: " + QT_ANDROID_DEFAULT_THEME);
        } catch (Exception e) {
            showLog("onCreate", "❌ Theme setzen fehlgeschlagen: " + e.getMessage());
            e.printStackTrace();
        }

        if (Build.VERSION.SDK_INT > 10) {
            try {
                requestWindowFeature(Window.class.getField("FEATURE_ACTION_BAR").getInt(null));
                showLog("onCreate", "🖥️ ActionBar aktiviert");
            } catch (Exception e) {
                showLog("onCreate", "⚠️ ActionBar nicht verfügbar");
                e.printStackTrace();
            }
        } else {
            requestWindowFeature(Window.FEATURE_NO_TITLE);
            showLog("onCreate", "🖥️ NoTitle aktiviert (API < 11)");
        }

        if (QtApplication.m_delegateObject != null && QtApplication.onCreate != null) {
            showLog("onCreate", "📞 Rufe QtApplication.onCreate Delegate auf");
            QtApplication.invokeDelegateMethod(QtApplication.onCreate, savedInstanceState);
            return;
        }

        m_displayDensity = getResources().getDisplayMetrics().densityDpi;
        showLog("onCreate", "📱 Display DPI: " + m_displayDensity);

        ENVIRONMENT_VARIABLES += "\tQT_ANDROID_THEME=" + QT_ANDROID_DEFAULT_THEME
                              + "/\tQT_ANDROID_THEME_DISPLAY_DPI=" + m_displayDensity + "\t";

        if (null == getLastNonConfigurationInstance()) {
            showLog("onCreate", "🔄 Keine gespeicherte Instanz, starte App...");
            
            if (m_activityInfo.metaData.containsKey("android.app.splash_screen_drawable")) {
                getWindow().setBackgroundDrawableResource(m_activityInfo.metaData.getInt("android.app.splash_screen_drawable"));
                showLog("onCreate", "🖼️ Splash Screen gesetzt");
            } else {
                getWindow().setBackgroundDrawable(new ColorDrawable(0xff000000));
            }

            if (m_activityInfo.metaData.containsKey("android.app.background_running")
                && m_activityInfo.metaData.getBoolean("android.app.background_running")) {
                ENVIRONMENT_VARIABLES += "QT_BLOCK_EVENT_LOOPS_WHEN_SUSPENDED=0\t";
                showLog("onCreate", "🔄 Background Running aktiviert");
            } else {
                ENVIRONMENT_VARIABLES += "QT_BLOCK_EVENT_LOOPS_WHEN_SUSPENDED=1\t";
                showLog("onCreate", "⏸️ Background Running deaktiviert");
            }
            startApp(true);
        }
        
        showLog("onCreate", "✅ QtActivity onCreate abgeschlossen");
    }

    // ============================================================
    // ★ ALLE DELEGATE-METHODEN ★
    // ============================================================
    @Override
    public boolean dispatchKeyEvent(KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.dispatchKeyEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.dispatchKeyEvent, event);
        else
            return super.dispatchKeyEvent(event);
    }

    @Override
    public boolean dispatchPopulateAccessibilityEvent(AccessibilityEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.dispatchPopulateAccessibilityEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.dispatchPopulateAccessibilityEvent, event);
        else
            return super.dispatchPopulateAccessibilityEvent(event);
    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.dispatchTouchEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.dispatchTouchEvent, ev);
        else
            return super.dispatchTouchEvent(ev);
    }

    @Override
    public boolean dispatchTrackballEvent(MotionEvent ev)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.dispatchTrackballEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.dispatchTrackballEvent, ev);
        else
            return super.dispatchTrackballEvent(ev);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        showLog("onActivityResult", "📨 onActivityResult: " + requestCode + ", " + resultCode);

        if (QtApplication.m_delegateObject != null && QtApplication.onActivityResult != null) {
            QtApplication.invokeDelegateMethod(QtApplication.onActivityResult, requestCode, resultCode, data);
            return;
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    protected void onApplyThemeResource(Theme theme, int resid, boolean first)
    {
        if (!QtApplication.invokeDelegate(theme, resid, first).invoked)
            super.onApplyThemeResource(theme, resid, first);
    }

    @Override
    protected void onChildTitleChanged(Activity childActivity, CharSequence title)
    {
        if (!QtApplication.invokeDelegate(childActivity, title).invoked)
            super.onChildTitleChanged(childActivity, title);
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig)
    {
        if (!QtApplication.invokeDelegate(newConfig).invoked)
            super.onConfigurationChanged(newConfig);
    }

    @Override
    public void onContentChanged()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onContentChanged();
    }

    @Override
    public boolean onContextItemSelected(MenuItem item)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(item);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onContextItemSelected(item);
    }

    @Override
    public void onContextMenuClosed(Menu menu)
    {
        if (!QtApplication.invokeDelegate(menu).invoked)
            super.onContextMenuClosed(menu);
    }

    @Override
    public void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo)
    {
        if (!QtApplication.invokeDelegate(menu, v, menuInfo).invoked)
            super.onCreateContextMenu(menu, v, menuInfo);
    }

    @Override
    public CharSequence onCreateDescription()
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate();
        if (res.invoked)
            return (CharSequence)res.methodReturns;
        else
            return super.onCreateDescription();
    }

    @Override
    protected Dialog onCreateDialog(int id)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(id);
        if (res.invoked)
            return (Dialog)res.methodReturns;
        else
            return super.onCreateDialog(id);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(menu);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onCreatePanelMenu(int featureId, Menu menu)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(featureId, menu);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onCreatePanelMenu(featureId, menu);
    }

    @Override
    public View onCreatePanelView(int featureId)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(featureId);
        if (res.invoked)
            return (View)res.methodReturns;
        else
            return super.onCreatePanelView(featureId);
    }

    @Override
    public boolean onCreateThumbnail(Bitmap outBitmap, Canvas canvas)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(outBitmap, canvas);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onCreateThumbnail(outBitmap, canvas);
    }

    @Override
    public View onCreateView(String name, Context context, AttributeSet attrs)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(name, context, attrs);
        if (res.invoked)
            return (View)res.methodReturns;
        else
            return super.onCreateView(name, context, attrs);
    }

    @Override
    protected void onDestroy()
    {
        showLog("onDestroy", "🗑️ onDestroy");
        super.onDestroy();
        QtApplication.invokeDelegate();
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onKeyDown != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onKeyDown, keyCode, event);
        else
            return super.onKeyDown(keyCode, event);
    }

    @Override
    public boolean onKeyMultiple(int keyCode, int repeatCount, KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onKeyMultiple != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onKeyMultiple, keyCode, repeatCount, event);
        else
            return super.onKeyMultiple(keyCode, repeatCount, event);
    }

    @Override
    public boolean onKeyUp(int keyCode, KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onKeyUp != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onKeyUp, keyCode, event);
        else
            return super.onKeyUp(keyCode, event);
    }

    @Override
    public void onLowMemory()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onLowMemory();
    }

    @Override
    public boolean onMenuItemSelected(int featureId, MenuItem item)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(featureId, item);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onMenuItemSelected(featureId, item);
    }

    @Override
    public boolean onMenuOpened(int featureId, Menu menu)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(featureId, menu);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onMenuOpened(featureId, menu);
    }

    @Override
    protected void onNewIntent(Intent intent)
    {
        if (!QtApplication.invokeDelegate(intent).invoked)
            super.onNewIntent(intent);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(item);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onOptionsItemSelected(item);
    }

    @Override
    public void onOptionsMenuClosed(Menu menu)
    {
        if (!QtApplication.invokeDelegate(menu).invoked)
            super.onOptionsMenuClosed(menu);
    }

    @Override
    public void onPanelClosed(int featureId, Menu menu)
    {
        if (!QtApplication.invokeDelegate(featureId, menu).invoked)
            super.onPanelClosed(featureId, menu);
    }

    @Override
    protected void onPause()
    {
        showLog("onPause", "⏸️ onPause");
        super.onPause();
        QtApplication.invokeDelegate();
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState)
    {
        super.onPostCreate(savedInstanceState);
        QtApplication.invokeDelegate(savedInstanceState);
    }

    @Override
    protected void onPostResume()
    {
        super.onPostResume();
        QtApplication.invokeDelegate();
    }

    @Override
    protected void onPrepareDialog(int id, Dialog dialog)
    {
        if (!QtApplication.invokeDelegate(id, dialog).invoked)
            super.onPrepareDialog(id, dialog);
    }

    @Override
    public boolean onPrepareOptionsMenu(Menu menu)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(menu);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onPrepareOptionsMenu(menu);
    }

    @Override
    public boolean onPreparePanel(int featureId, View view, Menu menu)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(featureId, view, menu);
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onPreparePanel(featureId, view, menu);
    }

    @Override
    protected void onRestart()
    {
        showLog("onRestart", "🔄 onRestart");
        super.onRestart();
        QtApplication.invokeDelegate();
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState)
    {
        if (!QtApplication.invokeDelegate(savedInstanceState).invoked)
            super.onRestoreInstanceState(savedInstanceState);
    }

    @Override
    protected void onResume()
    {
        showLog("onResume", "▶️ onResume");
        super.onResume();
        QtApplication.invokeDelegate();
    }

    @Override
    public Object onRetainNonConfigurationInstance()
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate();
        if (res.invoked)
            return res.methodReturns;
        else
            return super.onRetainNonConfigurationInstance();
    }

    @Override
    protected void onSaveInstanceState(Bundle outState)
    {
        if (!QtApplication.invokeDelegate(outState).invoked)
            super.onSaveInstanceState(outState);
    }

    @Override
    public boolean onSearchRequested()
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate();
        if (res.invoked)
            return (Boolean)res.methodReturns;
        else
            return super.onSearchRequested();
    }

    @Override
    protected void onStart()
    {
        showLog("onStart", "▶️ onStart");
        super.onStart();
        QtApplication.invokeDelegate();
    }

    @Override
    protected void onStop()
    {
        showLog("onStop", "⏹️ onStop");
        super.onStop();
        QtApplication.invokeDelegate();
    }

    @Override
    protected void onTitleChanged(CharSequence title, int color)
    {
        if (!QtApplication.invokeDelegate(title, color).invoked)
            super.onTitleChanged(title, color);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onTouchEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onTouchEvent, event);
        else
            return super.onTouchEvent(event);
    }

    @Override
    public boolean onTrackballEvent(MotionEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onTrackballEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onTrackballEvent, event);
        else
            return super.onTrackballEvent(event);
    }

    @Override
    public void onUserInteraction()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onUserInteraction();
    }

    @Override
    protected void onUserLeaveHint()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onUserLeaveHint();
    }

    @Override
    public void onWindowAttributesChanged(LayoutParams params)
    {
        if (!QtApplication.invokeDelegate(params).invoked)
            super.onWindowAttributesChanged(params);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus)
    {
        if (!QtApplication.invokeDelegate(hasFocus).invoked)
            super.onWindowFocusChanged(hasFocus);
    }

    // ============================================================
    // ★ API 5+ METHODEN ★
    // ============================================================
    @Override
    public void onAttachedToWindow()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onAttachedToWindow();
    }

    @Override
    public void onBackPressed()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onBackPressed();
    }

    @Override
    public void onDetachedFromWindow()
    {
        if (!QtApplication.invokeDelegate().invoked)
            super.onDetachedFromWindow();
    }

    @Override
    public boolean onKeyLongPress(int keyCode, KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onKeyLongPress != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onKeyLongPress, keyCode, event);
        else
            return super.onKeyLongPress(keyCode, event);
    }

    // ============================================================
    // ★ API 8+ METHODEN ★
    // ============================================================
    @Override
    protected Dialog onCreateDialog(int id, Bundle args)
    {
        QtApplication.InvokeResult res = QtApplication.invokeDelegate(id, args);
        if (res.invoked)
            return (Dialog)res.methodReturns;
        else
            return super.onCreateDialog(id, args);
    }

    @Override
    protected void onPrepareDialog(int id, Dialog dialog, Bundle args)
    {
        if (!QtApplication.invokeDelegate(id, dialog, args).invoked)
            super.onPrepareDialog(id, dialog, args);
    }

    // ============================================================
    // ★ API 11+ METHODEN ★
    // ============================================================
    @Override
    public boolean dispatchKeyShortcutEvent(KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.dispatchKeyShortcutEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.dispatchKeyShortcutEvent, event);
        else
            return super.dispatchKeyShortcutEvent(event);
    }

    @Override
    public boolean onKeyShortcut(int keyCode, KeyEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onKeyShortcut != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onKeyShortcut, keyCode, event);
        else
            return super.onKeyShortcut(keyCode, event);
    }

    @Override
    public boolean dispatchGenericMotionEvent(MotionEvent ev)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.dispatchGenericMotionEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.dispatchGenericMotionEvent, ev);
        else
            return super.dispatchGenericMotionEvent(ev);
    }

    @Override
    public boolean onGenericMotionEvent(MotionEvent event)
    {
        if (QtApplication.m_delegateObject != null && QtApplication.onGenericMotionEvent != null)
            return (Boolean) QtApplication.invokeDelegateMethod(QtApplication.onGenericMotionEvent, event);
        else
            return super.onGenericMotionEvent(event);
    }
}