[app]
# (List of inclusions for the app)
# You can add your specific inclusions here
title = AutoScope Client
source.dir = .
package.name = autoscopeclient
package.domain = org.autoscope.client
source.include_patterns = main/AndroidManifest.xml,main/java/org/kivy/myapp/UsbBroadcastReceiver.java
icon.filename = Icons/otoscope.png
presplash.filename = loadingScreen/loading_screen.png
orientation = portrait

# (The version of your app, e.g. 1.0)
version = 0.1

# (The Android permissions the app needs)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO

# (List of required dependencies)
requirements = python3,kivy,requests,urllib3,certifi,pyjnius,numpy

# (The path for the SDK and NDK)
android.sdk_path = /root/.buildozer/android/platform/android-sdk
android.ndk_path = /root/.buildozer/android/platform/android-ndk-r25c

# (The entrypoint for the app)
android.entrypoint = org.kivy.android.PythonActivity
android.activity_class_name = org.kivy.android.PythonActivity

# (The architecture of your app)
android.archs = arm64-v8a,armeabi-v7a

# (API version and other Android-related configurations)
android.api = 31
android.minapi = 21
android.p4a_clean_build = true
android.gradle_dependencies = com.android.tools.build:gradle:7.0.0
android.add_src = main/java/org/kivy/myapp/UsbBroadcastReceiver.java

# (Optional features)
# android.features = android.hardware.usb.host
