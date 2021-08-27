import discord


def WIP():
    """Work In Progress"""
    return discord.Embed(title="⏲ This feature is work in progress!",
                         description="Please stay tuned to our latest updates [here]("
                                     "https://github.com/RedCokeDevelopment/Teapot.py)!", color=0x89CFF0)


def permission_denied():
    """user don't have permission"""
    return discord.Embed(title="🛑 Permission Denied!", description="You do not have permission to do this!",
                         color=0xFF0000)


def notfound(s):
    return discord.Embed(title=f"😮 Oops! {s.capitalize()} not found!",
                         description=f"Unable to find the specified {s.lower()}!",
                         color=0xFF0000)


def downloading():
    return discord.Embed(title="⏱ Downloading File...", description="Please wait for up to 3 seconds!",
                         color=0xFF0000)


def error(e="executing command"):
    return discord.Embed(title=f"⚠ Unknown error occurred while {e}!",
                         description="Please report to [Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py) developers [here](https://github.com/RedCokeDevelopment/Teapot.py/issues)!",
                         color=0xFF0000)


def invalidargument(arg):
    return discord.Embed(title="🟥 Invalid argument!", description=f"Valid argument(s): ``{arg}``",
                         color=0xFF0000)


def toomanyarguments():
    return discord.Embed(title="🛑 Too many arguments!", description=f"You have entered too many arguments!",
                         color=0xFF0000)
