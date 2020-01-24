""" Database Manager """
import mysql.connector

import teapot


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
