import logging,tkinter as tk,os,re,threading,subprocess,time,urllib.request,requests,shutil,zipfile

from tkinter import font
from configparser import ConfigParser
from github import Github



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

path = os.path.join(config['Server']['Download-path'].strip('"'), 'run.bat')


class OnlinePlayerWidget(tk.Frame):
    def __init__(self, master, player):
        super().__init__(master, style='TFrame')
        self.player = player
        self.master = master
        self.configure(height=80, width=180)

        # create label to display username
        self.username_label = tk.Label(self, text=self.player.username, style='TLabel')
        self.username_label.pack(side='top', pady=5)

        # create canvas to display skin
        self.skin_canvas = tk.Canvas(self, height=60, width=60, bg='#ffffff', bd=0, highlightthickness=0)
        self.skin_canvas.pack(side='top', pady=5)

        # load skin from URL
        skin_url = f"https://crafatar.com/skins/{self.player.uuid}"
        skin_image_data = urllib.request.urlopen(skin_url).read()
        self.skin_image = tk.PhotoImage(data=skin_image_data)
        self.skin_canvas.create_image(0, 0, anchor='nw', image=self.skin_image)



class Server(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.console_frame = tk.Frame(self)
        self.console_frame.pack(side="top", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.console_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.console = tk.Listbox(self.console_frame, bg='#242424', fg='#ffffff')
        self.console.pack(side="left", fill="both", expand=True)

        bold_font = font.Font(self.console, self.console.cget("font"))
        bold_font.configure(weight="bold")
        self.console.configure(font=bold_font)  

        self.scrollbar.config(command=self.console.yview)

        self.status_bar = tk.Label(self, text="Server Stopped", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#FF0000')
        self.status_bar.pack(side=tk.TOP, fill=tk.X)

        self.process = None
        self.running = False



    def rgb(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'


    def get_online_players():
        log_dir = 'logs'
        # Wait for logs directory to be created
        while not os.path.exists(log_dir):
            time.sleep(1)
        # Wait for log file to be generated
        time.sleep(5)
        try:
            log_files = os.listdir(log_dir)
            latest_log_file = max(log_files, key=os.path.getctime)
            with open(f'{log_dir}/{latest_log_file}', 'r') as f:
                contents = f.read()
            matches = re.findall(r'(?<=UUID of player )(.+?)(?= is )', contents)
            players = set(matches)
            return players
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            return set()


    def start(self):

       
        self.status_bar.config(text="Server Starting...", bg = "#8B8000")
        os.system('taskkill /F /IM java.exe')

        self.console.insert('end', 'NOTE THAT THIS IS NOT A  OFFICAL MOJANG PRODUCT THIS JUST SOMETHING I MADE FOR FUN!\n')
        self.console.see('end')

        # Log a message when the server is starting
        logger.info('Starting server...')

        time.sleep(5)  # Wait for server to start up


        self.thread = threading.Thread(target=self._start)
        self.thread.start()

    def _start(self):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.process = subprocess.Popen([path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, startupinfo=startupinfo)
            self.running = True

            while self.running:
                output = None
                if self.process is not None:
                    output = self.process.stdout.readline().strip()
                    if output and self.running:
                        self.console.insert('end', output)
                        self.console.yview('end')
                        if 'Preparing level "world"' in output:
                            self.status_bar.config(text="Generating world...", bg = "#8B8000")
                        elif "Done (" in output:
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
                from src.Pythonfiles.Server.Server_main.Create import download
                (download)
                self.console.insert('end', "creating server")
                logger.info("creating server")
                print("creating server")
            except Exception as e:
                self.console.insert('end', f"error creating server {e}")
                logger.error(f"error creating server{e}")
                print(f"error creating server{e}")

            


class App(tk.Frame):
    def update_app():
    # get current version from config file
        current_version = config.get("App", "version")

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
            elif latest_tag.name == current_version:
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
                config.set("General", "version", latest_tag.name)
                with open("config.ini", "w") as config_file:
                    config.write(config_file)

                print("Downloaded and installed the latest version")

