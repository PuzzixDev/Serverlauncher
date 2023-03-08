import tkinter as tk
from tkinter import ttk
import customtkinter
import requests
import shutil
import os
import zipfile
from github import Github
from pypresence import Presence
from configparser import ConfigParser
from src.Pythonfiles.App.Defs import Server,App

config = ConfigParser()

config.read('config.ini')



# create the root window
root = tk.Tk()
root.title('Server Launcher')
root.configure(bg='#242424')
root.iconbitmap(r'src\images\icon.ico')
root.geometry("1000x400")
root.resizable(False, False)


style = ttk.Style()
style.configure('TFrame', background='#242424',foreground='#242424')
style.configure('TButton',background='#242424',foreground='#242424')
style.configure('TLabel', background='#242424',foreground='#242424')

#global variables

current_version = config.get('App','Version')

# create the notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# create the first frame
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Server Management")

frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="App Settings")


client_id = '1062914822452297790'
RPC = Presence(client_id)
RPC.connect()

server_type = config['Server']['Type'].strip('"')
version = config['Server']['Version'].strip('"')

RPC.update(
    state=f"Server Type: {server_type}",
    details=f"Version: {version}",
    large_image="large",
    small_image="small"
)

# create the "Create server" button in frame1




server = Server(root)
server.pack(side="top", fill="both", expand=True)

start_btn = customtkinter.CTkButton(master=frame1, text='Start server', command=server.start)
start_btn.pack(pady=(10), anchor='w')

#def create_server():
#        from src.Pythonfiles.Server.Create import download_server as e
#        (e)
        

#create_btn = customtkinter.CTkButton(master=frame1, text='Create server', command=create_server)
#create_btn.pack(pady=(10), anchor='w')

clear_btn = customtkinter.CTkButton(master=frame1, text="Clear Console", command=server.clear_console)
clear_btn.pack(pady=(10), anchor='w')

stop_btn = customtkinter.CTkButton(master=frame1, text='Stop server', command=server.stop)
stop_btn.pack(pady=(10), anchor='w')

def manual_update():
    # disable the update button to prevent multiple updates
    update_button.configure(state="disabled")

    # run the update function
    App.update_app()

    # enable the update button again
    update_button.configure(state="normal")

update_button = customtkinter.CTkButton(frame2, text="Update", command=manual_update)
update_button.pack(pady=(10), anchor='w')

# create a Github instance
g = Github()

# get the repository by name and owner
repo = g.get_repo("PuzzixDev/Serverlauncher")

# get the latest release tag with prefix "v"
latest_tag = None
for tag in repo.get_tags():
    if tag.name.startswith("v"):
        if not latest_tag or tag.commit.committer.date > latest_tag.commit.committer.date:
            latest_tag = tag

if not latest_tag:
    print("Latest tag not found")
else:
    # get the latest release associated with the tag
    latest_release = None
    for release in repo.get_releases():
        if release.tag_name == latest_tag.name:
            latest_release = release
            break

    if not latest_release:
        print("Latest release not found")
    elif not latest_release.assets:
        print("No assets found for the latest release")
    elif latest_tag.name == config.get("General", "version"):
        print("Already up-to-date")
    else:
        # download the latest release asset
        latest_asset = latest_release.assets[0]
        download_url = latest_asset.browser_download_url
        r = requests.get(download_url)
        with open("new_files.zip", "wb") as f:
            f.write(r.content)

        # extract the contents of the zip file
        with zipfile.ZipFile("new_files.zip", "r") as zip_ref:
            zip_ref.extractall("new_files")

        # delete the zip file
        os.remove("new_files.zip")

        # replace old files with new ones
        if os.path.exists("old_files"):
            shutil.rmtree("old_files")
        shutil.move("new_files", "old_files")

        # update the version in the config file
        config.set('App','Version', latest_tag.name)
        with open("config.ini", "w") as config_file:
            config.write(config_file)

        print("Downloaded and installed the latest version")

server.mainloop()