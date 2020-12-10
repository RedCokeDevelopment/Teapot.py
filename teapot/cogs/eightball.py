""" Module for generating random neko pictures"""
import io
import json

import aiohttp
import discord
import requests
from discord.ext import commands

import teapot
import teapot.tools.embed as dmbd


class EightBall(commands.Cog):
    """8 Ball"""

    def __init__(self, bot):
        """ Initialize 8ball class"""
        self.bot = bot

    def eightball_api(self, ctx):
        try:
            req = requests.get(f'https://nekos.life/api/v2/8ball/{x}')
            if req.status_code != 200:
                print("Could not get a response")
            apijson = json.loads(req.text)
            em = dmbd.newembed().set_image(url=apijson["url"])
            return em
        except:
            return teapot.messages.error(f"obtaining 8ball image ({req.status_code})")

    @commands.command(pass_context=True)
    async def eightball(self, ctx):
        await ctx.send(embed=self.eightball_api(ctx))

def setup(bot):
    """ Setup Eight Ball Module"""
    bot.add_cog(EightBall(bot))
