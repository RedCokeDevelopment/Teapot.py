import discord
from discord.ext import commands as cmd

import teapot


def __init__(bot):
    """ Initialize commands """
    helpcmd(bot)
    info(bot)
    leave(bot)
    ping(bot)
    purge(bot)
    kick(bot)
    ban(bot)
    admin(bot)


def helpcmd(bot):
    bot.remove_command('help')

    @bot.command(aliases=['?'])
    async def help(ctx):
        embed = discord.Embed(title="Developers: ColaIan, RedTea", description="Multi-purpose Discord Bot",
                              color=0x7400FF)
        embed.set_author(name=f"Teapot.py | {teapot.version()}",
                         icon_url="https://cdn.discordapp.com/avatars/612634758744113182/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
        embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/60006969?s=200&v=4")
        embed.add_field(name="Bot User:", value=bot.user, inline=True)
        embed.add_field(name="Guilds:", value=len(bot.guilds), inline=True)
        embed.add_field(name="Members:", value=len(set(bot.get_all_members())), inline=True)
        embed.add_field(name="O.S.:", value=str(teapot.platform()), inline=True)
        embed.add_field(name="Storage Type:", value=teapot.config.storage_type(), inline=True)
        embed.add_field(name="Prefix:", value=", ".join(teapot.config.bot_prefix()), inline=True)
        embed.add_field(name="Github Repo:", value="[Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py)",
                        inline=True)
        embed.add_field(name="Bug Report:", value="[Issues](https://github.com/RedCokeDevelopment/Teapot.py/issues)",
                        inline=True)
        embed.add_field(name="Discussion:", value="[Forums](https://forum.redtea.red)", inline=True)
        embed.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
        embed.set_image(
            url="https://user-images.githubusercontent.com/43201383/72987537-89830a80-3e25-11ea-95ef-ecfa0afcff7e.png")
        await ctx.send(embed=embed)


def info(bot):
    @bot.command(aliases=['about'])
    async def info(ctx):
        embed = discord.Embed(title="Developers: ColaIan, RedTea", description="Multi-purpose Discord Bot",
                              color=0x7400FF)
        embed.set_author(name=f"Teapot.py | {teapot.version()}",
                         icon_url="https://cdn.discordapp.com/avatars/612634758744113182/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
        embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/60006969?s=200&v=4")
        embed.add_field(name="Bot User:", value=bot.user, inline=True)
        embed.add_field(name="Guilds:", value=len(bot.guilds), inline=True)
        embed.add_field(name="Members:", value=len(set(bot.get_all_members())), inline=True)
        embed.add_field(name="O.S.:", value=str(teapot.platform()), inline=True)
        embed.add_field(name="Storage Type:", value=teapot.config.storage_type(), inline=True)
        embed.add_field(name="Prefix:", value=", ".join(teapot.config.bot_prefix()), inline=True)
        embed.add_field(name="Github Repo:", value="[Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py)",
                        inline=True)
        embed.add_field(name="Bug Report:", value="[Issues](https://github.com/RedCokeDevelopment/Teapot.py/issues)",
                        inline=True)
        embed.add_field(name="Discussion:", value="[Forums](https://forum.redtea.red)", inline=True)
        embed.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
        embed.set_image(
            url="https://user-images.githubusercontent.com/43201383/72987537-89830a80-3e25-11ea-95ef-ecfa0afcff7e.png")
        await ctx.send(embed=embed)


def leave(bot):
    @bot.command()
    async def leave(ctx):
        await ctx.voice_client.disconnect()


def ping(bot):
    @bot.command()
    async def ping(ctx):
        await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')


def purge(bot):
    @bot.command(aliases=['clear', 'cls'])
    @cmd.has_permissions(kick_members=True)
    async def purge(ctx, amount=0):
        if amount == 0:
            await ctx.send("Please specify the number of messages you want to delete!")
        else:
            await ctx.channel.purge(limit=amount + 1)


def kick(bot):
    @bot.command()
    @cmd.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member} has been kicked!')
            print(f'{member} has been kicked!')
        except Exception as failkick:
            await ctx.send("Failed to ban:" + str(failkick))


def ban(bot):
    @bot.command()
    @cmd.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member} has been banned!')
            print(f'{member} has been banned!')
        except Exception as e:
            await ctx.send("Failed to ban:" + e)


def admin(bot):
    @bot.command()
    async def admin(ctx):
        await ctx.send(embed=teapot.messages.WIP())
