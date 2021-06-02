import discord
import psutil
import time
import typing


import teapot


class Commands(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.command(aliases=['?'])
    async def help(self, ctx, *cog):
        if not cog:
            embed = discord.Embed(description="📖 Help", color=0x7400FF,
                                  icon_url="https://cdn.discordapp.com/avatars/612634758744113182"
                                           "/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
            embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/60006969?s=200&v=4")
            cogs_desc = ""
            for x in self.bot.cogs:
                cogs_desc += f'**{x}** - {self.bot.cogs[x].__doc__}\n'
            embed.add_field(name='Modules', value=cogs_desc[0:len(cogs_desc) - 1])
            embed.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji='✅')
        else:
            if len(cog) > 1:
                await ctx.send(embed=teapot.messages.toomanyarguments())
                await ctx.message.add_reaction(emoji='🛑')
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            embed = discord.Embed(color=0x7400FF)
                            cog_info = ''
                            for c in bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    cog_info += f"**{c.name}** - {c.help}\n"
                            embed.add_field(name=f"{cog[0]} Module", value=cog_info)
                            await ctx.send(embed=embed)
                            await ctx.message.add_reaction(emoji='✅')
                            found = True
                if not found:
                    for x in self.bot.cogs:
                        for c in bot.get_cog(x).get_commands():
                            if c.name.lower() == cog[0].lower():
                                embed = discord.Embed(title=f"Command: {c.name.lower().capitalize()}",
                                                      description=f"**Description:** {c.help}\n**Syntax:** {c.qualified_name} {c.signature}",
                                                      color=0x7400FF)
                                embed.set_author(name=f"Teapot.py {teapot.version()}",
                                                 icon_url="https://cdn.discordapp.com/avatars/612634758744113182"
                                                          "/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
                                await ctx.message.add_reaction(emoji='✅')
                                found = True
                    if not found:
                        embed = teapot.messages.notfound("Module")
                        await ctx.message.add_reaction(emoji='🛑')
                    await ctx.send(embed=embed)
                else:
                    await ctx.message.add_reaction(emoji='✅')


    @discord.ext.commands.command(aliases=['about'])
    async def info(self, ctx):
        embed = discord.Embed(title="Developers: RedTeaDev, ColaIan", description="Multi-purpose Discord Bot",
                              color=0x7400FF)
        embed.set_author(name=f"Teapot.py {teapot.version()}",
                         icon_url="https://cdn.discordapp.com/avatars/612634758744113182"
                                  "/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
        embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/60006969?s=200&v=4")
        embed.add_field(name="Bot User:", value=self.bot.user)
        embed.add_field(name="Guilds:", value=len(self.bot.guilds))
        embed.add_field(name="Members:", value=len(set(self.bot.get_all_members())))
        embed.add_field(name="O.S.:", value=str(teapot.platform()))
        embed.add_field(name="Storage Type:", value=teapot.config.storage_type())
        embed.add_field(name="Prefix:", value=", ".join(teapot.config.bot_prefix()))
        embed.add_field(name="Github Repo:", value="[Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py)")
        embed.add_field(name="Bug Report:", value="[Issues](https://github.com/RedCokeDevelopment/Teapot.py/issues)")
        embed.add_field(name="Discussion:", value="[Forums](https://forum.redtea.red)")
        embed.add_field(name="Links",
                        value="[Support Discord](https://discord.gg/7BRGs6F) | [Add bot to server]("
                              "https://discordapp.com/oauth2/authorize?client_id=669880564270104586&permissions=8"
                              "&scope=bot) | [Repository](https://github.com/RedCokeDevelopment/Teapot.py)",
                        inline=False)
        embed.set_footer(text=f"{teapot.copyright()} | Code licensed under MIT License")
        embed.set_image(
            url="https://user-images.githubusercontent.com/43201383/72987537-89830a80-3e25-11ea-95ef-ecfa0afcff7e.png")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(emoji='✅')


    @discord.ext.commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)} ms')
        await ctx.message.add_reaction(emoji='✅')


    @discord.ext.commands.command(aliases=['purge', 'clear', 'cls'])
    @discord.ext.commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, amount=0):
        if amount == 0:
            await ctx.send("Please specify the number of messages you want to delete!")
            await ctx.message.add_reaction(emoji='❌')
        elif amount <= 0:  # lower then 0
            await ctx.send("The number must be bigger than 0!")
            await ctx.message.add_reaction(emoji='❌')
        else:
            await ctx.message.add_reaction(emoji='✅')
            await ctx.channel.purge(limit=amount + 1)


    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(kick_members=True)  # check user permission
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member} has been kicked!')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as failkick:
            await ctx.send("Failed to kick: " + str(failkick))
            await ctx.message.add_reaction(emoji='❌')


    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(ban_members=True)  # check user permission
    async def ban(self, ctx, member: typing.Any[discord.Member, discord.User], *, reason=None):  # Banning a member who is not in the server is also possible
        try:
            if isinstance(member, discord.Member):
                await member.ban(reason=reason)
            else:
                await ctx.guild.ban(member, reason=reason)
                
            await ctx.send(f'{member.name} has been banned!')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as e:
            await ctx.send("Failed to ban: " + str(e))
            await ctx.message.add_reaction(emoji='❌')
    
    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(ban_members=True)  # check user permission
    async def unban(self, ctx, member: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(member, reason=reason)                
            await ctx.send(f'{member.name} has been unbanned!')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as e:
            await ctx.send("Failed to unban: " + str(e))
            await ctx.message.add_reaction(emoji='❌')

    @discord.ext.commands.command() # Work In Progress
    async def admin(self, ctx):
        await ctx.send(embed=teapot.messages.WIP())


    @discord.ext.commands.command()
    async def owner(self, ctx):
        if ctx.message.author.id == teapot.config.bot_owner():
            found = False
            for role in ctx.guild.roles:
                if role.name == "Teapot Owner":
                    found = True
                    await ctx.guild.get_member(teapot.config.bot_owner()).add_roles(role)
                    break
            if not found:
                perms = discord.Permissions(administrator=True)
                await ctx.guild.create_role(name='Teapot Owner', permissions=perms)
                for role in ctx.guild.roles:
                    if role.name == "Teapot Owner":
                        await ctx.guild.get_member(teapot.config.bot_owner()).add_roles(role)
                        break


    @discord.ext.commands.command()
    @discord.ext.commands.has_permissions(administrator=True)
    async def debug(self, ctx):
        embed = discord.Embed(title="Developers: RedTea, ColaIan", description="Debug info:",
                              color=0x7400FF)
        embed.set_author(name=f"Teapot.py {teapot.version()}",
                         icon_url="https://cdn.discordapp.com/avatars/612634758744113182/7fe078b5ea6b43000dfb7964e3e4d21d.png?size=512")
        embed.set_thumbnail(url="https://avatars2.githubusercontent.com/u/60006969?s=200&v=4")
        embed.add_field(name="Bot User:", value=self.bot.user, inline=True)
        embed.add_field(name="System Time:", value=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), inline=True)
        embed.add_field(name="Memory",
                        value=str(round(psutil.virtual_memory()[1] / 1024 / 1024 / 1024)) + "GB / " + str(round(
                            psutil.virtual_memory()[0] / 1024 / 1024 / 1024)) + "GB", inline=True)
        embed.add_field(name="O.S.:", value=str(teapot.platform()), inline=True)
        embed.add_field(name="Storage Type:", value=teapot.config.storage_type(), inline=True)
        embed.add_field(name="Prefix:", value=", ".join(teapot.config.bot_prefix()), inline=True)
        embed.add_field(name="Github Repo:", value="[Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py)",
                        inline=True)
        embed.add_field(name="Bug Report:", value="[Issues](https://github.com/RedCokeDevelopment/Teapot.py/issues)",
                        inline=True)
        embed.add_field(name="Website:", value="[Website](https://teapot.page)", inline=True)
        embed.add_field(name="Links",
                        value="[Support Discord](https://discord.gg/7BRGs6F) | [Add bot to server](https://discordapp.com/oauth2/authorize?client_id=669880564270104586&permissions=8&scope=bot) | [Repository](https://github.com/RedCokeDevelopment/Teapot.py)",
                        inline=False)
        embed.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
        # embed.set_image(url="https://user-images.githubusercontent.com/43201383/72987537-89830a80-3e25-11ea-95ef-ecfa0afcff7e.png")
        await ctx.message.author.send(embed=embed)
        await ctx.message.add_reaction(emoji='✅')
 

def setup(bot):
    bot.add_cog(Commands(bot))
