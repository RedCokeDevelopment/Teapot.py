""" Module for generating a random cat picture"""
import json

import requests
from bs4 import BeautifulSoup
from discord.ext import commands

import teapot.tools.embed as dmbd


class Cat(commands.Cog):
    """ Cat and dog command"""

    def __init__(self, bot):
        """ Initialize Cat Class"""

        self.bot = bot

    @commands.command(pass_context=True, aliases=['meow'])
    async def cat(self, ctx):
        """ Get a cat image """
        req = requests.get('https://api.thecatapi.com/v1/images/search')
        if req.status_code != 200:
            print("Could not get a meow")
        catlink = json.loads(req.text)[0]
        rngcat = catlink["url"]
        em = dmbd.newembed()
        em.set_image(url=rngcat)
        await ctx.send(embed=em)

    @commands.command(pass_context=True, aliases=['woof'])
    async def dog(self, ctx):
        """ Get a dog image """
        req = requests.get('http://random.dog/')
        if req.status_code != 200:
            print("Could not get a woof")
        doglink = BeautifulSoup(req.text, 'html.parser')
        rngdog = 'http://random.dog/' + doglink.img['src']
        em = dmbd.newembed()
        em.set_image(url=rngdog)
        await ctx.send(embed=em)


def setup(bot):
    """ Setup Cat Module"""
    bot.add_cog(Cat(bot))
