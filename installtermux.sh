#!/usr/bin/bash
pkg update && pkg upgrade
pkg install python3 -y
pkg install openjdk-17 -y
pkg install aapt apktool -y
pkg install imagemagick -y
pip3 install --upgrade pip
pip3 install Pillow
