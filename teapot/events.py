import json
import teapot
import discord


def __init__(bot):
    """ Initialize events """
    join(bot)
    leave(bot)
    on_guild_join(bot)
    # on_message is now handled by event_handler/loader.py
    message_edit(bot)
    message_delete(bot)
    on_command_error(bot)


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

def message_edit(bot):
    @bot.event
    async def on_raw_message_edit(ctx):
        if ctx.guild_id is None:
            return
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
