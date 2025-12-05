import teapot

async def on_message_handler(bot, message):
    if teapot.config.storage_type() == "mysql":
        try:
            database = teapot.database.__init__()
            db = teapot.database.db(database)
            db.execute("SELECT * FROM `users` WHERE user_id = '" + str(message.author.id) + "'")
            if db.rowcount == 0:
                db.execute("INSERT INTO `users`(user_id, user_name, user_display_name) VALUES(%s, %s, %s)",
                           (message.author.id, message.author.name, message.author.display_name))
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
