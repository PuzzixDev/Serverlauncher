import discord
import os
from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')

download = config['MinecraftServerDownload']['Download-path']

token = config['Discord']['TOKEN']
bot = discord.Bot()

@bot.event
async def on_ready():
    activity = discord.Game(name="Minecraft", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "start", description = "Starts the minecraft server")
async def Startserver(ctx):
    await ctx.respond("Starting server!")
    os.startfile(os.path.join(download + "//run.bat"))

bot.run(token)