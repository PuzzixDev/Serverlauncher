import tkinter as tk
from tkinter import ttk
import customtkinter
from pypresence import Presence
from configparser import ConfigParser

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


# create the notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# create the first frame
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Server Management")


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

from src.Pythonfiles.App.Defs import App

app = App(root)
app.pack(side="top", fill="both", expand=True)

start_btn = customtkinter.CTkButton(master=frame1, text='Start server', command=app.start)
start_btn.pack(pady=(10), anchor='w')

def create_server():
    try:
        from src.Pythonfiles.Server.Create import download as write
        (write)
    except Exception as e:
        print(f"Error creating server: {e}")

create_btn = customtkinter.CTkButton(master=frame1, text='Create server', command=create_server)
create_btn.pack(pady=(10), anchor='w')

clear_btn = customtkinter.CTkButton(master=frame1, text="Clear Console", command=app.clear_console)
clear_btn.pack(pady=(10), anchor='w')

stop_btn = customtkinter.CTkButton(master=frame1, text='Stop server', command=app.stop)
stop_btn.pack(pady=(10), anchor='w')





# start the event loop
app.mainloop()