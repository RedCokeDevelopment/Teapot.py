import discord


def WIP():
    return discord.Embed(title="⏲ This feature is Work In Progress!",
                         description="Please stay tuned to our latest updates!", color=0x89CFF0)


def PermissionDenied():
    return discord.Embed(title="🛑 Permission Denied!", description="You do not have permission to do this!",
                         color=0xFF0000)


def notfound(s):
    return discord.Embed(title=f"😮 Oops! {s.capitalize()} not found!",
                         description=f"Unable to find the specified {s.lower()}!",
                         color=0xFF0000)


def downloading():
    return discord.Embed(title="⏱ Downloading File...", description="Please wait for up to 10 seconds!",
                         color=0xFF0000)


def error():
    return discord.Embed(title="⚠ Unknown error occurred while executing command!",
                         description="Please report to [Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py) developers [here](https://github.com/RedCokeDevelopment/Teapot.py/issues)!",
                         color=0xFF0000)


def invalidarguments(arg):
    return discord.Embed(title="🟥 Invalid argument!", description=f"Valid argument: ``{arg}``",
                         color=0xFF0000)
