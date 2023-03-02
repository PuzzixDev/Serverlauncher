import os
import urllib.request
from configparser import ConfigParser
from Types.Vanilla import urls

config = ConfigParser()
config.read('config.ini')

version = config['Server']['Version'].split('"')[1]

Download_path = config['Server']['Download-path'].replace('"', '').split(',')
type = config['Server']['Type'].replace('"', '')
mem = config['Server']['Memory'].replace('"', '').replace('[', '').replace(']', '').replace(',', '')

url = urls.get(version)
url = url.split("?")[0]  # Remove any query string parameters from the URL
if url:
    # Get the filename from the URL
    filename = url.split("/")[-1]

    # Specify the file path in Dropbox
    dropbox_path = os.path.join('/.jars', filename)

    # Specify the local file path where the file will be downloaded
    local_path = os.path.join(Download_path[0], filename)

    print(f"Local path: {local_path}")

    # Download the file from Dropbox
    urllib.request.urlretrieve(url, local_path)

    # Rename the file if it doesn't already exist
    new_local_path = os.path.join(Download_path[0], f"{type}_{version}.jar")

    if not os.path.exists(new_local_path):
        os.rename(local_path, new_local_path)
    else:
        os.replace(local_path, new_local_path)

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
else:
    print(f"No URL found for version {version}")