// Copyright (C) 2023 The Qt Company Ltd.
// Copyright (c) 2016, BogDan Vatra <bogdan@kde.org>
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

package org.qtproject.qt.android.bindings;

import android.os.Bundle;

import org.qtproject.qt.android.QtActivityBase;

// ★ ★ ★ SHOWLOG IMPORT ★ ★ ★
import org.kivy.android.PythonService;

public class QtActivity extends QtActivityBase
{
    // ★ ★ ★ SHOWLOG ★ ★ ★
    private static void showLog(String msg) {
        android.util.Log.d("QtActivity", "📌 " + msg);
        PythonService.showLog("QtActivity", msg);
    }
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        showLog("🚀 onCreate - Lade Qt-Bibliotheken...");
        
        super.onCreate(savedInstanceState);
        showLog("✅ onCreate abgeschlossen");
    }
}