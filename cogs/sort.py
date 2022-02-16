import json

import discord
from discord.ext import commands

from util.generate_embed import generate_embed


class Sort(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sort(self, ctx, *, type=None):
        '''
        Sort list in different formats
        '''
        data = json.load(open('data\\tasks.json', 'r'))
        if str(ctx.message.author.id) in data:
            tasks = data[str(ctx.message.author.id)]

            if type in ['completed', 'complete', 'done', 'finished', 'unfinished', 'to-do', 'td', 'not done',
                        'incomplete']:
                completed = dict()
                uncompleted = dict()
                for task in tasks:
                    if tasks[task][0]:
                        completed[task] = [True, tasks[task][1]]
                    else:
                        uncompleted[task] = [False, tasks[task][1]]
                data[str(ctx.message.author.id)] = uncompleted | completed
                type = 'completed'
            elif type in ['priority', 'important', 'most important', 'pr', 'imp']:
                for task in tasks:
                    print({k: v for k, v in sorted(tasks.items(), key=lambda item: item[1][1], reverse=True)})

        json_data = json.dumps(data)
        f = open('data\\tasks.json', 'w')
        f.write(json_data)
        f.close()
        await ctx.send(
            embed=await generate_embed(ctx.message.author, 'Sort complete', f'Sorted your todo-list by **{type}**.',
                                       color=discord.Color.green()))


def setup(bot):
    bot.add_cog(Sort(bot))
