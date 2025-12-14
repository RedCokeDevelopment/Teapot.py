import discord
import teapot

async def on_message_handler(bot, message):
    punctuations = '!()-[]{};:\'"\\,<>./?@#$%^&*_~'
    msg = ""
    for char in message.content.lower():
        if char not in punctuations:
            msg = msg + char
    if msg.startswith("system call "):
        content = msg[12:].split(" ")
        if content[0].lower() == "inspect":
            if content[1].lower() == "entire":
                if content[2].lower() == "command":
                    if content[3].lower() == "list":
                        em = discord.Embed(title=f"🍢 SAO Command List", color=0x7400FF)
                        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/668816286784159763/674285661510959105/Kirito-Sao-Logo-1506655414__76221.1550241566.png")
                        em.add_field(name='Commands', value="generate xx element\ngenerate xx element xx shape\ninspect entire command list")
                        em.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
                        await message.channel.send(embed=em)
        elif content[0].lower() == "generate":
            if content[-1].lower() == "element":
                em = discord.Embed(title=f"✏ Generated {content[1].lower()} element!", color=0xFF0000)
                await message.channel.send(embed=em)
            if content[-1].lower() == "shape":
                if content[2].lower() == "element":
                    em = discord.Embed(title=f"✏ Generated {content[-2].lower()} shaped {content[1].lower()} element!", color=0xFF0000)
                    await message.channel.send(embed=em)
