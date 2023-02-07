import tkinter as tk 
from tkinter import *
import shutil
import customtkinter
from os import *
import os as os
from configparser import ConfigParser
from dotenv import load_dotenv
import time

config = ConfigParser()

config.read('config.ini')

root = customtkinter.CTk()
root.title('Server Launcher')
root.iconbitmap(r'images\icon.ico')
root.geometry("200x400")
root.resizable(False, False)

customtkinter.set_appearance_mode("System")
customtkinter.CTk

type = config['MinecraftServerDownload']['Type']
version = config['MinecraftServerDownload']['Version']
download= config['MinecraftServerDownload']['Download-path']

#target


def sserver():
        original = r'src/' + type + '/'+ version + '.jar'
        target = download
        shutil.copy(original, target)


start = customtkinter.CTkButton(master=root, text='Start server', command=sserver)
start.pack(pady=(10))


def server():
    os.startfile(r"windows\Server downloads.pyw")
Downloads = customtkinter.CTkButton(root, text="Server Downloads",command=server)
Downloads.pack(pady=(10))




#bungee cord
Name = config['Bungee']['Name']
def Bungeecord():
    os.startfile(config['Bungee']['Filepath'])
Bungee = customtkinter.CTkButton(master=root, text=Name, command=Bungeecord)
Bungee.pack(pady=(10))

#lobby
NAme = config['Lobby']['Name']
def lobby():
    os.startfile(config['Lobby']['Filepath'])
Lobby = customtkinter.CTkButton(root, text=NAme,command=lobby)
Lobby.pack(pady=(10))

#lifesteal
NaMe = config['Lifesteal']['Name']
def lifesteal():
    os.startfile(config['Lifesteal']['Filepath'])
Lifesteal = customtkinter.CTkButton(root, text=NaMe,command=lifesteal)
Lifesteal.pack(pady=(10))

#pvp
NAmE = config['Pvp']['Name']
def pvp():
    os.startfile(config['Pvp']['Filepath'])
Pvp = customtkinter.CTkButton(root, text=NAmE,command=pvp)
Pvp.pack(pady=(10))

#bedwars
NaME = config['Bedwars']['Name']
def bedwars():
    os.startfile(config['Bedwars']['Filepath'])
Bedwars = customtkinter.CTkButton(root, text=NaME,command=bedwars)
Bedwars.pack(pady=(10))



#Start All
def All():
    os.startfile(r"G:\Code\ARENA PVP\Mysql")
    time.sleep(0.5)
    os.startfile(r"Servers\Bungee.py")
    time.sleep(0.5)
    os.startfile(r"Servers\Lobby.py")
    time.sleep(46.303)
    os.startfile(r"Servers\Lifesteal.py")
    time.sleep(27.862)
    os.startfile(r"Servers\PVP.py")
    time.sleep(24.123)
    os.startfile(r"Servers\Bedwars.py")
Start = customtkinter.CTkButton(root, text="START ALL",command=All, fg_color="red", text_color="black")
Start.pack(pady=(10))


root.mainloop()
