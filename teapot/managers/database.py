""" Database Manager """
import mysql.connector
import teapot


# TABLES = {}
# TABLES['guilds'] = (
#     "CREATE TABLE IF NOT EXISTS `guilds` ("
#     "  `guild_id` int(18) NOT NULL,"
#     "  `guild_name` TINYTEXT NOT NULL,"
#     ") ENGINE=InnoDB")
# TABLES['channels'] = (
#     "CREATE TABLE IF NOT EXISTS `channels` ("
#     "  `channel_id` int(18) NOT NULL,"
#     "  `channel_name` TINYTEXT NOT NULL,"
#     ") ENGINE=InnoDB")
# TABLES['users'] = (
#     "CREATE TABLE IF NOT EXISTS `users` ("
#     "  `user_id` int(18) NOT NULL,"
#     "  `user_name` TINYTEXT NOT NULL,"
#     "  `user_discriminator` int(4) NOT NULL,"
#     ") ENGINE=InnoDB")


def __init__():
    try:
        database = mysql.connector.connect(
            host=teapot.config.db_host(),
            database=teapot.config.db_schema(),
            user=teapot.config.db_user(),
            passwd=teapot.config.db_password()
        )
        return (database)
    except Exception as error:
        print("\nUnable to connect to database. Please check your credentials!\n" + str(error) + "\n")
        quit()


def db(database):
    try:
        return database.cursor(buffered=True)
    except Exception as e:
        print(f"\nAn error occurred while executing SQL statement\n{e}\n")
        quit()


def create_guild_table(guild):
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)

    db.execute("SELECT * FROM `guilds` WHERE guild_id = '" + str(guild.id) + "'")
    if db.rowcount == 0:
        db.execute("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))
        database.commit()
    db.execute("CREATE TABLE IF NOT EXISTS `" + str(
        guild.id) + "_logs" + "` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` "
                              "BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT)")
