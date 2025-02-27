[app]
title = Paypy补单工具
package.name = paypy_retry
package.domain = com.mobantu
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.0
requirements = python3,kivy==2.1.0,requests,openssl
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
android.permissions = INTERNET
android.api = 33
android.ndk = 23b
android.sdk = 33
android.accept_sdk_license = True  # 自动接受SDK协议
[buildozer]
log_level = 2
android.sdk_path = /home/runner/android-sdk  # 使用预装路径
android.ndk_path = /home/runner/android-ndk
