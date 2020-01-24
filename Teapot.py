import os
import time
from os.path import join, dirname

import discord
from discord.ext import commands as dcmd
from dotenv import load_dotenv

import teapot

print("""
  _____                      _   
 |_   _|__  __ _ _ __   ___ | |_ 
   | |/ _ \/ _` | '_ \ / _ \| __|
   | |  __/ (_| | |_) | (_) | |_ 
   |_|\___|\__,_| .__/ \___/ \__|
    by ColaIan |_| & RedTea
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
    database = teapot.database.__init__()
    db = teapot.database.db(database)
    db.execute('CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `guild_name` TINYTEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS `channels` (`channel_id` BIGINT, `channel_name` TINYTEXT)')
    db.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `user_name` TINYTEXT, `user_discriminator` INT)")
    print(f"Connected to database ({teapot.config.db_host()}) in {round(time.perf_counter() - time_start, 2)}s")

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
            db.execute("SELECT * FROM `guilds` WHERE guild_id = '" + str(guild.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))
                database.commit()
            db.execute("CREATE TABLE IF NOT EXISTS `" + str(
                guild.id) + "_logs" + "` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` "
                                      "BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT)")
    elif teapot.config.storage_type() == "flatfile":
        print("[!] Flatfile storage has not been implemented yet. MySQL database is recommended")
    print(f"Registered commands and events in {round(time.perf_counter() - time_start, 2)}s")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(teapot.config.bot_status()))


@bot.event
async def on_message(message):
    guild = message.guild
    if teapot.config.storage_type() == "mysql":
        try:
            db.execute("SELECT * FROM `users` WHERE user_id = '" + str(message.author.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `users`(user_id, user_name, user_discriminator) VALUES(%s, %s, %s)",
                           (message.author.id, message.author.name, message.author.discriminator.zfill(4)))
                database.commit()
            db.execute("SELECT * FROM `channels` WHERE channel_id = '" + str(message.channel.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `channels`(channel_id, channel_name) VALUES(%s, %s)",
                           (message.channel.id, message.channel.name))
                database.commit()
            db.execute("INSERT INTO `" + str(
                guild.id) + "_logs" + "`(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                       (teapot.time(), message.guild.id, message.channel.id, message.id, message.author.id,
                        "MESSAGE_SEND", message.content))
            database.commit()
        except Exception as e:
            print(e)
    await bot.process_commands(message)


try:
    discord_time_start = time.perf_counter()
    bot.run(teapot.config.bot_token())
except Exception as e:
    print(e)
    print("[/!\] Failed to connect to DiscordAPI. Please check your bot token!")
