import os
import time
from os.path import join, dirname

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

Running Teapot.pt {teapot.version()}
""")

load_dotenv(join(dirname(__file__), '.env'))

if os.getenv('CONFIG_VERSION') != teapot.config_version():
    if os.path.isfile('.env'):
        print("Missing environment variables. Please delete .env and run Teapot.py again.")
        quit()
    print("Unable to find required environment variables. Running setup.py...")
    teapot.setup.__init__()

print("Initializing bot...")
if teapot.config.storage_type() == "mysql":
    time_start = time.perf_counter()
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)
    db.execute('CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `guild_name` TINYTEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS `channels` (`channel_id` BIGINT, `channel_name` TINYTEXT)')
    db.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `user_name` TINYTEXT, `user_discriminator` INT)")
    db.execute("CREATE TABLE IF NOT EXISTS `logs` (`timestamp` TEXT, `type` TINYTEXT, `class` TINYTEXT, `message` "
               "MEDIUMTEXT)")
    print(f"Connected to database ({teapot.config.db_host()}) in {round(time.perf_counter() - time_start, 2)}s")

    db.execute("INSERT INTO `logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
               (teapot.time(), "BOT_START", __name__, "Initialized bot"))
    database.commit()

bot = dcmd.Bot(command_prefix=teapot.config.bot_prefix())


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
    elif teapot.config.storage_type() == "flatfile":
        print("[!] Flatfile storage has not been implemented yet. MySQL database is recommended")
    print(f"Registered commands and events in {round(time.perf_counter() - time_start, 2)}s")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(teapot.config.bot_status()))



try:
    discord_time_start = time.perf_counter()
    bot.run(teapot.config.bot_token())
except Exception as e:
    print(f"[/!\\] Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    if teapot.config.storage_type() == "mysql":
        db.execute("INSERT INTO `logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
                   (teapot.time(), "ERROR", __name__, e))
