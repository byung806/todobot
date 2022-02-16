'''
Add a task to the todolist.
'''

import json

import discord
from discord.ext import commands

from util.generate_embed import generate_embed
from util.get_server_prefix import get_server_prefix


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *, task):
        data = json.load(open('data\\tasks.json', 'r'))

        priority = ''
        while not priority.isdigit():
            await ctx.send(embed=await generate_embed(ctx.message.author, 'Choose priority',
                                                      f'Choose the priority of **{task}** from 1-10. Type `cancel` to cancel or `default`'
                                                      f' to choose the default priority (last).'))
            priority = (await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content
            if priority == 'cancel':
                await ctx.send(embed=await generate_embed(ctx.message.author, 'Add command cancelled',
                                                          f'Add something to your todo-list with '
                                                          f'{get_server_prefix(self.bot, ctx)}add <task>'))
                return
            elif priority == 'default':
                priority = 1
        priority = int(priority)

        if str(ctx.message.author.id) in data:
            if task not in data[str(ctx.message.author.id)]:
                data[str(ctx.message.author.id)][task] = [False, priority]
                added = task
            else:
                count = 2
                while f'{task} (#{count})' in data[str(ctx.message.author.id)]:
                    count += 1
                data[str(ctx.message.author.id)][f'{task} (#{count})'] = [False, priority]
                added = f'{task} (#{count})'
        else:
            data[str(ctx.message.author.id)] = {task: False}
            added = task

        json_data = json.dumps(data)
        f = open('data\\tasks.json', 'w')
        f.write(json_data)
        f.close()
        await ctx.send(embed=await generate_embed(ctx.message.author, 'Task added',
                                                  f'Added **{added}** with priority **{priority}**.',
                                                  color=discord.Color.green()))

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(embed=await generate_embed(ctx.message.author, 'Provide a task name',
                                                      'You need *something* to put on your todo-list.\n'
                                                      f'Use `{await get_server_prefix(self.bot, ctx)}'
                                                      f'add <task>` to add a task.',
                                                      color=discord.Color.red()))
        else:
            raise error


def setup(bot):
    bot.add_cog(Add(bot))
