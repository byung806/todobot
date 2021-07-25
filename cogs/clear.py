'''
Clear all your tasks in your todo-list.
'''

import discord
import json
from discord.ext import commands

from util.send_embed import send_embed


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['empty', 'wipe'])
    async def clear(self, ctx, *, content=None):
        data = json.load(open('data\\tasks.json', 'r'))
        if str(ctx.message.author.id) in data:
            await send_embed(ctx, 'Confirmation',
                             'Are you sure you want to clear your todo-list? This is **irreversible**.')
            if (await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content.lower() in ['yes','y','yup','sure','ok','okay']:
                data[str(ctx.message.author.id)] = {}
                json_data = json.dumps(data)
                f = open('data\\tasks.json', 'w')
                f.write(json_data)
                f.close()
                await send_embed(ctx, 'Todo-list cleared', 'Cleared your todo-list!')
            else:
                await send_embed(ctx, 'Not cleared', 'Okay, didn\'t clear your todo-list.')
        else:
            await send_embed(ctx, 'No todo-list', 'You don\'t have a todo-list! Create one with the `add` command.')

def setup(bot):
    bot.add_cog(Clear(bot))