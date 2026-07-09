[app]
title = TUSKANIC Academy
package.name = tuskanicacademy
package.domain = org.tuskanic
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,kivy,kivymd
icon.filename = %(source.dir)s/icon.png
orientation = portrait
android.permissions = INTERNET
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
