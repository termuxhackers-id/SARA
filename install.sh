#!/usr/bin/bash
sudo apt-get install aapt wget python3 python3-pip zipalign imagemagick openjdk-8-jdk -y
wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.10.0.jar
sudo mv apktool /usr/bin/apktool && sudo chmod +x /usr/bin/apktool
sudo mv apktool_2.10.0.jar /usr/bin/apktool.jar && sudo chmod +x /usr/bin/apktool.jar
pip install Pillow
