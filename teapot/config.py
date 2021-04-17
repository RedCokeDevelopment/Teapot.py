import os

import teapot


def bot_owner():
    return eval(os.getenv('BOT_owner', "216127021028212737"))


def bot_token():
    return os.getenv('BOT_TOKEN')

def osu_api_key():
    return os.getenv('OSU_API_KEY')

def trn_api_key():
    return os.getenv('TRN_API_KEY')


def bot_prefix():
    return eval(os.getenv('BOT_PREFIX', "['/teapot ', '/tp']"))


def bot_status():
    default_prefix = f'{", ".join(teapot.config.bot_prefix())} | Teapot.py {teapot.version()}'
    try:
        return eval(os.getenv('BOT_STATUS', default_prefix))
    except:
        return os.getenv('BOT_STATUS', default_prefix)


def storage_type():
    if os.environ['STORAGE_TYPE'] != "mysql":
        os.environ['STORAGE_TYPE'] = "flatfile"
    return os.environ['STORAGE_TYPE']


def db_host():
    return os.environ['DB_HOST']


def db_port():
    return os.getenv('DB_PORT', "3306")


def db_schema():
    return os.environ['DB_SCHEMA']


def db_user():
    return os.environ['DB_USER']


def db_password():
    return os.environ['DB_PASSWORD']


def lavalink_host():
    return os.environ['LAVALINK_HOST']


def lavalink_port():
    return os.environ['LAVALINK_PORT']


def lavalink_password():
    return os.environ['LAVALINK_PASSWORD']
