from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')

hello = (config['MinecraftServerDownload']['Download-path'])
target = '\testing.txt'
making = hello,target

f = open(making, 'w')
f.write("hello there")
f.close()