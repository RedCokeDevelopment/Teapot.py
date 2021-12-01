import os
import time
from os.path import join, dirname
import json
import requests

import discord
from discord.ext import commands as dcmd
from discord.ext.commands import AutoShardedBot as asb
from dotenv import load_dotenv
from http import HTTPStatus

import teapot

print(f"""
  _____                      _   
 |_   _|__  __ _ _ __   ___ | |_ 
   | |/ _ \\/ _` | '_ \\ / _ \\| __|
   | |  __/ (_| | |_) | (_) | |_ 
   |_|\\___|\\__,_| .__/ \\___/ \\__|
    by ColaIan |_| & RedTea

Running Teapot.py {teapot.version()}
""")

req = requests.get(f'https://api.github.com/repos/RedCokeDevelopment/Teapot.py/tags')
response = json.loads(req.text)
if req.status_code == 200:
    if response[0]['name'] == teapot.version():
        print("You are currently running the latest version of Teapot.py!\n")
    else:
        version_listed = False
        for x in response:
            if x['name'] == teapot.version():
                version_listed = True
                print("You are not using our latest version! :(\n")
        if not version_listed:
            print("You are currently using an unlisted version!\n")
elif req.status_code == 404: print("Latest Teapot.py version not found!\n")
else: print(f"An error occurred while fetching the latest Teapot.py version. [{req.status_code}: {HTTPStatus(req.status_code).phrase}]")

load_dotenv(join(dirname(__file__), '.env'))

if os.getenv('CONFIG_VERSION') != teapot.config_version():
    if os.path.isfile('.env'):
        print("Missing environment variables. Please backup and delete .env, then run Teapot.py again.")
        quit(2)
    print("Unable to find required environment variables. Running setup.py...")  # if .env not found
    teapot.setup.__init__() # run setup.py

print("Initializing bot...")
if teapot.config.storage_type() == "mysql": # if .env use mysql, create the table if table not exists
    time_start = time.perf_counter()
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)
    db.execute('ALTER DATABASE `' + teapot.config.db_schema() + '` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute('CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `guild_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute('CREATE TABLE IF NOT EXISTS `channels` (`channel_id` BIGINT, `channel_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `user_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci, `user_discriminator` INT) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    db.execute("CREATE TABLE IF NOT EXISTS `bot_logs` (`timestamp` TEXT, `type` TINYTEXT, `class` TINYTEXT, `message` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    teapot.managers.database.create_table("CREATE TABLE IF NOT EXISTS `guild_logs` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

    print(f"Connected to database ({teapot.config.db_host()}:{teapot.config.db_port()}) in {round(time.perf_counter() - time_start, 2)}s")

    db.execute("INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)", (teapot.time(), "BOT_START", __name__, "Initialized bot"))
    database.commit()

class TeapotBot(asb):
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.typing = False
        
        super().__init__(
            command_prefix=teapot.config.bot_prefix(),
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
    
    def cogs(self):
        print("Loading cogs:")
        for file in os.listdir("./teapot/cogs"):
            if file.endswith(".py"):
                try:
                    if file == "cmds.py": continue
                    
                    self.load_extension(f"teapot.cogs.{file[:-3]}")
                    print(f"    Loaded '{file}'")
                except Exception as e: print(str(e))
    
    async def on_connect(self): print("Connected to Discord")
    async def on_ready(self):
        print(f"Bot initialised in {round(time.perf_counter() - discord_time_start, 2)}s")
        time_start = time.perf_counter()
        
        teapot.events.__init__(self)
        teapot.cogs.cmds.__init__(self)
        self.cogs()
        
        if teapot.config.storage_type() == "mysql":
            for guild in self.guilds:
                teapot.managers.database.create_guild_table(guild)
                
        elif teapot.config.storage_type() == "sqlite":
            print("[!] Warning: SQLite storage has not been implemented yet. MySQL is recommended")  # WIP
        print(f"Registered commands and events in {round(time.perf_counter() - time_start, 2)}s")
        await self.change_presence(status=discord.Status.online, activity=discord.Game(teapot.config.bot_status()))  # Update the bot's status
        
try:
    discord_time_start = time.perf_counter()
    TeapotBot().run(teapot.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to the Discord API. Please check your bot token!\n\n{e}")
    if teapot.config.storage_type() == "mysql": db.execute("INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)", (teapot.time(), "ERROR", __name__, e))
    
    time.sleep(5)
    exit(1)
