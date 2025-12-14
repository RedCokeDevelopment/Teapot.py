from discord import utils

async def on_message_handler(bot, message):
    if message.author.bot:
        return
    if ":" in message.content:
        emoji_cog = bot.get_cog("Emoji")  # obtain the Emoji Cog instance
        if emoji_cog is None:
            return
        msg = await emoji_cog.getinstr(message.content)
        ret = ""
        em = False
        smth = message.content.split(":")
        if len(smth) > 1:
            for word in msg:
                if word.startswith(":") and word.endswith(":") and len(word) > 1:
                    emoji = await emoji_cog.getemote(word)
                    if emoji is not None:
                        em = True
                        ret += f" {emoji}"
                    else:
                        ret += f" {word}"
                else:
                    ret += f" {word}"
        else:
            ret += msg
        if em:
            webhooks = await message.channel.webhooks()
            webhook = utils.get(webhooks, name="Imposter NQN")
            if webhook is None:
                webhook = await message.channel.create_webhook(name="Imposter NQN")
            await webhook.send(ret, username=message.author.name, avatar_url=message.author.display_avatar.url)
            await message.delete()
