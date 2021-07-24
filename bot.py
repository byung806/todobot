import discord
import os
from discord.ext import commands

from util.send_embed import send_embed
from data.prefix import PREFIX


def mixed_case(*args):
    total = []
    import itertools
    for string in args:
        a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in       string)))
        for x in list(a): total.append(x)
    return list(total)

TOKEN = "ODY3NTIwNDYyNzg3MDUxNTUy.YPiTZA.4jvfp4c8k60VsajvD05JLiAzvqE"
bot = commands.Bot(command_prefix=list(map(lambda x: x + ' ', mixed_case(f'{PREFIX}'))), case_insensitive=True)
bot.remove_command('help')

for extension in os.listdir('cogs'):
    if extension.endswith('.py'):
        bot.load_extension('cogs.' + extension[:-3])

@bot.event
async def on_ready():
    count = 0
    for guild in bot.guilds:
        count += guild.member_count
    print(f'Connected to {len(bot.guilds)} guild(s) and serving {count} members')

@bot.event
async def on_message(message):
    if f'<@!{bot.user.id}>' in message.content:
        await send_embed(message, 'Hey! I\'m Todo-bot.', f'Run `{PREFIX} help` to see my commands.', bot.user.avatar_url)
    await bot.process_commands(message)

bot.run(TOKEN)