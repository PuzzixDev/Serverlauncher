import os
import time
import shutil
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

Type = config['MinecraftServerDownload']['Type']
download = config['MinecraftServerDownload']['Download-path']
Version = config['MinecraftServerDownload']['Version']

class writing:
    original = os.path.join('src', 'Minecraft', Type, f'{Version}.jar')
    target = download
    os.makedirs(target, exist_ok=True)
    shutil.copy(original, target)

    path = os.path.join(download, 'eula.txt')
    with open(path, 'w') as f:
        l1 = "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula)."
        l2 = "#Wed Nov 30 21:33:20 EST 2022"
        l3 = "eula=true"
        f.write(f'{l1}\n{l2}\n{l3}\n')

    time.sleep(1)

    path = os.path.join(download, 'run.bat')
    with open(path, 'w') as f:
        l1 = "@ECHO OFF"
        l2 = "SET BINDIR=%~dp0"
        l3 = 'CD /D "%BINDIR%"'
        l4 = f'"C:\\Program Files\\java\\jdk-19\\bin\\java.exe" -Xmx1024M -Xms1024M -jar {Version}.jar nogui'
        l5 = "PAUSE"
        f.write(f'{l1}\n{l2}\n{l3}\n{l4}\n{l5}')