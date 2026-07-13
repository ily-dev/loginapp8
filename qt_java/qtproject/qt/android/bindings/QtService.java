package org.qtproject.qt.android.bindings;

import android.app.Service;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.IBinder;

public class QtService extends Service {

    // ============================================================
    // ★ SHOWLOG ★
    // ============================================================
    private static void showLog(String title, String message) {
        android.util.Log.d("QtService", title + ": " + message);
        // PythonService.showLog("QtService", title + ": " + message);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        showLog("onCreate", "🚀 QtService onCreate");
        // Deine eigene Initialisierung hier
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        showLog("onDestroy", "🗑️ QtService onDestroy");
    }

    @Override
    public IBinder onBind(Intent intent) {
        showLog("onBind", "📨 onBind aufgerufen");
        return null;  // Kein Binding
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        showLog("onStartCommand", "📨 onStartCommand aufgerufen");
        return START_NOT_STICKY;
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        showLog("onConfigurationChanged", "🔄 Configuration changed");
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        showLog("onLowMemory", "⚠️ Low memory");
    }

    @Override
    public void onTaskRemoved(Intent rootIntent) {
        super.onTaskRemoved(rootIntent);
        showLog("onTaskRemoved", "🗑️ Task removed");
    }

    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
        showLog("onTrimMemory", "💾 Trim memory: " + level);
    }

    @Override
    public boolean onUnbind(Intent intent) {
        showLog("onUnbind", "🔌 onUnbind aufgerufen");
        return super.onUnbind(intent);
    }
}