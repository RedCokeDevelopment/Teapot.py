""" Module for generating a random cat picture"""
import io
import json

import aiohttp
import discord
import requests
from discord.ext import commands

import teapot
import teapot.tools.embed as dmbd


class Neko(commands.Cog):
    """ Cat Module"""

    def __init__(self, bot):
        """ Initialize Cat Class"""

        self.bot = bot

    def neko_api(self, ctx, x):
        try:
            req = requests.get(f'https://nekos.life/api/v2/img/{x}')
            if req.status_code != 200:
                print("Could not get a neko")
            apijson = json.loads(req.text)
            url = apijson["url"]
            em = dmbd.newembed().set_image(url=url)
            return em
        except:
            return teapot.messages.error(f"obtaining image ({req.status_code})")

    @commands.command(pass_context=True)
    async def neko(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "neko"))

    @commands.command(pass_context=True)
    async def waifu(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "waifu"))

    @commands.command(pass_context=True)
    async def avatar(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "avatar"))

    @commands.command(pass_context=True)
    async def wallpaper(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "wallpaper"))

    @commands.command(pass_context=True)
    async def tickle(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "tickle"))

    @commands.command(pass_context=True)
    async def ngif(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "ngif"))

    @commands.command(pass_context=True)
    async def poke(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "poke"))

    @commands.command(pass_context=True)
    async def kiss(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "kiss"))

    @commands.command(pass_context=True, aliases=['8ball'])
    async def eightball(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "8ball"))

    @commands.command(pass_context=True)
    async def lizard(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "lizard"))

    @commands.command(pass_context=True)
    async def slap(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "slap"))

    @commands.command(pass_context=True)
    async def cuddle(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "cuddle"))

    @commands.command(pass_context=True)
    async def goose(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "goose"))

    @commands.command(pass_context=True)
    async def gox_girl(self, ctx):
        await ctx.send(embed=self.neko_api(ctx, "fox_girl"))

    @commands.command(pass_context=True)
    async def hentai(self, ctx, type=""):
        if ctx.message.channel.nsfw:
            api_types = ['femdom', 'classic', 'erofeet', 'erok', 'les',
                         'hololewd', 'lewdk', 'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri',
                         'tits', 'pussy_jpg', 'cum_jpg', 'pussy', 'lewdkemo', 'lewd', 'cum', 'spank',
                         'smallboobs', 'Random_hentai_gif', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat',
                         'feet', 'smug', 'kemonomimi', 'solog', 'holo', 'bj', 'woof', 'yuri', 'trap', 'anal', 'baka',
                         'blowjob', 'holoero', 'feed', 'gasm', 'hentai', 'futanari', 'ero', 'solo', 'pwankg', 'eron',
                         'erokemo']
            if type in api_types:
                try:
                    req = requests.get(f'https://nekos.life/api/v2/img/{type}')
                    if req.status_code != 200:
                        print("Unable to obtain image")
                    apijson = json.loads(req.text)
                    url = apijson["url"]

                    message = await ctx.send(embed=teapot.messages.downloading())
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            if resp.status != 200:
                                print(resp.status)
                                print(await resp.read())
                                return await ctx.send('Could not download file...')
                            data = io.BytesIO(await resp.read())
                            await ctx.send(
                                file=discord.File(data, f'SPOILER_HENTAI.{url.split("/")[-1].split(".")[-1]}'))
                            await message.delete()
                except:
                    await ctx.send(embed=teapot.messages.error(f"obtaining image ({req.status_code})"))
            else:
                await ctx.send(embed=teapot.messages.invalidargument(", ".join(api_types)))
        else:
            await ctx.send("This command only works in NSFW channels!")


def setup(bot):
    """ Setup Neko Module"""
    bot.add_cog(Neko(bot))
