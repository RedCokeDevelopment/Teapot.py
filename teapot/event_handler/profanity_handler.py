import teapot
from teapot.events import predict_prob
import discord

async def on_message_handler(bot, message):
    punctuations = '!()-[]{};:\'"\\,<>./?@#$%^&*_~'
    msg = ""
    for char in message.content.lower():
        if char not in punctuations:
            msg = msg + char
    prob = predict_prob([msg])
    if prob >= 0.8:
        em = discord.Embed(title=f"AI Analysis Results", color=0xC54B4F)
        em.add_field(name='PROFANITY DETECTED! ', value=str(prob[0]))
        await message.channel.send(embed=em)