/*
    Copyright (c) 2012-2013, BogDan Vatra <bogdan@kde.org>
    Contact: http://www.qt.io/licensing/

    Commercial License Usage
    Licensees holding valid commercial Qt licenses may use this file in
    accordance with the commercial license agreement provided with the
    Software or, alternatively, in accordance with the terms contained in
    a written agreement between you and The Qt Company. For licensing terms
    and conditions see http://www.qt.io/terms-conditions. For further
    information use the contact form at http://www.qt.io/contact-us.

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

import org.kde.necessitas.ministro.IMinistro;
import org.kde.necessitas.ministro.IMinistroCallback;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.ServiceConnection;
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
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
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



public class QtActivity extends Activity
{
    private final static int MINISTRO_INSTALL_REQUEST_CODE = 0xf3ee; // request code used to know when Ministro instalation is finished
    private static final int MINISTRO_API_LEVEL = 5; // Ministro api level (check IMinistro.aidl file)
    private static final int NECESSITAS_API_LEVEL = 2; // Necessitas api level used by platform plugin
    private static final int QT_VERSION = 0x050100; // This app requires at least Qt version 5.1.0

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

    /// Ministro server parameter keys
    private static final String REQUIRED_MODULES_KEY = "required.modules";
    private static final String APPLICATION_TITLE_KEY = "application.title";
    private static final String MINIMUM_MINISTRO_API_KEY = "minimum.ministro.api";
    private static final String MINIMUM_QT_VERSION_KEY = "minimum.qt.version";
    private static final String SOURCES_KEY = "sources";               // needs MINISTRO_API_LEVEL >=3 !!!
                                                                       // Use this key to specify any 3rd party sources urls
                                                                       // Ministro will download these repositories into their
                                                                       // own folders, check http://community.kde.org/Necessitas/Ministro
                                                                       // for more details.

    private static final String REPOSITORY_KEY = "repository";         // use this key to overwrite the default ministro repsitory
    private static final String ANDROID_THEMES_KEY = "android.themes"; // themes that your application uses


    public String APPLICATION_PARAMETERS = null; // use this variable to pass any parameters to your application,
                                                               // the parameters must not contain any white spaces
                                                               // and must be separated with "\t"
                                                               // e.g "-param1\t-param2=value2\t-param3\tvalue3"

    public String ENVIRONMENT_VARIABLES = "QT_USE_ANDROID_NATIVE_STYLE=1\tQT_USE_ANDROID_NATIVE_DIALOGS=1\t";
                                                               // use this variable to add any environment variables to your application.
                                                               // the env vars must be separated with "\t"
                                                               // e.g. "ENV_VAR1=1\tENV_VAR2=2\t"
                                                               // Currently the following vars are used by the android plugin:
                                                               // * QT_USE_ANDROID_NATIVE_STYLE - 1 to use the android widget style if available.
                                                               // * QT_USE_ANDROID_NATIVE_DIALOGS -1 to use the android native dialogs.

    public String[] QT_ANDROID_THEMES = null;     // A list with all themes that your application want to use.
                                                  // The name of the theme must be the same with any theme from
                                                  // http://developer.android.com/reference/android/R.style.html
                                                  // The most used themes are:
                                                  //  * "Theme" - (fallback) check http://developer.android.com/reference/android/R.style.html#Theme
                                                  //  * "Theme_Black" - check http://developer.android.com/reference/android/R.style.html#Theme_Black
                                                  //  * "Theme_Light" - (default for API <=10) check http://developer.android.com/reference/android/R.style.html#Theme_Light
                                                  //  * "Theme_Holo" - check http://developer.android.com/reference/android/R.style.html#Theme_Holo
                                                  //  * "Theme_Holo_Light" - (default for API 11-13) check http://developer.android.com/reference/android/R.style.html#Theme_Holo_Light
                                                  //  * "Theme_DeviceDefault" - check http://developer.android.com/reference/android/R.style.html#Theme_DeviceDefault
                                                  //  * "Theme_DeviceDefault_Light" - (default for API 14+) check http://developer.android.com/reference/android/R.style.html#Theme_DeviceDefault_Light

    public String QT_ANDROID_DEFAULT_THEME = null; // sets the default theme.

    private static final int INCOMPATIBLE_MINISTRO_VERSION = 1; // Incompatible Ministro version. Ministro needs to be upgraded.
    private static final int BUFFER_SIZE = 1024;

    private ActivityInfo m_activityInfo = null; // activity info object, used to access the libs and the strings
    private DexClassLoader m_classLoader = null; // loader object
    private String[] m_sources = {"https://download.qt-project.org/ministro/android/qt5/qt-5.2"}; // Make sure you are using ONLY secure locations
    private String m_repository = "default"; // Overwrites the default Ministro repository
                                                        // Possible values:
                                                        // * default - Ministro default repository set with "Ministro configuration tool".
                                                        // By default the stable version is used. Only this or stable repositories should
                                                        // be used in production.
                                                        // * stable - stable repository, only this and default repositories should be used
                                                        // in production.
                                                        // * testing - testing repository, DO NOT use this repository in production,
                                                        // this repository is used to push a new release, and should be used to test your application.
                                                        // * unstable - unstable repository, DO NOT use this repository in production,
                                                        // this repository is used to push Qt snapshots.
    private String[] m_qtLibs = null; // required qt libs
    private int m_displayDensity = -1;

    public QtActivity()
    {
        if (Build.VERSION.SDK_INT <= 10) {
            QT_ANDROID_THEMES = new String[] {"Theme_Light"};
            QT_ANDROID_DEFAULT_THEME = "Theme_Light";
        }
        else if ((Build.VERSION.SDK_INT >= 11 && Build.VERSION.SDK_INT <= 13) || Build.VERSION.SDK_INT >= 21){
            QT_ANDROID_THEMES = new String[] {"Theme_Holo_Light"};
            QT_ANDROID_DEFAULT_THEME = "Theme_Holo_Light";
        } else {
            QT_ANDROID_THEMES = new String[] {"Theme_DeviceDefault_Light"};
            QT_ANDROID_DEFAULT_THEME = "Theme_DeviceDefault_Light";
        }
    }

    // this function is used to load and start the loader
    private void loadApplication(Bundle loaderParams)
    {
        try {
            final int errorCode = loaderParams.getInt(ERROR_CODE_KEY);
            if (errorCode != 0) {
                if (errorCode == INCOMPATIBLE_MINISTRO_VERSION) {
                    downloadUpgradeMinistro(loaderParams.getString(ERROR_MESSAGE_KEY));
                    return;
                }

                // fatal error, show the error and quit
                AlertDialog errorDialog = new AlertDialog.Builder(QtActivity.this).create();
                errorDialog.setMessage(loaderParams.getString(ERROR_MESSAGE_KEY));
                errorDialog.setButton(getResources().getString(android.R.string.ok), new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        finish();
                    }
                });
                errorDialog.show();
                return;
            }

            // add all bundled Qt libs to loader params
            ArrayList<String> libs = new ArrayList<String>();
            if ( m_activityInfo.metaData.containsKey("android.app.bundled_libs_resource_id") )
                libs.addAll(Arrays.asList(getResources().getStringArray(m_activityInfo.metaData.getInt("android.app.bundled_libs_resource_id"))));

            String libName = null;
            if ( m_activityInfo.metaData.containsKey("android.app.lib_name") ) {
                libName = m_activityInfo.metaData.getString("android.app.lib_name");
                loaderParams.putString(MAIN_LIBRARY_KEY, libName); //main library contains main() function
            }

            loaderParams.putStringArrayList(BUNDLED_LIBRARIES_KEY, libs);
            loaderParams.putInt(NECESSITAS_API_LEVEL_KEY, NECESSITAS_API_LEVEL);

            // load and start QtLoader class
            m_classLoader = new DexClassLoader(loaderParams.getString(DEX_PATH_KEY), // .jar/.apk files
                                               getDir("outdex", Context.MODE_PRIVATE).getAbsolutePath(), // directory where optimized DEX files should be written.
                                               loaderParams.containsKey(LIB_PATH_KEY) ? loaderParams.getString(LIB_PATH_KEY) : null, // libs folder (if exists)
                                               getClassLoader()); // parent loader

            @SuppressWarnings("rawtypes")
            Class loaderClass = m_classLoader.loadClass(loaderParams.getString(LOADER_CLASS_NAME_KEY)); // load QtLoader class
            Object qtLoader = loaderClass.newInstance(); // create an instance
            Method perpareAppMethod = qtLoader.getClass().getMethod("loadApplication",
                                                                    Activity.class,
                                                                    ClassLoader.class,
                                                                    Bundle.class);
            if (!(Boolean)perpareAppMethod.invoke(qtLoader, this, m_classLoader, loaderParams))
                throw new Exception("");

            QtApplication.setQtActivityDelegate(qtLoader);

            // now load the application library so it's accessible from this class loader
            if (libName != null)
                System.loadLibrary(libName);

            Method startAppMethod=qtLoader.getClass().getMethod("startApplication");
            if (!(Boolean)startAppMethod.invoke(qtLoader))
                throw new Exception("");

        } catch (Exception e) {
            e.printStackTrace();
            AlertDialog errorDialog = new AlertDialog.Builder(QtActivity.this).create();
            if (m_activityInfo.metaData.containsKey("android.app.fatal_error_msg"))
                errorDialog.setMessage(m_activityInfo.metaData.getString("android.app.fatal_error_msg"));
            else
                errorDialog.setMessage("Fatal error, your application can't be started.");

            errorDialog.setButton(getResources().getString(android.R.string.ok), new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    finish();
                }
            });
            errorDialog.show();
        }
    }

    private ServiceConnection m_ministroConnection=new ServiceConnection() {
        private IMinistro m_service = null;
        @Override
        public void onServiceConnected(ComponentName name, IBinder service)
        {
            m_service = IMinistro.Stub.asInterface(service);
            try {
                if (m_service != null) {
                    Bundle parameters = new Bundle();
                    parameters.putStringArray(REQUIRED_MODULES_KEY, m_qtLibs);
                    parameters.putString(APPLICATION_TITLE_KEY, (String)QtActivity.this.getTitle());
                    parameters.putInt(MINIMUM_MINISTRO_API_KEY, MINISTRO_API_LEVEL);
                    parameters.putInt(MINIMUM_QT_VERSION_KEY, QT_VERSION);
                    parameters.putString(ENVIRONMENT_VARIABLES_KEY, ENVIRONMENT_VARIABLES);
                    if (APPLICATION_PARAMETERS != null)
                        parameters.putString(APPLICATION_PARAMETERS_KEY, APPLICATION_PARAMETERS);
                    parameters.putStringArray(SOURCES_KEY, m_sources);
                    parameters.putString(REPOSITORY_KEY, m_repository);
                    if (QT_ANDROID_THEMES != null)
                        parameters.putStringArray(ANDROID_THEMES_KEY, QT_ANDROID_THEMES);
                    m_service.requestLoader(m_ministroCallback, parameters);
                }
            } catch (RemoteException e) {
                    e.printStackTrace();
            }
        }

        private IMinistroCallback m_ministroCallback = new IMinistroCallback.Stub() {
            // this function is called back by Ministro.
            @Override
            public void loaderReady(final Bundle loaderParams) throws RemoteException {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        unbindService(m_ministroConnection);
                        loadApplication(loaderParams);
                    }
                });
            }
        };

        @Override
        public void onServiceDisconnected(ComponentName name) {
            m_service = null;
        }
    };

    private void downloadUpgradeMinistro(String msg)
    {
        AlertDialog.Builder downloadDialog = new AlertDialog.Builder(this);
        downloadDialog.setMessage(msg);
        downloadDialog.setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                try {
                    Uri uri = Uri.parse("market://search?q=pname:org.kde.necessitas.ministro");
                    Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                    startActivityForResult(intent, MINISTRO_INSTALL_REQUEST_CODE);
                } catch (Exception e) {
                    e.printStackTrace();
                    ministroNotFound();
                }
            }
        });

        downloadDialog.setNegativeButton(android.R.string.no, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                QtActivity.this.finish();
            }
        });
        downloadDialog.show();
    }

    private void ministroNotFound()
    {
        AlertDialog errorDialog = new AlertDialog.Builder(QtActivity.this).create();

        if (m_activityInfo.metaData.containsKey("android.app.ministro_not_found_msg"))
            errorDialog.setMessage(m_activityInfo.metaData.getString("android.app.ministro_not_found_msg"));
        else
   