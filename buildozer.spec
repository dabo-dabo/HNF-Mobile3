[app]

# (str) Title of your application
title = HNF Miner

# (str) Package name
package.name = hnf

# (str) Package domain (needed for android/ios packaging)
package.domain = org.hnf

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application version (هذا هو السطر الذي كان ناقصاً)
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.2.1,kivymd,ecdsa,psutil,cryptography,openssl

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (int) Android NDK version to use
android.ndk = 25b

# (bool) Skip trying to update the Android sdk
android.skip_update_sdk = False

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (list) Android architectures to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
