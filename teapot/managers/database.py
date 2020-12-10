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
            port=teapot.config.db_port(),
            db=teapot.config.db_schema(),
            user=teapot.config.db_user(),
            passwd=teapot.config.db_password(),
            charset='utf8',
            use_unicode=True
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


def create_table(stmt):
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)

    db.execute(stmt)
    db.close()
    del db


def insert(stmt, var):
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)

    db.execute(stmt, var)
    database.commit()

    db.close()
    del db


def insert_if_not_exists(stmt):
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)

    db.execute(stmt)
    database.commit()

    db.close()
    del db


def create_guild_table(guild):
    database = teapot.managers.database.__init__()
    db = teapot.managers.database.db(database)

    db.execute("SELECT * FROM `guilds` WHERE guild_id = '" + str(guild.id) + "'")
    if db.rowcount == 0:
        insert("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))
