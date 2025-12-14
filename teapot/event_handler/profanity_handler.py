import re
import teapot
from profanity_check import predict_prob
import discord
from teapot.tools.teascout_client import TeaScout

# Pre-initialize TeaScout client and model name if using external API
client = None
_profanity_model_name = None
cfg = teapot.config.profanity_filter()
if isinstance(cfg, str) and cfg.startswith("http"):
    # Expected format: https://api_key:model_name@example.com
    m = re.match(r'^(https?://)', cfg)
    scheme = m.group(1) if m else ''
    left, host = cfg.split('@', 1)
    # remove scheme from left if present
    if left.startswith('http://') or left.startswith('https://'):
        left = left.split('://', 1)[1]
    # left should now be 'api_key:model_name'
    if ':' in left:
        api_key, _profanity_model_name = left.split(':', 1)
    else:
        api_key = left
        _profanity_model_name = None
    base_url = scheme + host
    client = TeaScout(base_url, api_key)


async def on_message_handler(bot, message):
    punctuations = '!()-[]{};:\'"\\,<>./?@#$%^&*_~'
    msg = ""
    for char in message.content.lower():
        if char not in punctuations:
            msg = msg + char
    if teapot.config.profanity_filter() == "none":
        return
    elif teapot.config.profanity_filter() == "local":
        prob = predict_prob([msg])
        if prob[0] >= 0.8:
            em = discord.Embed(title=f"AI Analysis Results", color=0xC54B4F)
            em.add_field(name='PROFANITY DETECTED! ', value=str(prob[0]))
            await message.channel.send(embed=em)
    else:
        # Use parsed model name if available, otherwise fall back to default
        model_name = _profanity_model_name or "default"
        model = client.model(model_name).text(msg)
        result = model.inference()
        score = result.get('score', 0)
        if score >= 0.8:
            em = discord.Embed(title=f"AI Analysis Results", color=0xC54B4F)
            em.add_field(name='Hate Speech detected! ', value=str(score))
            em.set_footer(text="This is a experimental feature powered by TeaScout. Feedback is welcome!")
            await message.channel.send(embed=em)
