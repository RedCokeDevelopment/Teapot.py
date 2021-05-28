import os
import time
from os.path import join, dirname
import json
import requests

import discord
from discord.ext import commands as dcmd
from dotenv import load_dotenv

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
        versionlisted = False
        for x in response:
            if x['name'] == teapot.version():
                versionlisted = True
                print("You are not using our latest version! :(\n")
        if not versionlisted:
            print("You are currently using an unlisted version!\n")
elif req.status_code == 404:
    # 404 Not Found
    print("Latest Teapot.py version not found!\n")
elif req.status_code == 500:
    # 500 Internal Server Error
    print("An error occurred while fetching the latest Teapot.py version. [500 Internal Server Error]\n")
elif req.status_code == 502:
    # 502 Bad Gateway
    print("An error occurred while fetching the latest Teapot.py version. [502 Bad Gateway]\n")
elif req.status_code == 503:
    # 503 Service Unavailable
    print("An error occurred while fetching the latest Teapot.py version. [503 Service Unavailable]\n")
else:
    print("An unknown error has occurred when fetching the latest Teapot.py version\n")
    print("HTML Error Code:" + str(req.status_code))

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
    db.execute(
        'CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `guild_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute(
        'CREATE TABLE IF NOT EXISTS `channels` (`channel_id` BIGINT, `channel_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci')
    db.execute(
        "CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `user_name` TINYTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci, `user_discriminator` INT) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    db.execute(
        "CREATE TABLE IF NOT EXISTS `bot_logs` (`timestamp` TEXT, `type` TINYTEXT, `class` TINYTEXT, `message` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    teapot.managers.database.create_table(
        "CREATE TABLE IF NOT EXISTS `guild_logs` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")

    print(
        f"Connected to database ({teapot.config.db_host()}:{teapot.config.db_port()}) in {round(time.perf_counter() - time_start, 2)}s")

    db.execute("INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
               (teapot.time(), "BOT_START", __name__, "Initialized bot"))
    database.commit()

intents = discord.Intents.default()
intents.members = True
intents.typing = False
bot = dcmd.Bot(intents=intents, command_prefix=teapot.config.bot_prefix(), help_command=None)

@bot.event
async def on_ready():
    print(f"Connected to DiscordAPI in {round(time.perf_counter() - discord_time_start, 2)}s")
    time_start = time.perf_counter()
    teapot.events.__init__(bot)
    teapot.cogs.cmds.__init__(bot)
    teapot.cogs.music.setup(bot)
    teapot.cogs.osu.setup(bot)
    teapot.cogs.github.setup(bot)
    teapot.cogs.cat.setup(bot)
    teapot.cogs.neko.setup(bot)
    if teapot.config.storage_type() == "mysql":
        for guild in bot.guilds:
            teapot.managers.database.create_guild_table(guild)
    elif teapot.config.storage_type() == "sqlite":
        print("[!] Warning: SQLite storage has not been implemented yet. MySQL is recommended")  # WIP
    print(f"Registered commands and events in {round(time.perf_counter() - time_start, 2)}s")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(teapot.config.bot_status()))  # Update Bot status


try:
    discord_time_start = time.perf_counter()
    bot.run(teapot.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    if teapot.config.storage_type() == "mysql":
        db.execute("INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
                   (teapot.time(), "ERROR", __name__, e))
    time.sleep(5)
    exit(1)
