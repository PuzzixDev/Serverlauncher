import logging
import tkinter as tk
import os
import threading
from pypresence import Presence
from configparser import ConfigParser
import subprocess 
import time

# Create a logger object with the desired name
logger = logging.getLogger('logs')
logger.setLevel(logging.INFO)

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_path = os.path.join(log_dir,f"logs_{time.strftime('%Y%m%d-%H%M%S')}.txt")
file_handler = logging.FileHandler(log_path)

# Create a formatter to format log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

config = ConfigParser()
config.read('config.ini')

path = os.path.join(config['MinecraftServerDownload']['Download-path'], 'run.bat')



class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.console_frame = tk.Frame(self)
        self.console_frame.pack(side="top", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.console_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.console = tk.Listbox(self.console_frame, bg='#242424', fg='#ffffff')
        self.console.pack(side="left", fill="both", expand=True)

        bold_font = tk.font.Font(self.console, self.console.cget("font"))
        bold_font.configure(weight="bold")
        self.console.configure(font=bold_font)  

        self.scrollbar.config(command=self.console.yview)

        self.status_bar = tk.Label(self, text="Server Stopped", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#FF0000')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.process = None
        self.running = False
    def rgb(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'


    def Rich_presents(self, version, server_type):
        client_id = '1062914822452297790'
        RPC = Presence(client_id)
        RPC.connect()

        RPC.update(
            state=f"Server Type: {server_type}",
            details=f"Version: {version}",
            large_image="large",
            small_image="small"
        )

    def start(self):
        server_type = config['MinecraftServerDownload']['Type']
        version = config['MinecraftServerDownload']['Version']

        self.Rich_presents(version, server_type)

        self.status_bar.config(text="Server Starting...", bg = "#8B8000")
        os.system('taskkill /F /IM java.exe')

        self.console.insert('end', 'NOTE THAT THIS IS NOT A  OFFICAL MOJANG PRODUCT THIS JUST SOMETHING I MADE FOR FUN!\n')
        self.console.see('end')

        # Log a message when the server is starting
        logger.info('Starting server...')

        self.thread = threading.Thread(target=self._start)
        self.thread.start()

    def _start(self):
        try:
            self.process = subprocess.Popen([path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.running = True

            while self.running:
                output = None
                if self.process is not None:
                    output = self.process.stdout.readline().strip()
                    if output and self.running:
                        self.console.insert('end', output)
                        self.console.yview('end')
                        if "Done (" in output:
                            self.loading_complete()

                        # Log each line of output from the server to the log file
                        logger.info(output)
        except Exception as e:
            print(f"Could not start server: {e}")
            logger.error(f'Error starting server: {e}')

    def loading_complete(self):
        self.status_bar.config(text="Server Running",bg='#00ff00')

    def stop(self):
        self.status_bar.config(text="Server Stopping...")
        os.system('taskkill /F /IM java.exe')
        if self.process is not None:
            try:
                self.process.kill()
            except Exception as e:
                print(f"Error could not stop server: {e}")
                logger.error(f'Error stopping server: {e}')
            self.process = None
            self.running = False
        self.status_bar.config(text="Server Stop",bg='#FF0000')
        
        # Log a message when the server is stopped
        logger.info('Server stopped')
	
    def clear_console(self):
            try:
                self.console.delete(0, tk.END)
            except Exception as e:
                print(f"Error could not clear console: {e}")
                logger.error(f"Error could not clear console: {e}")
    
    def create(self):
            try:
                import src.Pythonfiles.Server.Create as writing
                (writing)
                logger.info('Server has been created')
            except Exception as e:
                print(f"Error creating server: {e}")
                logger.error(f"Error creating server: {e}")