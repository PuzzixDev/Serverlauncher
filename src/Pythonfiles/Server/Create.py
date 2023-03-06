import os
import urllib.request
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

version = config['Server']['Version'].split('"')[1]

Download_path = config['Server']['Download-path'].replace('"', '').split(',')
type = config['Server']['Type'].replace('"', '')
mem = config['Server']['Memory'].replace('"', '').replace('[', '').replace(']', '').replace(',', '')




    # Generate eula.txt file
eula_path = os.path.join(Download_path[0], "eula.txt")
with open(eula_path, 'w') as f:
        f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n")
        f.write("eula=true\n")

java_path = os.environ.get('JAVA_HOME')

        # Generate run.bat file
run_path = os.path.join(Download_path[0], "run.bat")
with open(run_path, 'w') as f:
        l1 = "@ECHO OFF\n"
        l2 = "SET BINDIR=%~dp0\n"
        l3 = 'CD /D "%BINDIR%"\n'
        l4 = f'"{java_path}\\bin\\java" -Xmx{mem}M -Xms{mem}M -jar {type}_{version}.jar nogui\n"'
        l5 = "PAUSE\n"
        f.write(l1 + l2 + l3 + l4 + l5)