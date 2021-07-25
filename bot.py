import json
import os

import discord
from discord.ext import commands
from discord.ext import tasks

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed
from data.default_prefix import PREFIX


def mixed_case(*args):
    total = []
    import itertools
    for string in args:
        a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string)))
        for x in list(a): total.append(x)
    return list(total)

TOKEN = "ODY3NTIwNDYyNzg3MDUxNTUy.YPiTZA.4jvfp4c8k60VsajvD05JLiAzvqE"
bot = commands.Bot(command_prefix=get_server_prefix, case_insensitive=True)
bot.remove_command('help')

for extension in os.listdir('cogs'):
    if extension.endswith('.py'):
        bot.load_extension('cogs.' + extension[:-3])

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            prefix = PREFIX
            embed = discord.Embed(
                description=f'Hey! I\'m **Todo-bot**, a productivity & organization bot.\n\n'
                            f'To see what I can do, send `{prefix} help`. All my commands are run like this,'
                            f'with a `{prefix}` before the command (for example `{prefix} add <task>`).\n\n'
            )
            embed.add_field(name='**My Links**',
                            value='[Invite]('
                                  'https://discord.com/api/oauth2/authorize?client_id=867520462787051552&permissions'
                                  '=2553670736&scope=bot'
                                  ') - Add this bot to one of your servers and up your productivity!',inline=False)
            await channel.send(embed=embed)
        break

@bot.event
async def on_ready():
    count = 0
    for guild in bot.guilds:
        count += guild.member_count
    print(f'Connected to {len(bot.guilds)} guild(s) and serving {count} members')

@bot.event
async def on_message(message):
    if f'<@!{bot.user.id}>' in message.content:
        await send_embed(message, 'Hey! I\'m Todo-bot.', f'Run `{await get_server_prefix(message, message.guild.id)}'
                                                         f' help` to see my commands.', bot.user.avatar_url)
    await bot.process_commands(message)

bot.run(TOKEN)