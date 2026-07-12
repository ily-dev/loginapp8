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

package org.qtproject.qt.android.bindings;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.HashMap;
import java.io.File;

import android.app.Application;
import android.content.Context;
import android.util.Log;

public class QtApplication extends Application
{
    public final static String QtTAG = "Qt";
    public static Object m_delegateObject = null;
    public static HashMap<String, ArrayList<Method>> m_delegateMethods = new HashMap<String, ArrayList<Method>>();
    public static Method dispatchKeyEvent = null;
    public static Method dispatchPopulateAccessibilityEvent = null;
    public static Method dispatchTouchEvent = null;
    public static Method dispatchTrackballEvent = null;
    public static Method onKeyDown = null;
    public static Method onKeyMultiple = null;
    public static Method onKeyUp = null;
    public static Method onTouchEvent = null;
    public static Method onTrackballEvent = null;
    public static Method onActivityResult = null;
    public static Method onCreate = null;
    public static Method onKeyLongPress = null;
    public static Method dispatchKeyShortcutEvent = null;
    public static Method onKeyShortcut = null;
    public static Method dispatchGenericMotionEvent = null;
    public static Method onGenericMotionEvent = null;

    // ★ ★ ★ SINGLETON INSTANCE ★ ★ ★
    private static QtApplication sInstance = null;

    // ★ ★ ★ RK APPLICATION REFLECTION ★ ★ ★
    private static boolean rkApplicationInitialized = false;
    private static Object rkApplicationInstance = null;
    private static Class<?> rkApplicationClass = null;

    // ★ ★ ★ GLOBALS ★ ★ ★
    private static Object globalsInstance = null;
    private static Class<?> globalsClass = null;
    private static File tempDir = null;

    // ============================================================
    // ★ CONSTRUCTOR ★
    // ============================================================
    public QtApplication() {
        super();
        sInstance = this;
    }

    // ============================================================
    // ★ SHOWLOG ★
    // ============================================================
    private static void showLog(String title, String message) {
        Log.d("QtApplication", "📌 " + title + ": " + message);
    }

    // ============================================================
    // ★ ON CREATE ★
    // ============================================================
    @Override
    public void onCreate() {
        super.onCreate();
        sInstance = this;
        showLog("onCreate", "🚀 QtApplication onCreate");
        
        // ★ ★ ★ Globals initialisieren ★ ★ ★
        initGlobals();
        
        // ★ ★ ★ Temporären Ordner erstellen ★ ★ ★
        initTempDir();
        
        // ★ ★ ★ RK Application initialisieren ★ ★ ★
        initRkApplication();
    }

    // ============================================================
    // ★ GLOBALS INIT ★
    // ============================================================
    private void initGlobals() {
        showLog("initGlobals", "🔍 Initialisiere Globals über Reflection...");
        
        try {
            // 1. Globals Klasse laden
            globalsClass = Class.forName("com.meinname.ssh.Globals");
            showLog("initGlobals", "✅ Klasse com.meinname.ssh.Globals gefunden");

            // 2. init(Context) Methode aufrufen
            Method initMethod = globalsClass.getDeclaredMethod("init", Context.class);
            initMethod.setAccessible(true);
            initMethod.invoke(null, this);
            showLog("initGlobals", "✅ Globals.init(Context) aufgerufen");

            // 3. Globals Instanz speichern (falls verfügbar)
            try {
                Field instanceField = globalsClass.getDeclaredField("INSTANCE");
                instanceField.setAccessible(true);
                globalsInstance = instanceField.get(null);
                showLog("initGlobals", "✅ Globals.INSTANCE geladen");
            } catch (Exception e) {
                showLog("initGlobals", "⚠️ Kein INSTANCE-Feld in Globals");
            }

            showLog("initGlobals", "✅ Globals erfolgreich initialisiert");

        } catch (ClassNotFoundException e) {
            showLog("initGlobals", "❌ Klasse com.meinname.ssh.Globals nicht gefunden - wird ignoriert");
        } catch (NoSuchMethodException e) {
            showLog("initGlobals", "❌ Globals.init(Context) nicht gefunden: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            showLog("initGlobals", "❌ Fehler: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // ============================================================
    // ★ TEMP DIR INIT ★
    // ============================================================
    private void initTempDir() {
        showLog("initTempDir", "📁 Erstelle temporären Ordner...");
        
        try {
            // 1. filesDir.parentFile für tmp Ordner
            File filesDir = getApplicationContext().getFilesDir();
            if (filesDir == null) {
                showLog("initTempDir", "❌ filesDir ist null!");
                return;
            }
            
            File parentDir = filesDir.getParentFile();
            if (parentDir == null) {
                showLog("initTempDir", "❌ parentDir ist null!");
                return;
            }
            
            tempDir = new File(parentDir, "tmp");
            
            // 2. Ordner erstellen
            if (!tempDir.exists()) {
                boolean created = tempDir.mkdirs();
                if (created) {
                    showLog("initTempDir", "✅ Temporärer Ordner erstellt: " + tempDir.getAbsolutePath());
                } else {
                    showLog("initTempDir", "❌ Konnte temporären Ordner nicht erstellen!");
                }
            } else {
                showLog("initTempDir", "⏭️ Temporärer Ordner existiert bereits: " + tempDir.getAbsolutePath());
            }

            // 3. Ordner löschen (für sauberen Start)
            if (tempDir.exists() && tempDir.isDirectory()) {
                File[] files = tempDir.listFiles();
                if (files != null && files.length > 0) {
                    showLog("initTempDir", "🗑️ Lösche " + files.length + " Dateien aus tmp-Ordner");
                    deleteRecursively(tempDir);
                    tempDir.mkdirs(); // neu erstellen
                    showLog("initTempDir", "✅ Temporärer Ordner neu erstellt");
                } else {
                    showLog("initTempDir", "⏭️ Temporärer Ordner ist leer");
                }
            }

        } catch (Exception e) {
            showLog("initTempDir", "❌ Fehler: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // ============================================================
    // ★ RECURSIVE DELETE ★
    // ============================================================
    private void deleteRecursively(File file) {
        if (file == null || !file.exists()) return;
        
        if (file.isDirectory()) {
            File[] files = file.listFiles();
            if (files != null) {
                for (File child : files) {
                    deleteRecursively(child);
                }
            }
        }
        file.delete();
    }

    // ============================================================
    // ★ RK APPLICATION INIT ★
    // ============================================================
    private void initRkApplication() {
        if (rkApplicationInitialized) {
            showLog("initRkApplication", "⏭️ RK Application bereits initialisiert");
            return;
        }

        showLog("initRkApplication", "🔍 Initialisiere RK Application über Reflection...");

        try {
            // 1. RK Application Klasse laden
            rkApplicationClass = Class.forName("com.rk.terminal.App");
            showLog("initRkApplication", "✅ Klasse com.rk.terminal.App gefunden");

            // 2. Konstruktor mit Context aufrufen
            Constructor<?> constructor = rkApplicationClass.getDeclaredConstructor(Context.class);
            constructor.setAccessible(true);
            rkApplicationInstance = constructor.newInstance(this);
            showLog("initRkApplication", "✅ App-Instanz erstellt");

            // 3. attach Methode aufrufen
            Method attachMethod = rkApplicationClass.getDeclaredMethod("attach", Context.class);
            attachMethod.setAccessible(true);
            attachMethod.invoke(rkApplicationInstance, this);
            showLog("initRkApplication", "✅ attach() aufgerufen");

            // 4. onCreate Methode aufrufen
            Method onCreateMethod = rkApplicationClass.getDeclaredMethod("onCreate");
            onCreateMethod.setAccessible(true);
            onCreateMethod.invoke(rkApplicationInstance);
            showLog("initRkApplication", "✅ onCreate() aufgerufen");

            // 5. Application-Instanz speichern (falls global benötigt)
            try {
                Field instanceField = rkApplicationClass.getDeclaredField("INSTANCE");
                instanceField.setAccessible(true);
                instanceField.set(null, rkApplicationInstance);
                showLog("initRkApplication", "✅ INSTANCE-Feld gesetzt");
            } catch (Exception e) {
                showLog("initRkApplication", "⚠️ INSTANCE-Feld nicht gefunden oder nicht setzbar");
            }

            rkApplicationInitialized = true;
            showLog("initRkApplication", "✅ RK Application erfolgreich initialisiert");

        } catch (ClassNotFoundException e) {
            showLog("initRkApplication", "❌ Klasse com.rk.terminal.App nicht gefunden - wird ignoriert");
        } catch (NoSuchMethodException e) {
            showLog("initRkApplication", "❌ Methode nicht gefunden: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            showLog("initRkApplication", "❌ Fehler: " + e.getMessage());
            e.printStackTrace();
        }
    }

    // ============================================================
    // ★ GETTER ★
    // ============================================================
    
    // Application Instance
    public static QtApplication getInstance() {
        return sInstance;
    }
    
    // Globals
    public static Object getGlobalsInstance() {
        return globalsInstance;
    }
    
    public static Class<?> getGlobalsClass() {
        return globalsClass;
    }
    
    // Temp Dir
    public static File getTempDir() {
        if (tempDir == null) {
            showLog("getTempDir", "⚠️ tempDir ist null! Versuche zu initialisieren...");
            // Fallback: Versuche zu initialisieren
            if (sInstance != null) {
                sInstance.initTempDir();
            } else {
                showLog("getTempDir", "❌ sInstance ist null! Kann nicht initialisieren.");
            }
        }
        return tempDir;
    }
    
    // RK Application
    public static Object getRkApplicationInstance() {
        return rkApplicationInstance;
    }

    public static Class<?> getRkApplicationClass() {
        return rkApplicationClass;
    }

    public static boolean isRkApplicationInitialized() {
        return rkApplicationInitialized;
    }

    // ============================================================
    // ★ SET QT ACTIVITY DELEGATE ★
    // ============================================================
    public static void setQtActivityDelegate(Object listener)
    {
        QtApplication.m_delegateObject = listener;

        ArrayList<Method> delegateMethods = new ArrayList<Method>();
        for (Method m : listener.getClass().getMethods()) {
            if (m.getDeclaringClass().getName().startsWith("org.qtproject.qt.android"))
                delegateMethods.add(m);
        }

        ArrayList<Field> applicationFields = new ArrayList<Field>();
        for (Field f : QtApplication.class.getFields()) {
            if (f.getDeclaringClass().getName().equals(QtApplication.class.getName()))
                applicationFields.add(f);
        }

        for (Method delegateMethod : delegateMethods) {
            try {
                QtActivity.class.getDeclaredMethod(delegateMethod.getName(), delegateMethod.getParameterTypes());
                if (QtApplication.m_delegateMethods.containsKey(delegateMethod.getName())) {
                    QtApplication.m_delegateMethods.get(delegateMethod.getName()).add(delegateMethod);
                } else {
                    ArrayList<Method> delegateSet = new ArrayList<Method>();
                    delegateSet.add(delegateMethod);
                    QtApplication.m_delegateMethods.put(delegateMethod.getName(), delegateSet);
                }
                for (Field applicationField:applicationFields) {
                    if (applicationField.getName().equals(delegateMethod.getName())) {
                        try {
                            applicationField.set(null, delegateMethod);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            } catch (Exception e) {
            }
        }
    }
    
    // ============================================================
    // ★ ON TERMINATE ★
    // ============================================================
    @Override
    public void onTerminate() {
        if (m_delegateObject != null && m_delegateMethods.containsKey("onTerminate"))
            invokeDelegateMethod(m_delegateMethods.get("onTerminate").get(0));
        super.onTerminate();
    }

    // ============================================================
    // ★ INVOKE DELEGATE ★
    // ============================================================
    public static class InvokeResult
    {
        public boolean invoked = false;
        public Object methodReturns = null;
    }

    private static int stackDeep=-1;
    public static InvokeResult invokeDelegate(Object... args)
    {
        InvokeResult result = new InvokeResult();
        if (m_delegateObject == null)
            return result;
        StackTraceElement[] elements = Thread.currentThread().getStackTrace();
        if (-1 == stackDeep) {
            String activityClassName = QtActivity.class.getCanonicalName();
            for (int it=0;it<elements.length;it++)
                if (elements[it].getClassName().equals(activityClassName)) {
                    stackDeep = it;
                    break;
                }
        }
        final String methodName=elements[stackDeep].getMethodName();
        if (-1 == stackDeep || !m_delegateMethods.containsKey(methodName))
            return result;

        for (Method m : m_delegateMethods.get(methodName)) {
            if (m.getParameterTypes().length == args.length) {
                result.methodReturns = invokeDelegateMethod(m, args);
                result.invoked = true;
                return result;
            }
        }
        return result;
    }

    public static Object invokeDelegateMethod(Method m, Object... args)
    {
        try {
            return m.invoke(m_delegateObject, args);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}