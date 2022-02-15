'''
The bot's help command.
'''

import ast
import os

import discord
from discord.ext import commands

from util.get_server_prefix import get_server_prefix


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = dict()
        for cmd in os.listdir('cogs'):
            if cmd.endswith('.py'):
                with open('cogs\\' + cmd, 'r') as f:
                    self.commands[cmd] = ast.get_docstring(ast.parse(f.read()))

    @commands.command()
    async def help(self, ctx, *, content=None):
        embed = discord.Embed(
            title='**Todo-bot Command List**',
            description=f'**Prefix: {await get_server_prefix(self.bot, ctx)}**',
            color=discord.Color.blue()
        )
        for cmd in self.commands:
            embed.add_field(name=cmd[:-3], value=self.commands[cmd])
        await ctx.message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
