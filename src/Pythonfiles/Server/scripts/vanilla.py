import os
import urllib.request
import json
from configparser import ConfigParser
from urllib.error import HTTPError

config = ConfigParser()
config.read('config.ini')

version = config['Server']['Version'].replace(',', '').replace("'", '').replace('[', '').replace(']', '').replace('"', '')
download_path = config['Server']['Download-path'].replace(',', '').replace("'", '').replace('[', '').replace(']', '').replace('"', '')
type = config['Server']['Type'].replace(',', '').replace("'", '').replace('[', '').replace(']', '').replace('"', '')
print(version,download_path)

def download_server(version, directory):
    print(f"Downloading server version {version}")
    url = f"https://s3.amazonaws.com/Minecraft.Download/versions/1.17.1/minecraft_server.1.17.1.jar"
    local_path = os.path.join(directory, f"{version}.jar")

    max_retries = 3
    for i in range(max_retries):
        try:
            urllib.request.urlretrieve(url, local_path)
            print(f"Downloaded server version {version}")
            break
        except HTTPError as e:
            if i == max_retries - 1:
                print(f"Failed to download server version {version}: {e}")
                return
            else:
                print(f"Failed to download server version {version}, retrying ({i+1}/{max_retries}): {e}")

# Example usage
download_server(version, download_path)
old_name = os.path.join(download_path,f"{version}.jar")
new_name = os.path.join(download_path,f"{type}_{version}.jar")
os.rename(old_name, new_name)
