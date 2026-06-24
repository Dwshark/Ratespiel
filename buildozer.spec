[app]
title = MyApp
package.name = myapp
package.domain = org.test

# Projektstruktur
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 0.1

# Anforderungen
requirements = python3,kivy

# Ausrichtung
orientation = portrait

# Android Einstellungen (MÜSSEN unter [app] stehen!)
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2

# Optional: Vollbild
fullscreen = 1


[buildozer]
log_level = 2


[android]
# WICHTIG: absolute Pfade, keine Variablen!
sdk_path = /home/runner/android-sdk
ndk_path = /home/runner/android-ndk/ndk
