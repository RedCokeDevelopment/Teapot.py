import json
import teapot
import discord


def __init__(bot):
    """ Initialize events """
    join(bot)
    leave(bot)
    on_guild_join(bot)
    message_send(bot)
    message_edit(bot)
    message_delete(bot)
    # on_command_error(bot)


def join(bot):
    @bot.event
    async def on_member_join(member):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
                    (teapot.time(), member.guild.id, member.channel.id, member.id, "MEMBER_JOIN"))
                database.commit()
            except Exception as e:
                print(e)


def leave(bot):
    @bot.event
    async def on_member_remove(member):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
                    (teapot.time(), member.guild.id, member.channel.id, member.id, "MEMBER_REMOVE"))
                database.commit()
            except Exception as e:
                print(e)


def on_guild_join(bot):
    @bot.event
    async def on_guild_join(ctx):
        if teapot.config.storage_type() == "mysql":
            teapot.database.create_guild_table(ctx.guild)


def message_send(bot):
    @bot.event
    async def on_message(message):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
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
                db.execute(
                    "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (teapot.time(), message.guild.id, message.channel.id, message.id, message.author.id,
                     "MESSAGE_SEND", message.content))
                database.commit()
            except Exception as e:
                print(e)
        await bot.process_commands(message)

    @bot.event
    async def on_message(message):
        # SAO Easter Egg
        if message.content.lower().startswith("system call "):
            content = message.content[12:].split(" ")
            if content[0].lower() == "inspect":
                if content[1].lower() == "entire":
                    if content[2].lower() == "command":
                        if content[3].lower() == "list":
                            em = discord.Embed(title=f"🍢 SAO Command List", color=0x7400FF)
                            em.set_thumbnail(
                                url="https://cdn.discordapp.com/attachments/668816286784159763/674285661510959105/Kirito-Sao-Logo-1506655414__76221.1550241566.png")
                            em.add_field(name='Commands',
                                         value="generate xx element\ngenerate xx element xx shape\ninspect entire command list")

                            em.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
                            await message.channel.send(embed=em)
            elif content[0].lower() == "generate":
                if content[-1].lower() == "element":
                    em = discord.Embed(title=f"✏ Generated {content[1].lower()} element!",
                                       color=0xFF0000)
                    await message.channel.send(embed=em)
                if content[-1].lower() == "shape":
                    if content[2].lower() == "element":
                        em = discord.Embed(
                            title=f"✏ Generatied {content[-2].lower()} shaped {content[1].lower()} element!",
                            color=0xFF0000)
                        await message.channel.send(embed=em)


def message_edit(bot):
    @bot.event
    async def on_raw_message_edit(ctx):
        guild_id = json.loads(json.dumps(ctx.data))['guild_id']
        channel_id = json.loads(json.dumps(ctx.data))['channel_id']
        message_id = json.loads(json.dumps(ctx.data))['id']
        try:
            author_id = json.loads(json.dumps(json.loads(json.dumps(ctx.data))['author']))['id']
            content = json.loads(json.dumps(ctx.data))['content']
            if teapot.config.storage_type() == "mysql":
                try:
                    database = teapot.database.__init__()
                    db = teapot.database.db(database)
                    db.execute(
                        "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (teapot.time(), guild_id, channel_id, message_id, author_id, "MESSAGE_EDIT", content))
                    database.commit()
                except Exception as e:
                    print(e)
        except:
            content = str(json.loads(json.dumps(ctx.data))['embeds'])
            if teapot.config.storage_type() == "mysql":
                try:
                    database = teapot.database.__init__()
                    db = teapot.database.db(database)
                    db.execute(
                        "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s)",
                        (teapot.time(), guild_id, channel_id, message_id, "MESSAGE_EDIT", content))
                    database.commit()
                except Exception as e:
                    print(e)


def message_delete(bot):
    @bot.event
    async def on_message_delete(ctx):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s, %s)",
                    (teapot.time(), ctx.guild.id, ctx.channel.id, ctx.id, ctx.author.id, "MESSAGE_DELETE"))
                database.commit()
            except Exception as e:
                print(e)


def on_command_error(bot):
    @bot.event
    async def on_command_error(ctx, e):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
                    (teapot.time(), "CMD_ERROR", __name__, str(e)))
                database.commit()
            except Exception as e:
                print(e)
