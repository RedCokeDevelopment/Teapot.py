import discord

import teapot


def newembed(c=0x428DFF):
    em = discord.Embed(colour=c)
    em.set_footer(text=teapot.copyright(),
                  icon_url="https://cdn.discordapp.com/avatars/612634758744113182/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")

    return em
