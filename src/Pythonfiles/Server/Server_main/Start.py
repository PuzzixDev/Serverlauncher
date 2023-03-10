import subprocess
import os

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
download = config['MinecraftServerDownload']['Download-path']
class start():
    path = os.path.join(download, 'run.bat')
    subprocess.Popen([path], creationflags=subprocess.CREATE_NEW_CONSOLE)