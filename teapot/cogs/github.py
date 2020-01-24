import json

import requests
from bs4 import BeautifulSoup
from discord.ext import commands

import teapot
import teapot.tools.embed as dmbd


class GitHub(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['gh'])
    async def github(self, ctx, arg):
        req = requests.get(f'https://api.github.com/repos/{arg}')
        apijson = json.loads(req.text)
        if req.status_code == 200:
            em = dmbd.newembed()
            em.set_author(name=apijson['owner']['login'], icon_url=apijson['owner']['avatar_url'],
                          url=apijson['owner']['html_url'])
            em.set_thumbnail(url=apijson['owner']['avatar_url'])
            em.add_field(name="Repository:", value=f"[{apijson['name']}]({apijson['html_url']})", inline=True)
            em.add_field(name="Language:", value=apijson['language'], inline=True)

            try:
                license = f"[{apijson['license']['spdx_id']}]({json.loads(requests.get(apijson['license']['url']).text)['html_url']})"
            except:
                license = "None"
            em.add_field(name="License:", value=license, inline=True)
            if apijson['stargazers_count'] != 0:
                em.add_field(name="Star:", value=apijson['stargazers_count'], inline=True)
            if apijson['forks_count'] != 0:
                em.add_field(name="Fork:", value=apijson['forks_count'], inline=True)
            if apijson['open_issues'] != 0:
                em.add_field(name="Issues:", value=apijson['open_issues'], inline=True)
            em.add_field(name="Description:", value=apijson['description'], inline=False)

            for meta in BeautifulSoup(requests.get(apijson['html_url']).text, features="html.parser").find_all('meta'):
                try:
                    if meta.attrs['property'] == "og:image":
                        em.set_image(url=meta.attrs['content'])
                        break
                except:
                    pass

            await ctx.send(embed=em)
        elif req.status_code == 404:
            ctx.send(embed=teapot.messages.notfound("repository"))
        else:
            ctx.send(embed=teapot.messages.error("repository"))


def setup(bot):
    """ Setup GitHub Module"""
    bot.add_cog(GitHub(bot))
