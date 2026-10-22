#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py
ينشئ مشروع أندرويد كامل باسم VoiceAssistant (com.example.voiceassistant).

الميزات المضافة في هذا الإصدار:
  1. المساعد الافتراضي (ASSIST + VoiceInteractionService) مع الاستماع التلقائي.
  2. المحادثة المستمرة (إعادة تشغيل الميكروفون بعد ثانية من انتهاء الرد الصوتي).
  3. المحادثة مع الذكاء الاصطناعي (Gemini) عبر OkHttp عندما لا يُفهم الأمر.
  4. التحكم بمفاتيح الإعدادات (Wi-Fi / Bluetooth ...) عبر خدمة الوصول.
  5. كتابة الأكواد والملفات (HTML / CSS / Java / setup وغيرها) مع نسخ وحفظ (موسّعة).
  6. توليد الصور بالذكاء الاصطناعي (مثال: «ارسم لي قطة») مع حفظ الصورة.
  7. قراءة ملفات الأكواد والتعديل عليها بالصوت أو الكتابة، ثم كتابة التعديل فوق الملف الأصلي.
  8. واجهة محسّنة: الأفاتار ظاهر دائماً، الميكروفون داخل شريط الكتابة،
     والرد على النص المكتوب صامت (الرد الصوتي فقط عند التحدث).
  9. تذكيرات صوتية («ذكرني بشرب الماء بعد 10 دقائق») عبر AlarmManager + ReminderReceiver +
     SpeakingService (خدمة أمامية + TTS) وتعمل حتى لو كان التطبيق مغلقاً.
 10. تفاعل استباقي: ترحيب صوتي عند فتح التطبيق، وسؤال عن الأحوال كل 6 ساعات في الخلفية
     عبر WorkManager (ProactiveWorker) مع إشعار ونطق (TTS).

الاستخدام:
    python setup.py            # ينشئ المشروع في المجلد الحالي
    python setup.py MyDir      # ينشئ المشروع في المجلد MyDir

بعد ذلك:  gradle assembleDebug   (Gradle 8.10+, JDK 17, Android SDK 35)
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(ROOT, exist_ok=True)
os.chdir(ROOT)

print(">> Creating VoiceAssistant project in:", os.getcwd())

# ------------------------------------------------------------------------------
# المجلدات
# ------------------------------------------------------------------------------
DIRS = [
    ".github/workflows",
    "app",
    "app/src/main",
    "app/src/main/java/com/example/voiceassistant",
    "app/src/main/java/com/example/voiceassistant/commands",
    "app/src/main/java/com/example/voiceassistant/commands/commands",
    "app/src/main/java/com/example/voiceassistant/data",
    "app/src/main/java/com/example/voiceassistant/data/models",
    "app/src/main/java/com/example/voiceassistant/service",
    "app/src/main/java/com/example/voiceassistant/speech",
    "app/src/main/java/com/example/voiceassistant/ui",
    "app/src/main/java/com/example/voiceassistant/ui/components",
    "app/src/main/java/com/example/voiceassistant/ui/theme",
    "app/src/main/java/com/example/voiceassistant/viewmodel",
    "app/src/main/res/values",
    "app/src/main/res/xml",
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

FILES_CREATED = [0]


def write_file(path, content):
    """Writes one file as UTF-8 (needed for the Arabic strings)."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    FILES_CREATED[0] += 1


# ------------------------------------------------------------------------------
# الملفات
# ------------------------------------------------------------------------------
# 1. settings.gradle.kts
write_file("settings.gradle.kts", r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "VoiceAssistant"
include(":app")
''')

# 2. build.gradle.kts
write_file("build.gradle.kts", r'''// Top-level build file
plugins {
    id("com.android.application") version "8.7.3" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
''')

# 3. gradle.properties
write_file("gradle.properties", r'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.code.style=official
''')

# 4. proguard-rules.pro
write_file("proguard-rules.pro", r'''# Add project specific ProGuard rules here.
# The accessibility service is referenced from the manifest.
-keep class com.example.voiceassistant.service.VoiceAccessibilityService { *; }
-keep class com.example.voiceassistant.service.VaInteractionService { *; }
-keep class com.example.voiceassistant.service.VaSessionService { *; }
-keep class com.example.voiceassistant.service.VaRecognitionService { *; }
-keep class com.example.voiceassistant.VoiceAssistantApp { *; }
-keep class com.example.voiceassistant.service.ReminderReceiver { *; }
-keep class com.example.voiceassistant.service.SpeakingService { *; }
-keep class com.example.voiceassistant.service.ProactiveWorker { *; }

# Keep line numbers for readable crash reports
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
''')

# 5. app/build.gradle.kts
write_file("app/build.gradle.kts", r'''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.example.voiceassistant"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.voiceassistant"
        minSdk = 26
        targetSdk = 35
        versionCode = 3
        versionName = "2.1"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "../proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("androidx.security:security-crypto:1.1.0-alpha06")

    // HTTP client for the conversational AI service
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    // Background scheduling for the proactive "how are you?" check-ins
    implementation("androidx.work:work-runtime-ktx:2.9.1")

    val composeBom = platform("androidx.compose:compose-bom:2024.10.01")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")

    debugImplementation("androidx.compose.ui:ui-tooling")
}
''')

# 6. app/src/main/AndroidManifest.xml
write_file("app/src/main/AndroidManifest.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.CALL_PHONE" />
    <uses-permission android:name="com.android.alarm.permission.SET_ALARM" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.READ_CLIPBOARD" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />

    <uses-feature
        android:name="android.hardware.microphone"
        android:required="false" />
    <uses-feature
        android:name="android.hardware.telephony"
        android:required="false" />

    <!-- Package visibility (Android 11+) -->
    <queries>
        <intent>
            <action android:name="android.speech.RecognitionService" />
        </intent>
        <intent>
            <action android:name="android.intent.action.TTS_SERVICE" />
        </intent>
        <intent>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent>
    </queries>

    <application
        android:name=".VoiceAssistantApp"
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.VoiceAssistant">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>

            <!-- Default digital assistant entry point -->
            <intent-filter>
                <action android:name="android.intent.action.ASSIST" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.VoiceAccessibilityService"
            android:exported="true"
            android:label="@string/app_name"
            android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
            <intent-filter>
                <action android:name="android.accessibilityservice.AccessibilityService" />
            </intent-filter>
            <meta-data
                android:name="android.accessibilityservice"
                android:resource="@xml/accessibility_service_config" />
        </service>

        <!-- Voice interaction (makes the app selectable as the default assistant) -->
        <service
            android:name=".service.VaInteractionService"
            android:exported="true"
            android:label="@string/app_name"
            android:permission="android.permission.BIND_VOICE_INTERACTION">
            <meta-data
                android:name="android.voice_interaction"
                android:resource="@xml/assist_interaction" />
            <intent-filter>
                <action android:name="android.service.voice.VoiceInteractionService" />
            </intent-filter>
        </service>

        <service
            android:name=".service.VaSessionService"
            android:exported="true"
            android:permission="android.permission.BIND_VOICE_INTERACTION" />

        <service
            android:name=".service.VaRecognitionService"
            android:exported="true"
            android:label="@string/app_name">
            <intent-filter>
                <action android:name="android.speech.RecognitionService" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </service>

        <!-- Reminders: fired by AlarmManager; also re-arms everything after a reboot -->
        <receiver
            android:name=".service.ReminderReceiver"
            android:exported="false">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.app.action.SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED" />
            </intent-filter>
        </receiver>

        <!-- Speaks reminders / check-ins (TTS) while the app is closed -->
        <service
            android:name=".service.SpeakingService"
            android:exported="false"
            android:foregroundServiceType="mediaPlayback" />

        <!-- Security monitor: watches the clipboard for suspicious links while protection is on -->
        <service
            android:name=".service.SecurityMonitorService"
            android:exported="false"
            android:foregroundServiceType="dataSync" />

    </application>

</manifest>
''')

# 7. app/src/main/res/values/strings.xml
write_file("app/src/main/res/values/strings.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Voice Assistant</string>
    <string name="accessibility_service_description">Lets the voice assistant perform on-screen actions such as Back, Home, Recents, Notifications, scrolling, taking a screenshot, tapping items by name and flipping switches (Wi-Fi, Bluetooth...) in Settings.</string>
</resources>
''')

# 8. app/src/main/res/values/colors.xml
write_file("app/src/main/res/values/colors.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="background">#FFFBFAFF</color>
    <color name="primary">#FF4F5BD5</color>
    <color name="primary_dark">#FF3640A8</color>
    <color name="accent">#FF00B8A9</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
''')

# 9. app/src/main/res/values/themes.xml
write_file("app/src/main/res/values/themes.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.VoiceAssistant" parent="android:Theme.Material.Light.NoActionBar">
        <item name="android:statusBarColor">@android:color/transparent</item>
        <item name="android:navigationBarColor">@android:color/transparent</item>
        <item name="android:windowBackground">@color/background</item>
    </style>
</resources>
''')

# 10. app/src/main/res/xml/accessibility_service_config.xml
write_file("app/src/main/res/xml/accessibility_service_config.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagDefault|flagIncludeNotImportantViews"
    android:canRetrieveWindowContent="true"
    android:description="@string/accessibility_service_description"
    android:notificationTimeout="100" />
''')

# 11. app/src/main/res/xml/backup_rules.xml
write_file("app/src/main/res/xml/backup_rules.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
    <exclude domain="sharedpref" path="." />
    <exclude domain="database" path="." />
</full-backup-content>
''')

# 12. app/src/main/res/xml/data_extraction_rules.xml
write_file("app/src/main/res/xml/data_extraction_rules.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="sharedpref" path="." />
        <exclude domain="database" path="." />
    </cloud-backup>
    <device-transfer>
        <exclude domain="sharedpref" path="." />
        <exclude domain="database" path="." />
    </device-transfer>
</data-extraction-rules>
''')

# 12b. app/src/main/res/xml/assist_interaction.xml  (NEW)
write_file("app/src/main/res/xml/assist_interaction.xml", r'''<?xml version="1.0" encoding="utf-8"?>
<voice-interaction-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:recognitionService="com.example.voiceassistant.service.VaRecognitionService"
    android:sessionService="com.example.voiceassistant.service.VaSessionService"
    android:supportsAssist="true" />
''')

# 13. .github/workflows/build.yml
write_file(".github/workflows/build.yml", r'''name: Build VoiceAssistant APK

on:
  push:
    branches: [ main, master ]
  pull_request:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Set up Android SDK
        uses: android-actions/setup-android@v3

      - name: Set up Gradle
        uses: gradle/actions/setup-gradle@v4
        with:
          gradle-version: '8.10.2'

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Generate project files from setup.py
        run: python setup.py

      - name: Build debug APK
        run: gradle assembleDebug --stacktrace

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: VoiceAssistant-debug-apk
          path: app/build/outputs/apk/debug/*.apk
''')

# 14. app/src/main/java/com/example/voiceassistant/MainActivity.kt
write_file("app/src/main/java/com/example/voiceassistant/MainActivity.kt", r'''package com.example.voiceassistant

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.WindowManager
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.core.view.WindowCompat
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import com.example.voiceassistant.ui.MainScreen
import com.example.voiceassistant.ui.theme.VoiceAssistantTheme

class MainActivity : ComponentActivity() {

    companion object {
        /** Set by the voice-interaction session when the user invokes the default assistant. */
        const val EXTRA_AUTO_LISTEN = "com.example.voiceassistant.AUTO_LISTEN"
    }

    /** Android 13+: reminders and check-ins need the notification permission. */
    private val notificationPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { }

    /** Incremented every time the app is opened as the assistant; the UI reacts by listening. */
    private var autoListenToken by mutableIntStateOf(0)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // لوحة المفاتيح: أندرويد 15+ يفرض edge-to-edge (و Compose يتولى الأمر عبر imePadding).
        // في الإصدارات الأقدم لا نستعمل edge-to-edge، فيقوم النظام نفسه بتصغير النافذة فوق لوحة المفاتيح
        // (adjustResize)، وهذا يعمل على كل الأجهزة وكل لوحات المفاتيح.
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE)
        if (Build.VERSION.SDK_INT >= 35) {
            enableEdgeToEdge()
        } else {
            WindowCompat.setDecorFitsSystemWindows(window, true)
        }

        // Ask for the notification permission (not when opened as the assistant: the mic prompt comes first).
        if (savedInstanceState == null && !isAssistLaunch(intent)) {
            requestNotificationPermissionIfNeeded()
        }

        // savedInstanceState == null: don't re-trigger after rotation / recreation.
        if (savedInstanceState == null && isAssistLaunch(intent)) {
            autoListenToken++
        }

        setContent {
            VoiceAssistantTheme {
                MainScreen(autoListenToken = autoListenToken)
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        if (isAssistLaunch(intent)) {
            autoListenToken++
        }
    }

    private fun requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) !=
            PackageManager.PERMISSION_GRANTED
        ) {
            notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }

    private fun isAssistLaunch(intent: Intent?): Boolean =
        intent?.action == Intent.ACTION_ASSIST ||
            intent?.getBooleanExtra(EXTRA_AUTO_LISTEN, false) == true
}
''')

# 15. app/src/main/java/com/example/voiceassistant/VoiceAssistantApp.kt
write_file("app/src/main/java/com/example/voiceassistant/VoiceAssistantApp.kt", r'''package com.example.voiceassistant

import android.app.Application
import com.example.voiceassistant.data.ConversationRepository
import com.example.voiceassistant.service.NotificationHelper
import com.example.voiceassistant.service.ProactiveScheduler

class VoiceAssistantApp : Application() {
    /** Single in-memory conversation store shared by the whole process. */
    val conversationRepository: ConversationRepository by lazy { ConversationRepository() }

    override fun onCreate() {
        super.onCreate()
        // Notification channels are required on Android 8+ for any notification to show.
        NotificationHelper.createChannels(this)
        // Periodic "how are you?" check-in (KEEP: no duplicates, survives reboot).
        ProactiveScheduler.schedule(this)
    }
}
''')

# 16. app/src/main/java/com/example/voiceassistant/data/models/Message.kt
write_file("app/src/main/java/com/example/voiceassistant/data/models/Message.kt", r'''package com.example.voiceassistant.data.models

/** A block of code returned by the AI (language tag + full source). */
data class CodeBlock(
    val language: String,
    val content: String,
    /** True when this block is the COMPLETE edited version of the working file. */
    val isEdit: Boolean = false,
    /** Name of the file this code belongs to (null = unknown). */
    val fileName: String? = null,
    /** content:// Uri of the original file so the edit can be written back (null = not possible). */
    val sourceUri: String? = null
)

data class Message(
    val id: Long,
    val text: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis(),
    val code: List<CodeBlock> = emptyList(),
    /** Path of a generated picture (null = no picture). */
    val imagePath: String? = null
)
''')

# 17. app/src/main/java/com/example/voiceassistant/data/ConversationRepository.kt
write_file("app/src/main/java/com/example/voiceassistant/data/ConversationRepository.kt", r'''package com.example.voiceassistant.data

import com.example.voiceassistant.data.models.CodeBlock
import com.example.voiceassistant.data.models.Message
import java.util.concurrent.atomic.AtomicLong
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class ConversationRepository {

    private val nextId = AtomicLong(1)
    private val _messages = MutableStateFlow<List<Message>>(emptyList())
    val messages: StateFlow<List<Message>> = _messages.asStateFlow()

    fun addUserMessage(text: String): Message = add(text, isUser = true)

    fun addAssistantMessage(
        text: String,
        code: List<CodeBlock> = emptyList(),
        imagePath: String? = null
    ): Message =
        add(text, isUser = false, code = code, imagePath = imagePath)

    fun clear() {
        _messages.value = emptyList()
    }

    /** Replaces the whole conversation (used to restore a saved session). */
    fun setMessages(messages: List<Message>) {
        val maxId = messages.maxOfOrNull { it.id } ?: 0L
        nextId.set(maxOf(nextId.get(), maxId + 1))
        _messages.value = messages
    }

    private fun add(
        text: String,
        isUser: Boolean,
        code: List<CodeBlock> = emptyList(),
        imagePath: String? = null
    ): Message {
        val message = Message(
            id = nextId.getAndIncrement(),
            text = text,
            isUser = isUser,
            code = code,
            imagePath = imagePath
        )
        _messages.update { it + message }
        return message
    }
}
''')

# 17a. app/src/main/java/com/example/voiceassistant/data/ChatHistoryManager.kt
write_file("app/src/main/java/com/example/voiceassistant/data/ChatHistoryManager.kt", r'''package com.example.voiceassistant.data

import android.content.Context
import com.example.voiceassistant.data.models.CodeBlock
import com.example.voiceassistant.data.models.Message
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject

/**
 * One saved conversation. [messagesJson] holds the full Message objects
 * (text, code blocks, picture path ...) as a JSON array string.
 */
data class SavedSession(
    val id: Long,
    val title: String,
    val timestamp: Long,
    val messagesJson: String
)

/** Stores conversations in SharedPreferences as a JSON array (newest first). */
class ChatHistoryManager(context: Context) {

    private val prefs = context.applicationContext
        .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    /**
     * Saves [messages] as a session and returns its id.
     * Passing an existing [id] updates that session instead of creating a duplicate.
     */
    fun saveSession(title: String, messages: List<Message>, id: Long? = null): Long {
        val existing = readArray()
        var sessionId = id ?: System.currentTimeMillis()
        if (id == null) {
            while (containsId(existing, sessionId)) sessionId++
        }
        val result = JSONArray()
        result.put(
            JSONObject()
                .put("id", sessionId)
                .put("title", title)
                .put("timestamp", System.currentTimeMillis())
                .put("messagesJson", messagesToJson(messages).toString())
        )
        for (i in 0 until existing.length()) {
            val item = existing.optJSONObject(i) ?: continue
            if (item.optLong("id") != sessionId) result.put(item)
        }
        prefs.edit().putString(KEY_SESSIONS, result.toString()).apply()
        return sessionId
    }

    fun getAllSessions(): List<SavedSession> {
        val array = readArray()
        val list = ArrayList<SavedSession>(array.length())
        for (i in 0 until array.length()) {
            val item = array.optJSONObject(i) ?: continue
            list.add(
                SavedSession(
                    id = item.optLong("id"),
                    title = item.optString("title"),
                    timestamp = item.optLong("timestamp"),
                    messagesJson = item.optString("messagesJson", "[]")
                )
            )
        }
        return list
    }

    fun deleteSession(id: Long) {
        val existing = readArray()
        val result = JSONArray()
        for (i in 0 until existing.length()) {
            val item = existing.optJSONObject(i) ?: continue
            if (item.optLong("id") != id) result.put(item)
        }
        prefs.edit().putString(KEY_SESSIONS, result.toString()).apply()
    }

    private fun containsId(array: JSONArray, id: Long): Boolean {
        for (i in 0 until array.length()) {
            if (array.optJSONObject(i)?.optLong("id") == id) return true
        }
        return false
    }

    private fun readArray(): JSONArray = try {
        JSONArray(prefs.getString(KEY_SESSIONS, null) ?: "[]")
    } catch (e: JSONException) {
        JSONArray()
    }

    companion object {
        private const val PREFS_NAME = "chat_history"
        private const val KEY_SESSIONS = "sessions"

        fun messagesToJson(messages: List<Message>): JSONArray {
            val array = JSONArray()
            for (m in messages) {
                val codeArray = JSONArray()
                for (c in m.code) {
                    val code = JSONObject()
                        .put("language", c.language)
                        .put("content", c.content)
                        .put("isEdit", c.isEdit)
                    if (c.fileName != null) code.put("fileName", c.fileName)
                    if (c.sourceUri != null) code.put("sourceUri", c.sourceUri)
                    codeArray.put(code)
                }
                val obj = JSONObject()
                    .put("id", m.id)
                    .put("text", m.text)
                    .put("isUser", m.isUser)
                    .put("timestamp", m.timestamp)
                    .put("code", codeArray)
                if (m.imagePath != null) obj.put("imagePath", m.imagePath)
                array.put(obj)
            }
            return array
        }

        fun parseMessages(json: String): List<Message> {
            val array = try {
                JSONArray(json)
            } catch (e: JSONException) {
                return emptyList()
            }
            val list = ArrayList<Message>(array.length())
            for (i in 0 until array.length()) {
                val obj = array.optJSONObject(i) ?: continue
                val codeArray = obj.optJSONArray("code") ?: JSONArray()
                val blocks = ArrayList<CodeBlock>(codeArray.length())
                for (j in 0 until codeArray.length()) {
                    val c = codeArray.optJSONObject(j) ?: continue
                    blocks.add(
                        CodeBlock(
                            language = c.optString("language"),
                            content = c.optString("content"),
                            isEdit = c.optBoolean("isEdit", false),
                            fileName = if (c.has("fileName") && !c.isNull("fileName")) c.getString("fileName") else null,
                            sourceUri = if (c.has("sourceUri") && !c.isNull("sourceUri")) c.getString("sourceUri") else null
                        )
                    )
                }
                list.add(
                    Message(
                        id = obj.optLong("id", (i + 1).toLong()),
                        text = obj.optString("text"),
                        isUser = obj.optBoolean("isUser", false),
                        timestamp = obj.optLong("timestamp", System.currentTimeMillis()),
                        code = blocks,
                        imagePath = if (obj.has("imagePath") && !obj.isNull("imagePath")) obj.getString("imagePath") else null
                    )
                )
            }
            return list
        }
    }
}
''')

# 17b. AiChatService.kt (النسخة المحسّنة مدمجة بالكامل داخل السكريبت)
#   - ترتيب النماذج: الأسرع أولاً (gemini-2.5-flash-lite ...) مع تخطي النماذج التي ترجع 404
#   - مهلات أقصر: readTimeout 40s و callTimeout 45s لكل محاولة
# مفتاح Gemini لا يُكتب داخل السكريبت. يُؤخذ بالترتيب من:
#   1) متغير البيئة GEMINI_API_KEY
#   2) ملف AiChatService.kt قديم بجوار السكريبت (يُقرأ منه المفتاح فقط)
def _resolve_gemini_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    for folder in (SCRIPT_DIR, os.getcwd()):
        candidate = os.path.join(folder, "AiChatService.kt")
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                found = re.search(r'const val GEMINI_API_KEY = "([^"]*)"', f.read())
            if found and found.group(1) and found.group(1) != "__GEMINI_API_KEY__":
                return found.group(1)
    return ""


GEMINI_KEY = _resolve_gemini_key()
if not GEMINI_KEY:
    print(">> WARNING: no Gemini key found. Set env GEMINI_API_KEY or edit GEMINI_API_KEY in AiChatService.kt.")

AI_SERVICE_TEMPLATE = r'''package com.example.voiceassistant.data

import android.util.Base64
import android.util.Log
import com.example.voiceassistant.data.models.CodeBlock
import com.example.voiceassistant.viewmodel.AppLanguage
import java.io.IOException
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject

const val GEMINI_API_KEY = "__GEMINI_API_KEY__"
const val OPENAI_API_KEY = ""
const val CLAUDE_API_KEY = ""

// الترتيب = الأسرع والأكثر استقراراً أولاً. نماذج gemini-1.5 أُوقفت نهائياً من Google (تعطي model not found)،
// لذلك لا تضعها هنا. نماذج Flash-Lite هي الأسرع، و gemini-3.8-flash الأذكى كخيار احتياطي.
val GEMINI_MODELS = listOf(
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite"
)
val IMAGE_MODELS = listOf(
    "gemini-2.5-flash-image-preview",
    "gemini-2.0-flash-exp-image-generation",
    "gemini-2.5-flash-image"
)

private const val GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
private const val OPENAI_BASE = "https://api.openai.com/v1/chat/completions"
private const val CLAUDE_BASE = "https://api.anthropic.com/v1/messages"

private val RETRY_CODES = setOf(429, 500, 502, 503, 504)
private const val MAX_HISTORY_MESSAGES = 12
private const val TAG = "AiChat"

// أقصى زمن إجمالي لسلسلة نماذج Gemini كلها: بعده تظهر رسالة خطأ بدل أن تبقى "جارٍ المعالجة" معلّقة.
private const val GEMINI_TOTAL_TIMEOUT_MS = 40_000L

// عند وجود ملف عمل (قراءة/تعديل كود) يتضمن الرد الملف كاملاً، لذلك نمنحه وقتاً أطول.
private const val EDIT_TOTAL_TIMEOUT_MS = 110_000L

enum class AiError { NOT_CONFIGURED, BAD_KEY, RATE_LIMIT, NETWORK, EMPTY, OTHER }

sealed class AiResult {
    data class Success(val text: String, val code: List<CodeBlock> = emptyList()) : AiResult()
    data class Error(val kind: AiError, val detail: String = "") : AiResult()
}

sealed class ImageResult {
    class Success(val bytes: ByteArray) : ImageResult()
    data class Error(val kind: AiError, val detail: String = "") : ImageResult()
}

/** The code file the user is working on: read once, then explained / edited over several requests. */
data class WorkingFile(
    val name: String,
    /** Uri of the original file (null = unknown, so the edit can only be copied or saved as new). */
    val uri: String?,
    val content: String
)

class AiChatService {

    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .writeTimeout(10, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .callTimeout(25, TimeUnit.SECONDS)   // حد أقصى لكل محاولة (نموذج) حتى لا يعلق الطلب
        .build()

    // للطلبات الثقيلة فقط (توليد الصور / تحليل الملفات): تحتاج وقتاً أطول من الدردشة العادية.
    private val longClient: OkHttpClient = client.newBuilder()
        .readTimeout(90, TimeUnit.SECONDS)
        .callTimeout(100, TimeUnit.SECONDS)
        .build()

    // نماذج رجعت 404 (غير موجودة/متوقفة): نتجاوزها في بقية الجلسة بدل إعادة تجربتها كل مرة.
    private val unavailableModels: MutableSet<String> = java.util.concurrent.ConcurrentHashMap.newKeySet()

    private fun activeModels(): List<String> =
        GEMINI_MODELS.filter { it !in unavailableModels }.ifEmpty { GEMINI_MODELS }

    private val history = ArrayList<Pair<String, String>>()
    private val lock = Any()

    /** While set, its content is sent with every request so the AI can read and edit it. */
    @Volatile
    var workingFile: WorkingFile? = null

    fun isConfigured(): Boolean = GEMINI_API_KEY.isNotBlank() || OPENAI_API_KEY.isNotBlank() || CLAUDE_API_KEY.isNotBlank()

    fun clearHistory() {
        synchronized(lock) { history.clear() }
    }

    suspend fun ask(text: String, lang: AppLanguage): AiResult = withContext(Dispatchers.IO) {
        if (!isConfigured()) return@withContext AiResult.Error(AiError.NOT_CONFIGURED)

        val trace = ArrayList<String>()
        var lastError: AiResult.Error = AiResult.Error(AiError.OTHER, "No models tried")

        if (GEMINI_API_KEY.isNotBlank()) {
            var timedOut = true
            val editing = workingFile != null
            val totalTimeout = if (editing) EDIT_TOTAL_TIMEOUT_MS else GEMINI_TOTAL_TIMEOUT_MS
            // للتعديل على الكود نفضّل النماذج الأقوى (غير lite) أولاً.
            val models = if (editing) activeModels().sortedBy { if (it.contains("lite")) 1 else 0 } else activeModels()
            val geminiResult: AiResult? = withTimeoutOrNull(totalTimeout) {
                for (modelName in models) {
                    val started = System.currentTimeMillis()
                    val result = askGeminiModel(modelName, text, lang)
                    val took = System.currentTimeMillis() - started
                    if (result is AiResult.Success) {
                        Log.i(TAG, "$modelName OK in ${took}ms")
                        timedOut = false
                        return@withTimeoutOrNull result
                    }
                    if (result is AiResult.Error) {
                        val line = "$modelName ${took}ms ${result.kind} ${result.detail}".take(140)
                        Log.w(TAG, line)   // Logcat: فلتر AiChat
                        trace.add(line)
                        lastError = result
                        if (result.kind == AiError.BAD_KEY || result.kind == AiError.NOT_CONFIGURED) break
                    }
                }
                timedOut = false
                null
            }
            if (geminiResult is AiResult.Success) return@withContext geminiResult
            val summary = trace.joinToString(" | ").take(400)
            lastError = if (timedOut) {
                AiResult.Error(AiError.NETWORK, "timeout ${totalTimeout / 1000}s | $summary")
            } else {
                lastError.copy(detail = summary.ifBlank { lastError.detail })
            }
        }

        if (OPENAI_API_KEY.isNotBlank()) {
            val result = askChatGPT(text, lang)
            if (result is AiResult.Success) return@withContext result
            if (result is AiResult.Error) lastError = result
        }

        if (CLAUDE_API_KEY.isNotBlank()) {
            val result = askClaude(text, lang)
            if (result is AiResult.Success) return@withContext result
            if (result is AiResult.Error) lastError = result
        }

        return@withContext lastError
    }

    private suspend fun askGeminiModel(modelName: String, text: String, lang: AppLanguage): AiResult {
        try {
            val json = buildGeminiBody(text, lang).toString()
            val request = Request.Builder()
                .url("$GEMINI_BASE$modelName:generateContent")
                .header("x-goog-api-key", GEMINI_API_KEY)
                .post(json.toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()

            (if (workingFile != null) longClient else client).newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    if (response.code == 404) unavailableModels.add(modelName)
                    return AiResult.Error(kindForGemini(response.code, raw), apiError(response.code, raw))
                }
                val full = extractGeminiText(raw)
                if (full.isBlank()) return AiResult.Error(AiError.EMPTY)
                val (spoken, rawCode) = splitCode(full, lang)
                val code = applyEdit(rawCode)
                // The edited file already lives in the system prompt, so history only keeps the short summary.
                remember(text, if (code.any { it.isEdit }) spoken else full)
                return AiResult.Success(spoken, code)
            }
        } catch (e: IOException) {
            return AiResult.Error(AiError.NETWORK, e.toString().take(160))
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            return AiResult.Error(AiError.OTHER, e.toString().take(160))
        }
    }

    private suspend fun askChatGPT(text: String, lang: AppLanguage): AiResult {
        try {
            val json = JSONObject()
                .put("model", "gpt-4o-mini")
                .put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", text)))
                .toString()
            val request = Request.Builder()
                .url(OPENAI_BASE)
                .header("Authorization", "Bearer $OPENAI_API_KEY")
                .post(json.toRequestBody("application/json".toMediaType()))
                .build()
            client.newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    return AiResult.Error(if (response.code == 401) AiError.BAD_KEY else AiError.OTHER, "HTTP ${response.code}")
                }
                val full = JSONObject(raw).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content")
                val (spoken, code) = splitCode(full, lang)
                return AiResult.Success(spoken, code)
            }
        } catch (e: Exception) {
            return AiResult.Error(AiError.NETWORK, e.toString().take(160))
        }
    }

    private suspend fun askClaude(text: String, lang: AppLanguage): AiResult {
        try {
            val json = JSONObject()
                .put("model", "claude-3-haiku-20240307")
                .put("max_tokens", 4096)
                .put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", text)))
                .toString()
            val request = Request.Builder()
                .url(CLAUDE_BASE)
                .header("x-api-key", CLAUDE_API_KEY)
                .header("anthropic-version", "2023-06-01")
                .post(json.toRequestBody("application/json".toMediaType()))
                .build()
            client.newCall(request).await().use { response ->
                val raw = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    return AiResult.Error(if (response.code == 401) AiError.BAD_KEY else AiError.OTHER, "HTTP ${response.code}")
                }
                val full = JSONObject(raw).getJSONArray("content").getJSONObject(0).getString("text")
                val (spoken, code) = splitCode(full, lang)
                return AiResult.Success(spoken, code)
            }
        } catch (e: Exception) {
            return AiResult.Error(AiError.NETWORK, e.toString().take(160))
        }
    }

    suspend fun generateImage(prompt: String): ImageResult = withContext(Dispatchers.IO) {
        if (GEMINI_API_KEY.isBlank()) return@withContext ImageResult.Error(AiError.NOT_CONFIGURED)
        try {
            val json = JSONObject()
                .put("contents", JSONArray().put(turn("user", prompt)))
                .put("generationConfig", JSONObject().put("responseModalities", JSONArray().put("TEXT").put("IMAGE")))
                .toString()
            var lastError: ImageResult.Error = ImageResult.Error(AiError.OTHER, "No image models tried")
            for (modelName in IMAGE_MODELS) {
                val request = Request.Builder()
                    .url("$GEMINI_BASE$modelName:generateContent")
                    .header("x-goog-api-key", GEMINI_API_KEY)
                    .post(json.toRequestBody("application/json; charset=utf-8".toMediaType()))
                    .build()
                try {
                    longClient.newCall(request).await().use { response ->
                        val raw = response.body?.string().orEmpty()
                        if (!response.isSuccessful) {
                            if (response.code == 404) unavailableModels.add(modelName)
                            lastError = ImageResult.Error(kindForGemini(response.code, raw), apiError(response.code, raw))
                            return@use
                        }
                        val parts = JSONObject(raw).optJSONArray("candidates")?.optJSONObject(0)?.optJSONObject("content")?.optJSONArray("parts")
                        if (parts == null) {
                            lastError = ImageResult.Error(AiError.EMPTY)
                            return@use
                        }
                        for (i in 0 until parts.length()) {
                            val part = parts.optJSONObject(i) ?: continue
                            val inline = part.optJSONObject("inlineData") ?: part.optJSONObject("inline_data")
                            val data = inline?.optString("data").orEmpty()
                            if (data.isNotBlank()) {
                                return@withContext ImageResult.Success(Base64.decode(data, Base64.DEFAULT))
                            }
                        }
                        lastError = ImageResult.Error(AiError.EMPTY)
                    }
                } catch (e: CancellationException) {
                    throw e
                } catch (e: Exception) {
                    lastError = ImageResult.Error(AiError.NETWORK, e.toString().take(160))
                }
            }
            return@withContext lastError
        } catch (e: Exception) {
            return@withContext ImageResult.Error(AiError.NETWORK, e.toString().take(160))
        }
    }

    /** تنفيذ الطلب بشكل قابل للإلغاء: عند انتهاء المهلة أو إلغاء الكوروتين يُقطع الاتصال فعلاً. */
    private suspend fun Call.await(): Response = suspendCancellableCoroutine { cont ->
        cont.invokeOnCancellation { cancel() }
        enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                if (cont.isActive) cont.resumeWithException(e)
            }

            override fun onResponse(call: Call, response: Response) {
                if (cont.isActive) cont.resume(response) else response.close()
            }
        })
    }

    private fun kindForGemini(code: Int, raw: String): AiError = when (code) {
        401, 403 -> AiError.BAD_KEY
        400 -> if (raw.contains("API key", ignoreCase = true)) AiError.BAD_KEY else AiError.OTHER
        429 -> AiError.RATE_LIMIT
        else -> AiError.OTHER
    }

    private fun apiError(code: Int, raw: String): String {
        val msg = try { JSONObject(raw).optJSONObject("error")?.optString("message").orEmpty() } catch (e: Exception) { "" }
        return "HTTP $code: " + msg.replace("\n", " ").take(200)
    }

    private fun turn(role: String, text: String): JSONObject =
        JSONObject().put("role", role).put("parts", JSONArray().put(JSONObject().put("text", text)))

    private fun basePrompt(lang: AppLanguage): String = lang.tr(
        "أنت مساعد صوتي ذكي. أجب بالعربية وبإيجاز. إذا طلب المستخدم كوداً، اكتبه داخل كتلة markdown.",
        "You are a smart voice assistant. Answer briefly in English. If the user asks for code, provide it in a markdown block."
    )

    private fun editingRules(): String = """
        The user is working on the code file given below. You can read it, explain it, find bugs and edit it when asked.
        Rules:
        1. When asked to change, fix, add or refactor something, return the COMPLETE updated file (never only a snippet, never "rest unchanged") in exactly ONE code block. Write the word edit after the language on the opening fence, for example ```kotlin edit. Keep all unrelated code and formatting exactly as it was.
        2. Outside the code block write 1-3 short plain sentences saying what you changed. They are read aloud, so put no code or symbols there.
        3. If the user only asks a question or wants an explanation, answer in plain text and do NOT return the whole file.
        4. If the request is unclear, ask one short question instead of guessing.
        5. If the question is unrelated to this file, ignore the file.
    """.trimIndent()

    private fun systemPrompt(lang: AppLanguage): String {
        val base = basePrompt(lang)
        val file = workingFile ?: return base
        return base + "\n\n" + editingRules() +
            "\n\n=== BEGIN FILE: ${file.name} ===\n" + file.content + "\n=== END FILE ==="
    }

    private fun buildGeminiBody(text: String, lang: AppLanguage): JSONObject {
        val contents = JSONArray()
        synchronized(lock) { history.forEach { (role, t) -> contents.put(turn(role, t)) } }
        contents.put(turn("user", text))
        return JSONObject()
            .put("system_instruction", JSONObject().put("parts", JSONArray().put(JSONObject().put("text", systemPrompt(lang)))))
            .put("contents", contents)
            .put("generationConfig", JSONObject().put("maxOutputTokens", if (workingFile != null) 32768 else 8192))
    }

    private fun extractGeminiText(raw: String): String {
        val parts = JSONObject(raw).optJSONArray("candidates")?.optJSONObject(0)?.optJSONObject("content")?.optJSONArray("parts") ?: return ""
        val sb = StringBuilder()
        for (i in 0 until parts.length()) {
            parts.optJSONObject(i)?.optString("text")?.let { sb.append(it) }
        }
        return sb.toString().trim()
    }

    // group 1 = language, group 2 = extra words on the fence line (e.g. "edit"), group 3 = the code.
    private val fence = Regex("```([A-Za-z0-9+#._-]*)([^\\r\\n]*)\\r?\\n([\\s\\S]*?)```")

    private fun splitCode(full: String, lang: AppLanguage): Pair<String, List<CodeBlock>> {
        if (!full.contains("```")) return clean(full) to emptyList()
        val text = if (Regex("```").findAll(full).count() % 2 == 1) full + "\n```" else full
        val blocks = fence.findAll(text).map {
            CodeBlock(
                language = it.groupValues[1].lowercase(),
                content = it.groupValues[3].trimEnd(),
                isEdit = it.groupValues[2].contains("edit", ignoreCase = true)
            )
        }.toList()
        if (blocks.isEmpty()) return clean(full) to emptyList()
        var spoken = clean(fence.replace(text, " "))
        if (spoken.isBlank()) spoken = lang.tr("تفضل، هذا هو الكود.", "Here is the code.")
        return spoken to blocks
    }

    /**
     * If the answer holds the complete edited file, it becomes the new working file and the block is tagged
     * with the original file name / Uri so the UI can write it back. Short snippets are left untouched.
     */
    private fun applyEdit(blocks: List<CodeBlock>): List<CodeBlock> {
        val file = workingFile ?: return blocks
        val originalLines = file.content.lines().size
        val edited = blocks.firstOrNull { it.isEdit }
            ?: blocks.singleOrNull()?.takeIf { it.content.lines().size >= originalLines * 6 / 10 }
            ?: return blocks
        val trailing = if (file.content.endsWith("\n")) "\n" else ""
        workingFile = file.copy(content = edited.content + trailing)
        return blocks.map {
            if (it === edited) it.copy(isEdit = true, fileName = file.name, sourceUri = file.uri) else it
        }
    }

    private fun clean(text: String): String = text.replace("*", "").replace("#", "").replace("`", "").replace(Regex("\\n{2,}"), "\n").trim()

    private fun remember(userText: String, answer: String) {
        synchronized(lock) {
            history.add("user" to userText)
            history.add("model" to answer)
            while (history.size > MAX_HISTORY_MESSAGES) history.removeAt(0)
        }
    }
}
'''

write_file(
    "app/src/main/java/com/example/voiceassistant/data/AiChatService.kt",
    AI_SERVICE_TEMPLATE.replace("__GEMINI_API_KEY__", GEMINI_KEY)
)

# 18. app/src/main/java/com/example/voiceassistant/speech/SpeechRecognizerManager.kt
write_file("app/src/main/java/com/example/voiceassistant/speech/SpeechRecognizerManager.kt", r'''package com.example.voiceassistant.speech

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer

/**
 * Thin wrapper around [SpeechRecognizer]. Must be used from the main thread.
 * A fresh recognizer is created for every session, which is the most robust approach.
 */
class SpeechRecognizerManager(context: Context) {

    interface Listener {
        fun onReady()
        fun onPartial(text: String)
        fun onResult(text: String)
        fun onError(code: Int)
        fun onEnd()
    }

    private val appContext = context.applicationContext
    private var recognizer: SpeechRecognizer? = null

    var listener: Listener? = null

    fun isAvailable(): Boolean = SpeechRecognizer.isRecognitionAvailable(appContext)

    fun start(languageTag: String) {
        destroy()
        val created = SpeechRecognizer.createSpeechRecognizer(appContext)
        created.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) {
                listener?.onReady()
            }

            override fun onBeginningOfSpeech() {}

            override fun onRmsChanged(rmsdB: Float) {}

            override fun onBufferReceived(buffer: ByteArray?) {}

            override fun onEndOfSpeech() {
                listener?.onEnd()
            }

            override fun onError(error: Int) {
                listener?.onError(error)
            }

            override fun onResults(results: Bundle?) {
                val text = results
                    ?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    ?.firstOrNull()
                    .orEmpty()
                listener?.onResult(text)
            }

            override fun onPartialResults(partialResults: Bundle?) {
                val text = partialResults
                    ?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    ?.firstOrNull()
                    .orEmpty()
                if (text.isNotBlank()) listener?.onPartial(text)
            }

            override fun onEvent(eventType: Int, params: Bundle?) {}
        })
        recognizer = created

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, languageTag)
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
            putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, appContext.packageName)
        }
        created.startListening(intent)
    }

    /** Stops listening and lets the recognizer deliver what it heard so far. */
    fun stop() {
        recognizer?.stopListening()
    }

    /** Aborts the current session without delivering results. */
    fun cancel() {
        recognizer?.cancel()
    }

    fun destroy() {
        recognizer?.destroy()
        recognizer = null
    }
}
''')

# 19. app/src/main/java/com/example/voiceassistant/speech/TextToSpeechManager.kt
write_file("app/src/main/java/com/example/voiceassistant/speech/TextToSpeechManager.kt", r'''package com.example.voiceassistant.speech

import android.content.Context
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import java.util.Locale

class TextToSpeechManager(context: Context) {

    /** Called (possibly from a background thread) when speaking starts or stops. */
    var onSpeakingChanged: ((Boolean) -> Unit)? = null

    @Volatile
    private var ready = false
    @Volatile
    private var pendingSpeech: Pair<String, Locale>? = null
    private var counter = 0
    private var engine: TextToSpeech? = null

    private val progressListener = object : UtteranceProgressListener() {
        override fun onStart(utteranceId: String?) {
            onSpeakingChanged?.invoke(true)
        }

        override fun onDone(utteranceId: String?) {
            onSpeakingChanged?.invoke(false)
        }

        @Deprecated("Deprecated in Java")
        override fun onError(utteranceId: String?) {
            onSpeakingChanged?.invoke(false)
        }

        override fun onError(utteranceId: String?, errorCode: Int) {
            onSpeakingChanged?.invoke(false)
        }

        override fun onStop(utteranceId: String?, interrupted: Boolean) {
            onSpeakingChanged?.invoke(false)
        }
    }

    init {
        engine = TextToSpeech(context.applicationContext) { status ->
            if (status == TextToSpeech.SUCCESS) {
                engine?.setOnUtteranceProgressListener(progressListener)
                ready = true
                // A sentence requested before the engine was ready (e.g. the welcome greeting).
                pendingSpeech?.let { p ->
                    pendingSpeech = null
                    speak(p.first, p.second)
                }
            }
        }
    }

    /** @return true if speaking was started, false if TTS isn't ready or the language is unsupported. */
    fun speak(text: String, locale: Locale): Boolean {
        val tts = engine
        if (!ready || tts == null || text.isBlank()) return false
        val result = tts.setLanguage(locale)
        if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
            return false
        }
        // TextToSpeech rejects input longer than its maximum (usually 4000 characters).
        val safeText = text.take(TextToSpeech.getMaxSpeechInputLength() - 1)
        counter += 1
        return tts.speak(safeText, TextToSpeech.QUEUE_FLUSH, null, "va-$counter") == TextToSpeech.SUCCESS
    }

    /** Speaks now if the engine is ready, otherwise as soon as it becomes ready. */
    fun speakWhenReady(text: String, locale: Locale) {
        if (ready) {
            speak(text, locale)
        } else {
            pendingSpeech = text to locale
        }
    }

    fun stop() {
        pendingSpeech = null
        engine?.stop()
    }

    fun shutdown() {
        engine?.stop()
        engine?.shutdown()
        engine = null
        ready = false
    }
}
''')

# 20. app/src/main/java/com/example/voiceassistant/speech/AudioPermissionHandler.kt
write_file("app/src/main/java/com/example/voiceassistant/speech/AudioPermissionHandler.kt", r'''package com.example.voiceassistant.speech

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat

object AudioPermissionHandler {
    const val PERMISSION = Manifest.permission.RECORD_AUDIO

    fun hasPermission(context: Context): Boolean =
        ContextCompat.checkSelfPermission(context, PERMISSION) == PackageManager.PERMISSION_GRANTED
}

/**
 * Returns a function that makes sure RECORD_AUDIO is granted.
 * If it already is, [onGranted] runs immediately; otherwise the system dialog is shown first.
 */
@Composable
fun rememberAudioPermissionRequest(
    onGranted: () -> Unit,
    onDenied: () -> Unit = {}
): () -> Unit {
    val context = LocalContext.current
    val currentOnGranted by rememberUpdatedState(onGranted)
    val currentOnDenied by rememberUpdatedState(onDenied)

    val launcher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) currentOnGranted() else currentOnDenied()
    }

    return remember(context, launcher) {
        {
            if (AudioPermissionHandler.hasPermission(context)) {
                currentOnGranted()
            } else {
                launcher.launch(AudioPermissionHandler.PERMISSION)
            }
        }
    }
}
''')

# 21. app/src/main/java/com/example/voiceassistant/viewmodel/MainUiState.kt
write_file("app/src/main/java/com/example/voiceassistant/viewmodel/MainUiState.kt", r'''package com.example.voiceassistant.viewmodel

import com.example.voiceassistant.data.models.Message
import java.util.Locale

enum class AppLanguage(val tag: String, val locale: Locale, val label: String) {
    ARABIC("ar-SA", Locale.forLanguageTag("ar"), "العربية"),
    ENGLISH("en-US", Locale.US, "English");

    /** Picks the Arabic or English variant of a string. */
    fun tr(ar: String, en: String): String = if (this == ARABIC) ar else en

    companion object {
        /** Arabic if the text contains Arabic letters, English otherwise. */
        fun detect(text: String): AppLanguage =
            if (text.any { it in '\u0600'..'\u06FF' }) ARABIC else ENGLISH
    }
}

enum class AssistantStatus { IDLE, LISTENING, PROCESSING, SPEAKING, ERROR }

data class MainUiState(
    val messages: List<Message> = emptyList(),
    val status: AssistantStatus = AssistantStatus.IDLE,
    val partialText: String = "",
    val language: AppLanguage = AppLanguage.ARABIC,
    val errorMessage: String? = null,
    /** A runtime permission the UI should request right now (null = none). */
    val pendingPermission: String? = null,
    val isAccessibilityEnabled: Boolean = false,
    /** Continuous conversation: listen again automatically after the assistant finishes speaking. */
    val handsFree: Boolean = true,
    /** Name of the code file being read / edited right now (null = none). */
    val workingFileName: String? = null
)
''')

# 22. app/src/main/java/com/example/voiceassistant/viewmodel/MainViewModel.kt
write_file("app/src/main/java/com/example/voiceassistant/viewmodel/MainViewModel.kt", r'''package com.example.voiceassistant.viewmodel

import android.app.Application
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.os.Build
import android.speech.SpeechRecognizer
import java.io.File
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.voiceassistant.VoiceAssistantApp
import com.example.voiceassistant.commands.CommandParser
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.IntentCommandHandler
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.SecurityAction
import com.example.voiceassistant.data.AiChatService
import com.example.voiceassistant.data.models.CodeBlock
import com.example.voiceassistant.data.AiError
import com.example.voiceassistant.data.AiResult
import com.example.voiceassistant.data.ImageResult
import com.example.voiceassistant.data.ChatHistoryManager
import com.example.voiceassistant.data.SavedSession
import com.example.voiceassistant.data.ConversationRepository
import com.example.voiceassistant.service.ProactiveMessages
import com.example.voiceassistant.service.ProactiveScheduler
import com.example.voiceassistant.service.SecurityMonitorService
import com.example.voiceassistant.service.VoiceAccessibilityService
import com.example.voiceassistant.speech.SpeechRecognizerManager
import com.example.voiceassistant.speech.TextToSpeechManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.withContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.getAndUpdate
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private companion object {
        /** Delay between the end of the assistant's speech and the next listening session. */
        const val RESTART_DELAY_MS = 1000L

        /** After this many silent listening sessions in a row the hands-free loop stops. */
        const val MAX_SILENT_STRIKES = 3
    }

    private val repository: ConversationRepository =
        (application as VoiceAssistantApp).conversationRepository
    private val speech = SpeechRecognizerManager(application)
    private val tts = TextToSpeechManager(application)
    private val parser = CommandParser()
    private val handler = IntentCommandHandler(application)
    private val ai = AiChatService()
    private val historyManager = ChatHistoryManager(application)

    private val _savedSessions = MutableStateFlow(historyManager.getAllSessions())
    val savedSessions: StateFlow<List<SavedSession>> = _savedSessions.asStateFlow()

    /** Id of the saved session currently shown on screen (null = a fresh, never-saved chat). */
    private var currentSessionId: Long? = null

    /** True while the security monitor service is running. */
    val securityEnabled: StateFlow<Boolean> = SecurityMonitorService.running

    private val _uiState = MutableStateFlow(
        MainUiState(
            isAccessibilityEnabled = VoiceAccessibilityService.isRunning,
            language = ProactiveScheduler.language(application)
        )
    )
    val uiState: StateFlow<MainUiState> = _uiState.asStateFlow()

    /** Emitted when the UI should move the app to the background (so on-screen actions hit other apps). */
    private val _backgroundRequests = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val backgroundRequests: SharedFlow<Unit> = _backgroundRequests.asSharedFlow()

    private var pendingText: String? = null
    private var pendingSpeak = true

    // Continuous conversation state
    @Volatile
    private var conversationActive = false

    @Volatile
    private var isForeground = false
    private var silentStrikes = 0

    @Volatile
    private var restartJob: Job? = null

    init {
        viewModelScope.launch {
            repository.messages.collect { list ->
                _uiState.update { it.copy(messages = list) }
            }
        }

        tts.onSpeakingChanged = { speaking ->
            val previous = _uiState.getAndUpdate { s ->
                when {
                    speaking -> s.copy(status = AssistantStatus.SPEAKING)
                    s.status == AssistantStatus.SPEAKING -> s.copy(status = AssistantStatus.IDLE)
                    else -> s
                }
            }
            // The assistant just finished talking -> maybe listen again in a second.
            if (!speaking && previous.status == AssistantStatus.SPEAKING) {
                scheduleAutoRestart()
            }
        }

        speech.listener = object : SpeechRecognizerManager.Listener {
            override fun onReady() {
                _uiState.update { it.copy(status = AssistantStatus.LISTENING) }
            }

            override fun onPartial(text: String) {
                _uiState.update { it.copy(partialText = text) }
            }

            override fun onResult(text: String) {
                handleUtterance(text)
            }

            override fun onError(code: Int) {
                handleRecognizerError(code)
            }

            override fun onEnd() {
                _uiState.update {
                    if (it.status == AssistantStatus.LISTENING) {
                        it.copy(status = AssistantStatus.PROCESSING)
                    } else it
                }
            }
        }

        if (repository.messages.value.isEmpty()) {
            repository.addAssistantMessage(
                _uiState.value.language.tr(
                    "مرحباً! اضغط على الميكروفون وتحدث. جرّب: «اتصل بأحمد» أو «شغل الواي فاي» أو اسألني أي سؤال.",
                    "Hi! Tap the mic and speak. Try: \"call Ahmed\", \"turn on Wi-Fi\" or just ask me anything."
                )
            )
        }
    }

    init {
        greetOnStart()
    }

    /** Spoken welcome when the app opens: good morning / good evening + "how are you?". */
    private fun greetOnStart() {
        val lang = _uiState.value.language
        val greeting = ProactiveMessages.greeting(lang)
        // Fresh conversation: also show the greeting in the chat.
        if (repository.messages.value.size <= 1) {
            repository.addAssistantMessage(greeting)
        }
        tts.speakWhenReady(greeting, lang.locale)
    }

    // ------------------------------------------------------------------ UI actions

    fun toggleListening() {
        when (_uiState.value.status) {
            AssistantStatus.LISTENING -> speech.stop()
            AssistantStatus.SPEAKING -> {
                // Tapping while the assistant talks interrupts it and ends the hands-free loop.
                conversationActive = false
                restartJob?.cancel()
                tts.stop()
                _uiState.update { it.copy(status = AssistantStatus.IDLE) }
            }
            AssistantStatus.PROCESSING -> Unit
            else -> {
                conversationActive = true
                silentStrikes = 0
                startListening()
            }
        }
    }

    /** Called when the app is opened as the default assistant (after the mic permission is granted). */
    fun startHandsFree() {
        conversationActive = true
        silentStrikes = 0
        val status = _uiState.value.status
        if (status == AssistantStatus.IDLE || status == AssistantStatus.ERROR) {
            startListening()
        }
    }

    fun setHandsFree(enabled: Boolean) {
        _uiState.update { it.copy(handsFree = enabled) }
        if (!enabled) {
            conversationActive = false
            restartJob?.cancel()
        }
    }

    fun setForeground(foreground: Boolean) {
        isForeground = foreground
        if (!foreground) {
            restartJob?.cancel()
            // Android blocks microphone capture for background apps, so don't keep listening.
            if (_uiState.value.status == AssistantStatus.LISTENING) {
                speech.cancel()
                _uiState.update { it.copy(status = AssistantStatus.IDLE, partialText = "") }
            }
        }
    }

    fun setLanguage(language: AppLanguage) {
        _uiState.update { it.copy(language = language) }
        // Background check-ins use the same language.
        ProactiveScheduler.saveLanguage(getApplication<Application>(), language)
    }

    fun clearConversation() {
        conversationActive = false
        restartJob?.cancel()
        tts.stop()
        speech.cancel()
        ai.clearHistory()
        ai.workingFile = null
        repository.clear()
        currentSessionId = null
        _uiState.update { it.copy(status = AssistantStatus.IDLE, partialText = "", errorMessage = null, workingFileName = null) }
    }

    /** Saves the conversation on screen (only if the user wrote something) and refreshes the list. */
    private fun saveCurrentSession() {
        val messages = repository.messages.value
        if (messages.none { it.isUser }) return
        currentSessionId = historyManager.saveSession(sessionTitle(messages), messages, currentSessionId)
        _savedSessions.value = historyManager.getAllSessions()
    }

    private fun sessionTitle(messages: List<com.example.voiceassistant.data.models.Message>): String {
        val source = messages.firstOrNull { it.isUser && it.text.isNotBlank() }
            ?: messages.firstOrNull { it.text.isNotBlank() }
        val line = source?.text?.lineSequence()?.firstOrNull { it.isNotBlank() }?.trim().orEmpty()
        return when {
            line.isEmpty() -> _uiState.value.language.tr("محادثة جديدة", "New chat")
            line.length > 40 -> line.take(40) + "…"
            else -> line
        }
    }

    /** Stops speech / listening and resets the AI context so chats never mix. */
    private fun resetForOtherChat() {
        conversationActive = false
        restartJob?.cancel()
        tts.stop()
        speech.cancel()
        ai.clearHistory()
        ai.workingFile = null
        _uiState.update { it.copy(status = AssistantStatus.IDLE, partialText = "", errorMessage = null, workingFileName = null) }
    }

    fun startNewChat() {
        saveCurrentSession()
        resetForOtherChat()
        repository.clear()
        currentSessionId = null
    }

    fun loadSession(id: Long) {
        saveCurrentSession()
        val session = historyManager.getAllSessions().firstOrNull { it.id == id } ?: return
        val messages = ChatHistoryManager.parseMessages(session.messagesJson)
        resetForOtherChat()
        repository.setMessages(messages)
        currentSessionId = id
    }

    fun deleteSession(id: Long) {
        historyManager.deleteSession(id)
        if (currentSessionId == id) currentSessionId = null
        _savedSessions.value = historyManager.getAllSessions()
    }

    fun toggleSecurityMonitoring(enabled: Boolean) {
        if (!setSecurityMonitoring(enabled)) {
            setError(
                _uiState.value.language.tr("تعذّر تشغيل الحماية.", "Couldn't turn protection on.")
            )
        }
    }

    fun scanInstalledApps() {
        viewModelScope.launch { runAppScan(_uiState.value.language, speak = true) }
    }

    private fun setSecurityMonitoring(enabled: Boolean): Boolean = try {
        val app = getApplication<Application>()
        if (enabled) SecurityMonitorService.start(app) else SecurityMonitorService.stop(app)
        true
    } catch (e: Exception) {
        false
    }

    private suspend fun handleSecurityCommand(
        command: ParsedCommand.Security,
        lang: AppLanguage,
        speak: Boolean
    ) {
        when (command.action) {
            SecurityAction.ENABLE -> {
                val started = setSecurityMonitoring(true)
                reply(
                    if (started) {
                        lang.tr("تم تشغيل الحماية.", "Protection is on.")
                    } else {
                        lang.tr("تعذّر تشغيل الحماية.", "Couldn't turn protection on.")
                    },
                    lang,
                    speak = speak
                )
            }
            SecurityAction.DISABLE -> {
                setSecurityMonitoring(false)
                reply(lang.tr("تم إيقاف الحماية.", "Protection is off."), lang, speak = speak)
            }
            SecurityAction.SCAN_APPS -> runAppScan(lang, speak)
        }
    }

    private suspend fun runAppScan(lang: AppLanguage, speak: Boolean) {
        val suspicious = withContext(Dispatchers.IO) { findSuspiciousApps() }
        val message = if (suspicious.isEmpty()) {
            lang.tr(
                "تم فحص التطبيقات. لم يتم اكتشاف أي تطبيق مشبوه.",
                "Apps scanned. No suspicious apps were found."
            )
        } else {
            val names = suspicious.take(3).joinToString(lang.tr("، ", ", "))
            lang.tr(
                "تم فحص التطبيقات. تم اكتشاف ${suspicious.size} تطبيق مشبوه: $names",
                "Apps scanned. Found ${suspicious.size} suspicious app(s): $names"
            )
        }
        reply(message, lang, speak = speak)
    }

    /** Installed (non-system) apps that ask for INTERNET together with SMS / call-log access. */
    private fun findSuspiciousApps(): List<String> {
        val app = getApplication<Application>()
        val pm = app.packageManager
        val risky = setOf(
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_SMS",
            "android.permission.SEND_SMS",
            "android.permission.READ_CALL_LOG"
        )
        val packages = try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                pm.getInstalledPackages(
                    PackageManager.PackageInfoFlags.of(PackageManager.GET_PERMISSIONS.toLong())
                )
            } else {
                @Suppress("DEPRECATION")
                pm.getInstalledPackages(PackageManager.GET_PERMISSIONS)
            }
        } catch (e: Exception) {
            emptyList()
        }

        val found = mutableListOf<String>()
        for (info in packages) {
            val appInfo = info.applicationInfo ?: continue
            if ((appInfo.flags and ApplicationInfo.FLAG_SYSTEM) != 0) continue
            if (info.packageName == app.packageName) continue
            val permissions = info.requestedPermissions?.toSet() ?: continue
            if ("android.permission.INTERNET" in permissions && permissions.any { it in risky }) {
                found.add(pm.getApplicationLabel(appInfo).toString())
            }
        }
        return found
    }

    fun refreshAccessibilityStatus() {
        _uiState.update { it.copy(isAccessibilityEnabled = VoiceAccessibilityService.isRunning) }
    }

    fun onMicPermissionDenied() {
        conversationActive = false
        val lang = _uiState.value.language
        setError(lang.tr("أحتاج إذن الميكروفون لكي أسمعك.", "I need the microphone permission to hear you."))
    }

    fun onPermissionResult(granted: Boolean) {
        val text = pendingText
        pendingText = null
        val speak = pendingSpeak
        pendingSpeak = true
        _uiState.update { it.copy(pendingPermission = null) }
        val lang = text?.let { AppLanguage.detect(it) } ?: _uiState.value.language
        if (granted && text != null) {
            process(text, speak)
        } else {
            reply(
                lang.tr(
                    "لا أستطيع تنفيذ الأمر بدون هذا الإذن.",
                    "I can't do that without the permission."
                ),
                lang,
                speak = speak
            )
        }
    }

    // ------------------------------------------------------------------ internals

    private fun startListening() {
        restartJob?.cancel()
        val lang = _uiState.value.language
        if (!speech.isAvailable()) {
            conversationActive = false
            setError(
                lang.tr(
                    "خدمة التعرف على الصوت غير متوفرة على هذا الجهاز.",
                    "Speech recognition isn't available on this device."
                )
            )
            return
        }
        tts.stop()
        _uiState.update {
            it.copy(status = AssistantStatus.LISTENING, partialText = "", errorMessage = null)
        }
        speech.start(lang.tag)
    }

    /**
     * Hands-free loop: one second after the assistant stops speaking (or after a silent
     * session) the microphone is started again, as long as the loop is still active.
     */
    private fun scheduleAutoRestart() {
        if (!conversationActive || !_uiState.value.handsFree) return
        restartJob?.cancel()
        restartJob = viewModelScope.launch {
            delay(RESTART_DELAY_MS)
            val s = _uiState.value
            if (conversationActive &&
                s.handsFree &&
                isForeground &&
                s.status == AssistantStatus.IDLE &&
                s.pendingPermission == null
            ) {
                startListening()
            }
        }
    }

    private fun handleUtterance(text: String) {
        val clean = text.trim()
        if (clean.isEmpty()) {
            onSilence(_uiState.value.language)
            return
        }
        silentStrikes = 0
        repository.addUserMessage(clean)
        // The user spoke -> the assistant answers out loud.
        process(clean, speak = true)
    }

    /** Nothing was heard. Keep the loop going a few times, then give up politely. */
    private fun onSilence(lang: AppLanguage) {
        val s = _uiState.value
        if (conversationActive && s.handsFree) {
            silentStrikes++
            if (silentStrikes < MAX_SILENT_STRIKES) {
                _uiState.update { it.copy(status = AssistantStatus.IDLE, partialText = "") }
                scheduleAutoRestart()
                return
            }
        }
        conversationActive = false
        silentStrikes = 0
        setError(lang.tr("لم أسمعك جيداً، حاول مرة أخرى.", "I didn't catch that, please try again."))
    }

    private fun process(text: String, speak: Boolean = true) {
        viewModelScope.launch {
            _uiState.update { it.copy(status = AssistantStatus.PROCESSING, partialText = "") }
            val lang = AppLanguage.detect(text)
            val parsed = parser.parse(text)

            // Not a phone command -> have a normal conversation with the AI.
            if (parsed is ParsedCommand.Unknown) {
                if (isImageRequest(text)) generateImage(text, lang, speak) else askAi(text, lang, speak)
                return@launch
            }

            if (parsed is ParsedCommand.Security) {
                handleSecurityCommand(parsed, lang, speak)
                return@launch
            }

            // Screen actions must hit the *other* app, so step aside first.
            if (parsed is ParsedCommand.Accessibility &&
                parsed.action.targetsOtherApp &&
                VoiceAccessibilityService.isRunning
            ) {
                _backgroundRequests.tryEmit(Unit)
                delay(700)
            }

            when (val result = handler.execute(parsed, lang)) {
                is CommandResult.Success -> reply(result.message, lang, speak = speak)
                is CommandResult.Failure -> reply(result.message, lang, speak = speak)
                is CommandResult.NeedsPermission -> {
                    pendingText = text
                    pendingSpeak = speak
                    _uiState.update { it.copy(pendingPermission = result.permission) }
                    reply(result.message, lang, speak = speak)
                }
            }
        }
    }

    private suspend fun askAi(text: String, lang: AppLanguage, speak: Boolean = true) {
        when (val result = ai.ask(text, lang)) {
            is AiResult.Success -> reply(result.text, lang, result.code, speak = speak)
            is AiResult.Error -> {
                // Configuration problems won't fix themselves, so stop the hands-free loop.
                if (result.kind == AiError.NOT_CONFIGURED || result.kind == AiError.BAD_KEY) {
                    conversationActive = false
                }
                replyAiError(result.kind, result.detail, lang, speak)
            }
        }
    }

    /** True when the user asks for a picture ("ارسم لي ...", "generate an image of ..."). */
    private fun isImageRequest(text: String): Boolean {
        val t = text.lowercase()
        // Code / file requests that merely mention a picture stay normal AI answers.
        val codeWords = Regex("(html|css|javascript|java|kotlin|python|setup|script|code|كود|أكواد|اكواد|برمجة|سكربت|صفحة|موقع|ملف|تطبيق)")
        if (codeWords.containsMatchIn(t)) return false
        val arabic = Regex("(ارسم|ارسمي|صمم|ولد|أنشئ|انشئ|اصنع|اعمل|أنتج|انتج|سوي|توليد|رسم).{0,30}(صورة|صوره|صور|لوحة|رسمة|رسمه|شعار|لوجو)")
        val english = Regex("(generate|create|draw|make|paint|design|produce).{0,30}(image|picture|photo|drawing|illustration|logo|painting)")
        val drawStart = Regex("^\\s*(ارسم|ارسمي|draw)\\s")
        return arabic.containsMatchIn(t) || english.containsMatchIn(t) || drawStart.containsMatchIn(t)
    }

    private suspend fun generateImage(prompt: String, lang: AppLanguage, speak: Boolean = true) {
        when (val result = ai.generateImage(prompt)) {
            is ImageResult.Success -> {
                val path = withContext(Dispatchers.IO) { saveImage(result.bytes) }
                if (path == null) {
                    reply(aiErrorMessage(AiError.OTHER, lang), lang, speak = speak)
                } else {
                    reply(lang.tr("تفضل، هذه هي الصورة.", "Here is your image."), lang, imagePath = path, speak = speak)
                }
            }
            is ImageResult.Error -> {
                if (result.kind == AiError.NOT_CONFIGURED || result.kind == AiError.BAD_KEY) {
                    conversationActive = false
                }
                replyAiError(result.kind, result.detail, lang, speak)
            }
        }
    }

    /** Speaks the friendly message and also prints the technical detail (not spoken) so the real cause is visible. */
    private fun replyAiError(kind: AiError, detail: String, lang: AppLanguage, speak: Boolean = true) {
        reply(aiErrorMessage(kind, lang), lang, speak = speak)
        if (detail.isNotBlank()) repository.addAssistantMessage("[$detail]")
    }

    private fun saveImage(bytes: ByteArray): String? = try {
        val dir = File(getApplication<Application>().filesDir, "images").apply { mkdirs() }
        val file = File(dir, "img_${System.currentTimeMillis()}.png")
        file.writeBytes(bytes)
        file.absolutePath
    } catch (e: Exception) {
        null
    }

    private fun aiErrorMessage(kind: AiError, lang: AppLanguage): String = when (kind) {
        AiError.NOT_CONFIGURED -> lang.tr(
            "لم يتم ضبط مفتاح الذكاء الاصطناعي. ضع مفتاحك في الملف AiChatService.kt.",
            "The AI key isn't set. Put your key in AiChatService.kt."
        )
        AiError.BAD_KEY -> lang.tr(
            "مفتاح الذكاء الاصطناعي غير صالح.",
            "The AI key is not valid."
        )
        AiError.RATE_LIMIT -> lang.tr(
            "تجاوزت حد الطلبات، حاول بعد قليل.",
            "Too many requests, please try again shortly."
        )
        AiError.NETWORK -> lang.tr(
            "تعذّر الاتصال بالإنترنت.",
            "I couldn't reach the internet."
        )
        AiError.EMPTY -> lang.tr(
            "لم أستطع الإجابة على ذلك.",
            "I couldn't come up with an answer."
        )
        AiError.OTHER -> lang.tr(
            "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي.",
            "Something went wrong while contacting the AI."
        )
    }

    private fun reply(
        message: String,
        lang: AppLanguage,
        code: List<CodeBlock> = emptyList(),
        imagePath: String? = null,
        speak: Boolean = true
    ) {
        repository.addAssistantMessage(message, code, imagePath)
        // Typed requests are answered silently (the user reads the text); spoken requests are answered out loud.
        val speaking = speak && tts.speak(message, lang.locale)
        _uiState.update {
            it.copy(
                status = if (speaking) AssistantStatus.SPEAKING else AssistantStatus.IDLE,
                partialText = ""
            )
        }
        // If a spoken reply produced no speech there is no "finished speaking" event, so schedule the restart now.
        // A silent (typed) reply never restarts the microphone on its own.
        if (speak && !speaking) scheduleAutoRestart()
    }

    private fun handleRecognizerError(code: Int) {
        val lang = _uiState.value.language
        when (code) {
            SpeechRecognizer.ERROR_CLIENT -> {
                // we cancelled it ourselves
                _uiState.update { it.copy(status = AssistantStatus.IDLE, partialText = "") }
            }
            SpeechRecognizer.ERROR_NO_MATCH,
            SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> onSilence(lang)
            else -> {
                conversationActive = false
                val message = when (code) {
                    SpeechRecognizer.ERROR_NETWORK,
                    SpeechRecognizer.ERROR_NETWORK_TIMEOUT ->
                        lang.tr("مشكلة في الاتصال بالإنترنت.", "There's a network problem.")
                    SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS ->
                        lang.tr("أحتاج إذن الميكروفون.", "Microphone permission is required.")
                    SpeechRecognizer.ERROR_RECOGNIZER_BUSY ->
                        lang.tr("خدمة التعرف مشغولة، حاول بعد قليل.", "The recognizer is busy, try again shortly.")
                    else ->
                        lang.tr("تعذّر التعرف على الصوت.", "Speech recognition failed.")
                }
                setError(message)
            }
        }
    }

    private fun setError(message: String) {
        _uiState.update {
            it.copy(status = AssistantStatus.ERROR, partialText = "", errorMessage = message)
        }
    }

    override fun onCleared() {
        conversationActive = false
        restartJob?.cancel()
        speech.destroy()
        tts.shutdown()
        super.onCleared()
    }
}
''')

# 23. app/src/main/java/com/example/voiceassistant/service/VoiceAccessibilityService.kt
write_file("app/src/main/java/com/example/voiceassistant/service/VoiceAccessibilityService.kt", r'''package com.example.voiceassistant.service

import android.accessibilityservice.AccessibilityService
import android.content.Intent
import android.os.Build
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.example.voiceassistant.commands.TextNormalizer
import com.example.voiceassistant.commands.commands.AccessibilityAction

/** Result of trying to flip a switch / toggle by its name. */
enum class ToggleResult { SUCCESS, ALREADY_IN_STATE, NOT_FOUND, FAILED }

class VoiceAccessibilityService : AccessibilityService() {

    companion object {
        @Volatile
        var instance: VoiceAccessibilityService? = null
            private set

        val isRunning: Boolean
            get() = instance != null

        private const val MAX_DEPTH = 40
        private const val MAX_ANCESTOR_LEVELS = 4
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
    }

    override fun onUnbind(intent: Intent?): Boolean {
        instance = null
        return super.onUnbind(intent)
    }

    override fun onDestroy() {
        instance = null
        super.onDestroy()
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // Not needed: this service only performs actions on demand.
    }

    override fun onInterrupt() {}

    /** Executes a voice-requested screen action. Returns true on success. */
    fun execute(action: AccessibilityAction, argument: String?): Boolean = when (action) {
        AccessibilityAction.BACK -> performGlobalAction(GLOBAL_ACTION_BACK)
        AccessibilityAction.HOME -> performGlobalAction(GLOBAL_ACTION_HOME)
        AccessibilityAction.RECENTS -> performGlobalAction(GLOBAL_ACTION_RECENTS)
        AccessibilityAction.NOTIFICATIONS -> performGlobalAction(GLOBAL_ACTION_NOTIFICATIONS)
        AccessibilityAction.QUICK_SETTINGS -> performGlobalAction(GLOBAL_ACTION_QUICK_SETTINGS)
        AccessibilityAction.SCREENSHOT ->
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                performGlobalAction(GLOBAL_ACTION_TAKE_SCREENSHOT)
            } else false
        AccessibilityAction.LOCK_SCREEN ->
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                performGlobalAction(GLOBAL_ACTION_LOCK_SCREEN)
            } else false
        AccessibilityAction.SCROLL_DOWN -> scroll(forward = true)
        AccessibilityAction.SCROLL_UP -> scroll(forward = false)
        AccessibilityAction.CLICK_TEXT -> argument?.let { clickByText(it) } ?: false
    }

    // ------------------------------------------------------------------ switches / toggles

    /**
     * Finds a Switch / Toggle / checkable item whose label matches one of [names]
     * (for example "Wi-Fi" or "Bluetooth") on the current screen and clicks it.
     *
     * @param enable true = make sure it is ON, false = make sure it is OFF, null = just flip it.
     */
    fun setToggleByName(names: List<String>, enable: Boolean?): ToggleResult {
        val root = rootInActiveWindow ?: return ToggleResult.NOT_FOUND
        val targets = names
            .map { TextNormalizer.key(TextNormalizer.light(it)) }
            .filter { it.isNotEmpty() }
        if (targets.isEmpty()) return ToggleResult.NOT_FOUND

        val switches = ArrayList<AccessibilityNodeInfo>()
        collectCheckables(root, switches, 0)

        var best: AccessibilityNodeInfo? = null
        var bestScore = -1
        for (candidate in switches) {
            val score = matchScore(candidate, targets)
            if (score > bestScore) {
                bestScore = score
                best = candidate
            }
        }

        val node = best ?: return ToggleResult.NOT_FOUND
        if (enable != null && node.isChecked == enable) return ToggleResult.ALREADY_IN_STATE
        return if (clickNodeOrAncestor(node)) ToggleResult.SUCCESS else ToggleResult.FAILED
    }

    private fun collectCheckables(
        node: AccessibilityNodeInfo,
        out: MutableList<AccessibilityNodeInfo>,
        depth: Int
    ) {
        if (depth > MAX_DEPTH) return
        if (node.isCheckable) out.add(node)
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            collectCheckables(child, out, depth + 1)
        }
    }

    private fun countCheckables(node: AccessibilityNodeInfo, depth: Int = 0): Int {
        if (depth > MAX_DEPTH) return 0
        var count = if (node.isCheckable) 1 else 0
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            count += countCheckables(child, depth + 1)
        }
        return count
    }

    private fun collectTexts(node: AccessibilityNodeInfo, sb: StringBuilder, depth: Int) {
        if (depth > MAX_DEPTH) return
        node.text?.let { sb.append(it).append(' ') }
        node.contentDescription?.let { sb.append(it).append(' ') }
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            collectTexts(child, sb, depth + 1)
        }
    }

    /**
     * Climbs from the switch to its row (at most a few levels, and never into a container that
     * holds other switches) and checks whether the row's text contains one of the names.
     * Closer matches and shorter labels score higher. Returns -1 when nothing matches.
     */
    private fun matchScore(switchNode: AccessibilityNodeInfo, targets: List<String>): Int {
        var current: AccessibilityNodeInfo? = switchNode
        var level = 0
        while (current != null && level <= MAX_ANCESTOR_LEVELS) {
            if (countCheckables(current) > 1) break
            val sb = StringBuilder()
            collectTexts(current, sb, 0)
            val label = TextNormalizer.key(TextNormalizer.light(sb.toString()))
            if (label.isNotEmpty() && targets.any { label.contains(it) }) {
                return 1000 - level * 100 - minOf(label.length, 99)
            }
            current = current.parent
            level++
        }
        return -1
    }

    private fun clickNodeOrAncestor(node: AccessibilityNodeInfo): Boolean {
        var current: AccessibilityNodeInfo? = node
        var level = 0
        while (current != null && level <= MAX_ANCESTOR_LEVELS) {
            if (current.isClickable && current.isEnabled) {
                return current.performAction(AccessibilityNodeInfo.ACTION_CLICK)
            }
            current = current.parent
            level++
        }
        return false
    }

    // ------------------------------------------------------------------ scroll / click by text

    private fun scroll(forward: Boolean): Boolean {
        val root = rootInActiveWindow ?: return false
        val node = findScrollable(root) ?: return false
        val action = if (forward) {
            AccessibilityNodeInfo.ACTION_SCROLL_FORWARD
        } else {
            AccessibilityNodeInfo.ACTION_SCROLL_BACKWARD
        }
        return node.performAction(action)
    }

    private fun findScrollable(node: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        if (node.isScrollable) return node
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            val found = findScrollable(child)
            if (found != null) return found
        }
        return null
    }

    private fun clickByText(text: String): Boolean {
        val root = rootInActiveWindow ?: return false
        val matches = root.findAccessibilityNodeInfosByText(text)
        for (match in matches) {
            var current: AccessibilityNodeInfo? = match
            while (current != null) {
                if (current.isClickable && current.isEnabled) {
                    return current.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                }
                current = current.parent
            }
        }
        return false
    }
}
''')

# 23b. app/src/main/java/com/example/voiceassistant/service/AssistantSession.kt  (NEW)
write_file("app/src/main/java/com/example/voiceassistant/service/AssistantSession.kt", r'''package com.example.voiceassistant.service

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.service.voice.VoiceInteractionService
import android.service.voice.VoiceInteractionSession
import android.service.voice.VoiceInteractionSessionService
import android.speech.RecognitionService
import android.speech.SpeechRecognizer
import com.example.voiceassistant.MainActivity

/**
 * Registers the app as a selectable "Digital assistant app"
 * (Settings > Apps > Default apps > Digital assistant app).
 */
class VaInteractionService : VoiceInteractionService()

/** Creates a session every time the user invokes the assistant (long-press Home, power button...). */
class VaSessionService : VoiceInteractionSessionService() {
    override fun onNewSession(args: Bundle?): VoiceInteractionSession = VaSession(this)
}

/** Opens the main screen with the "auto listen" flag so the microphone starts immediately. */
class VaSession(context: Context) : VoiceInteractionSession(context) {

    override fun onShow(args: Bundle?, showFlags: Int) {
        super.onShow(args, showFlags)

        val intent = Intent(context, MainActivity::class.java)
            .putExtra(MainActivity.EXTRA_AUTO_LISTEN, true)

        try {
            startAssistantActivity(intent)
        } catch (e: Exception) {
            try {
                intent.addFlags(
                    Intent.FLAG_ACTIVITY_NEW_TASK or
                        Intent.FLAG_ACTIVITY_CLEAR_TOP or
                        Intent.FLAG_ACTIVITY_SINGLE_TOP
                )
                context.startActivity(intent)
            } catch (_: Exception) {
                // Nothing else we can do.
            }
        }
        hide()
    }
}

/**
 * Minimal recognition service required by the voice-interaction declaration.
 * The app itself uses the system's default recognizer, so this one never recognizes anything.
 */
class VaRecognitionService : RecognitionService() {
    override fun onStartListening(recognizerIntent: Intent?, listener: Callback?) {
        listener?.error(SpeechRecognizer.ERROR_CLIENT)
    }

    override fun onCancel(listener: Callback?) {}

    override fun onStopListening(listener: Callback?) {}
}
''')

# 24. app/src/main/java/com/example/voiceassistant/commands/CommandResult.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/CommandResult.kt", r'''package com.example.voiceassistant.commands

sealed class CommandResult {
    data class Success(val message: String) : CommandResult()
    data class Failure(val message: String) : CommandResult()

    /** The command can run once the user grants [permission]; it is then re-executed. */
    data class NeedsPermission(val permission: String, val message: String) : CommandResult()
}
''')

# 25. app/src/main/java/com/example/voiceassistant/commands/CommandParser.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/CommandParser.kt", r'''package com.example.voiceassistant.commands

import com.example.voiceassistant.commands.commands.AccessibilityAction
import com.example.voiceassistant.commands.commands.InfoType
import com.example.voiceassistant.commands.commands.SettingsTarget

sealed class ParsedCommand {
    data class Call(val target: String) : ParsedCommand()
    data class Sms(val target: String, val body: String?) : ParsedCommand()

    /** [hour] == null means "just show my alarms". */
    data class Alarm(val hour: Int?, val minute: Int = 0) : ParsedCommand()
    data class WebSearch(val query: String) : ParsedCommand()

    /** [toggle]: true = turn ON, false = turn OFF, null = only open the settings page. */
    data class OpenSettings(val target: SettingsTarget, val toggle: Boolean? = null) : ParsedCommand()
    data class Accessibility(val action: AccessibilityAction, val argument: String? = null) : ParsedCommand()
    data class Info(val type: InfoType) : ParsedCommand()
    data class LaunchApp(val appName: String) : ParsedCommand()

    /** Spoken reminder; [triggerAtMillis] == null means the time could not be understood. */
    data class Reminder(val text: String, val triggerAtMillis: Long?) : ParsedCommand()

    /** Protection commands: turn the clipboard monitor on / off, or scan the installed apps. */
    data class Security(val action: SecurityAction) : ParsedCommand()
    object Unknown : ParsedCommand()
}

enum class SecurityAction { ENABLE, DISABLE, SCAN_APPS }

/** Text helpers shared by the parser and the contact / app lookups. */
object TextNormalizer {

    /** Removes Arabic diacritics/tatweel, converts Arabic-Indic digits and tidies whitespace/punctuation. */
    fun light(raw: String): String {
        val sb = StringBuilder(raw.length)
        for (ch in raw) {
            when (ch) {
                in '\u064B'..'\u065F', '\u0640', '\u0670' -> Unit
                in '\u0660'..'\u0669' -> sb.append('0' + (ch - '\u0660'))
                in '\u06F0'..'\u06F9' -> sb.append('0' + (ch - '\u06F0'))
                '\u2019' -> sb.append('\'')
                else -> sb.append(ch)
            }
        }
        return sb.toString()
            .replace(Regex("\\s+"), " ")
            .trim()
            .trimEnd('.', ',', '\u060C', '\u061F', '?', '!', '\u061B')
            .trim()
    }

    /** Same-length matching key: unifies Arabic letter variants and lower-cases Latin text. */
    fun key(text: String): String {
        val sb = StringBuilder(text.length)
        for (ch in text) {
            sb.append(
                when (ch) {
                    '\u0623', '\u0625', '\u0622', '\u0671' -> '\u0627' // أ إ آ ٱ -> ا
                    '\u0649' -> '\u064A'                               // ى -> ي
                    '\u0629' -> '\u0647'                               // ة -> ه
                    else -> ch.lowercaseChar()
                }
            )
        }
        return sb.toString()
    }
}

/**
 * Turns a spoken sentence (Arabic or English) into a [ParsedCommand].
 *
 * Patterns are written against the normalized key (see [TextNormalizer.key]):
 * أ/إ/آ -> ا, ى -> ي, ة -> ه. Captured values are taken from the original text.
 */
class CommandParser {

    internal class Prepared(val light: String) {
        val key: String = TextNormalizer.key(light)

        fun groups(regex: Regex): List<String>? {
            val m = regex.matchEntire(key) ?: return null
            return (1 until m.groups.size).map { i ->
                val g = m.groups[i]
                if (g == null) "" else light.substring(g.range.first, g.range.last + 1).trim()
            }
        }

        fun containsAny(vararg words: String): Boolean = words.any { key.contains(it) }
    }

    // ---- patterns ---------------------------------------------------------------------------
    private val smsEnBody = Regex("""^(?:please )?(?:send (?:a |an )?(?:message|sms|text)|text|message)\s+(?:to )?(.+?)\s+(?:saying|that says|says|and say|say)\s+(.+)$""")
    private val smsEn = Regex("""^(?:please )?(?:send (?:a |an )?(?:message|sms|text)|text|message)\s+(?:to )?(.+)$""")
    private val smsArBody = Regex("""^(?:ارسل|ابعث|ارسلي|ابعثي)\s+(?:رساله|رسايل|sms)\s+(?:الي\s+)?(.+?)\s+(?:تقول|نصها|مفادها|بنص|وقل|وقول|مضمونها)\s+(.+)$""")
    private val smsAr = Regex("""^(?:ارسل|ابعث|ارسلي|ابعثي)\s+(?:رساله|رسايل|sms)\s+(?:الي\s+)?(.+)$""")

    private val callEn = Regex("""^(?:please )?(?:call|dial|phone|ring)\s+(?:to )?(?:number )?(.+)$""")
    private val callAr = Regex("""^(?:اتصل|كلم|رن|اتصلي|كلمي)\s+(?:بالرقم\s+|ب\s+)?(.+)$""")

    private val timeRegex = Regex("""(\d{1,2})(?:[:.](\d{2}))?""")
    private val pmRegex = Regex("""(?<![a-z])(?:pm|p\.m\.?)(?![a-z])""")
    private val amRegex = Regex("""(?<![a-z])(?:am|a\.m\.?)(?![a-z])""")

    private val searchEn = Regex("""^(?:please )?(?:search(?: for| about)?|google|look up|lookup)\s+(.+)$""")
    private val searchAr = Regex("""^(?:ابحث|دور|فتش)(?:\s+لي)?(?:\s+في\s+(?:جوجل|قوقل|غوغل|الانترنت|النت|الويب))?(?:\s+عن)?\s+(.+)$""")
    private val searchAr2 = Regex("""^(?:جوجل|قوقل|غوغل)\s+(.+)$""")

    private val backRegex = Regex("""^(?:please )?(?:go )?back(?: button)?$|^(?:ارجع|رجوع|ارجعي|ارجع للخلف|ارجع الي الخلف|للخلف|الي الخلف|زر الرجوع|اضغط رجوع)$""")
    private val clickEn = Regex("""^(?:click|tap|press)(?: on)?\s+(.+)$""")
    private val clickAr = Regex("""^(?:اضغط|انقر|دوس)(?:\s+علي)?\s+(.+)$""")

    private val greetingEn = Regex("""^(?:hi|hello|hey|good (?:morning|afternoon|evening))(?: there| claude)?$""")
    private val greetingAr = Regex("""^(?:مرحبا|اهلا|اهلا وسهلا|السلام عليكم|صباح الخير|مساء الخير|هلا)$""")

    private val launchEn = Regex("""^(?:please )?(?:open|launch|start|run)\s+(?:the )?(?:app )?(.+?)(?: app)?$""")
    private val launchAr = Regex("""^(?:افتح|شغل|افتحي|روح الي|اذهب الي|ابدا)\s+(?:لي\s+)?(?:تطبيق\s+)?(.+)$""")

    // ---- entry point ------------------------------------------------------------------------
    fun parse(raw: String): ParsedCommand {
        val t = Prepared(TextNormalizer.light(raw))
        if (t.key.isEmpty()) return ParsedCommand.Unknown
        return parseReminder(t)
            ?: parseSms(t)
            ?: parseCall(t)
            ?: parseAlarm(t)
            ?: parseSearch(t)
            ?: parseAccessibility(t)
            ?: parseSettings(t)
            ?: parseSecurity(t)
            ?: parseInfo(t)
            ?: parseLaunch(t)
            ?: ParsedCommand.Unknown
    }

    // ---- reminders ("ذكرني بشرب الماء بعد 10 دقائق") -----------------------------------------
    private val reminderTrigger = Regex("""(?:ذكرني|ذكريني|نبهني|نبهيني|remind me|تذكير|تذكيري|اضبط لي تذكير|اضبط تذكير)""")

    private val relAr = Regex(
        """بعد\s+(?:(\d+(?:\.\d+)?)|([\u0621-\u064A]+))?\s*(ثانيه|ثواني|ثوان|دقيقه|دقيقتين|دقايق|دقائق|ساعه|ساعتين|ساعات|يوم|يومين|ايام)(?:\s+و\s*(نصف|نص|ربع))?"""
    )
    private val relEn = Regex(
        """(?<![a-z])(?:in|after)\s+(?:(\d+(?:\.\d+)?)|(an?|one|two|three|four|five|six|seven|eight|nine|ten|fifteen|twenty|thirty|forty five|forty|half an|half a|a half|quarter of an|a quarter of an))\s*(seconds?|secs?|minutes?|mins?|hours?|hrs?|days?)\b"""
    )
    private val clockPrefixed = Regex("""(?:الساعه|ساعه|(?<![a-z])at)\s*(\d{1,2})(?:[:.](\d{2}))?""")
    private val clockWordMinutes = Regex("""(?:(?:عند|في)\s+)?(?:الساعه|ساعه)\s*(\d{1,2})\s+و\s*([\u0621-\u064A]+|\d+)\s*(?:دقيقه|دقائق|دقايق)""")
    private val clockAmPm = Regex("""(\d{1,2})(?:[:.](\d{2}))?\s*(?:am|pm|a\.m\.?|p\.m\.?)(?![a-z])""")

    private val dayAfterTomorrow = Regex("""بعد\s+غد(?![\u0621-\u064A])|day after tomorrow""")
    private val dayTomorrow = Regex("""(?<![\u0621-\u064A])(?:غدا|بكره|بكرا)(?![\u0621-\u064A])|tomorrow""")
    private val dayToday = Regex("""(?<![\u0621-\u064A])اليوم(?![\u0621-\u064A])|today""")

    private val periodPm = Regex("""(?<![\u0621-\u064A])(?:مساء|عصرا|عصر|ليلا|ليل)(?![\u0621-\u064A])""")
    private val periodAm = Regex("""(?<![\u0621-\u064A])(?:صباحا|صباح|فجرا|فجر)(?![\u0621-\u064A])""")
    private val periodNoon = Regex("""(?<![\u0621-\u064A])(?:ظهرا|ظهر)(?![\u0621-\u064A])""")

    private val arNumberWords = mapOf(
        "واحد" to 1, "واحده" to 1, "اثنين" to 2, "اثنتين" to 2, "ثنتين" to 2,
        "ثلاث" to 3, "ثلاثه" to 3, "اربع" to 4, "اربعه" to 4, "خمس" to 5, "خمسه" to 5,
        "ست" to 6, "سته" to 6, "سبع" to 7, "سبعه" to 7, "ثمان" to 8, "ثمانيه" to 8,
        "تسع" to 9, "تسعه" to 9, "عشر" to 10, "عشره" to 10, "عشرين" to 20,
        "ثلاثين" to 30, "اربعين" to 40, "خمسين" to 50, "ستين" to 60
    )
    private val enNumberWords = mapOf(
        "a" to 1.0, "an" to 1.0, "one" to 1.0, "two" to 2.0, "three" to 3.0, "four" to 4.0,
        "five" to 5.0, "six" to 6.0, "seven" to 7.0, "eight" to 8.0, "nine" to 9.0, "ten" to 10.0,
        "fifteen" to 15.0, "twenty" to 20.0, "thirty" to 30.0, "forty" to 40.0, "forty five" to 45.0,
        "half an" to 0.5, "half a" to 0.5, "a half" to 0.5,
        "quarter of an" to 0.25, "a quarter of an" to 0.25
    )

    private fun unitMillis(unit: String): Long = when {
        unit.startsWith("ثان") || unit.startsWith("ثوان") || unit.startsWith("sec") -> 1_000L
        unit.startsWith("دق") || unit.startsWith("min") -> 60_000L
        unit.startsWith("ساع") || unit.startsWith("hour") || unit.startsWith("hr") -> 3_600_000L
        else -> 86_400_000L
    }

    /** Milliseconds from now for phrases like "بعد 10 دقائق" / "in half an hour"; null if none found. */
    private fun relativeDelay(key: String, ranges: MutableList<IntRange>): Long? {
        relAr.find(key)?.let { m ->
            val digits = m.groupValues[1]
            val word = m.groupValues[2]
            val unit = m.groupValues[3]
            val extra = m.groupValues[4]
            var amount = when {
                digits.isNotEmpty() -> digits.toDouble()
                word == "نصف" || word == "نص" -> 0.5
                word == "ربع" -> 0.25
                word.isNotEmpty() -> (arNumberWords[word] ?: 0).toDouble()
                unit == "ساعتين" || unit == "دقيقتين" || unit == "يومين" -> 2.0
                else -> 1.0
            }
            if (amount > 0.0) {
                when (extra) {
                    "نصف", "نص" -> amount += 0.5
                    "ربع" -> amount += 0.25
                }
                ranges.add(m.range)
                return (amount * unitMillis(unit)).toLong()
            }
        }
        relEn.find(key)?.let { m ->
            val digits = m.groupValues[1]
            val word = m.groupValues[2]
            val unit = m.groupValues[3]
            val amount = if (digits.isNotEmpty()) digits.toDouble() else (enNumberWords[word] ?: 0.0)
            if (amount > 0.0) {
                ranges.add(m.range)
                return (amount * unitMillis(unit)).toLong()
            }
        }
        return null
    }

    private fun timeOn(dayOffset: Int, hour: Int, minute: Int): Long {
        val cal = java.util.Calendar.getInstance()
        cal.add(java.util.Calendar.DAY_OF_YEAR, dayOffset)
        cal.set(java.util.Calendar.HOUR_OF_DAY, hour)
        cal.set(java.util.Calendar.MINUTE, minute)
        cal.set(java.util.Calendar.SECOND, 0)
        cal.set(java.util.Calendar.MILLISECOND, 0)
        return cal.timeInMillis
    }

    /** Absolute time like "غداً الساعة 5 مساءً" / "tomorrow at 5 pm"; null if no time of day was said. */
    private fun absoluteTime(key: String, ranges: MutableList<IntRange>): Long? {
        val dayOffset = when {
            dayAfterTomorrow.containsMatchIn(key) -> 2
            dayTomorrow.containsMatchIn(key) -> 1
            else -> 0
        }
        for (r in listOf(dayAfterTomorrow, dayTomorrow, dayToday)) {
            r.find(key)?.let { ranges.add(it.range) }
        }

        val clock = clockWordMinutes.find(key) ?: clockAmPm.find(key) ?: clockPrefixed.find(key)
        val pm = periodPm.containsMatchIn(key) || pmRegex.containsMatchIn(key)
        val am = periodAm.containsMatchIn(key) || amRegex.containsMatchIn(key)
        val noon = periodNoon.containsMatchIn(key)
        for (r in listOf(periodPm, periodAm, periodNoon, pmRegex, amRegex, clockAmPm, clockPrefixed, clockWordMinutes)) {
            r.find(key)?.let { ranges.add(it.range) }
        }

        if (clock == null) {
            // "tomorrow" alone -> 09:00; nothing at all -> unknown time
            return if (dayOffset > 0) timeOn(dayOffset, 9, 0) else null
        }

        val h0 = clock.groupValues[1].toInt()
        val minuteStr = clock.groupValues[2].ifEmpty { "0" }
        val minute = if (minuteStr.all { it.isDigit() }) minuteStr.toInt() else (arNumberWords[minuteStr] ?: 0)
        if (h0 > 23 || minute > 59) return null

        var hour = h0
        val hasPeriod = pm || am || noon
        when {
            pm && !am && hour in 1..11 -> hour += 12
            am && hour == 12 -> hour = 0
            noon && hour in 1..5 -> hour += 12
            !hasPeriod && hour in 1..6 -> hour += 12 // "at 5" most likely means 5 pm
        }

        val now = System.currentTimeMillis()
        var millis = timeOn(dayOffset, hour, minute)
        if (millis <= now) {
            if (!hasPeriod && dayOffset == 0 && h0 in 1..11) {
                // try the other half of the day before pushing to tomorrow
                val alt = timeOn(0, if (hour >= 12) h0 else h0 + 12, minute)
                millis = if (alt > now) alt else timeOn(1, hour, minute)
            } else if (dayOffset == 0) {
                millis = timeOn(1, hour, minute)
            }
        }
        return millis
    }

    private fun parseReminder(t: Prepared): ParsedCommand? {
        val trigger = reminderTrigger.find(t.key) ?: return null
        val ranges = mutableListOf(trigger.range)

        val delay = relativeDelay(t.key, ranges)
        val at = if (delay != null) System.currentTimeMillis() + delay else absoluteTime(t.key, ranges)

        // The reminder text = the sentence without the trigger and the time phrases.
        val sb = StringBuilder()
        var pos = 0
        for (r in ranges.sortedBy { it.first }) {
            if (r.first > pos) sb.append(t.light, pos, r.first)
            pos = maxOf(pos, r.last + 1)
        }
        if (pos < t.light.length) sb.append(t.light, pos, t.light.length)

        var text = sb.toString().replace(Regex("""\s+"""), " ").trim()
        text = text.replace(Regex("""^(?:please\s+|to\s+|about\s+|that\s+|of\s+|ان\s+|أن\s+|علي\s+|على\s+|عند\s+|في\s+)+""", RegexOption.IGNORE_CASE), "")
        text = text.replace(Regex("""(?:\s+(?:please|في|at|on|in|و))+$""", RegexOption.IGNORE_CASE), "").trim()
        val arabicTrigger = !trigger.value.startsWith("remind")
        if (arabicTrigger && text.length > 3 && text.startsWith("ب")) text = text.substring(1)
        text = text.trim().take(200)
        if (text.isEmpty()) {
            text = if (arabicTrigger) "التذكير" else "your reminder"
        }
        return ParsedCommand.Reminder(text, at)
    }

    // ---- individual parsers -----------------------------------------------------------------
    private fun parseSms(t: Prepared): ParsedCommand? {
        t.groups(smsEnBody)?.let { return ParsedCommand.Sms(it[0], it[1]) }
        t.groups(smsArBody)?.let { return ParsedCommand.Sms(it[0], it[1]) }
        t.groups(smsEn)?.let { return ParsedCommand.Sms(it[0], null) }
        t.groups(smsAr)?.let { return ParsedCommand.Sms(it[0], null) }
        return null
    }

    private fun parseCall(t: Prepared): ParsedCommand? {
        t.groups(callAr)?.let { return ParsedCommand.Call(it[0]) }
        t.groups(callEn)?.let { return ParsedCommand.Call(it[0]) }
        return null
    }

    private fun parseAlarm(t: Prepared): ParsedCommand? {
        if (!t.containsAny("منبه", "alarm", "wake me")) return null
        val m = timeRegex.find(t.key) ?: return ParsedCommand.Alarm(null)
        var hour = m.groupValues[1].toInt()
        val minute = m.groupValues[2].ifEmpty { "0" }.toInt()

        val pm = t.containsAny("مساء", "ليل", "عصر") || pmRegex.containsMatchIn(t.key)
        val am = t.containsAny("صباح", "فجر") || amRegex.containsMatchIn(t.key)
        val noon = t.containsAny("ظهر", "noon")
        when {
            pm && !am && hour in 1..11 -> hour += 12
            am && hour == 12 -> hour = 0
            noon && hour in 1..5 -> hour += 12
        }
        return if (hour in 0..23 && minute in 0..59) {
            ParsedCommand.Alarm(hour, minute)
        } else {
            ParsedCommand.Unknown
        }
    }

    private fun parseSearch(t: Prepared): ParsedCommand? {
        t.groups(searchAr)?.let { return ParsedCommand.WebSearch(it[0]) }
        t.groups(searchAr2)?.let { return ParsedCommand.WebSearch(it[0]) }
        t.groups(searchEn)?.let { return ParsedCommand.WebSearch(it[0]) }
        return null
    }

    private fun parseAccessibility(t: Prepared): ParsedCommand? {
        fun a(action: AccessibilityAction, arg: String? = null) =
            ParsedCommand.Accessibility(action, arg)

        val mentionsSettings = t.containsAny("اعدادات", "settings")

        val global: ParsedCommand.Accessibility? = when {
            t.containsAny("الاعدادات السريعه", "quick settings", "اللوحه السريعه") ->
                a(AccessibilityAction.QUICK_SETTINGS)
            t.containsAny("لقطه شاشه", "لقطه الشاشه", "صوره الشاشه", "سكرين شوت", "screenshot", "screen shot") ->
                a(AccessibilityAction.SCREENSHOT)
            t.containsAny("اقفل الشاشه", "قفل الشاشه", "اقفل الجهاز", "اقفل الهاتف", "lock screen", "lock the screen", "lock the phone", "lock phone") ->
                a(AccessibilityAction.LOCK_SCREEN)
            t.containsAny("التطبيقات الاخيره", "التطبيقات الحديثه", "recent apps", "recents", "app switcher") ->
                a(AccessibilityAction.RECENTS)
            !mentionsSettings && t.containsAny("الاشعارات", "notifications", "notification panel") ->
                a(AccessibilityAction.NOTIFICATIONS)
            t.containsAny("الشاشه الرئيسيه", "الصفحه الرئيسيه", "الرئيسيه", "go home", "home screen", "press home") || t.key == "home" ->
                a(AccessibilityAction.HOME)
            backRegex.matches(t.key) ->
                a(AccessibilityAction.BACK)
            t.containsAny("مرر لاسفل", "مرر للاسفل", "مرر الي الاسفل", "مرر الي تحت", "مرر لتحت", "انزل", "scroll down", "page down") ->
                a(AccessibilityAction.SCROLL_DOWN)
            t.containsAny("مرر لاعلي", "مرر للاعلي", "مرر الي الاعلي", "مرر لفوق", "مرر الي فوق", "اطلع", "scroll up", "page up") ->
                a(AccessibilityAction.SCROLL_UP)
            else -> null
        }
        if (global != null) return global

        t.groups(clickAr)?.let { return a(AccessibilityAction.CLICK_TEXT, it[0]) }
        t.groups(clickEn)?.let { return a(AccessibilityAction.CLICK_TEXT, it[0]) }
        return null
    }

    private fun parseSettings(t: Prepared): ParsedCommand? {
        val wantsSettings = t.containsAny(
            "افتح", "شغل", "فعل", "عطل", "اطفي", "اطفئ", "اوقف", "اقفل", "اغلق", "اعدادات",
            "open", "turn on", "turn off", "enable", "disable", "settings", "setting", "switch", "go to"
        )
        if (!wantsSettings) return null

        val target: SettingsTarget = when {
            t.containsAny("واي فاي", "وايفاي", "wifi", "wi-fi", "wi fi") -> SettingsTarget.WIFI
            t.containsAny("بلوتوث", "bluetooth") -> SettingsTarget.BLUETOOTH
            t.containsAny("وضع الطيران", "الطيران", "airplane", "flight mode") -> SettingsTarget.AIRPLANE
            t.containsAny("الاتاحه", "سهوله الوصول", "accessibility") -> SettingsTarget.ACCESSIBILITY
            t.containsAny("البطاريه", "battery") -> SettingsTarget.BATTERY
            t.containsAny("الصوت", "sound", "volume") -> SettingsTarget.SOUND
            t.containsAny("السطوع", "الشاشه", "brightness", "display") -> SettingsTarget.DISPLAY
            t.containsAny("الموقع", "location", "gps") -> SettingsTarget.LOCATION
            t.containsAny("اعدادات", "settings", "setting") -> SettingsTarget.MAIN
            else -> return null
        }

        // "شغل الواي فاي" / "turn off bluetooth" -> flip the switch; "افتح ..." -> only open the page.
        val turnOn = t.containsAny("شغل", "فعل", "turn on", "switch on", "enable")
        val turnOff = t.containsAny(
            "اطفي", "اطفئ", "عطل", "اوقف", "اقفل", "اغلق", "turn off", "switch off", "disable"
        )
        val toggle: Boolean? = when {
            turnOn && !turnOff -> true
            turnOff && !turnOn -> false
            else -> null
        }
        return ParsedCommand.OpenSettings(target, toggle)
    }

    private fun parseInfo(t: Prepared): ParsedCommand? {
        val type: InfoType = when {
            greetingAr.matches(t.key) || greetingEn.matches(t.key) -> InfoType.GREETING
            t.containsAny(
                "كم الساعه", "الساعه كم", "الساعه كام", "كام الساعه", "كم الوقت", "ما الوقت",
                "ما هو الوقت", "الوقت الان", "what time", "current time", "time is it", "tell me the time"
            ) -> InfoType.TIME
            t.containsAny(
                "ما التاريخ", "تاريخ اليوم", "كم التاريخ", "ما اليوم", "اي يوم", "ايش اليوم",
                "what's the date", "whats the date", "what is the date", "today's date", "what day", "date today"
            ) -> InfoType.DATE
            t.containsAny("البطاريه", "battery", "نسبه الشحن") -> InfoType.BATTERY
            t.containsAny(
                "مساعده", "ساعدني", "ماذا يمكنك", "ماذا تستطيع", "ماذا تفعل", "من انت",
                "what can you do", "who are you"
            ) || t.key == "help" -> InfoType.HELP
            t.containsAny("شكرا", "thanks", "thank you") -> InfoType.THANKS
            else -> return null
        }
        return ParsedCommand.Info(type)
    }

    private fun parseSecurity(t: Prepared): ParsedCommand? {
        val action: SecurityAction = when {
            t.containsAny(
                "افحص التطبيقات", "فحص التطبيقات", "افحص تطبيقات",
                "scan apps", "scan my apps", "scan installed apps", "check my apps", "check installed apps"
            ) -> SecurityAction.SCAN_APPS
            t.containsAny(
                "شغل الحمايه", "فعل الحمايه", "ابدا الحمايه", "تفعيل الحمايه",
                "turn on protection", "enable protection", "start protection", "turn on security", "enable security"
            ) -> SecurityAction.ENABLE
            t.containsAny(
                "اوقف الحمايه", "عطل الحمايه", "اطفي الحمايه", "اطفئ الحمايه", "الغ الحمايه", "ايقاف الحمايه",
                "turn off protection", "disable protection", "stop protection", "turn off security", "disable security"
            ) -> SecurityAction.DISABLE
            else -> return null
        }
        return ParsedCommand.Security(action)
    }

    private fun parseLaunch(t: Prepared): ParsedCommand? {
        t.groups(launchAr)?.let { return ParsedCommand.LaunchApp(it[0]) }
        t.groups(launchEn)?.let { return ParsedCommand.LaunchApp(it[0]) }
        return null
    }
}
''')

# 26. app/src/main/java/com/example/voiceassistant/commands/IntentCommandHandler.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/IntentCommandHandler.kt", r'''package com.example.voiceassistant.commands

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import com.example.voiceassistant.commands.commands.AccessibilityCommand
import com.example.voiceassistant.commands.commands.AlarmCommand
import com.example.voiceassistant.commands.commands.AppLaunchCommand
import com.example.voiceassistant.commands.commands.CallCommand
import com.example.voiceassistant.commands.commands.InfoCommand
import com.example.voiceassistant.commands.commands.ReminderCommand
import com.example.voiceassistant.commands.commands.SearchCommand
import com.example.voiceassistant.commands.commands.SettingsCommand
import com.example.voiceassistant.commands.commands.SmsCommand
import com.example.voiceassistant.viewmodel.AppLanguage
import kotlinx.coroutines.CancellationException

/** Starts an activity from a non-activity context. */
fun Context.startNewTask(intent: Intent) {
    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    startActivity(intent)
}

/** Routes a [ParsedCommand] to the command that knows how to execute it. */
class IntentCommandHandler(context: Context) {

    private val appContext = context.applicationContext

    suspend fun execute(command: ParsedCommand, lang: AppLanguage): CommandResult = try {
        when (command) {
            is ParsedCommand.Call -> CallCommand.execute(appContext, command, lang)
            is ParsedCommand.Sms -> SmsCommand.execute(appContext, command, lang)
            is ParsedCommand.Alarm -> AlarmCommand.execute(appContext, command, lang)
            is ParsedCommand.WebSearch -> SearchCommand.execute(appContext, command, lang)
            is ParsedCommand.OpenSettings -> SettingsCommand.execute(appContext, command, lang)
            is ParsedCommand.Accessibility -> AccessibilityCommand.execute(appContext, command, lang)
            is ParsedCommand.Info -> InfoCommand.execute(appContext, command, lang)
            is ParsedCommand.LaunchApp -> AppLaunchCommand.execute(appContext, command, lang)
            is ParsedCommand.Reminder -> ReminderCommand.execute(appContext, command, lang)
            // Needs the ViewModel (service state, app scan): MainViewModel handles it before reaching here.
            is ParsedCommand.Security -> CommandResult.Failure(
                lang.tr(
                    "أمر الحماية يُنفَّذ من الشاشة الرئيسية.",
                    "Protection commands are handled by the main screen."
                )
            )
            ParsedCommand.Unknown -> CommandResult.Failure(
                lang.tr(
                    "لم أفهم الأمر. قل «مساعدة» لمعرفة ما يمكنني فعله.",
                    "I didn't understand that. Say \"help\" to see what I can do."
                )
            )
        }
    } catch (e: CancellationException) {
        throw e
    } catch (e: ActivityNotFoundException) {
        CommandResult.Failure(
            lang.tr(
                "لا يوجد تطبيق على الجهاز يستطيع تنفيذ هذا الأمر.",
                "No app on this device can handle that."
            )
        )
    } catch (e: SecurityException) {
        CommandResult.Failure(
            lang.tr(
                "ليس لدي الصلاحية لتنفيذ هذا الأمر.",
                "I don't have permission to do that."
            )
        )
    } catch (e: Exception) {
        CommandResult.Failure(
            lang.tr(
                "حدث خطأ أثناء تنفيذ الأمر.",
                "Something went wrong while running that command."
            )
        )
    }
}
''')

# 27. app/src/main/java/com/example/voiceassistant/commands/commands/AccessibilityCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/AccessibilityCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.content.Context
import android.content.Intent
import android.provider.Settings
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.service.VoiceAccessibilityService
import com.example.voiceassistant.viewmodel.AppLanguage

/**
 * @param targetsOtherApp true if the action must run against another app's window,
 * so the assistant moves itself to the background first.
 */
enum class AccessibilityAction(val targetsOtherApp: Boolean) {
    BACK(true),
    HOME(false),
    RECENTS(false),
    NOTIFICATIONS(false),
    QUICK_SETTINGS(false),
    SCREENSHOT(true),
    LOCK_SCREEN(false),
    SCROLL_DOWN(true),
    SCROLL_UP(true),
    CLICK_TEXT(true)
}

object AccessibilityCommand {

    fun execute(
        context: Context,
        command: ParsedCommand.Accessibility,
        lang: AppLanguage
    ): CommandResult {
        val service = VoiceAccessibilityService.instance
        if (service == null) {
            context.startNewTask(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            return CommandResult.Failure(
                lang.tr(
                    "خدمة الوصول غير مفعّلة. فعّل «Voice Assistant» من إعدادات الاتاحة ثم أعد الأمر.",
                    "The accessibility service is off. Enable \"Voice Assistant\" in Accessibility settings, then try again."
                )
            )
        }

        val ok = service.execute(command.action, command.argument)
        return if (ok) {
            CommandResult.Success(doneMessage(command, lang))
        } else {
            CommandResult.Failure(failMessage(command, lang))
        }
    }

    private fun doneMessage(command: ParsedCommand.Accessibility, lang: AppLanguage): String =
        when (command.action) {
            AccessibilityAction.BACK -> lang.tr("تم الرجوع.", "Went back.")
            AccessibilityAction.HOME -> lang.tr("الشاشة الرئيسية.", "Going home.")
            AccessibilityAction.RECENTS -> lang.tr("فتحت التطبيقات الأخيرة.", "Opened recent apps.")
            AccessibilityAction.NOTIFICATIONS -> lang.tr("فتحت الإشعارات.", "Opened notifications.")
            AccessibilityAction.QUICK_SETTINGS -> lang.tr("فتحت الإعدادات السريعة.", "Opened quick settings.")
            AccessibilityAction.SCREENSHOT -> lang.tr("التقطت لقطة للشاشة.", "Took a screenshot.")
            AccessibilityAction.LOCK_SCREEN -> lang.tr("قفلت الشاشة.", "Locked the screen.")
            AccessibilityAction.SCROLL_DOWN -> lang.tr("مررت للأسفل.", "Scrolled down.")
            AccessibilityAction.SCROLL_UP -> lang.tr("مررت للأعلى.", "Scrolled up.")
            AccessibilityAction.CLICK_TEXT -> lang.tr(
                "ضغطت على ${command.argument.orEmpty()}.",
                "Tapped ${command.argument.orEmpty()}."
            )
        }

    private fun failMessage(command: ParsedCommand.Accessibility, lang: AppLanguage): String =
        if (command.action == AccessibilityAction.CLICK_TEXT) {
            lang.tr(
                "لم أجد عنصراً يمكن الضغط عليه باسم ${command.argument.orEmpty()}.",
                "I couldn't find anything tappable called ${command.argument.orEmpty()}."
            )
        } else {
            lang.tr("تعذّر تنفيذ الأمر على الشاشة الحالية.", "I couldn't do that on the current screen.")
        }
}
''')

# 28. app/src/main/java/com/example/voiceassistant/commands/commands/AlarmCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/AlarmCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.content.Context
import android.content.Intent
import android.provider.AlarmClock
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.viewmodel.AppLanguage
import java.util.Locale

object AlarmCommand {

    fun execute(context: Context, command: ParsedCommand.Alarm, lang: AppLanguage): CommandResult {
        val hour = command.hour
        if (hour == null) {
            context.startNewTask(Intent(AlarmClock.ACTION_SHOW_ALARMS))
            return CommandResult.Success(
                lang.tr(
                    "فتحت المنبهات. قل مثلاً «اضبط منبه الساعة 7:30 صباحاً».",
                    "Opened your alarms. Say for example \"set an alarm for 7:30 am\"."
                )
            )
        }

        val intent = Intent(AlarmClock.ACTION_SET_ALARM).apply {
            putExtra(AlarmClock.EXTRA_HOUR, hour)
            putExtra(AlarmClock.EXTRA_MINUTES, command.minute)
            putExtra(AlarmClock.EXTRA_MESSAGE, "Voice Assistant")
            putExtra(AlarmClock.EXTRA_SKIP_UI, true)
        }
        context.startNewTask(intent)

        val time = String.format(Locale.US, "%02d:%02d", hour, command.minute)
        return CommandResult.Success(
            lang.tr("ضبطت المنبه على الساعة $time.", "Alarm set for $time.")
        )
    }
}
''')

# 29. app/src/main/java/com/example/voiceassistant/commands/commands/CallCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/CallCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.provider.ContactsContract.CommonDataKinds.Phone
import androidx.core.content.ContextCompat
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.TextNormalizer
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.viewmodel.AppLanguage

data class ContactMatch(val name: String, val number: String)

/** Finds a phone contact by (fuzzy, Arabic-aware) name. Requires READ_CONTACTS. */
object ContactResolver {

    private val phoneNumberRegex = Regex("^\\+?\\d{3,}$")

    fun hasPermission(context: Context): Boolean =
        ContextCompat.checkSelfPermission(context, Manifest.permission.READ_CONTACTS) ==
            PackageManager.PERMISSION_GRANTED

    /** Returns the cleaned number if [text] looks like a phone number, otherwise null. */
    fun asPhoneNumber(text: String): String? {
        val digits = text.replace(Regex("[\\s\\-().]"), "")
        return if (phoneNumberRegex.matches(digits)) digits else null
    }

    fun find(context: Context, query: String): ContactMatch? {
        val base = TextNormalizer.key(query.trim())
        // Arabic speech often glues the preposition to the name ("باحمد", "لاحمد"), so try without it too.
        val candidates = buildList {
            add(base)
            if (base.startsWith("\u0628") || base.startsWith("\u0644")) add(base.drop(1))
        }.filter { it.length >= 2 }.distinct()
        if (candidates.isEmpty()) return null

        var best: ContactMatch? = null
        var bestScore = 0

        context.contentResolver.query(
            Phone.CONTENT_URI,
            arrayOf(Phone.DISPLAY_NAME, Phone.NUMBER),
            null,
            null,
            null
        )?.use { cursor ->
            val nameIdx = cursor.getColumnIndexOrThrow(Phone.DISPLAY_NAME)
            val numberIdx = cursor.getColumnIndexOrThrow(Phone.NUMBER)
            while (cursor.moveToNext()) {
                val name = cursor.getString(nameIdx) ?: continue
                val number = cursor.getString(numberIdx) ?: continue
                val key = TextNormalizer.key(name)
                val words = key.split(" ")
                var score = 0
                for (c in candidates) {
                    val s = when {
                        key == c -> 4
                        words.any { it == c } -> 3
                        key.startsWith(c) || words.any { it.startsWith(c) } -> 2
                        key.contains(c) -> 1
                        else -> 0
                    }
                    if (s > score) score = s
                }
                if (score > bestScore) {
                    bestScore = score
                    best = ContactMatch(name, number)
                }
            }
        }
        return best
    }
}

object CallCommand {

    fun execute(context: Context, command: ParsedCommand.Call, lang: AppLanguage): CommandResult {
        val number: String
        val label: String

        val direct = ContactResolver.asPhoneNumber(command.target)
        if (direct != null) {
            number = direct
            label = direct
        } else {
            if (!ContactResolver.hasPermission(context)) {
                return CommandResult.NeedsPermission(
                    Manifest.permission.READ_CONTACTS,
                    lang.tr(
                        "أحتاج إذن جهات الاتصال للبحث عن الاسم.",
                        "I need contacts permission to look up that name."
                    )
                )
            }
            val match = ContactResolver.find(context, command.target)
                ?: return CommandResult.Failure(
                    lang.tr(
                        "لم أجد جهة اتصال باسم ${command.target}.",
                        "I couldn't find a contact named ${command.target}."
                    )
                )
            number = match.number
            label = match.name
        }

        val canCall = ContextCompat.checkSelfPermission(context, Manifest.permission.CALL_PHONE) ==
            PackageManager.PERMISSION_GRANTED
        val action = if (canCall) Intent.ACTION_CALL else Intent.ACTION_DIAL
        context.startNewTask(Intent(action, Uri.fromParts("tel", number, null)))

        return CommandResult.Success(
            if (canCall) {
                lang.tr("جارٍ الاتصال بـ ${label}.", "Calling ${label}.")
            } else {
                lang.tr("فتحت لوحة الاتصال برقم ${label}.", "Opened the dialer for ${label}.")
            }
        )
    }
}
''')

# 30. app/src/main/java/com/example/voiceassistant/commands/commands/SearchCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/SearchCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.app.SearchManager
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.viewmodel.AppLanguage

object SearchCommand {

    fun execute(context: Context, command: ParsedCommand.WebSearch, lang: AppLanguage): CommandResult {
        val query = command.query.trim()
        if (query.isEmpty()) {
            return CommandResult.Failure(
                lang.tr("ماذا تريد أن أبحث عنه؟", "What would you like me to search for?")
            )
        }

        try {
            val intent = Intent(Intent.ACTION_WEB_SEARCH).putExtra(SearchManager.QUERY, query)
            context.startNewTask(intent)
        } catch (e: ActivityNotFoundException) {
            val url = "https://www.google.com/search?q=" + Uri.encode(query)
            context.startNewTask(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
        }

        return CommandResult.Success(
            lang.tr("أبحث عن ${query}.", "Searching for ${query}.")
        )
    }
}
''')

# 31. app/src/main/java/com/example/voiceassistant/commands/commands/SettingsCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/SettingsCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.content.Context
import android.content.Intent
import android.provider.Settings
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.service.ToggleResult
import com.example.voiceassistant.service.VoiceAccessibilityService
import com.example.voiceassistant.viewmodel.AppLanguage
import kotlinx.coroutines.delay

enum class SettingsTarget {
    MAIN, WIFI, BLUETOOTH, SOUND, DISPLAY, LOCATION, AIRPLANE, ACCESSIBILITY, BATTERY
}

object SettingsCommand {

    private const val FIRST_WAIT_MS = 900L
    private const val RETRY_WAIT_MS = 500L
    private const val MAX_ATTEMPTS = 6

    /**
     * "افتح الواي فاي" only opens the page. "شغل الواي فاي" / "اطفي البلوتوث" opens the page and then,
     * using the accessibility service, finds the switch by its name and clicks it.
     */
    suspend fun execute(
        context: Context,
        command: ParsedCommand.OpenSettings,
        lang: AppLanguage
    ): CommandResult {
        context.startNewTask(Intent(actionFor(command.target)))

        val wantOn = command.toggle
        val names = toggleNames(command.target)
        if (wantOn == null || names.isEmpty()) {
            return CommandResult.Success(
                lang.tr(
                    "فتحت ${labelAr(command.target)}.",
                    "Opened ${labelEn(command.target)}."
                )
            )
        }

        val service = VoiceAccessibilityService.instance
            ?: return CommandResult.Failure(
                lang.tr(
                    "فتحت ${labelAr(command.target)}. فعّل خدمة الوصول لكي أستطيع التشغيل والإطفاء بدون لمس.",
                    "Opened ${labelEn(command.target)}. Enable the accessibility service so I can switch it for you."
                )
            )

        val switchName = toggleLabel(command.target, lang)

        // Give the Settings screen time to appear, then look for the switch (retrying a few times).
        delay(FIRST_WAIT_MS)
        var result = ToggleResult.NOT_FOUND
        for (attempt in 0 until MAX_ATTEMPTS) {
            result = service.setToggleByName(names, wantOn)
            if (result != ToggleResult.NOT_FOUND) break
            delay(RETRY_WAIT_MS)
        }

        return when (result) {
            ToggleResult.SUCCESS -> CommandResult.Success(
                if (wantOn) {
                    lang.tr("شغّلت $switchName.", "Turned on $switchName.")
                } else {
                    lang.tr("أطفأت $switchName.", "Turned off $switchName.")
                }
            )

            ToggleResult.ALREADY_IN_STATE -> CommandResult.Success(
                if (wantOn) {
                    lang.tr("$switchName مفعّل بالفعل.", "$switchName is already on.")
                } else {
                    lang.tr("$switchName مطفأ بالفعل.", "$switchName is already off.")
                }
            )

            ToggleResult.NOT_FOUND -> CommandResult.Failure(
                lang.tr(
                    "فتحت الإعدادات لكني لم أجد مفتاح $switchName. اضغط عليه يدوياً.",
                    "I opened Settings but couldn't find the $switchName switch. Please tap it yourself."
                )
            )

            ToggleResult.FAILED -> CommandResult.Failure(
                lang.tr(
                    "وجدت مفتاح $switchName لكن تعذّر الضغط عليه.",
                    "I found the $switchName switch but couldn't tap it."
                )
            )
        }
    }

    private fun actionFor(target: SettingsTarget): String = when (target) {
        SettingsTarget.MAIN -> Settings.ACTION_SETTINGS
        SettingsTarget.WIFI -> Settings.ACTION_WIFI_SETTINGS
        SettingsTarget.BLUETOOTH -> Settings.ACTION_BLUETOOTH_SETTINGS
        SettingsTarget.SOUND -> Settings.ACTION_SOUND_SETTINGS
        SettingsTarget.DISPLAY -> Settings.ACTION_DISPLAY_SETTINGS
        SettingsTarget.LOCATION -> Settings.ACTION_LOCATION_SOURCE_SETTINGS
        SettingsTarget.AIRPLANE -> Settings.ACTION_AIRPLANE_MODE_SETTINGS
        SettingsTarget.ACCESSIBILITY -> Settings.ACTION_ACCESSIBILITY_SETTINGS
        SettingsTarget.BATTERY -> Settings.ACTION_BATTERY_SAVER_SETTINGS
    }

    /** Texts the Settings app may show next to the switch (Arabic names are already normalized). */
    private fun toggleNames(target: SettingsTarget): List<String> = when (target) {
        SettingsTarget.WIFI -> listOf("wi-fi", "wifi", "wi fi", "واي فاي", "وايفاي")
        SettingsTarget.BLUETOOTH -> listOf("bluetooth", "بلوتوث")
        SettingsTarget.AIRPLANE -> listOf("airplane", "flight mode", "الطيران")
        SettingsTarget.LOCATION -> listOf("use location", "location", "الموقع")
        SettingsTarget.BATTERY -> listOf("battery saver", "power saving", "توفير الطاقه", "توفير البطاريه")
        else -> emptyList()
    }

    private fun toggleLabel(target: SettingsTarget, lang: AppLanguage): String = when (target) {
        SettingsTarget.WIFI -> lang.tr("الواي فاي", "Wi-Fi")
        SettingsTarget.BLUETOOTH -> lang.tr("البلوتوث", "Bluetooth")
        SettingsTarget.AIRPLANE -> lang.tr("وضع الطيران", "Airplane mode")
        SettingsTarget.LOCATION -> lang.tr("الموقع", "Location")
        SettingsTarget.BATTERY -> lang.tr("توفير الطاقة", "Battery Saver")
        else -> lang.tr(labelAr(target), labelEn(target))
    }

    private fun labelAr(target: SettingsTarget): String = when (target) {
        SettingsTarget.MAIN -> "الإعدادات"
        SettingsTarget.WIFI -> "إعدادات الواي فاي"
        SettingsTarget.BLUETOOTH -> "إعدادات البلوتوث"
        SettingsTarget.SOUND -> "إعدادات الصوت"
        SettingsTarget.DISPLAY -> "إعدادات الشاشة"
        SettingsTarget.LOCATION -> "إعدادات الموقع"
        SettingsTarget.AIRPLANE -> "إعدادات وضع الطيران"
        SettingsTarget.ACCESSIBILITY -> "إعدادات الاتاحة"
        SettingsTarget.BATTERY -> "إعدادات البطارية"
    }

    private fun labelEn(target: SettingsTarget): String = when (target) {
        SettingsTarget.MAIN -> "Settings"
        SettingsTarget.WIFI -> "Wi-Fi settings"
        SettingsTarget.BLUETOOTH -> "Bluetooth settings"
        SettingsTarget.SOUND -> "Sound settings"
        SettingsTarget.DISPLAY -> "Display settings"
        SettingsTarget.LOCATION -> "Location settings"
        SettingsTarget.AIRPLANE -> "Airplane mode settings"
        SettingsTarget.ACCESSIBILITY -> "Accessibility settings"
        SettingsTarget.BATTERY -> "Battery settings"
    }
}
''')

# 32. app/src/main/java/com/example/voiceassistant/commands/commands/SmsCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/SmsCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.Manifest
import android.content.Context
import android.content.Intent
import android.net.Uri
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.viewmodel.AppLanguage

/**
 * Opens the default messaging app with the recipient and text pre-filled.
 * The user confirms by pressing send, so no SEND_SMS permission is needed.
 */
object SmsCommand {

    fun execute(context: Context, command: ParsedCommand.Sms, lang: AppLanguage): CommandResult {
        val number: String
        val label: String

        val direct = ContactResolver.asPhoneNumber(command.target)
        if (direct != null) {
            number = direct
            label = direct
        } else {
            if (!ContactResolver.hasPermission(context)) {
                return CommandResult.NeedsPermission(
                    Manifest.permission.READ_CONTACTS,
                    lang.tr(
                        "أحتاج إذن جهات الاتصال للبحث عن الاسم.",
                        "I need contacts permission to look up that name."
                    )
                )
            }
            val match = ContactResolver.find(context, command.target)
                ?: return CommandResult.Failure(
                    lang.tr(
                        "لم أجد جهة اتصال باسم ${command.target}.",
                        "I couldn't find a contact named ${command.target}."
                    )
                )
            number = match.number
            label = match.name
        }

        val intent = Intent(Intent.ACTION_SENDTO, Uri.fromParts("smsto", number, null)).apply {
            command.body?.takeIf { it.isNotBlank() }?.let { putExtra("sms_body", it) }
        }
        context.startNewTask(intent)

        return CommandResult.Success(
            lang.tr(
                "جهّزت الرسالة إلى ${label}. راجعها واضغط إرسال.",
                "Message to ${label} is ready. Review it and press send."
            )
        )
    }
}
''')

# 33. app/src/main/java/com/example/voiceassistant/commands/commands/InfoCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/InfoCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.content.Context
import android.os.BatteryManager
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.viewmodel.AppLanguage
import java.text.DateFormat
import java.text.SimpleDateFormat
import java.util.Date

enum class InfoType { TIME, DATE, BATTERY, HELP, GREETING, THANKS }

object InfoCommand {

    fun execute(context: Context, command: ParsedCommand.Info, lang: AppLanguage): CommandResult =
        when (command.type) {
            InfoType.TIME -> {
                val time = DateFormat.getTimeInstance(DateFormat.SHORT, lang.locale).format(Date())
                CommandResult.Success(lang.tr("الساعة الآن $time.", "It's $time."))
            }

            InfoType.DATE -> {
                val date = SimpleDateFormat("EEEE d MMMM yyyy", lang.locale).format(Date())
                CommandResult.Success(lang.tr("اليوم $date.", "Today is $date."))
            }

            InfoType.BATTERY -> batteryInfo(context, lang)

            InfoType.HELP -> CommandResult.Success(
                lang.tr(
                    "يمكنني: الاتصال بجهة اتصال، إرسال رسالة، ضبط منبه، البحث في الويب، " +
                        "فتح التطبيقات والإعدادات، تشغيل وإطفاء الواي فاي والبلوتوث، " +
                        "والتحكم بالشاشة مثل رجوع والرئيسية والإشعارات والتمرير. " +
                        "ويمكنك أيضاً أن تسألني أي سؤال وسأجيبك.",
                    "I can: call a contact, send a message, set an alarm, search the web, " +
                        "open apps and settings, switch Wi-Fi and Bluetooth on or off, " +
                        "and control the screen: back, home, notifications, scrolling. " +
                        "You can also ask me anything and I'll answer."
                )
            )

            InfoType.GREETING -> CommandResult.Success(
                lang.tr("أهلاً بك! كيف أساعدك؟", "Hello! How can I help?")
            )

            InfoType.THANKS -> CommandResult.Success(
                lang.tr("عفواً! أنا في الخدمة.", "You're welcome!")
            )
        }

    private fun batteryInfo(context: Context, lang: AppLanguage): CommandResult {
        val manager = context.getSystemService(Context.BATTERY_SERVICE) as? BatteryManager
            ?: return CommandResult.Failure(
                lang.tr("لا أستطيع قراءة حالة البطارية.", "I can't read the battery status.")
            )
        val level = manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        val charging = manager.isCharging
        return CommandResult.Success(
            if (charging) {
                lang.tr(
                    "البطارية عند $level بالمئة وهي قيد الشحن.",
                    "Battery is at $level percent and charging."
                )
            } else {
                lang.tr("البطارية عند $level بالمئة.", "Battery is at $level percent.")
            }
        )
    }
}
''')

# 34. app/src/main/java/com/example/voiceassistant/commands/commands/AppLaunchCommand.kt
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/AppLaunchCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.pm.ResolveInfo
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.TextNormalizer
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.viewmodel.AppLanguage

object AppLaunchCommand {

    /** Spoken (usually Arabic) app names -> the English token found in the app's label / package. */
    private val aliases: Map<String, String> = mapOf(
        "واتساب" to "whatsapp",
        "واتس اب" to "whatsapp",
        "يوتيوب" to "youtube",
        "كروم" to "chrome",
        "جوجل كروم" to "chrome",
        "كاميرا" to "camera",
        "خرائط" to "maps",
        "خرائط جوجل" to "maps",
        "صور" to "photos",
        "معرض" to "gallery",
        "حاسبة" to "calculator",
        "ساعة" to "clock",
        "تقويم" to "calendar",
        "جيميل" to "gmail",
        "بريد" to "mail",
        "تيليجرام" to "telegram",
        "تلجرام" to "telegram",
        "انستقرام" to "instagram",
        "انستجرام" to "instagram",
        "فيسبوك" to "facebook",
        "ماسنجر" to "messenger",
        "سناب شات" to "snapchat",
        "سناب" to "snapchat",
        "تويتر" to "twitter",
        "تيك توك" to "tiktok",
        "نتفليكس" to "netflix",
        "سبوتيفاي" to "spotify",
        "هاتف" to "phone",
        "جهات الاتصال" to "contacts",
        "رسائل" to "messages",
        "ملفات" to "files",
        "ملاحظات" to "notes",
        "بلاي ستور" to "play store",
        "متجر بلاي" to "play store",
        "زوم" to "zoom"
    )

    private val normalizedAliases: Map<String, String> by lazy {
        aliases.mapKeys { TextNormalizer.key(it.key) }
    }

    fun execute(context: Context, command: ParsedCommand.LaunchApp, lang: AppLanguage): CommandResult {
        val pm = context.packageManager
        val launcher = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        val apps: List<ResolveInfo> = pm.queryIntentActivities(launcher, 0)

        val base = TextNormalizer.key(command.appName).trim()
        val stripped = base.removePrefix("\u0627\u0644") // leading "ال"
        val candidates = listOfNotNull(
            base,
            stripped,
            normalizedAliases[base],
            normalizedAliases[stripped]
        ).filter { it.length >= 2 }.distinct()

        var best: ResolveInfo? = null
        var bestScore = 0
        for (info in apps) {
            val label = TextNormalizer.key(info.loadLabel(pm).toString())
            val labelStripped = label.removePrefix("\u0627\u0644")
            val pkg = info.activityInfo.packageName.lowercase()

            var score = 0
            for (c in candidates) {
                val s = when {
                    label == c || labelStripped == c -> 4
                    label.startsWith(c) || labelStripped.startsWith(c) -> 3
                    label.contains(c) -> 2
                    c.length >= 3 && pkg.contains(c.replace(" ", "")) -> 1
                    label.length >= 3 && c.contains(label) -> 1
                    else -> 0
                }
                if (s > score) score = s
            }
            if (score > bestScore) {
                bestScore = score
                best = info
            }
        }

        val match = best ?: return CommandResult.Failure(
            lang.tr(
                "لم أجد تطبيقاً باسم ${command.appName}.",
                "I couldn't find an app called ${command.appName}."
            )
        )

        val appInfo = match.activityInfo
        val launch = Intent(Intent.ACTION_MAIN)
            .addCategory(Intent.CATEGORY_LAUNCHER)
            .setComponent(ComponentName(appInfo.packageName, appInfo.name))
        context.startNewTask(launch)

        val appLabel = match.loadLabel(pm).toString()
        return CommandResult.Success(
            lang.tr("فتحت ${appLabel}.", "Opening ${appLabel}.")
        )
    }
}
''')

# 35. app/src/main/java/com/example/voiceassistant/ui/theme/Color.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/theme/Color.kt", r'''package com.example.voiceassistant.ui.theme

import androidx.compose.ui.graphics.Color

val Indigo40 = Color(0xFF4F5BD5)
val IndigoOn40 = Color(0xFFFFFFFF)
val IndigoContainer40 = Color(0xFFE0E0FF)
val Teal40 = Color(0xFF00796B)
val TealContainer40 = Color(0xFFB2F2E8)
val Red40 = Color(0xFFBA1A1A)
val RedContainer40 = Color(0xFFFFDAD6)
val Surface40 = Color(0xFFFBFAFF)
val SurfaceVariant40 = Color(0xFFE4E1EC)
val OnSurface40 = Color(0xFF1B1B1F)
val OnSurfaceVariant40 = Color(0xFF46464F)
val Outline40 = Color(0xFF777680)

val Indigo80 = Color(0xFFBBC3FF)
val IndigoOn80 = Color(0xFF0A1480)
val IndigoContainer80 = Color(0xFF2E3AB0)
val Teal80 = Color(0xFF4FDBC8)
val TealContainer80 = Color(0xFF005048)
val Red80 = Color(0xFFFFB4AB)
val RedContainer80 = Color(0xFF93000A)
val Surface80 = Color(0xFF121317)
val SurfaceVariant80 = Color(0xFF46464F)
val OnSurface80 = Color(0xFFE4E1E6)
val OnSurfaceVariant80 = Color(0xFFC7C5D0)
val Outline80 = Color(0xFF918F9A)
''')

# 36. app/src/main/java/com/example/voiceassistant/ui/theme/Type.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/theme/Type.kt", r'''package com.example.voiceassistant.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    titleLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.SemiBold,
        fontSize = 22.sp,
        lineHeight = 28.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp
    ),
    labelMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp
    )
)
''')

# 37. app/src/main/java/com/example/voiceassistant/ui/theme/Theme.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/theme/Theme.kt", r'''package com.example.voiceassistant.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColors = lightColorScheme(
    primary = Indigo40,
    onPrimary = IndigoOn40,
    primaryContainer = IndigoContainer40,
    tertiary = Teal40,
    tertiaryContainer = TealContainer40,
    error = Red40,
    errorContainer = RedContainer40,
    background = Surface40,
    surface = Surface40,
    onBackground = OnSurface40,
    onSurface = OnSurface40,
    surfaceVariant = SurfaceVariant40,
    onSurfaceVariant = OnSurfaceVariant40,
    outline = Outline40
)

private val DarkColors = darkColorScheme(
    primary = Indigo80,
    onPrimary = IndigoOn80,
    primaryContainer = IndigoContainer80,
    tertiary = Teal80,
    tertiaryContainer = TealContainer80,
    error = Red80,
    errorContainer = RedContainer80,
    background = Surface80,
    surface = Surface80,
    onBackground = OnSurface80,
    onSurface = OnSurface80,
    surfaceVariant = SurfaceVariant80,
    onSurfaceVariant = OnSurfaceVariant80,
    outline = Outline80
)

@Composable
fun VoiceAssistantTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        typography = Typography,
        content = content
    )
}
''')

# 38. app/src/main/java/com/example/voiceassistant/ui/components/ChatBubble.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/components/ChatBubble.kt", r'''package com.example.voiceassistant.ui.components

import android.graphics.BitmapFactory
import android.net.Uri
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.voiceassistant.data.models.CodeBlock
import com.example.voiceassistant.data.models.Message
import com.example.voiceassistant.viewmodel.AppLanguage
import java.io.File

@Composable
fun ChatBubble(
    message: Message,
    modifier: Modifier = Modifier,
    language: AppLanguage = AppLanguage.ARABIC
) {
    val isUser = message.isUser
    val container = if (isUser) {
        MaterialTheme.colorScheme.primary
    } else {
        MaterialTheme.colorScheme.surfaceVariant
    }
    val content = if (isUser) {
        MaterialTheme.colorScheme.onPrimary
    } else {
        MaterialTheme.colorScheme.onSurfaceVariant
    }
    val shape = RoundedCornerShape(
        topStart = 18.dp,
        topEnd = 18.dp,
        bottomStart = if (isUser) 18.dp else 4.dp,
        bottomEnd = if (isUser) 4.dp else 18.dp
    )

    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
        ) {
            Surface(
                color = container,
                contentColor = content,
                shape = shape,
                modifier = Modifier.widthIn(max = 320.dp)
            ) {
                Text(
                    text = message.text,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                    style = MaterialTheme.typography.bodyLarge
                )
            }
        }
        message.code.forEach { block -> CodeCard(block, language) }
        message.imagePath?.let { path -> ImageCard(path, language) }
    }
}

/** Shows a generated picture with a Save button. */
@Composable
private fun ImageCard(path: String, language: AppLanguage) {
    val context = LocalContext.current
    var bitmap by remember(path) { mutableStateOf<androidx.compose.ui.graphics.ImageBitmap?>(null) }
    LaunchedEffect(path) {
        bitmap = withContext(Dispatchers.IO) {
            try {
                BitmapFactory.decodeFile(path)?.asImageBitmap()
            } catch (e: Exception) {
                null
            }
        }
    }

    val saver = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("image/png")
    ) { uri ->
        if (uri != null) {
            val ok = try {
                context.contentResolver.openOutputStream(uri)?.use { out ->
                    out.write(File(path).readBytes())
                }
                true
            } catch (e: Exception) {
                false
            }
            Toast.makeText(
                context,
                if (ok) language.tr("تم الحفظ", "Saved") else language.tr("تعذّر الحفظ", "Couldn't save"),
                Toast.LENGTH_SHORT
            ).show()
        }
    }

    val currentBitmap = bitmap ?: return

    Surface(
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column {
            Image(
                bitmap = currentBitmap,
                contentDescription = null,
                contentScale = ContentScale.FillWidth,
                modifier = Modifier.fillMaxWidth()
            )
            TextButton(onClick = { saver.launch("image_" + System.currentTimeMillis() + ".png") }) {
                Text(language.tr("حفظ الصورة", "Save image"))
            }
        }
    }
}

/** Shows one code block (always left-to-right) with Copy and Save buttons. */
@Composable
private fun CodeCard(block: CodeBlock, language: AppLanguage) {
    val context = LocalContext.current
    val clipboard = LocalClipboardManager.current
    var copied by remember { mutableStateOf(false) }
    var applied by remember { mutableStateOf(false) }
    val ext = extensionFor(block.language)
    val fileName = block.fileName ?: when {
        ext == "html" -> "index.html"
        block.language.equals("setup", ignoreCase = true) ||
            (ext == "py" && block.content.contains("setup(")) -> "setup.py"
        else -> "code.$ext"
    }

    val saver = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/octet-stream")
    ) { uri ->
        if (uri != null) {
            val ok = try {
                context.contentResolver.openOutputStream(uri)?.use {
                    it.write(block.content.toByteArray(Charsets.UTF_8))
                }
                true
            } catch (e: Exception) {
                false
            }
            Toast.makeText(
                context,
                if (ok) language.tr("تم الحفظ", "Saved") else language.tr("تعذّر الحفظ", "Couldn't save"),
                Toast.LENGTH_SHORT
            ).show()
        }
    }

    val buttonColors = ButtonDefaults.textButtonColors(
        contentColor = MaterialTheme.colorScheme.inversePrimary
    )

    Surface(
        color = MaterialTheme.colorScheme.inverseSurface,
        contentColor = MaterialTheme.colorScheme.inverseOnSurface,
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Ltr) {
            Column {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = 12.dp, end = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = block.fileName ?: block.language.ifBlank { "code" },
                        style = MaterialTheme.typography.labelMedium
                    )
                    Row {
                        TextButton(
                            colors = buttonColors,
                            onClick = {
                                clipboard.setText(AnnotatedString(block.content))
                                copied = true
                            }
                        ) {
                            Text(
                                if (copied) language.tr("تم النسخ", "Copied")
                                else language.tr("نسخ", "Copy")
                            )
                        }
                        TextButton(
                            colors = buttonColors,
                            onClick = { saver.launch(fileName) }
                        ) {
                            Text(language.tr("حفظ", "Save"))
                        }
                        // The edited version of a file the user opened: write it straight back to the original.
                        if (block.sourceUri != null) {
                            TextButton(
                                colors = buttonColors,
                                onClick = {
                                    val ok = try {
                                        context.contentResolver
                                            .openOutputStream(Uri.parse(block.sourceUri), "wt")
                                            ?.use { it.write((block.content + "\n").toByteArray(Charsets.UTF_8)) } != null
                                    } catch (e: Exception) {
                                        false
                                    }
                                    applied = ok
                                    Toast.makeText(
                                        context,
                                        if (ok) language.tr("تم تحديث الملف الأصلي", "Original file updated")
                                        else language.tr("تعذّر الكتابة على الملف الأصلي، استخدم حفظ", "Couldn't write to the original file, use Save"),
                                        Toast.LENGTH_SHORT
                                    ).show()
                                }
                            ) {
                                Text(
                                    if (applied) language.tr("تم التطبيق", "Applied")
                                    else language.tr("تطبيق على الملف", "Apply to file")
                                )
                            }
                        }
                    }
                }
                Text(
                    text = block.content,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    modifier = Modifier
                        .horizontalScroll(rememberScrollState())
                        .padding(12.dp)
                )
            }
        }
    }
}

private fun extensionFor(lang: String): String = when (lang.lowercase()) {
    "html" -> "html"
    "css" -> "css"
    "javascript", "js" -> "js"
    "typescript", "ts" -> "ts"
    "kotlin", "kt" -> "kt"
    "kts" -> "kts"
    "java" -> "java"
    "python", "py" -> "py"
    "xml" -> "xml"
    "json" -> "json"
    "bash", "sh", "shell" -> "sh"
    "c" -> "c"
    "cpp", "c++" -> "cpp"
    "sql" -> "sql"
    "yaml", "yml" -> "yml"
    "markdown", "md" -> "md"
    "setup" -> "py"
    "php" -> "php"
    "go" -> "go"
    "rust", "rs" -> "rs"
    "swift" -> "swift"
    "dart" -> "dart"
    "bat", "batch" -> "bat"
    "gradle" -> "gradle"
    "toml" -> "toml"
    "ini" -> "ini"
    else -> "txt"
}

''')

# 39. app/src/main/java/com/example/voiceassistant/ui/components/MicButton.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/components/MicButton.kt", r'''package com.example.voiceassistant.ui.components

import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilledIconButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.unit.dp
import com.example.voiceassistant.viewmodel.AssistantStatus

@Composable
fun MicButton(
    status: AssistantStatus,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    compact: Boolean = false
) {
    val listening = status == AssistantStatus.LISTENING

    // compact = small round button that sits inside the chat input bar
    val boxSize = if (compact) 48.dp else 120.dp
    val buttonSize = if (compact) 44.dp else 80.dp
    val iconSize = if (compact) 22.dp else 36.dp
    val progressSize = if (compact) 22.dp else 32.dp

    val transition = rememberInfiniteTransition(label = "micPulse")
    val pulse by transition.animateFloat(
        initialValue = 1f,
        targetValue = if (listening) (if (compact) 1.3f else 1.45f) else 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 900),
            repeatMode = RepeatMode.Reverse
        ),
        label = "micPulseScale"
    )

    val containerColor = when (status) {
        AssistantStatus.LISTENING -> MaterialTheme.colorScheme.error
        AssistantStatus.ERROR -> MaterialTheme.colorScheme.errorContainer
        else -> MaterialTheme.colorScheme.primary
    }
    val contentColor = when (status) {
        AssistantStatus.ERROR -> MaterialTheme.colorScheme.error
        AssistantStatus.LISTENING -> MaterialTheme.colorScheme.onError
        else -> MaterialTheme.colorScheme.onPrimary
    }

    Box(modifier = modifier.size(boxSize), contentAlignment = Alignment.Center) {
        if (listening) {
            Box(
                modifier = Modifier
                    .size(buttonSize)
                    .scale(pulse)
                    .background(MaterialTheme.colorScheme.error.copy(alpha = 0.25f), CircleShape)
            )
        }
        FilledIconButton(
            onClick = onClick,
            modifier = Modifier.size(buttonSize),
            colors = IconButtonDefaults.filledIconButtonColors(
                containerColor = containerColor,
                contentColor = contentColor
            )
        ) {
            when (status) {
                AssistantStatus.PROCESSING -> CircularProgressIndicator(
                    modifier = Modifier.size(progressSize),
                    color = contentColor,
                    strokeWidth = if (compact) 2.dp else 3.dp
                )
                AssistantStatus.LISTENING -> Icon(
                    imageVector = Icons.Filled.Stop,
                    contentDescription = "Stop",
                    modifier = Modifier.size(iconSize)
                )
                AssistantStatus.SPEAKING -> Icon(
                    imageVector = Icons.AutoMirrored.Filled.VolumeUp,
                    contentDescription = "Speaking",
                    modifier = Modifier.size(iconSize)
                )
                else -> Icon(
                    imageVector = Icons.Filled.Mic,
                    contentDescription = "Microphone",
                    modifier = Modifier.size(iconSize)
                )
            }
        }
    }
}
''')

# 40. app/src/main/java/com/example/voiceassistant/ui/components/StatusIndicator.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/components/StatusIndicator.kt", r'''package com.example.voiceassistant.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.voiceassistant.viewmodel.AppLanguage
import com.example.voiceassistant.viewmodel.AssistantStatus

@Composable
fun StatusIndicator(
    status: AssistantStatus,
    partialText: String,
    errorMessage: String?,
    language: AppLanguage,
    modifier: Modifier = Modifier
) {
    val text = when (status) {
        AssistantStatus.IDLE -> language.tr("اضغط على الميكروفون وتحدث", "Tap the mic and speak")
        AssistantStatus.LISTENING -> partialText.ifBlank { language.tr("أستمع إليك…", "Listening…") }
        AssistantStatus.PROCESSING -> language.tr("جارٍ المعالجة…", "Working on it…")
        AssistantStatus.SPEAKING -> language.tr("أتحدث…", "Speaking…")
        AssistantStatus.ERROR -> errorMessage ?: language.tr("حدث خطأ", "Something went wrong")
    }

    val dotColor by animateColorAsState(
        targetValue = when (status) {
            AssistantStatus.IDLE -> MaterialTheme.colorScheme.outline
            AssistantStatus.LISTENING -> MaterialTheme.colorScheme.error
            AssistantStatus.PROCESSING -> MaterialTheme.colorScheme.tertiary
            AssistantStatus.SPEAKING -> MaterialTheme.colorScheme.primary
            AssistantStatus.ERROR -> MaterialTheme.colorScheme.error
        },
        label = "statusDotColor"
    )

    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(10.dp)
                .background(dotColor, CircleShape)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis,
            textAlign = TextAlign.Center
        )
    }
}
''')

# 41. app/src/main/java/com/example/voiceassistant/ui/components/LanguageToggle.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/components/LanguageToggle.kt", r'''package com.example.voiceassistant.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.voiceassistant.viewmodel.AppLanguage

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LanguageToggle(
    selected: AppLanguage,
    onSelected: (AppLanguage) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        AppLanguage.entries.forEach { language ->
            FilterChip(
                selected = language == selected,
                onClick = { onSelected(language) },
                label = { Text(language.label) }
            )
        }
    }
}
''')

# 42. app/src/main/java/com/example/voiceassistant/ui/MainScreen.kt
write_file("app/src/main/java/com/example/voiceassistant/ui/MainScreen.kt", r'''package com.example.voiceassistant.ui

import android.app.Activity
import android.content.Intent
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.isImeVisible
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Security
import androidx.compose.material3.Button
import androidx.compose.material3.DrawerValue
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.ModalNavigationDrawer
import androidx.compose.material3.rememberDrawerState
import androidx.compose.material3.InputChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.activity.compose.BackHandler
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.voiceassistant.data.SavedSession
import com.example.voiceassistant.speech.rememberAudioPermissionRequest
import com.example.voiceassistant.ui.components.AnimeAvatar
import com.example.voiceassistant.ui.components.ChatBubble
import com.example.voiceassistant.ui.components.ChatInputBar
import com.example.voiceassistant.ui.components.CharacterMenuButton
import com.example.voiceassistant.ui.components.LanguageToggle
import com.example.voiceassistant.ui.components.StatusIndicator
import com.example.voiceassistant.ui.components.rememberCharacterSelection
import com.example.voiceassistant.viewmodel.AppLanguage
import com.example.voiceassistant.viewmodel.MainViewModel

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun MainScreen(
    autoListenToken: Int = 0,
    viewModel: MainViewModel = viewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val savedSessions by viewModel.savedSessions.collectAsStateWithLifecycle()
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val drawerScope = rememberCoroutineScope()
    val securityEnabled by viewModel.securityEnabled.collectAsStateWithLifecycle()
    var showSecurityMenu by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val listState = rememberLazyListState()
    // While the keyboard is open, the status / language / hands-free controls are hidden so the chat stays visible.
    // The microphone lives inside the input bar, so it is never hidden.
    val imeVisible = WindowInsets.isImeVisible
    var inputFocused by remember { mutableStateOf(false) }
    val focusManager = LocalFocusManager.current
    // الشخصية المختارة (محفوظة في SharedPreferences) + حجم الشخصية: كبيرة عندما تكون المحادثة فارغة.
    val characters = rememberCharacterSelection()
    val avatarTap = remember { MutableInteractionSource() }
    // The welcome message doesn't count: the avatar stays big until the user says or types something.
    val conversationEmpty = state.messages.none { it.isUser }
    val avatarHeight by animateDpAsState(
        targetValue = if (conversationEmpty) 220.dp else 120.dp,
        label = "avatarHeight"
    )
    val keyboard = LocalSoftwareKeyboardController.current
    // Compact mode: keyboard open OR the text field has focus (works even if the IME insets aren't reported).
    val typing = imeVisible || inputFocused
    BackHandler(enabled = inputFocused) {
        keyboard?.hide()
        focusManager.clearFocus()
    }

    // Microphone permission, then start / stop listening (mic button).
    val requestMic = rememberAudioPermissionRequest(
        onGranted = { viewModel.toggleListening() },
        onDenied = { viewModel.onMicPermissionDenied() }
    )

    // Same permission, but used when the app is opened as the default assistant: start listening at once.
    val requestMicAuto = rememberAudioPermissionRequest(
        onGranted = { viewModel.startHandsFree() },
        onDenied = { viewModel.onMicPermissionDenied() }
    )

    // Runtime permissions requested on behalf of a command (e.g. contacts).
    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted -> viewModel.onPermissionResult(granted) }

    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) {
        viewModel.setForeground(true)
        viewModel.refreshAccessibilityStatus()
    }

    LifecycleEventEffect(Lifecycle.Event.ON_PAUSE) {
        viewModel.setForeground(false)
    }

    // Opened through the default-assistant gesture -> listen immediately.
    LaunchedEffect(autoListenToken) {
        if (autoListenToken > 0) requestMicAuto()
    }

    LaunchedEffect(state.pendingPermission) {
        state.pendingPermission?.let { permissionLauncher.launch(it) }
    }

    LaunchedEffect(Unit) {
        viewModel.backgroundRequests.collect {
            (context as? Activity)?.moveTaskToBack(true)
        }
    }

    LaunchedEffect(state.messages.size) {
        if (state.messages.isNotEmpty()) {
            listState.animateScrollToItem(state.messages.lastIndex)
        }
    }

    // ظهور/اختفاء لوحة المفاتيح: نثبّت آخر رسالة ظاهرة فوراً (بدون أنيميشن).
    LaunchedEffect(typing) {
        if (state.messages.isNotEmpty()) {
            listState.scrollToItem(state.messages.lastIndex)
        }
    }

    val direction = if (state.language == AppLanguage.ARABIC) LayoutDirection.Rtl else LayoutDirection.Ltr

    CompositionLocalProvider(LocalLayoutDirection provides direction) {
        ModalNavigationDrawer(
            drawerState = drawerState,
            drawerContent = {
                SessionsDrawerContent(
                    sessions = savedSessions,
                    language = state.language,
                    onNewChat = {
                        viewModel.startNewChat()
                        drawerScope.launch { drawerState.close() }
                    },
                    onOpen = { id ->
                        viewModel.loadSession(id)
                        drawerScope.launch { drawerState.close() }
                    },
                    onDelete = viewModel::deleteSession
                )
            }
        ) {
        Scaffold(
            modifier = Modifier.imePadding(),
            topBar = {
                TopAppBar(
                    title = {
                        Text(
                            text = state.language.tr("المساعد الصوتي", "Voice Assistant"),
                            style = MaterialTheme.typography.titleLarge
                        )
                    },
                    navigationIcon = {
                        IconButton(onClick = { drawerScope.launch { drawerState.open() } }) {
                            Icon(
                                imageVector = Icons.Filled.Menu,
                                contentDescription = state.language.tr("القائمة", "Menu")
                            )
                        }
                    },
                    actions = {
                        CharacterMenuButton(
                            selected = characters.current,
                            language = state.language,
                            onSelected = characters::select
                        )
                        Box {
                            IconButton(onClick = { showSecurityMenu = true }) {
                                Icon(
                                    imageVector = Icons.Filled.Security,
                                    contentDescription = state.language.tr("الحماية", "Protection"),
                                    tint = if (securityEnabled) {
                                        MaterialTheme.colorScheme.primary
                                    } else {
                                        LocalContentColor.current
                                    }
                                )
                            }
                            DropdownMenu(
                                expanded = showSecurityMenu,
                                onDismissRequest = { showSecurityMenu = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text(state.language.tr("الحماية", "Protection")) },
                                    onClick = { viewModel.toggleSecurityMonitoring(!securityEnabled) },
                                    trailingIcon = {
                                        Switch(
                                            checked = securityEnabled,
                                            onCheckedChange = viewModel::toggleSecurityMonitoring
                                        )
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text(state.language.tr("فحص التطبيقات", "Scan apps")) },
                                    onClick = {
                                        showSecurityMenu = false
                                        viewModel.scanInstalledApps()
                                    }
                                )
                            }
                        }
                        IconButton(onClick = viewModel::startNewChat) {
                            Icon(
                                imageVector = Icons.Filled.Add,
                                contentDescription = state.language.tr("محادثة جديدة", "New chat")
                            )
                        }
                        IconButton(onClick = viewModel::clearConversation) {
                            Icon(
                                imageVector = Icons.Filled.DeleteSweep,
                                contentDescription = state.language.tr("مسح المحادثة", "Clear conversation")
                            )
                        }
                    }
                )
            }
        ) { padding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
            ) {
                if (!state.isAccessibilityEnabled && !typing) {
                    AccessibilityBanner(
                        language = state.language,
                        onEnable = {
                            context.startActivity(
                                Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
                                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            )
                        }
                    )
                }

                // Always at the top of the screen (not tied to the keyboard state).
                AnimeAvatar(
                    character = characters.current,
                    status = state.status,
                    contentDescription = state.language.tr(
                        "الشخصية ${characters.current.nameAr} — اضغط للتبديل",
                        "${characters.current.nameEn} — tap to switch"
                    ),
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(avatarHeight)
                        .clickable(
                            interactionSource = avatarTap,
                            indication = null,
                            onClick = characters::next
                        )
                )

                LazyColumn(
                    state = listState,
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(state.messages, key = { it.id }) { message ->
                        ChatBubble(message, language = state.language)
                    }
                }

                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, vertical = if (typing) 2.dp else 8.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(if (typing) 0.dp else 8.dp)
                ) {
                    // The code file being read / edited: every typed or spoken request applies to it until closed.
                    state.workingFileName?.let { fileName ->
                        InputChip(
                            selected = true,
                            onClick = viewModel::clearWorkingFile,
                            label = {
                                Text(
                                    text = state.language.tr("الملف الحالي: $fileName", "Working on: $fileName"),
                                    maxLines = 1
                                )
                            },
                            trailingIcon = {
                                Icon(
                                    imageVector = Icons.Filled.Close,
                                    contentDescription = state.language.tr("إغلاق الملف", "Close file"),
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                        )
                    }
                    // One row: [file] [image] [text field] [mic] [send]
                    ChatInputBar(
                        language = state.language,
                        micStatus = state.status,
                        onMicClick = {
                            // Close the keyboard first so the listening status is visible.
                            keyboard?.hide()
                            focusManager.clearFocus()
                            requestMic()
                        },
                        onSend = viewModel::sendTyped,
                        onFocusChange = { inputFocused = it }
                    )
                    if (!typing) {
                        StatusIndicator(
                            status = state.status,
                            partialText = state.partialText,
                            errorMessage = state.errorMessage,
                            language = state.language
                        )
                        LanguageToggle(
                            selected = state.language,
                            onSelected = viewModel::setLanguage
                        )
                        FilterChip(
                            selected = state.handsFree,
                            onClick = { viewModel.setHandsFree(!state.handsFree) },
                            label = {
                                Text(state.language.tr("محادثة مستمرة", "Hands-free"))
                            }
                        )
                    }
                }
            }
        }
        }
    }
}

@Composable
private fun SessionsDrawerContent(
    sessions: List<SavedSession>,
    language: AppLanguage,
    onNewChat: () -> Unit,
    onOpen: (Long) -> Unit,
    onDelete: (Long) -> Unit
) {
    val dateFormat = remember { java.text.SimpleDateFormat("yyyy-MM-dd HH:mm", java.util.Locale.US) }
    ModalDrawerSheet {
        Column(modifier = Modifier.fillMaxSize()) {
            Button(
                onClick = onNewChat,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Icon(imageVector = Icons.Filled.Add, contentDescription = null)
                Text(
                    text = language.tr("محادثة جديدة", "New chat"),
                    modifier = Modifier.padding(start = 8.dp)
                )
            }
            if (sessions.isEmpty()) {
                Text(
                    text = language.tr("لا توجد محادثات سابقة.", "No previous chats."),
                    modifier = Modifier.padding(horizontal = 16.dp),
                    style = MaterialTheme.typography.bodyMedium
                )
            } else {
                LazyColumn(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    items(sessions, key = { it.id }) { session ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { onOpen(session.id) }
                                .padding(start = 12.dp, top = 4.dp, bottom = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = session.title,
                                    maxLines = 1,
                                    style = MaterialTheme.typography.bodyLarge
                                )
                                Text(
                                    text = dateFormat.format(java.util.Date(session.timestamp)),
                                    style = MaterialTheme.typography.bodySmall
                                )
                            }
                            IconButton(onClick = { onDelete(session.id) }) {
                                Icon(
                                    imageVector = Icons.Filled.Delete,
                                    contentDescription = language.tr("حذف", "Delete")
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun AccessibilityBanner(language: AppLanguage, onEnable: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.tertiaryContainer
        )
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = language.tr(
                    "فعّل خدمة الوصول لأوامر التحكم بالشاشة (رجوع، تمرير، ضغط، تشغيل الواي فاي…).",
                    "Enable the accessibility service for screen control (back, scroll, tap, Wi-Fi switch…)."
                ),
                modifier = Modifier.weight(1f),
                style = MaterialTheme.typography.bodyMedium
            )
            TextButton(onClick = onEnable) {
                Text(language.tr("تفعيل", "Enable"))
            }
        }
    }
}
''')

# ------------------------------------------------------------------------------
# الإضافة: الكتابة بلوحة المفاتيح + إرسال الصور والملفات
# هذا القسم لا يعدّل أي سطر من الكود الأصلي أعلاه. يضيف ملفات جديدة فقط،
# ويُدرج أسطراً جديدة عند نقاط محددة في الملفات المولّدة (بعد التحقق من أن
# كل نقطة تظهر مرة واحدة بالضبط).
# ------------------------------------------------------------------------------
def insert_before(path, anchor, insertion):
    """Inserts `insertion` right before the single occurrence of `anchor`."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if text.count(anchor) != 1:
        raise RuntimeError("Anchor is not unique in {}: {!r}".format(path, anchor[:70]))
    text = text.replace(anchor, insertion + anchor, 1)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# 40. نموذج المرفق (صورة أو ملف) الذي يختاره المستخدم من لوحة الإدخال
write_file("app/src/main/java/com/example/voiceassistant/data/AttachmentData.kt", r'''package com.example.voiceassistant.data

/** A picture or file the user attached from the keyboard input bar. */
class AttachmentData(
    val name: String,
    val mime: String,
    val bytes: ByteArray,
    /** Uri of the picked file (lets an edited code file be written back to the original). */
    val uri: String? = null
) {
    companion object {
        /** Largest attachment accepted (keeps the request under the AI service limit). */
        const val MAX_BYTES = 15 * 1024 * 1024
    }
}
''')

# 41. شريط الإدخال: حقل كتابة + زر إرسال + زر صورة + زر ملف
write_file("app/src/main/java/com/example/voiceassistant/ui/components/ChatInputBar.kt", r'''package com.example.voiceassistant.ui.components

import android.content.Intent
import android.net.Uri
import android.provider.OpenableColumns
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.AttachFile
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Image
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import com.example.voiceassistant.data.AttachmentData
import com.example.voiceassistant.viewmodel.AppLanguage
import com.example.voiceassistant.viewmodel.AssistantStatus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * Bottom bar in ONE row: [file] [image] [text field] [microphone] [send].
 * The microphone is always visible next to the text field.
 * onSend receives the typed text (may be empty when only a file is sent) and the attachment.
 */
@Composable
fun ChatInputBar(
    language: AppLanguage,
    micStatus: AssistantStatus,
    onMicClick: () -> Unit,
    onSend: (String, AttachmentData?) -> Unit,
    onFocusChange: (Boolean) -> Unit = {}
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var text by remember { mutableStateOf("") }
    var attachment by remember { mutableStateOf<AttachmentData?>(null) }

    // Reads the chosen file (name, type and bytes) off the main thread.
    fun loadAttachment(uri: Uri?) {
        if (uri == null) return
        scope.launch {
            val loaded = withContext(Dispatchers.IO) {
                val resolver = context.contentResolver
                val mime = resolver.getType(uri) ?: "application/octet-stream"
                var name = "file"
                resolver.query(uri, null, null, null, null)?.use { cursor ->
                    val index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                    if (cursor.moveToFirst() && index >= 0) {
                        name = cursor.getString(index) ?: name
                    }
                }
                resolver.openInputStream(uri)?.use { stream ->
                    AttachmentData(name, mime, stream.readBytes(), uri.toString())
                }
            }
            if (loaded != null) attachment = loaded
        }
    }

    val pickImage = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        loadAttachment(uri)
    }
    // OpenDocument (instead of GetContent) so a code file can later be overwritten with the edited version.
    val pickFile = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            val resolver = context.contentResolver
            try {
                resolver.takePersistableUriPermission(
                    uri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                )
            } catch (e: Exception) {
                // This provider is read-only: reading still works, writing back will fall back to "Save".
                try {
                    resolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } catch (_: Exception) {
                }
            }
        }
        loadAttachment(uri)
    }

    fun send() {
        val clean = text.trim()
        if (clean.isEmpty() && attachment == null) return
        onSend(clean, attachment)
        text = ""
        attachment = null
    }

    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        attachment?.let { att ->
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Filled.AttachFile,
                    contentDescription = null,
                    modifier = Modifier.size(18.dp)
                )
                Text(
                    text = att.name,
                    modifier = Modifier
                        .weight(1f)
                        .padding(start = 6.dp),
                    style = MaterialTheme.typography.bodySmall,
                    maxLines = 1
                )
                IconButton(onClick = { attachment = null }) {
                    Icon(
                        imageVector = Icons.Filled.Close,
                        contentDescription = language.tr("إزالة المرفق", "Remove attachment")
                    )
                }
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = { pickFile.launch(arrayOf("*/*")) }) {
                Icon(
                    imageVector = Icons.Filled.AttachFile,
                    contentDescription = language.tr("إرسال ملف", "Send file")
                )
            }
            IconButton(onClick = { pickImage.launch("image/*") }) {
                Icon(
                    imageVector = Icons.Filled.Image,
                    contentDescription = language.tr("إرسال صورة", "Send image")
                )
            }
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                modifier = Modifier
                    .weight(1f)
                    .onFocusChanged { onFocusChange(it.isFocused) },
                placeholder = { Text(language.tr("اكتب رسالتك...", "Type a message...")) },
                maxLines = 4,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                keyboardActions = KeyboardActions(onSend = { send() })
            )
            MicButton(
                status = micStatus,
                onClick = onMicClick,
                compact = true
            )
            IconButton(onClick = { send() }) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.Send,
                    contentDescription = language.tr("إرسال", "Send")
                )
            }
        }
    }
}
''')

# 42. ConversationRepository: رسالة مستخدم تحمل صورة مرفقة
insert_before(
    "app/src/main/java/com/example/voiceassistant/data/ConversationRepository.kt",
    "    fun clear() {\n",
    r'''    /** Adds a user message that also shows an attached picture. */
    fun addUserMessageWithImage(text: String, imagePath: String?): Message =
        add(text, isUser = true, imagePath = imagePath)

''')

# 43. AiChatService: إرسال سؤال مع ملف (صورة / PDF / نص) إلى Gemini
insert_before(
    "app/src/main/java/com/example/voiceassistant/data/AiChatService.kt",
    "    private fun turn(role: String, text: String): JSONObject =\n",
    r'''    /** Sends a question together with one attached file (image, PDF or text) to Gemini. */
    suspend fun askWithFile(
        text: String,
        lang: AppLanguage,
        mime: String,
        name: String,
        bytes: ByteArray
    ): AiResult = withContext(Dispatchers.IO) {
        if (!isConfigured()) return@withContext AiResult.Error(AiError.NOT_CONFIGURED)

        val isMedia = mime.startsWith("image/") || mime == "application/pdf"
        val parts = JSONArray()
        if (isMedia) {
            parts.put(JSONObject().put("text", text))
            parts.put(
                JSONObject().put(
                    "inline_data",
                    JSONObject()
                        .put("mime_type", mime)
                        .put("data", java.util.Base64.getEncoder().encodeToString(bytes))
                )
            )
        } else {
            // Any other file is sent as plain text, so it must be valid UTF-8 and reasonably small.
            if (bytes.size > 1_000_000) {
                return@withContext AiResult.Error(AiError.OTHER, lang.tr("الملف النصي كبير جداً.", "Text file is too large."))
            }
            val decoded = try {
                Charsets.UTF_8.newDecoder()
                    .onMalformedInput(java.nio.charset.CodingErrorAction.REPORT)
                    .decode(java.nio.ByteBuffer.wrap(bytes))
                    .toString()
            } catch (e: java.nio.charset.CharacterCodingException) {
                return@withContext AiResult.Error(AiError.OTHER, lang.tr("نوع هذا الملف غير مدعوم (الصور و PDF والملفات النصية فقط).", "This file type is not supported (images, PDF and text files only)."))
            }
            parts.put(JSONObject().put("text", "$text\n\n--- ${lang.tr("محتوى الملف", "File content")}: $name ---\n$decoded"))
        }

        try {
            val contents = JSONArray()
            synchronized(lock) {
                history.forEach { (role, t) -> contents.put(turn(role, t)) }
            }
            contents.put(JSONObject().put("role", "user").put("parts", parts))

            val body = JSONObject()
                .put(
                    "system_instruction",
                    JSONObject().put("parts", JSONArray().put(JSONObject().put("text", systemPrompt(lang))))
                )
                .put("contents", contents)
                .put("generationConfig", JSONObject().put("maxOutputTokens", 16384))

            var lastError: AiResult.Error = AiResult.Error(AiError.OTHER, "No models tried")
            for (modelName in activeModels()) {
                try {
                    val request = Request.Builder()
                        .url("$GEMINI_BASE$modelName:generateContent")
                        .header("x-goog-api-key", GEMINI_API_KEY)
                        .post(body.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
                        .build()

                    val result: AiResult? = longClient.newCall(request).execute().use { response ->
                        val raw = response.body?.string().orEmpty()
                        if (!response.isSuccessful) {
                            if (response.code == 404) unavailableModels.add(modelName)
                            lastError = AiResult.Error(kindForGemini(response.code, raw), apiError(response.code, raw))
                            null
                        } else {
                            val full = extractGeminiText(raw)
                            if (full.isBlank()) {
                                lastError = AiResult.Error(AiError.EMPTY)
                                null
                            } else {
                                val (spoken, code) = splitCode(full, lang)
                                remember("$text [$name]", full)
                                AiResult.Success(spoken, code)
                            }
                        }
                    }
                    if (result != null) return@withContext result
                } catch (e: IOException) {
                    lastError = AiResult.Error(AiError.NETWORK, e.toString().take(160))
                } catch (e: CancellationException) {
                    throw e
                } catch (e: Exception) {
                    lastError = AiResult.Error(AiError.OTHER, e.toString().take(160))
                }
            }
            return@withContext lastError
        } catch (e: IOException) {
            AiResult.Error(AiError.NETWORK, e.toString().take(160))
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            AiResult.Error(AiError.OTHER, e.toString().take(160))
        }
    }

''')

# 44. MainViewModel: إرسال النص المكتوب (مع مرفق اختياري)
insert_before(
    "app/src/main/java/com/example/voiceassistant/viewmodel/MainViewModel.kt",
    "    private fun process(text: String, speak: Boolean = true) {\n",
    r'''    private val maxWorkingFileBytes = 300_000

    private fun decodeUtf8(bytes: ByteArray): String? = try {
        Charsets.UTF_8.newDecoder()
            .onMalformedInput(java.nio.charset.CodingErrorAction.REPORT)
            .onUnmappableCharacter(java.nio.charset.CodingErrorAction.REPORT)
            .decode(java.nio.ByteBuffer.wrap(bytes))
            .toString()
            .removePrefix("\uFEFF")
    } catch (e: java.nio.charset.CharacterCodingException) {
        null
    }

    /** Stops editing the current code file (the chip next to the input bar). */
    fun clearWorkingFile() {
        ai.workingFile = null
        _uiState.update { it.copy(workingFileName = null) }
    }

    /** Text typed on the keyboard, optionally with one attached picture or file. */
    fun sendTyped(text: String, attachment: com.example.voiceassistant.data.AttachmentData? = null) {
        if (_uiState.value.status == AssistantStatus.PROCESSING) return
        val clean = text.trim()
        if (clean.isEmpty() && attachment == null) return
        val lang = if (clean.isEmpty()) _uiState.value.language else AppLanguage.detect(clean)

        if (attachment != null &&
            attachment.bytes.size > com.example.voiceassistant.data.AttachmentData.MAX_BYTES
        ) {
            reply(lang.tr("الملف كبير جداً (الحد الأقصى 15 ميغابايت).", "The file is too large (15 MB max)."), lang, speak = false)
            return
        }

        silentStrikes = 0
        viewModelScope.launch {
            // Plain typed text goes through the same path as spoken text (phone commands, AI, images).
            if (attachment == null) {
                repository.addUserMessage(clean)
                // Typed -> silent: the user reads the answer, nothing is spoken.
                process(clean, speak = false)
                return@launch
            }

            // Code / text file: it becomes the "working file", so later requests (typed or spoken) can
            // read, explain and edit it. Images and PDFs still go through askWithFile below.
            val isMedia = attachment.mime.startsWith("image/") || attachment.mime == "application/pdf"
            if (!isMedia) {
                val content = withContext(Dispatchers.Default) { decodeUtf8(attachment.bytes) }
                if (content == null) {
                    reply(
                        lang.tr(
                            "نوع هذا الملف غير مدعوم (الصور و PDF والملفات النصية والأكواد فقط).",
                            "This file type is not supported (images, PDF, text and code files only)."
                        ),
                        lang,
                        speak = false
                    )
                    return@launch
                }
                if (attachment.bytes.size > maxWorkingFileBytes) {
                    reply(
                        lang.tr(
                            "الملف كبير جداً للتعديل (الحد الأقصى 300 كيلوبايت).",
                            "The file is too large to edit (300 KB max)."
                        ),
                        lang,
                        speak = false
                    )
                    return@launch
                }
                ai.workingFile = com.example.voiceassistant.data.WorkingFile(attachment.name, attachment.uri, content)
                _uiState.update {
                    it.copy(workingFileName = attachment.name, status = AssistantStatus.PROCESSING, partialText = "")
                }
                val fileHeader = "📎 ${attachment.name}"
                repository.addUserMessage(if (clean.isEmpty()) fileHeader else "$fileHeader\n$clean")
                askAi(
                    clean.ifEmpty {
                        lang.tr(
                            "اقرأ هذا الملف ولخّص ما يفعله وأي مشاكل واضحة فيه.",
                            "Read this file, summarize what it does and any obvious problems in it."
                        )
                    },
                    lang,
                    speak = false
                )
                return@launch
            }

            // A picture is shown in the chat; any file is shown by its name.
            val imagePath = if (attachment.mime.startsWith("image/")) {
                withContext(Dispatchers.IO) { saveImage(attachment.bytes) }
            } else {
                null
            }
            val header = "📎 ${attachment.name}"
            repository.addUserMessageWithImage(
                if (clean.isEmpty()) header else "$header\n$clean",
                imagePath
            )
            _uiState.update { it.copy(status = AssistantStatus.PROCESSING, partialText = "") }

            val prompt = clean.ifEmpty { lang.tr("حلّل هذا الملف واشرحه.", "Analyze this file and explain it.") }
            when (val result = ai.askWithFile(prompt, lang, attachment.mime, attachment.name, attachment.bytes)) {
                is AiResult.Success -> reply(result.text, lang, result.code, speak = false)
                is AiResult.Error -> replyAiError(result.kind, result.detail, lang, speak = false)
            }
        }
    }

''')

# 45. MainScreen: استيراد شريط الإدخال ووضعه فوق زر الميكروفون
_main_screen_path = "app/src/main/java/com/example/voiceassistant/ui/MainScreen.kt"
with open(_main_screen_path, "r", encoding="utf-8") as _f:
    _main_screen_has_input_bar = "import com.example.voiceassistant.ui.components.ChatInputBar\n" in _f.read()
if not _main_screen_has_input_bar:
    insert_before(
        _main_screen_path,
        "import com.example.voiceassistant.ui.components.LanguageToggle\n",
        "import com.example.voiceassistant.ui.components.ChatInputBar\n")


# ------------------------------------------------------------------------------
# الإضافة: شخصيات الأنمي المتحركة (تستبدل شكل الروبوت) + التبديل بينها
# ------------------------------------------------------------------------------
write_file("app/src/main/java/com/example/voiceassistant/ui/components/AnimeCharacter.kt", r'''package com.example.voiceassistant.ui.components

import android.content.Context
import android.content.SharedPreferences
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.platform.LocalContext
import com.example.voiceassistant.viewmodel.AppLanguage

/** شكل الشعر: يحدد طريقة رسم الشعر الخلفي والأمامي. */
enum class HairStyle { TWIN_TAILS, BOB, SPIKY, LONG }

/** إكسسوار مميز لكل شخصية. */
enum class Accessory { RIBBONS, CAT_EARS, HEADBAND, HAIRPIN }

/**
 * شخصية أنمي مرسومة بالكامل بالكود (Canvas) — بدون صور ولا مكتبات خارجية.
 * لإضافة شخصية جديدة: أضف عنصراً إلى [AnimeCharacters.all] فقط.
 */
data class AnimeCharacter(
    val id: String,
    val nameAr: String,
    val nameEn: String,
    val hairStyle: HairStyle,
    val accessory: Accessory,
    val hair: Color,
    val hairShade: Color,
    val eye: Color,
    val skin: Color,
    val outfit: Color,
    val accent: Color,
    val aura: Color
) {
    val skinShade: Color get() = lerp(skin, Color(0xFF8D4F3F), 0.22f)
    val eyeDark: Color get() = lerp(eye, Color.Black, 0.5f)

    fun name(language: AppLanguage): String = language.tr(nameAr, nameEn)
}

object AnimeCharacters {
    val all: List<AnimeCharacter> = listOf(
        AnimeCharacter(
            id = "hikari", nameAr = "هيكاري", nameEn = "Hikari",
            hairStyle = HairStyle.TWIN_TAILS, accessory = Accessory.RIBBONS,
            hair = Color(0xFFFFB04A), hairShade = Color(0xFFE07B1F),
            eye = Color(0xFF39A8FF), skin = Color(0xFFFFE3D1),
            outfit = Color(0xFF2F3E8F), accent = Color(0xFFE53950),
            aura = Color(0xFFFFC27A)
        ),
        AnimeCharacter(
            id = "ryo", nameAr = "ريو", nameEn = "Ryo",
            hairStyle = HairStyle.SPIKY, accessory = Accessory.HEADBAND,
            hair = Color(0xFF3D6BFF), hairShade = Color(0xFF2342B8),
            eye = Color(0xFFFFB300), skin = Color(0xFFF8D5BC),
            outfit = Color(0xFF00897B), accent = Color(0xFFFFD54F),
            aura = Color(0xFF7FA2FF)
        ),
        AnimeCharacter(
            id = "luna", nameAr = "لونا", nameEn = "Luna",
            hairStyle = HairStyle.LONG, accessory = Accessory.HAIRPIN,
            hair = Color(0xFFD1C4F5), hairShade = Color(0xFF9575CD),
            eye = Color(0xFFE040FB), skin = Color(0xFFFFE9DD),
            outfit = Color(0xFF1A237E), accent = Color(0xFFFFD54F),
            aura = Color(0xFFB39DDB)
        ),
        AnimeCharacter(
            id = "momo", nameAr = "مومو", nameEn = "Momo",
            hairStyle = HairStyle.BOB, accessory = Accessory.CAT_EARS,
            hair = Color(0xFF7FDCC8), hairShade = Color(0xFF3FB8A0),
            eye = Color(0xFFFF6F91), skin = Color(0xFFFFE0CC),
            outfit = Color(0xFFF48FB1), accent = Color(0xFFFF80AB),
            aura = Color(0xFF9CE8D8)
        )
    )

    fun byId(id: String?): AnimeCharacter = all.firstOrNull { it.id == id } ?: all.first()
}

/** يحفظ الشخصية المختارة في SharedPreferences لتبقى بعد إغلاق التطبيق. */
class CharacterSelection(private val prefs: SharedPreferences) {

    var current: AnimeCharacter by mutableStateOf(
        AnimeCharacters.byId(prefs.getString(KEY, null))
    )
        private set

    fun select(character: AnimeCharacter) {
        current = character
        prefs.edit().putString(KEY, character.id).apply()
    }

    /** الشخصية التالية (للتبديل بالضغط على الشخصية). */
    fun next() {
        val all = AnimeCharacters.all
        val index = all.indexOfFirst { it.id == current.id }
        select(all[(index + 1) % all.size])
    }

    private companion object {
        const val KEY = "avatar_character"
    }
}

@Composable
fun rememberCharacterSelection(): CharacterSelection {
    val context = LocalContext.current
    return remember {
        CharacterSelection(
            context.applicationContext.getSharedPreferences("avatar_prefs", Context.MODE_PRIVATE)
        )
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/ui/components/AnimeCharacterPainter.kt", r'''package com.example.voiceassistant.ui.components

import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.lerp
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.sin

internal const val TWO_PI = 6.2831855f

private val Ink = Color(0xFF2B2233)
private val MouthInside = Color(0xFF7A2335)
private val Tongue = Color(0xFFFF8FA3)
private val BlushColor = Color(0xFFFF5C7A)
private val SweatColor = Color(0xFF8EC9FF)

/**
 * "وضعية" الشخصية في لحظة معينة. كل القيم بين 0 و 1 (ما لم يُذكر غير ذلك).
 * AnimeAvatar يبني هذه الوضعية في كل إطار حسب حالة المساعد.
 */
data class AvatarPose(
    /** 1 = العين مفتوحة، 0 = مغلقة (للرمش). */
    val blink: Float = 1f,
    val eyeScale: Float = 1f,
    /** فتحة الفم (للكلام). */
    val mouthOpen: Float = 0f,
    /** 1 = ابتسامة، 0 = مستقيم، -1 = عبوس. */
    val mouthCurve: Float = 1f,
    /** اتجاه النظر -1..1. */
    val lookX: Float = 0f,
    val lookY: Float = 0f,
    val browLift: Float = 0f,
    val browSad: Float = 0f,
    val blush: Float = 0.3f,
    /** فقاعة التفكير (PROCESSING). */
    val thinking: Float = 0f,
    /** حلقات الاستماع (LISTENING). */
    val ring: Float = 0f,
    /** قطرة العرق (ERROR). */
    val sweat: Float = 0f,
    /** النجوم المتلألئة (SPEAKING). */
    val sparkle: Float = 0f,
    /** مرحلة حركة دورية 0..1 تُستخدم للنقاط والحلقات والنجوم. */
    val phase: Float = 0f
)

/** يرسم الشخصية داخل مربع (يستعمل size.minDimension) — كل الإحداثيات بالأسفل نسب من 0 إلى 1. */
fun DrawScope.drawAnimeCharacter(character: AnimeCharacter, pose: AvatarPose) {
    scale(scale = size.minDimension, pivot = Offset.Zero) {
        drawAura(character, pose)
        drawBackHair(character)
        drawBody(character)
        drawFace(character, pose)
        drawFrontHair(character)
        drawOverlays(character, pose)
    }
}

// ------------------------------------------------------------------ الخلفية

private fun DrawScope.drawAura(c: AnimeCharacter, pose: AvatarPose) {
    val center = Offset(0.5f, 0.5f)
    drawCircle(
        brush = Brush.radialGradient(
            colors = listOf(c.aura.copy(alpha = 0.55f), c.aura.copy(alpha = 0f)),
            center = center,
            radius = 0.5f
        ),
        radius = 0.5f,
        center = center
    )
    if (pose.ring > 0.01f) {
        listOf(pose.phase, (pose.phase + 0.5f) % 1f).forEach { p ->
            drawCircle(
                color = c.accent.copy(alpha = (1f - p) * 0.6f * pose.ring),
                radius = 0.34f + 0.16f * p,
                center = center,
                style = Stroke(width = 0.008f)
            )
        }
    }
}

// ------------------------------------------------------------------ الشعر الخلفي

private fun tailPath(mirror: Boolean): Path {
    fun x(v: Float) = if (mirror) 1f - v else v
    return Path().apply {
        moveTo(x(0.25f), 0.30f)
        cubicTo(x(0.04f), 0.36f, x(0.00f), 0.72f, x(0.10f), 0.97f)
        cubicTo(x(0.21f), 0.82f, x(0.27f), 0.62f, x(0.31f), 0.46f)
        close()
    }
}

private fun longBackPath(): Path = Path().apply {
    moveTo(0.22f, 0.32f)
    cubicTo(0.12f, 0.50f, 0.14f, 0.80f, 0.12f, 0.98f)
    lineTo(0.88f, 0.98f)
    cubicTo(0.86f, 0.80f, 0.88f, 0.50f, 0.78f, 0.32f)
    close()
}

private fun DrawScope.drawBackHair(c: AnimeCharacter) {
    val longBrush = Brush.verticalGradient(
        colors = listOf(c.hair, c.hairShade),
        startY = 0.3f,
        endY = 1f
    )
    when (c.hairStyle) {
        HairStyle.TWIN_TAILS -> {
            drawPath(tailPath(false), longBrush)
            drawPath(tailPath(true), longBrush)
        }
        HairStyle.LONG -> drawPath(longBackPath(), longBrush)
        HairStyle.BOB -> drawRoundRect(
            color = c.hairShade,
            topLeft = Offset(0.19f, 0.20f),
            size = Size(0.62f, 0.50f),
            cornerRadius = CornerRadius(0.20f)
        )
        HairStyle.SPIKY -> drawRoundRect(
            color = c.hairShade,
            topLeft = Offset(0.20f, 0.20f),
            size = Size(0.60f, 0.36f),
            cornerRadius = CornerRadius(0.15f)
        )
    }
}

// ------------------------------------------------------------------ الجسم

private fun DrawScope.drawBody(c: AnimeCharacter) {
    // الرقبة
    drawRoundRect(
        color = c.skinShade,
        topLeft = Offset(0.445f, 0.68f),
        size = Size(0.11f, 0.15f),
        cornerRadius = CornerRadius(0.03f)
    )
    // الكتفان / الملابس
    val body = Path().apply {
        moveTo(0.12f, 1f)
        cubicTo(0.12f, 0.84f, 0.30f, 0.77f, 0.50f, 0.77f)
        cubicTo(0.70f, 0.77f, 0.88f, 0.84f, 0.88f, 1f)
        close()
    }
    drawPath(body, c.outfit)
    drawPath(
        body,
        Brush.verticalGradient(
            colors = listOf(Color.White.copy(alpha = 0.14f), Color.Transparent),
            startY = 0.77f,
            endY = 1f
        )
    )
    // فتحة الياقة
    val collar = Path().apply {
        moveTo(0.41f, 0.775f)
        lineTo(0.50f, 0.875f)
        lineTo(0.59f, 0.775f)
        close()
    }
    drawPath(collar, c.skin)
    drawBow(c.accent, Offset(0.5f, 0.885f), 0.045f)
}

// ------------------------------------------------------------------ الوجه

private fun facePath(): Path = Path().apply {
    moveTo(0.24f, 0.42f)
    cubicTo(0.24f, 0.14f, 0.76f, 0.14f, 0.76f, 0.42f)
    cubicTo(0.76f, 0.58f, 0.64f, 0.73f, 0.50f, 0.75f)
    cubicTo(0.36f, 0.73f, 0.24f, 0.58f, 0.24f, 0.42f)
    close()
}

private fun DrawScope.drawFace(c: AnimeCharacter, pose: AvatarPose) {
    // الأذنان
    drawOval(c.skin, Offset(0.215f, 0.49f), Size(0.04f, 0.07f))
    drawOval(c.skin, Offset(0.745f, 0.49f), Size(0.04f, 0.07f))

    val face = facePath()
    drawPath(face, c.skin)
    // ظل خفيف تحت الغرة
    clipPath(face) {
        drawRect(
            brush = Brush.verticalGradient(
                colors = listOf(c.skinShade.copy(alpha = 0.55f), Color.Transparent),
                startY = 0.28f,
                endY = 0.46f
            ),
            topLeft = Offset(0.2f, 0.2f),
            size = Size(0.6f, 0.3f)
        )
    }

    // احمرار الخدين
    if (pose.blush > 0.01f) {
        val blush = BlushColor.copy(alpha = (pose.blush * 0.5f).coerceIn(0f, 1f))
        drawOval(blush, Offset(0.29f, 0.615f), Size(0.09f, 0.04f))
        drawOval(blush, Offset(0.62f, 0.615f), Size(0.09f, 0.04f))
    }

    drawBrow(c, pose, 0.385f, left = true)
    drawBrow(c, pose, 0.615f, left = false)
    drawEye(c, pose, 0.385f, 0.525f, left = true)
    drawEye(c, pose, 0.615f, 0.525f, left = false)

    // الأنف
    drawCircle(c.skinShade.copy(alpha = 0.8f), 0.005f, Offset(0.5f, 0.625f))
    drawMouth(pose)
}

private fun DrawScope.drawBrow(c: AnimeCharacter, pose: AvatarPose, cx: Float, left: Boolean) {
    val inner = if (left) 1f else -1f // الاتجاه نحو منتصف الوجه
    val baseY = 0.425f - pose.browLift * 0.018f
    val outer = Offset(cx - inner * 0.058f, baseY + pose.browSad * 0.010f)
    val innerPt = Offset(cx + inner * 0.058f, baseY - pose.browSad * 0.026f)
    drawLine(c.hairShade, outer, innerPt, strokeWidth = 0.012f, cap = StrokeCap.Round)
}

private fun DrawScope.drawEye(
    c: AnimeCharacter,
    pose: AvatarPose,
    cx: Float,
    cy: Float,
    left: Boolean
) {
    val w = 0.135f * pose.eyeScale
    val h = max(0.004f, 0.17f * pose.eyeScale * pose.blink)
    val rect = Rect(cx - w / 2f, cy - h / 2f, cx + w / 2f, cy + h / 2f)
    val eyePath = Path().apply { addOval(rect) }

    drawPath(eyePath, Color.White)
    clipPath(eyePath) {
        val irisW = 0.098f * pose.eyeScale
        val irisH = 0.15f * pose.eyeScale
        val ix = cx + pose.lookX * 0.018f
        val iy = cy + pose.lookY * 0.02f
        drawOval(
            brush = Brush.verticalGradient(
                colors = listOf(c.eyeDark, c.eye, lerp(c.eye, Color.White, 0.25f)),
                startY = iy - irisH / 2f,
                endY = iy + irisH / 2f
            ),
            topLeft = Offset(ix - irisW / 2f, iy - irisH / 2f),
            size = Size(irisW, irisH)
        )
        // البؤبؤ
        drawOval(Color(0xFF1B1B2B), Offset(ix - 0.027f, iy - 0.04f), Size(0.054f, 0.08f))
        // لمعة العين
        drawCircle(Color.White, 0.02f, Offset(ix - 0.022f, iy - 0.035f))
        drawCircle(Color.White.copy(alpha = 0.85f), 0.009f, Offset(ix + 0.02f, iy + 0.03f))
    }
    // الرمش العلوي
    drawArc(
        color = Ink,
        startAngle = 180f,
        sweepAngle = 180f,
        useCenter = false,
        topLeft = rect.topLeft,
        size = rect.size,
        style = Stroke(width = 0.012f, cap = StrokeCap.Round)
    )
    // ذيل الرمش الخارجي
    val dir = if (left) -1f else 1f
    drawLine(
        color = Ink,
        start = Offset(cx + dir * w / 2f, cy - h * 0.1f),
        end = Offset(cx + dir * (w / 2f + 0.014f), cy - h * 0.32f - 0.004f),
        strokeWidth = 0.011f,
        cap = StrokeCap.Round
    )
}

private fun DrawScope.drawMouth(pose: AvatarPose) {
    val cx = 0.5f
    val cy = 0.675f
    if (pose.mouthOpen > 0.06f) {
        val w = 0.05f + pose.mouthOpen * 0.03f
        val h = 0.012f + pose.mouthOpen * 0.05f
        val rect = Rect(cx - w / 2f, cy - h / 2f + 0.005f, cx + w / 2f, cy + h / 2f + 0.005f)
        val mouth = Path().apply { addOval(rect) }
        drawPath(mouth, MouthInside)
        clipPath(mouth) {
            drawOval(Tongue, Offset(cx - w * 0.35f, cy + h * 0.05f), Size(w * 0.7f, h * 0.6f))
        }
        return
    }
    val amount = abs(pose.mouthCurve)
    if (amount < 0.1f) {
        drawLine(
            color = Ink,
            start = Offset(cx - 0.025f, cy),
            end = Offset(cx + 0.025f, cy),
            strokeWidth = 0.010f,
            cap = StrokeCap.Round
        )
    } else {
        val depth = 0.04f * amount
        val smile = pose.mouthCurve > 0f
        val cy0 = if (smile) cy - depth / 2f else cy + depth / 2f
        drawArc(
            color = Ink,
            startAngle = if (smile) 20f else 200f,
            sweepAngle = 140f,
            useCenter = false,
            topLeft = Offset(cx - 0.035f, cy0 - depth),
            size = Size(0.07f, depth * 2f),
            style = Stroke(width = 0.010f, cap = StrokeCap.Round)
        )
    }
}

// ------------------------------------------------------------------ الشعر الأمامي

/** الغرة: خط سفلي متعرّج يبدأ من اليمين إلى اليسار. */
private fun Path.bangsToLeft() {
    lineTo(0.75f, 0.39f)
    lineTo(0.70f, 0.40f)
    lineTo(0.655f, 0.335f)
    lineTo(0.60f, 0.395f)
    lineTo(0.55f, 0.33f)
    lineTo(0.50f, 0.395f)
    lineTo(0.45f, 0.33f)
    lineTo(0.40f, 0.395f)
    lineTo(0.345f, 0.335f)
    lineTo(0.30f, 0.40f)
    lineTo(0.25f, 0.39f)
    close()
}

private fun roundCapPath(): Path = Path().apply {
    moveTo(0.215f, 0.50f)
    cubicTo(0.15f, 0.06f, 0.85f, 0.06f, 0.785f, 0.50f)
    bangsToLeft()
}

private fun spikyCapPath(): Path = Path().apply {
    moveTo(0.215f, 0.50f)
    lineTo(0.15f, 0.24f)
    lineTo(0.27f, 0.28f)
    lineTo(0.25f, 0.07f)
    lineTo(0.40f, 0.18f)
    lineTo(0.50f, 0.02f)
    lineTo(0.60f, 0.18f)
    lineTo(0.75f, 0.07f)
    lineTo(0.73f, 0.28f)
    lineTo(0.85f, 0.24f)
    lineTo(0.785f, 0.50f)
    bangsToLeft()
}

private fun DrawScope.sideLocks(c: AnimeCharacter, top: Float, height: Float, width: Float) {
    val r = CornerRadius(width / 2f)
    drawRoundRect(c.hair, Offset(0.205f, top), Size(width, height), r)
    drawRoundRect(c.hair, Offset(0.795f - width, top), Size(width, height), r)
}

private fun DrawScope.drawCatEars(c: AnimeCharacter) {
    listOf(false, true).forEach { mirror ->
        fun x(v: Float) = if (mirror) 1f - v else v
        val outer = Path().apply {
            moveTo(x(0.25f), 0.26f)
            lineTo(x(0.27f), 0.04f)
            lineTo(x(0.43f), 0.17f)
            close()
        }
        val inner = Path().apply {
            moveTo(x(0.285f), 0.22f)
            lineTo(x(0.295f), 0.10f)
            lineTo(x(0.38f), 0.17f)
            close()
        }
        drawPath(outer, c.hair)
        drawPath(inner, c.accent.copy(alpha = 0.75f))
    }
}

private fun DrawScope.drawFrontHair(c: AnimeCharacter) {
    if (c.accessory == Accessory.CAT_EARS) drawCatEars(c)

    val cap = if (c.hairStyle == HairStyle.SPIKY) spikyCapPath() else roundCapPath()
    drawPath(
        cap,
        Brush.verticalGradient(
            colors = listOf(lerp(c.hair, Color.White, 0.2f), c.hair),
            startY = 0.05f,
            endY = 0.42f
        )
    )
    // لمعة الشعر
    drawArc(
        color = Color.White.copy(alpha = 0.35f),
        startAngle = 205f,
        sweepAngle = 55f,
        useCenter = false,
        topLeft = Offset(0.30f, 0.20f),
        size = Size(0.40f, 0.26f),
        style = Stroke(width = 0.016f, cap = StrokeCap.Round)
    )

    when (c.hairStyle) {
        HairStyle.BOB -> sideLocks(c, top = 0.30f, height = 0.38f, width = 0.085f)
        HairStyle.LONG -> sideLocks(c, top = 0.30f, height = 0.52f, width = 0.07f)
        HairStyle.TWIN_TAILS -> sideLocks(c, top = 0.30f, height = 0.26f, width = 0.06f)
        HairStyle.SPIKY -> sideLocks(c, top = 0.34f, height = 0.18f, width = 0.05f)
    }

    when (c.accessory) {
        Accessory.RIBBONS -> {
            drawBow(c.accent, Offset(0.25f, 0.31f), 0.05f)
            drawBow(c.accent, Offset(0.75f, 0.31f), 0.05f)
        }
        Accessory.HEADBAND -> {
            val band = Path().apply {
                moveTo(0.215f, 0.36f)
                cubicTo(0.30f, 0.20f, 0.70f, 0.20f, 0.785f, 0.36f)
            }
            drawPath(band, c.accent, style = Stroke(width = 0.03f, cap = StrokeCap.Round))
            drawRoundRect(
                color = Color(0xFFCFD8DC),
                topLeft = Offset(0.465f, 0.22f),
                size = Size(0.07f, 0.04f),
                cornerRadius = CornerRadius(0.01f)
            )
        }
        Accessory.HAIRPIN -> {
            drawSparkle(Offset(0.66f, 0.30f), 0.035f, c.accent)
            drawCircle(Color.White.copy(alpha = 0.8f), 0.006f, Offset(0.66f, 0.30f))
        }
        Accessory.CAT_EARS -> Unit
    }
}

// ------------------------------------------------------------------ تأثيرات الحالات

private fun DrawScope.drawOverlays(c: AnimeCharacter, pose: AvatarPose) {
    // PROCESSING: فقاعة تفكير بثلاث نقاط تقفز
    if (pose.thinking > 0.01f) {
        val a = pose.thinking.coerceIn(0f, 1f)
        val white = Color.White.copy(alpha = 0.92f * a)
        drawRoundRect(white, Offset(0.65f, 0.03f), Size(0.30f, 0.12f), CornerRadius(0.06f))
        drawCircle(white, 0.014f, Offset(0.67f, 0.18f))
        drawCircle(white, 0.008f, Offset(0.655f, 0.205f))
        for (i in 0..2) {
            val bounce = max(0f, sin((pose.phase - i * 0.18f) * TWO_PI))
            drawCircle(
                color = c.accent.copy(alpha = a),
                radius = 0.016f + 0.006f * bounce,
                center = Offset(0.72f + i * 0.075f, 0.09f - 0.012f * bounce)
            )
        }
    }

    // SPEAKING: نجوم متلألئة
    if (pose.sparkle > 0.01f) {
        val spots = listOf(
            Offset(0.10f, 0.24f) to 0f,
            Offset(0.90f, 0.34f) to 0.33f,
            Offset(0.06f, 0.55f) to 0.66f
        )
        spots.forEach { (pos, offset) ->
            val t = (sin((pose.phase + offset) * TWO_PI) + 1f) / 2f
            drawSparkle(
                center = pos,
                r = 0.02f + 0.03f * t,
                color = c.accent.copy(alpha = (pose.sparkle * (0.35f + 0.65f * t)).coerceIn(0f, 1f))
            )
        }
    }

    // ERROR: قطرة عرق
    if (pose.sweat > 0.01f) {
        val x = 0.79f
        val y = 0.50f
        val drop = Path().apply {
            moveTo(x, y - 0.045f)
            cubicTo(x + 0.03f, y - 0.01f, x + 0.03f, y + 0.03f, x, y + 0.03f)
            cubicTo(x - 0.03f, y + 0.03f, x - 0.03f, y - 0.01f, x, y - 0.045f)
            close()
        }
        drawPath(drop, SweatColor.copy(alpha = pose.sweat.coerceIn(0f, 1f)))
    }
}

// ------------------------------------------------------------------ أدوات مساعدة

private fun DrawScope.drawBow(color: Color, center: Offset, size: Float) {
    val left = Path().apply {
        moveTo(center.x, center.y)
        lineTo(center.x - size, center.y - size * 0.8f)
        lineTo(center.x - size, center.y + size * 0.8f)
        close()
    }
    val right = Path().apply {
        moveTo(center.x, center.y)
        lineTo(center.x + size, center.y - size * 0.8f)
        lineTo(center.x + size, center.y + size * 0.8f)
        close()
    }
    drawPath(left, color)
    drawPath(right, color)
    drawCircle(lerp(color, Color.Black, 0.25f), size * 0.35f, center)
}

/** نجمة رباعية الرؤوس. */
private fun DrawScope.drawSparkle(center: Offset, r: Float, color: Color) {
    val cx = center.x
    val cy = center.y
    val star = Path().apply {
        moveTo(cx, cy - r)
        cubicTo(cx, cy, cx, cy, cx + r, cy)
        cubicTo(cx, cy, cx, cy, cx, cy + r)
        cubicTo(cx, cy, cx, cy, cx - r, cy)
        cubicTo(cx, cy, cx, cy, cx, cy - r)
        close()
    }
    drawPath(star, color)
}
''')

write_file("app/src/main/java/com/example/voiceassistant/ui/components/AnimeAvatar.kt", r'''package com.example.voiceassistant.ui.components

import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import com.example.voiceassistant.viewmodel.AssistantStatus
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random
import kotlinx.coroutines.delay

/**
 * شخصية الأنمي المتحركة. تتفاعل مع حالة المساعد:
 *  - IDLE:       تنفّس هادئ + رمش + ابتسامة.
 *  - LISTENING:  تميل برأسها، عيون أوسع، حواجب مرفوعة، حلقات صوتية تنتشر.
 *  - PROCESSING: تنظر للأعلى وتتحرك عيناها + فقاعة تفكير بثلاث نقاط.
 *  - SPEAKING:   الفم يتحرك مع الكلام + ارتداد خفيف + نجوم متلألئة.
 *  - ERROR:      حاجبان حزينان + عبوس + قطرة عرق.
 *
 * عند تغيير [character] يحدث تلاشٍ ناعم بين الشخصيتين.
 */
@Composable
fun AnimeAvatar(
    character: AnimeCharacter,
    status: AssistantStatus,
    modifier: Modifier = Modifier,
    contentDescription: String? = null
) {
    val semanticsModifier = if (contentDescription != null) {
        Modifier.semantics { this.contentDescription = contentDescription }
    } else {
        Modifier
    }

    Crossfade(
        targetState = character,
        modifier = modifier.then(semanticsModifier),
        animationSpec = tween(350),
        label = "avatarCrossfade"
    ) { current ->
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            AnimatedCharacter(
                character = current,
                status = status,
                modifier = Modifier
                    .fillMaxHeight()
                    .aspectRatio(1f)
            )
        }
    }
}

@Composable
private fun AnimatedCharacter(
    character: AnimeCharacter,
    status: AssistantStatus,
    modifier: Modifier
) {
    val listening = status == AssistantStatus.LISTENING
    val processing = status == AssistantStatus.PROCESSING
    val speaking = status == AssistantStatus.SPEAKING
    val error = status == AssistantStatus.ERROR

    // ---- التعابير: تنتقل بنعومة عند تغيّر الحالة
    val smooth = tween<Float>(durationMillis = 350)
    val tilt = animateFloatAsState(
        targetValue = when {
            listening -> 5f
            error -> -4f
            processing -> -2f
            else -> 0f
        },
        animationSpec = smooth, label = "tilt"
    )
    val eyeScale = animateFloatAsState(
        targetValue = when {
            listening -> 1.12f
            error -> 0.94f
            else -> 1f
        },
        animationSpec = smooth, label = "eyeScale"
    )
    val browLift = animateFloatAsState(if (listening) 1f else 0f, animationSpec = smooth, label = "browLift")
    val browSad = animateFloatAsState(if (error) 1f else 0f, animationSpec = smooth, label = "browSad")
    val blush = animateFloatAsState(
        targetValue = when {
            speaking -> 0.8f
            listening -> 0.5f
            error -> 0f
            else -> 0.3f
        },
        animationSpec = smooth, label = "blush"
    )
    val curve = animateFloatAsState(
        targetValue = when {
            error -> -1f
            processing -> 0f
            listening -> 0.4f
            else -> 1f
        },
        animationSpec = smooth, label = "curve"
    )
    val thinking = animateFloatAsState(if (processing) 1f else 0f, animationSpec = smooth, label = "thinking")
    val ring = animateFloatAsState(if (listening) 1f else 0f, animationSpec = smooth, label = "ring")
    val sweat = animateFloatAsState(if (error) 1f else 0f, animationSpec = smooth, label = "sweat")
    val sparkle = animateFloatAsState(if (speaking) 1f else 0f, animationSpec = smooth, label = "sparkle")
    val talkAmount = animateFloatAsState(if (speaking) 1f else 0f, animationSpec = tween(150), label = "talkAmount")

    // ---- حركات دائمة
    val infinite = rememberInfiniteTransition(label = "avatarLoop")
    val float = infinite.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(2600, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "float"
    )
    val phase = infinite.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(1400, easing = LinearEasing)),
        label = "phase"
    )
    // فتح/إغلاق الفم: موجتان بسرعتين مختلفتين لإحساس طبيعي
    val talkA = infinite.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(170, easing = LinearEasing), RepeatMode.Reverse),
        label = "talkA"
    )
    val talkB = infinite.animateFloat(
        initialValue = 0.55f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(430, easing = LinearEasing), RepeatMode.Reverse),
        label = "talkB"
    )

    // ---- الرمش العشوائي
    val blink = remember { Animatable(1f) }
    LaunchedEffect(Unit) {
        while (true) {
            delay(Random.nextLong(2200L, 5200L))
            blink.animateTo(0f, tween(70))
            blink.animateTo(1f, tween(120))
        }
    }

    Canvas(
        modifier = modifier.graphicsLayer {
            val s = size.height
            val breathing = (float.value - 0.5f) * 0.03f * s
            val bounce = talkA.value * 0.012f * s * talkAmount.value
            translationY = breathing - bounce
            rotationZ = tilt.value + sin(phase.value * TWO_PI) * 2f * thinking.value
            transformOrigin = TransformOrigin(0.5f, 0.85f)
        }
    ) {
        val t = phase.value * TWO_PI
        val think = thinking.value
        drawAnimeCharacter(
            character,
            AvatarPose(
                blink = blink.value,
                eyeScale = eyeScale.value,
                mouthOpen = talkA.value * talkB.value * talkAmount.value,
                mouthCurve = curve.value,
                lookX = cos(t) * think,
                lookY = (-0.6f + sin(t) * 0.3f) * think,
                browLift = browLift.value,
                browSad = browSad.value,
                blush = blush.value,
                thinking = think,
                ring = ring.value,
                sweat = sweat.value,
                sparkle = sparkle.value,
                phase = phase.value
            )
        )
    }
}

/** صورة مصغّرة ثابتة للوجه (للقائمة وزر الاختيار) — بدون أنيميشن لتخفيف الحمل. */
@Composable
fun CharacterThumbnail(character: AnimeCharacter, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.aspectRatio(1f)) {
        scale(scale = 1.75f, pivot = Offset(size.width * 0.5f, size.height * 0.42f)) {
            drawAnimeCharacter(character, AvatarPose())
        }
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/ui/components/CharacterPicker.kt", r'''package com.example.voiceassistant.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import com.example.voiceassistant.viewmodel.AppLanguage

/**
 * زر دائري (وجه الشخصية الحالية) يفتح قائمة اختيار الشخصيات.
 * يوضع داخل actions الخاصة بـ TopAppBar.
 */
@Composable
fun CharacterMenuButton(
    selected: AnimeCharacter,
    language: AppLanguage,
    onSelected: (AnimeCharacter) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    val label = language.tr("تغيير الشخصية", "Change character")

    Box(modifier = modifier) {
        IconButton(onClick = { expanded = true }) {
            Box(
                modifier = Modifier
                    .size(32.dp)
                    .clip(CircleShape)
                    .background(selected.aura.copy(alpha = 0.4f))
                    .border(1.5.dp, MaterialTheme.colorScheme.primary, CircleShape)
                    .semantics { contentDescription = label }
            ) {
                CharacterThumbnail(selected, Modifier.fillMaxSize())
            }
        }

        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            Text(
                text = language.tr("اختر الشخصية", "Choose a character"),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp)
            )
            AnimeCharacters.all.forEach { character ->
                DropdownMenuItem(
                    text = { Text(character.name(language)) },
                    leadingIcon = {
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(character.aura.copy(alpha = 0.4f))
                        ) {
                            CharacterThumbnail(character, Modifier.fillMaxSize())
                        }
                    },
                    trailingIcon = {
                        if (character.id == selected.id) {
                            Icon(Icons.Filled.Check, contentDescription = null)
                        }
                    },
                    onClick = {
                        onSelected(character)
                        expanded = false
                    }
                )
            }
        }
    }
}
''')



# ------------------------------------------------------------------------------
# الإضافة: التذكيرات الصوتية + التفاعل الاستباقي
# ------------------------------------------------------------------------------

# 46. تذكيرات صوتية: الأمر + الجدولة + المستقبِل + الخدمة الأمامية
write_file("app/src/main/java/com/example/voiceassistant/commands/commands/ReminderCommand.kt", r'''package com.example.voiceassistant.commands.commands

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.content.ContextCompat
import com.example.voiceassistant.commands.CommandResult
import com.example.voiceassistant.commands.ParsedCommand
import com.example.voiceassistant.commands.startNewTask
import com.example.voiceassistant.service.ReminderScheduler
import com.example.voiceassistant.viewmodel.AppLanguage
import java.util.Calendar
import java.util.Locale

/** «ذكرني بشرب الماء بعد 10 دقائق» -> an exact alarm that speaks the reminder even if the app is closed. */
object ReminderCommand {

    fun execute(context: Context, command: ParsedCommand.Reminder, lang: AppLanguage): CommandResult {
        val at = command.triggerAtMillis ?: return CommandResult.Failure(
            lang.tr(
                "متى تريد أن أذكّرك؟ قل مثلاً «ذكرني بشرب الماء بعد 10 دقائق» أو «ذكرني بموعد الطبيب غداً الساعة 5 مساءً».",
                "When should I remind you? Say for example \"remind me to drink water in 10 minutes\" or \"remind me about the doctor tomorrow at 5 pm\"."
            )
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) !=
            PackageManager.PERMISSION_GRANTED
        ) {
            return CommandResult.NeedsPermission(
                Manifest.permission.POST_NOTIFICATIONS,
                lang.tr("أحتاج إذن الإشعارات لكي أذكّرك.", "I need the notification permission to remind you.")
            )
        }

        val exact = ReminderScheduler.schedule(context, command.text, at)
        val whenText = describe(at, lang)
        val ok = lang.tr(
            "حسناً، سأذكّرك بـ«${command.text}» $whenText.",
            "Okay, I'll remind you about \"${command.text}\" $whenText."
        )
        if (exact) return CommandResult.Success(ok)

        // "Alarms & reminders" is off (Android 12+): the reminder still works but may be a bit late.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            try {
                context.startNewTask(
                    Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM, Uri.parse("package:${context.packageName}"))
                )
            } catch (e: Exception) {
                // settings page not available on this device
            }
        }
        return CommandResult.Success(
            ok + " " + lang.tr(
                "فعّل «التنبيهات والتذكيرات» من الإعدادات ليكون التذكير في وقته بالضبط.",
                "Turn on \"Alarms & reminders\" in Settings so it fires exactly on time."
            )
        )
    }

    private fun describe(at: Long, lang: AppLanguage): String {
        val now = Calendar.getInstance()
        val target = Calendar.getInstance().apply { timeInMillis = at }
        val time = String.format(
            Locale.US, "%02d:%02d",
            target.get(Calendar.HOUR_OF_DAY), target.get(Calendar.MINUTE)
        )
        val dayDiff = dayNumber(target) - dayNumber(now)
        return when {
            dayDiff <= 0 -> lang.tr("الساعة $time", "at $time")
            dayDiff == 1L -> lang.tr("غداً الساعة $time", "tomorrow at $time")
            else -> String.format(
                Locale.US, "%02d/%02d %s",
                target.get(Calendar.DAY_OF_MONTH), target.get(Calendar.MONTH) + 1, time
            ).let { lang.tr("بتاريخ $it", "on $it") }
        }
    }

    private fun dayNumber(c: Calendar): Long {
        val zone = c.timeZone.getOffset(c.timeInMillis).toLong()
        return (c.timeInMillis + zone) / 86_400_000L
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/service/NotificationHelper.kt", r'''package com.example.voiceassistant.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.example.voiceassistant.MainActivity
import com.example.voiceassistant.viewmodel.AppLanguage

/** Notification channels (Android 8+) and the notifications used by reminders and check-ins. */
object NotificationHelper {

    const val CHANNEL_REMINDERS = "va_reminders"
    const val CHANNEL_PROACTIVE = "va_proactive"
    const val CHANNEL_SPEAKING = "va_speaking"

    /** Safe to call many times; channels are only created once by the system. */
    fun createChannels(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val nm = context.getSystemService(NotificationManager::class.java) ?: return

        val reminders = NotificationChannel(
            CHANNEL_REMINDERS,
            "التذكيرات / Reminders",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "تذكيرات صوتية بمواعيدك / Spoken reminders"
            enableVibration(true)
        }
        val proactive = NotificationChannel(
            CHANNEL_PROACTIVE,
            "السؤال عن الأحوال / Check-ins",
            NotificationManager.IMPORTANCE_DEFAULT
        ).apply {
            description = "رسائل ودية من المساعد بين الحين والآخر / Friendly check-ins"
        }
        val speaking = NotificationChannel(
            CHANNEL_SPEAKING,
            "النطق / Speaking",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "يظهر أثناء نطق المساعد في الخلفية / Shown while speaking in the background"
            setShowBadge(false)
        }
        nm.createNotificationChannels(listOf(reminders, proactive, speaking))
    }

    private fun openAppIntent(context: Context, requestCode: Int): PendingIntent {
        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
        return PendingIntent.getActivity(
            context,
            requestCode,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }

    fun postReminder(context: Context, id: Int, text: String, missed: Boolean = false) {
        createChannels(context)
        val lang = AppLanguage.detect(text)
        val title = if (missed) {
            lang.tr("تذكير فائت", "Missed reminder")
        } else {
            lang.tr("تذكير", "Reminder")
        }
        val notification = NotificationCompat.Builder(context, CHANNEL_REMINDERS)
            .setSmallIcon(android.R.drawable.ic_popup_reminder)
            .setContentTitle(title)
            .setContentText(text)
            .setStyle(NotificationCompat.BigTextStyle().bigText(text))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setAutoCancel(true)
            .setContentIntent(openAppIntent(context, id))
            .build()
        notify(context, 20000 + id, notification)
    }

    fun postProactive(context: Context, text: String) {
        createChannels(context)
        val lang = AppLanguage.detect(text)
        val notification = NotificationCompat.Builder(context, CHANNEL_PROACTIVE)
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .setContentTitle(lang.tr("المساعد الصوتي", "Voice Assistant"))
            .setContentText(text)
            .setStyle(NotificationCompat.BigTextStyle().bigText(text))
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .setContentIntent(openAppIntent(context, 9001))
            .build()
        notify(context, 9001, notification)
    }

    private fun notify(context: Context, id: Int, notification: android.app.Notification) {
        try {
            context.getSystemService(NotificationManager::class.java)?.notify(id, notification)
        } catch (e: Exception) {
            // Missing notification permission or similar: nothing else we can do here.
        }
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/service/ProactiveMessages.kt", r'''package com.example.voiceassistant.service

import com.example.voiceassistant.viewmodel.AppLanguage
import java.util.Calendar
import kotlin.random.Random

/** The short sentences the assistant says on its own (greeting, check-ins, reminders). */
object ProactiveMessages {

    /** Time-of-day greeting that also asks how the user is doing. */
    fun greeting(lang: AppLanguage, hour: Int = Calendar.getInstance().get(Calendar.HOUR_OF_DAY)): String =
        when (hour) {
            in 5..11 -> lang.tr(
                "صباح الخير! كيف حالك هذا الصباح؟",
                "Good morning! How are you doing this morning?"
            )
            in 12..17 -> lang.tr(
                "مساء الخير! كيف حالك اليوم؟",
                "Good afternoon! How are you doing today?"
            )
            in 18..22 -> lang.tr(
                "مساء الخير! كيف كان يومك؟ كيف حالك الآن؟",
                "Good evening! How was your day? How are you feeling?"
            )
            else -> lang.tr(
                "أهلاً بك! كيف حالك؟",
                "Hello there! How are you?"
            )
        }

    /** One of a few friendly check-in sentences. */
    fun checkIn(lang: AppLanguage): String {
        val options = if (lang == AppLanguage.ARABIC) {
            listOf(
                "أتمنى أن يكون يومك سعيداً، هل تحتاج مساعدتي في شيء؟",
                "كيف حالك الآن؟ أنا هنا إذا احتجت أي مساعدة.",
                "مرحباً! أردت أن أطمئن عليك. هل أستطيع مساعدتك في شيء؟"
            )
        } else {
            listOf(
                "I hope you're having a lovely day. Is there anything I can help you with?",
                "How are you doing right now? I'm here if you need anything.",
                "Hi! Just checking in on you. Can I help with anything?"
            )
        }
        return options[Random.nextInt(options.size)]
    }

    /** What is spoken out loud when a reminder fires. */
    fun reminderSpeech(text: String): String {
        val lang = AppLanguage.detect(text)
        return lang.tr("تذكير: $text", "Reminder: $text")
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/service/ReminderScheduler.kt", r'''package com.example.voiceassistant.service

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import org.json.JSONArray
import org.json.JSONObject

/**
 * Schedules reminders with AlarmManager (setExactAndAllowWhileIdle) so they fire even when the
 * app is closed or the phone is in Doze. Pending reminders are kept in SharedPreferences so they
 * can be re-armed after a reboot ([ReminderReceiver]).
 */
object ReminderScheduler {

    const val ACTION_REMINDER = "com.example.voiceassistant.action.REMINDER"
    const val EXTRA_ID = "reminder_id"
    const val EXTRA_TEXT = "reminder_text"

    private const val PREFS = "va_reminders"
    private const val KEY_LIST = "list"
    private const val KEY_NEXT_ID = "next_id"

    data class Reminder(val id: Int, val text: String, val atMillis: Long)

    /** Android 12+ lets the user revoke "Alarms & reminders"; without it only inexact alarms work. */
    fun canScheduleExact(context: Context): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.S) return true
        val am = context.getSystemService(AlarmManager::class.java) ?: return false
        return am.canScheduleExactAlarms()
    }

    /** @return true if the alarm is exact, false if it had to fall back to an inexact alarm. */
    @Synchronized
    fun schedule(context: Context, text: String, atMillis: Long): Boolean {
        val app = context.applicationContext
        val reminder = Reminder(nextId(app), text, atMillis)
        save(app, load(app) + reminder)
        return setAlarm(app, reminder)
    }

    @Synchronized
    fun remove(context: Context, id: Int) {
        val app = context.applicationContext
        save(app, load(app).filter { it.id != id })
    }

    /** Re-arms every stored reminder (after reboot / app update). Overdue ones become notifications. */
    @Synchronized
    fun rescheduleAll(context: Context) {
        val app = context.applicationContext
        val now = System.currentTimeMillis()
        val all = load(app)
        val keep = mutableListOf<Reminder>()
        for (r in all) {
            if (r.atMillis > now) {
                setAlarm(app, r)
                keep.add(r)
            } else {
                NotificationHelper.postReminder(app, r.id, r.text, missed = true)
            }
        }
        save(app, keep)
    }

    private fun pendingIntent(context: Context, id: Int, text: String): PendingIntent {
        val intent = Intent(context, ReminderReceiver::class.java).apply {
            action = ACTION_REMINDER
            putExtra(EXTRA_ID, id)
            putExtra(EXTRA_TEXT, text)
        }
        return PendingIntent.getBroadcast(
            context,
            id,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
    }

    private fun setAlarm(context: Context, r: Reminder): Boolean {
        val am = context.getSystemService(AlarmManager::class.java) ?: return false
        val pi = pendingIntent(context, r.id, r.text)
        if (canScheduleExact(context)) {
            try {
                am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, r.atMillis, pi)
                return true
            } catch (e: SecurityException) {
                // permission was revoked in the meantime -> fall through to the inexact alarm
            }
        }
        am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, r.atMillis, pi)
        return false
    }

    // ---- tiny persistence layer ------------------------------------------------------------

    private fun nextId(context: Context): Int {
        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val id = prefs.getInt(KEY_NEXT_ID, 1000)
        prefs.edit().putInt(KEY_NEXT_ID, if (id >= 1_000_000) 1000 else id + 1).apply()
        return id
    }

    private fun load(context: Context): List<Reminder> {
        val raw = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString(KEY_LIST, null)
            ?: return emptyList()
        return try {
            val arr = JSONArray(raw)
            (0 until arr.length()).map { i ->
                val o = arr.getJSONObject(i)
                Reminder(o.getInt("id"), o.getString("text"), o.getLong("at"))
            }
        } catch (e: Exception) {
            emptyList()
        }
    }

    private fun save(context: Context, list: List<Reminder>) {
        val arr = JSONArray()
        list.forEach {
            arr.put(JSONObject().put("id", it.id).put("text", it.text).put("at", it.atMillis))
        }
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putString(KEY_LIST, arr.toString()).apply()
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/service/ReminderReceiver.kt", r'''package com.example.voiceassistant.service

import android.app.AlarmManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

/**
 * Receives (a) the exact alarm of a reminder and (b) boot / update events.
 *
 * When a reminder fires it always posts a notification first (the fallback), then tries to start
 * [SpeakingService] so the reminder is also spoken out loud.
 */
class ReminderReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {
            ReminderScheduler.ACTION_REMINDER -> {
                val id = intent.getIntExtra(ReminderScheduler.EXTRA_ID, 0)
                val text = intent.getStringExtra(ReminderScheduler.EXTRA_TEXT).orEmpty()
                if (text.isBlank()) return
                ReminderScheduler.remove(context, id)
                NotificationHelper.postReminder(context, id, text)
                try {
                    SpeakingService.start(context, ProactiveMessages.reminderSpeech(text), alarm = true)
                } catch (e: Exception) {
                    // The notification is already visible; speech simply isn't possible right now.
                }
            }

            Intent.ACTION_BOOT_COMPLETED,
            Intent.ACTION_MY_PACKAGE_REPLACED,
            AlarmManager.ACTION_SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED -> {
                ReminderScheduler.rescheduleAll(context)
                ProactiveScheduler.schedule(context)
            }
        }
    }
}
''')

write_file("app/src/main/java/com/example/voiceassistant/service/SpeakingService.kt", r'''package com.example.voiceassistant.service

import android.app.Notification
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.AudioAttributes
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.PowerManager
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import androidx.core.content.ContextCompat
import com.example.voiceassistant.viewmodel.AppLanguage
import java.util.ArrayDeque
import java.util.Locale

/**
 * Foreground service that speaks a sentence with TextToSpeech while the app is closed
 * (reminders and proactive check-ins). It stops itself when everything has been said.
 */
class SpeakingService : Service() {

    companion object {
        const val EXTRA_TEXT = "speak_text"
        const val EXTRA_ALARM = "speak_alarm"
        private const val FOREGROUND_ID = 7001
        private const val MAX_LIFETIME_MS = 60_000L

        /** @throws IllegalStateException on Android 12+ when the system forbids starting it right now. */
        fun start(context: Context, text: String, alarm: Boolean) {
            val intent = Intent(context, SpeakingService::class.java)
                .putExtra(EXTRA_TEXT, text)
                .putExtra(EXTRA_ALARM, alarm)
            ContextCompat.startForegroundService(context, intent)
        }
    }

    private val mainHandler = Handler(Looper.getMainLooper())
    private val pending = ArrayDeque<Pair<String, Boolean>>()
    private var engine: TextToSpeech? = null
    private var ready = false
    private var active = 0
    private var wakeLock: PowerManager.WakeLock? = null
    private var counter = 0

    private val listener = object : UtteranceProgressListener() {
        override fun onStart(utteranceId: String?) = Unit

        override fun onDone(utteranceId: String?) = utteranceFinished()

        @Deprecated("Deprecated in Java")
        override fun onError(utteranceId: String?) = utteranceFinished()

        override fun onError(utteranceId: String?, errorCode: Int) = utteranceFinished()

        override fun onStop(utteranceId: String?, interrupted: Boolean) = utteranceFinished()
    }

    override fun onCreate() {
        super.onCreate()
        NotificationHelper.createChannels(this)
        acquireWakeLock()
        engine = TextToSpeech(applicationContext) { status ->
            mainHandler.post {
                if (status == TextToSpeech.SUCCESS) {
                    engine?.setOnUtteranceProgressListener(listener)
                    ready = true
                    flush()
                } else {
                    finish()
                }
            }
        }
        // Safety net: never keep the foreground service alive forever.
        mainHandler.postDelayed({ finish() }, MAX_LIFETIME_MS)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val text = intent?.getStringExtra(EXTRA_TEXT).orEmpty()
        val alarm = intent?.getBooleanExtra(EXTRA_ALARM, false) ?: false

        // Must be called within a few seconds of startForegroundService().
        try {
            val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK
            } else {
                0
            }
            ServiceCompat.startForeground(this, FOREGROUND_ID, buildNotification(text), type)
        } catch (e: Exception) {
            stopSelf()
            return START_NOT_STICKY
        }

        if (text.isNotBlank()) {
            pending.add(text to alarm)
            active++
        }
        if (ready) flush()
        if (active <= 0 && ready) finish()
        return START_NOT_STICKY
    }

    private fun flush() {
        val tts = engine ?: return
        while (pending.isNotEmpty()) {
            val (text, alarm) = pending.poll() ?: break
            val lang = AppLanguage.detect(text)
            val result = tts.setLanguage(lang.locale)
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                tts.setLanguage(Locale.getDefault())
            }
            tts.setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(if (alarm) AudioAttributes.USAGE_ALARM else AudioAttributes.USAGE_ASSISTANT)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()
            )
            counter++
            val safe = text.take(TextToSpeech.getMaxSpeechInputLength() - 1)
            val code = tts.speak(safe, TextToSpeech.QUEUE_ADD, null, "va-svc-$counter")
            if (code != TextToSpeech.SUCCESS) utteranceFinished()
        }
    }

    private fun utteranceFinished() {
        mainHandler.post {
            active--
            if (active <= 0 && pending.isEmpty()) finish()
        }
    }

    private fun finish() {
        ServiceCompat.stopForeground(this, ServiceCompat.STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun buildNotification(text: String): Notification {
        val lang = AppLanguage.detect(text)
        return NotificationCompat.Builder(this, NotificationHelper.CHANNEL_SPEAKING)
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .setContentTitle(lang.tr("المساعد الصوتي", "Voice Assistant"))
            .setContentText(text.ifBlank { lang.tr("جارٍ النطق…", "Speaking…") })
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()
    }

    private fun acquireWakeLock() {
        try {
            val pm = getSystemService(PowerManager::class.java)
            wakeLock = pm?.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "voiceassistant:speaking")
                ?.apply { acquire(MAX_LIFETIME_MS) }
        } catch (e: Exception) {
            wakeLock = null
        }
    }

    override fun onDestroy() {
        mainHandler.removeCallbacksAndMessages(null)
        engine?.stop()
        engine?.shutdown()
        engine = null
        try {
            if (wakeLock?.isHeld == true) wakeLock?.release()
        } catch (e: Exception) {
            // already released
        }
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
''')

# 47. التفاعل الاستباقي: WorkManager كل 6 ساعات (إشعار + نطق)
write_file("app/src/main/java/com/example/voiceassistant/service/ProactiveWorker.kt", r'''package com.example.voiceassistant.service

import android.content.Context
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.voiceassistant.viewmodel.AppLanguage
import java.util.Calendar
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/** Schedules the periodic "how are you?" check-in with WorkManager (survives app close and reboot). */
object ProactiveScheduler {

    /** How often the assistant asks how you are (4 or 6 hours is a good range). */
    const val INTERVAL_HOURS = 6L

    private const val UNIQUE_NAME = "va_proactive_checkin"
    private const val PREFS = "va_proactive"
    private const val KEY_LANG = "lang"

    fun schedule(context: Context) {
        val request = PeriodicWorkRequestBuilder<ProactiveWorker>(INTERVAL_HOURS, TimeUnit.HOURS)
            .setInitialDelay(INTERVAL_HOURS, TimeUnit.HOURS)
            .build()
        WorkManager.getInstance(context.applicationContext)
            .enqueueUniquePeriodicWork(UNIQUE_NAME, ExistingPeriodicWorkPolicy.KEEP, request)
    }

    fun cancel(context: Context) {
        WorkManager.getInstance(context.applicationContext).cancelUniqueWork(UNIQUE_NAME)
    }

    /** Remembers the app language so background check-ins use the same one. */
    fun saveLanguage(context: Context, language: AppLanguage) {
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putString(KEY_LANG, language.name).apply()
    }

    fun language(context: Context): AppLanguage {
        val name = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .getString(KEY_LANG, null)
        return AppLanguage.values().firstOrNull { it.name == name } ?: AppLanguage.ARABIC
    }

    /** No spoken check-ins at night (22:00 - 08:00). */
    fun isQuietHour(): Boolean {
        val hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY)
        return hour >= 22 || hour < 8
    }
}

/** Shows a notification and says a short friendly sentence (TTS) every few hours. */
class ProactiveWorker(context: Context, params: WorkerParameters) : Worker(context, params) {

    override fun doWork(): Result {
        val ctx = applicationContext
        if (ProactiveScheduler.isQuietHour()) return Result.success()

        val lang = ProactiveScheduler.language(ctx)
        val text = ProactiveMessages.checkIn(lang)

        NotificationHelper.postProactive(ctx, text)
        try {
            SpeakingService.start(ctx, text, alarm = false)
        } catch (e: Exception) {
            // Background workers can't always start a foreground service: speak from the worker itself.
            speakDirectly(text, lang)
        }
        return Result.success()
    }

    /** Blocking one-shot TTS (the worker thread is a background thread, so waiting is fine). */
    private fun speakDirectly(text: String, lang: AppLanguage) {
        val latch = CountDownLatch(1)
        var engine: TextToSpeech? = null
        engine = TextToSpeech(applicationContext) { status ->
            val tts = engine
            if (status == TextToSpeech.SUCCESS && tts != null) {
                tts.setLanguage(lang.locale)
                tts.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                    override fun onStart(utteranceId: String?) = Unit
                    override fun onDone(utteranceId: String?) = latch.countDown()

                    @Deprecated("Deprecated in Java")
                    override fun onError(utteranceId: String?) = latch.countDown()
                })
                if (tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "va-worker") != TextToSpeech.SUCCESS) {
                    latch.countDown()
                }
            } else {
                latch.countDown()
            }
        }
        try {
            latch.await(30, TimeUnit.SECONDS)
        } catch (e: InterruptedException) {
            Thread.currentThread().interrupt()
        } finally {
            engine?.stop()
            engine?.shutdown()
        }
    }
}
''')


# Security monitor: foreground service that watches the clipboard for suspicious links / scam phrases
write_file("app/src/main/java/com/example/voiceassistant/service/SecurityMonitorService.kt", r'''package com.example.voiceassistant.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import androidx.core.content.ContextCompat
import com.example.voiceassistant.MainActivity
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Foreground service that listens for clipboard changes and speaks a warning (through
 * [SpeakingService]) when the copied text contains a link or a typical scam phrase.
 */
class SecurityMonitorService : Service() {

    companion object {
        private const val CHANNEL_SECURITY = "va_security"
        private const val FOREGROUND_ID = 7002
        private const val WARNING_COOLDOWN_MS = 5_000L

        private val suspiciousWords = listOf("حسابك محظور", "تحديث بياناتك", "فيروس", "اختراق")

        private val _running = MutableStateFlow(false)

        /** True while the service is alive (the UI switch follows this). */
        val running: StateFlow<Boolean> = _running.asStateFlow()

        /** @throws IllegalStateException on Android 12+ when the system forbids starting it right now. */
        fun start(context: Context) {
            ContextCompat.startForegroundService(
                context,
                Intent(context, SecurityMonitorService::class.java)
            )
        }

        fun stop(context: Context) {
            context.stopService(Intent(context, SecurityMonitorService::class.java))
        }
    }

    private var clipboard: ClipboardManager? = null
    private var lastWarnedText: String? = null
    private var lastWarnedAt = 0L

    private val clipListener = ClipboardManager.OnPrimaryClipChangedListener { checkClipboard() }

    override fun onCreate() {
        super.onCreate()
        createChannel()
        clipboard = getSystemService(ClipboardManager::class.java)
        clipboard?.addPrimaryClipChangedListener(clipListener)
        _running.value = true
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Must be called within a few seconds of startForegroundService().
        try {
            val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
            } else {
                0
            }
            ServiceCompat.startForeground(this, FOREGROUND_ID, buildNotification(), type)
        } catch (e: Exception) {
            stopSelf()
            return START_NOT_STICKY
        }
        return START_STICKY
    }

    /** Android 15 limits dataSync foreground services in time: stop cleanly when the system asks. */
    override fun onTimeout(startId: Int, fgsType: Int) {
        stopSelf()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        clipboard?.removePrimaryClipChangedListener(clipListener)
        clipboard = null
        _running.value = false
        super.onDestroy()
    }

    private fun checkClipboard() {
        val text = try {
            clipboard?.primaryClip
                ?.takeIf { it.itemCount > 0 }
                ?.getItemAt(0)
                ?.coerceToText(this)
                ?.toString()
        } catch (e: Exception) {
            null
        }
        if (text.isNullOrBlank() || !isSuspicious(text)) return

        // Some devices report one copy twice: warn only once.
        val now = System.currentTimeMillis()
        if (text == lastWarnedText && now - lastWarnedAt < WARNING_COOLDOWN_MS) return
        lastWarnedText = text
        lastWarnedAt = now

        val warning = ProactiveScheduler.language(this).tr(
            "تحذير أمني: تم اكتشاف نص أو رابط مشبوه في الحافظة",
            "Security warning: a suspicious text or link was found on the clipboard"
        )
        try {
            SpeakingService.start(applicationContext, warning, alarm = true)
        } catch (e: Exception) {
            // The system refused to start the speaking service right now: nothing else we can do.
        }
    }

    private fun isSuspicious(text: String): Boolean =
        text.contains("http", ignoreCase = true) || suspiciousWords.any { text.contains(it) }

    private fun createChannel() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val nm = getSystemService(NotificationManager::class.java) ?: return
        val channel = NotificationChannel(
            CHANNEL_SECURITY,
            "الحماية / Security",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "إشعار دائم أثناء مراقبة الحافظة / Shown while the clipboard is monitored"
            setShowBadge(false)
        }
        nm.createNotificationChannel(channel)
    }

    private fun buildNotification(): android.app.Notification {
        val lang = ProactiveScheduler.language(this)
        val openApp = PendingIntent.getActivity(
            this,
            9002,
            Intent(this, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            },
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        return NotificationCompat.Builder(this, CHANNEL_SECURITY)
            .setSmallIcon(android.R.drawable.ic_lock_idle_lock)
            .setContentTitle(lang.tr("الحماية نشطة", "Protection is active"))
            .setContentText(
                lang.tr(
                    "مراقبة الحافظة بحثاً عن الروابط والنصوص المشبوهة",
                    "Watching the clipboard for suspicious links and texts"
                )
            )
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setContentIntent(openApp)
            .build()
    }
}
''')

print(">> Done. {} files created in: {}".format(FILES_CREATED[0], os.getcwd()))
print(">> Next steps:")
print("   1. Gemini key: set env GEMINI_API_KEY before running, or edit GEMINI_API_KEY in data/AiChatService.kt.")
print("   2. gradle assembleDebug  (or push to GitHub and let the workflow build it).")
print("   3. Install, then Settings > Apps > Default apps > Digital assistant app > Voice Assistant.")
print("   4. Enable the accessibility service for screen control and Wi-Fi/Bluetooth switches.")
print("   5. Allow notifications when asked (Android 13+). For on-time reminders also enable")
print("      Settings > Apps > Voice Assistant > Alarms & reminders (Android 12+).")
print("   6. Try: \"ذكرني بشرب الماء بعد 10 دقائق\"  /  \"ذكرني بموعد الطبيب غداً الساعة 5 مساءً\".")
