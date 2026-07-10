package com.rk.terminal.ui.activities.terminal

import android.Manifest
import android.app.Activity
import android.app.PendingIntent
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.content.pm.PackageManager
import android.graphics.Rect
import android.graphics.drawable.Drawable
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.IBinder
import android.provider.Settings
import android.view.View
import android.view.inputmethod.InputMethodManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.rk.terminal.service.SessionService
import com.rk.terminal.ui.navHosts.MainActivityNavHost
import com.rk.terminal.ui.routes.MainActivityRoutes
import com.rk.terminal.ui.screens.terminal.TerminalScreen
import com.rk.terminal.ui.screens.terminal.terminalView
import com.rk.terminal.ui.theme.KarbonTheme
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileWriter
import java.text.SimpleDateFormat
import java.util.*
import android.util.Log
import android.widget.Toast

import androidx.compose.material3.Text

class MainActivity : ComponentActivity() {
    var sessionBinder: SessionService.SessionBinder? = null
    var isBound = false
    private val TAG = "MainActivity"

    // ============================================================
    // ★ Companion Object
    // ============================================================
    companion object {
        private const val TAG = "MainActivity"

        fun showLog(title: String, message: String) {
            Log.d(TAG, "$title: $message")
            try {
                val logFile = File(
                    Environment.getExternalStorageDirectory(),
                    "main_core.log"
                )
                logFile.parentFile?.mkdirs()
                val timestamp = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
                    .format(Date())
                FileWriter(logFile, true).use { writer ->
                    writer.write("$timestamp - $title: $message\n")
                    writer.flush()
                }
            } catch (e: Exception) {
                Log.e(TAG, "Fehler beim Schreiben auf SD-Karte: ${e.message}")
            }
        }
    }

    // ============================================================
    // ★ REQUEST CODES
    // ============================================================
    private val REQUEST_CODE_STORAGE_PERMISSION = 100
    private val REQUEST_CODE_MANAGE_EXTERNAL_STORAGE = 101

    // ============================================================
    // ★ SERVICE CONNECTION
    // ============================================================
    private val serviceConnection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            val binder = service as SessionService.SessionBinder
            sessionBinder = binder
            isBound = true

            lifecycleScope.launch(Dispatchers.Main) {
                setContent {
                    KarbonTheme {
                        Surface {
                            val navController = rememberNavController()
                            MainActivityNavHost(navController = navController, mainActivity = this@MainActivity)

                            val backStackEntry by navController.currentBackStackEntryAsState()

                            val focusManager = LocalFocusManager.current
                            val keyboardController = LocalSoftwareKeyboardController.current

                            LaunchedEffect(backStackEntry?.destination?.route) {
                                if (backStackEntry?.destination?.route != MainActivityRoutes.MainScreen.route) {
                                    focusManager.clearFocus(force = true)
                                    terminalView.get()?.clearFocus()
                                    keyboardController?.hide()
                                }
                            }
                        }
                    }
                }
            }
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            isBound = false
            sessionBinder = null
        }
    }

    // ============================================================
    // ★ LIFECYCLE
    // ============================================================
    override fun onStart() {
        super.onStart()
        showLog("onStart", "▶️ onStart")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            showLog("start", "startForegroundService(Shell)")
            startForegroundService(Intent(this, SessionService::class.java))
        } else {
            startService(Intent(this, SessionService::class.java))
        }
        Intent(this, SessionService::class.java).also { intent ->
            bindService(intent, serviceConnection, BIND_AUTO_CREATE)
        }
    }

    override fun onStop() {
        super.onStop()
        showLog("onStop", "⏹️ onStop")
        if (isBound) {
            unbindService(serviceConnection)
            isBound = false
        }
    }

    // ============================================================
    // ★ NOTIFICATION PERMISSION (Android 13+)
    // ============================================================
    private var denied = 1
    private val requestNotificationPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { isGranted ->
            if (!isGranted && denied <= 2) {
                denied++
                requestNotificationPermission()
            }
        }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                requestNotificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
    }

    // ============================================================
    // ★ SPEICHERBERECHTIGUNG
    // ============================================================
    private fun checkAndRequestStoragePermission() {
        showLog("Permission", "🔍 Prüfe Speicherberechtigung...")

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                showLog("Permission", "📤 Fordere MANAGE_EXTERNAL_STORAGE an...")
                try {
                    val intent = Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
                    startActivityForResult(intent, REQUEST_CODE_MANAGE_EXTERNAL_STORAGE)
                } catch (e: Exception) {
                    showLog("Permission", "❌ Fehler: ${e.message}")
                    Toast.makeText(this, "Fehler beim Öffnen der Berechtigung", Toast.LENGTH_LONG).show()
                }
                return
            } else {
                showLog("Permission", "✅ MANAGE_EXTERNAL_STORAGE bereits erteilt")
            }
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val permissions = arrayOf(
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
            )

            val missingPermissions = permissions.filter {
                ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
            }.toTypedArray()

            if (missingPermissions.isNotEmpty()) {
                showLog("Permission", "📤 Fordere READ/WRITE_EXTERNAL_STORAGE an...")
                ActivityCompat.requestPermissions(this, missingPermissions, REQUEST_CODE_STORAGE_PERMISSION)
            } else {
                showLog("Permission", "✅ READ/WRITE_EXTERNAL_STORAGE bereits erteilt")
            }
        } else {
            showLog("Permission", "✅ Keine Speicherberechtigung nötig (API < 23)")
        }
    }

    // ============================================================
    // ★ ON ACTIVITY RESULT (für MANAGE_EXTERNAL_STORAGE)
    // ============================================================
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == REQUEST_CODE_MANAGE_EXTERNAL_STORAGE) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                if (Environment.isExternalStorageManager()) {
                    showLog("Permission", "✅ MANAGE_EXTERNAL_STORAGE erteilt")
                    Toast.makeText(this, "Speicherzugriff erlaubt", Toast.LENGTH_SHORT).show()
                } else {
                    showLog("Permission", "❌ MANAGE_EXTERNAL_STORAGE verweigert")
                    Toast.makeText(this, "Speicherzugriff benötigt!", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    // ============================================================
    // ★ ON CREATE
    // ============================================================
    var isKeyboardVisible = false

    // In MainActivity.kt - onCreate():
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
    
        showLog("onCreate", "🚀 MainActivity onCreate")
    
        // ★ ★ ★ SOFORT UI ANZEIGEN (auch ohne Service) ★ ★ ★
        setContent {
            KarbonTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("Terminal wird gestartet...")
                    }
                }
            }
        }
    
        checkAndRequestStoragePermission()
        requestNotificationPermission()
    
        if (intent.hasExtra("awake_intent")) {
            moveTaskToBack(true)
            showLog("onCreate", "🔄 moveTaskToBack aufgerufen")
        }
    }

    // ============================================================
    // ★ KEYBOARD LOGIC
    // ============================================================
    var wasKeyboardOpen = false

    override fun onPause() {
        super.onPause()
        wasKeyboardOpen = isKeyboardVisible
        showLog("onPause", "⏸️ onPause, keyboardVisible: $isKeyboardVisible")
    }

    override fun onResume() {
        super.onResume()
        showLog("onResume", "▶️ onResume")

        val rootView = findViewById<View>(android.R.id.content)
        rootView.viewTreeObserver.addOnGlobalLayoutListener {
            val rect = Rect()
            rootView.getWindowVisibleDisplayFrame(rect)
            val screenHeight = rootView.rootView.height
            val keypadHeight = screenHeight - rect.bottom
            val isVisible = keypadHeight > screenHeight * 0.15

            isKeyboardVisible = isVisible
        }

        if (wasKeyboardOpen && !isKeyboardVisible) {
            terminalView.get()?.let {
                val imm = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
                imm.showSoftInput(it, InputMethodManager.SHOW_IMPLICIT)
                showLog("onResume", "⌨️ Keyboard wiederhergestellt")
            }
        }
    }
}