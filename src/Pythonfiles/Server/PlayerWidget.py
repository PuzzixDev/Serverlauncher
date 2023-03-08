from mcipc.rcon.je import Client
import tkinter as tk

SERVER_IP = "localhost"
RCON_PORT = 25575

class OnlinePlayersWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.players_list = tk.Listbox(self)
        self.players_list.pack(fill="both", expand=True)
        self.update_online_players()
        
    def update_online_players(self):
        with Client(SERVER_IP, RCON_PORT, passwd="1234") as client:
            online_players = client.send_command("list")
            online_players = online_players.strip().split(": ")[-1].split(", ")
            self.players_list.delete(0, tk.END)
            for player in online_players:
                self.players_list.insert(tk.END, player)
        self.after(1000, self.update_online_players)