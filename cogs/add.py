'''
Add a task to the todolist.
'''

import discord
import json
from discord.ext import commands

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *, task):
        data = json.load(open('data\\tasks.json', 'r'))
        if str(ctx.message.author.id) in data:
            if task not in data[str(ctx.message.author.id)]:
                data[str(ctx.message.author.id)][task] = False
                added = task
            else:
                count = 2
                while f'{task} (#{count})' in data[str(ctx.message.author.id)]:
                    count += 1
                data[str(ctx.message.author.id)][f'{task} (#{count})'] = False
                added = f'{task} (#{count})'
        else:
            data[str(ctx.message.author.id)] = {task: False}
            added = task
        json_data = json.dumps(data)
        f = open('data\\tasks.json', 'w')
        f.write(json_data)
        f.close()
        await send_embed(ctx, 'Task added', f'Added **{added}**.')

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await send_embed(ctx, 'Provide a task name', 'You need *something* to put on your todo-list.\n'
                                                         f'Use `{await get_server_prefix(self.bot, ctx)}'
                                                         f'add <task>` to add a task.')
        else:
            raise error

def setup(bot):
    bot.add_cog(Add(bot))