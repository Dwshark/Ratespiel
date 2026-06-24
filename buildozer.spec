[app]
title = MyApp
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2

[android]
sdk_path = $HOME/android-sdk
ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
android_api = 33
ndk_api = 21
build_tools_version = 33.0.2
