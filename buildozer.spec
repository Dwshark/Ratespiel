[app]
title = MyApp
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait

android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2

[buildozer]
log_level = 2

[android]
sdk_path = $HOME/android-sdk
ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
