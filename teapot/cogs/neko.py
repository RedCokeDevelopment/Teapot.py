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

    # api_options = ['femdom', 'tickle', 'classic', 'ngif', 'erofeet', 'meow', 'erok', 'poke', 'les', 'v3',
    # 'hololewd', 'nekoapi_v3.1', 'lewdk', 'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri', 'kiss', '8ball', 'kuni',
    # 'tits', 'pussy_jpg', 'cum_jpg', 'pussy', 'lewdkemo', 'lizard', 'slap', 'lewd', 'cum', 'cuddle', 'spank',
    # 'smallboobs', 'goose', 'Random_hentai_gif', 'avatar', 'fox_girl', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat',
    # 'feet', 'smug', 'kemonomimi', 'solog', 'holo', 'wallpaper', 'bj', 'woof', 'yuri', 'trap', 'anal', 'baka',
    # 'blowjob', 'holoero', 'feed', 'neko', 'gasm', 'hentai', 'futanari', 'ero', 'solo', 'waifu', 'pwankg', 'eron',
    # 'erokemo']

    def __init__(self, bot):
        """ Initialize Cat Class"""

        self.bot = bot

    @commands.command(pass_context=True)
    async def neko(self, ctx):
        """ When User Types ~neko, return a neko link """
        req = requests.get('https://nekos.life/api/v2/img/neko')
        if req.status_code != 200:
            print("Could not get a neko")
        nekolink = json.loads(req.text)
        rngneko = nekolink["url"]
        em = dmbd.newembed()
        em.set_image(url=rngneko)
        await ctx.send(embed=em)

    @commands.command(pass_context=True)
    async def waifu(self, ctx):
        """ When User Types ~waifu, return a waifu link """
        req = requests.get('https://nekos.life/api/v2/img/waifu')
        if req.status_code != 200:
            print("Could not get a waifu")
        waifulink = json.loads(req.text)
        rngwaifu = waifulink["url"]
        em = dmbd.newembed()
        em.set_image(url=rngwaifu)
        await ctx.send(embed=em)

    @commands.command(pass_context=True, aliases=['manofculture'])
    async def hentai(self, ctx, type=""):
        """ When User Types ~hentai, return a hentai link """
        if ctx.message.channel.nsfw:
            if type.lower() == "ero":
                req = requests.get('https://nekos.life/api/v2/img/ero')
                if req.status_code != 200:
                    print("Could not get a hentai image")
                hentailink = json.loads(req.text)
                hentaiimg = hentailink["url"]

                message = await ctx.send(embed=teapot.messages.downloading())
                async with aiohttp.ClientSession() as session:
                    async with session.get(hentaiimg) as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.send(file=discord.File(data, 'SPOILER_HENTAI.gif'))
                        await message.delete()
            elif type.lower() == "neko":
                req = requests.get('https://nekos.life/api/v2/img/nsfw_neko_gif')
                if req.status_code != 200:
                    print("Could not get a hentai image")
                hentailink = json.loads(req.text)
                hentaiimg = hentailink["url"]

                message = await ctx.send(embed=teapot.messages.downloading())
                async with aiohttp.ClientSession() as session:
                    async with session.get(hentaiimg) as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.send(file=discord.File(data, 'SPOILER_HENTAI.gif'))
                        await message.delete()
            elif type.lower() == "random":
                req = requests.get('https://nekos.life/api/v2/img/Random_hentai_gif')
                if req.status_code != 200:
                    print("Could not get a hentai image")
                hentailink = json.loads(req.text)
                hentaiimg = hentailink["url"]

                message = await ctx.send(embed=teapot.messages.downloading())
                async with aiohttp.ClientSession() as session:
                    async with session.get(hentaiimg) as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.send(file=discord.File(data, 'SPOILER_HENTAI.gif'))
                        await message.delete()
            else:
                try:
                    req = requests.get(f'https://nekos.life/api/v2/img/{type}')
                    if req.status_code != 200:
                        print("Could not get a hentai image")
                    hentailink = json.loads(req.text)
                    hentaiimg = hentailink["url"]

                    message = await ctx.send(embed=teapot.messages.downloading())
                    async with aiohttp.ClientSession() as session:
                        async with session.get(hentaiimg) as resp:
                            if resp.status != 200:
                                return await ctx.send('Could not download file...')
                            data = io.BytesIO(await resp.read())
                            await ctx.send(file=discord.File(data, 'SPOILER_HENTAI.gif'))
                            await message.delete()
                except:
                    await ctx.send(embed=teapot.messages.invalidarguments("ero, neko, random"))
        else:
            await ctx.send("This command only works in NSFW channels!")


def setup(bot):
    """ Setup Neko Module"""
    bot.add_cog(Neko(bot))
