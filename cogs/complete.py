'''
Mark a task as complete in your todo-list.
'''

import discord
import json
from discord.ext import commands

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Complete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['finish'])
    async def complete(self, ctx, *, task):
        data = json.load(open('data\\tasks.json', 'r'))
        if str(ctx.message.author.id) in data:
            found = []
            for t in data[str(ctx.message.author.id)].keys():  # finding matching tasks with diff capitalization
                if t.lower() == task.lower():
                    found.append(t)

            if len(found) >= 2:  # found 2 or more matching tasks to delete
                if task not in found:
                    await send_embed(ctx, 'Multiple tasks found',
                                     f'Which task would you like to mark as complete? ({", ".join(found)})')
                    choice = (await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content
                    while choice not in found:
                        await send_embed(ctx,
                                         'Choose a task from the list',
                                         f'Which task would you like to mark as complete? ({", ".join(found)})\n(Case sensitive)')
                        choice = (await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content
                    data[str(ctx.message.author.id)][choice] = True  # valid choice inside found
                    complete = choice
                else:  # if exact same capitalization is found
                    data[str(ctx.message.author.id)][task] = True
                    complete = task

            elif len(found) == 1:  # only 1 is found
                data[str(ctx.message.author.id)][found[0]] = True
                complete = found[0]

            else:  # no matches are found
                await send_embed(ctx, 'Couldn\'t find any tasks with that name',
                                 'No matches were found. Use the `list` command to check your todo-list.')
                return
        else:  # no todo-list found
            await send_embed(ctx, 'Empty todo-list', 'Your todo-list is empty. Add a task using the `add` command.')
            return

        json_data = json.dumps(data)
        f = open('data\\tasks.json', 'w')
        f.write(json_data)
        f.close()
        await send_embed(ctx, 'Task marked as complete', f'Marked **{complete}** as complete.')

    @complete.error
    async def complete_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await send_embed(ctx, 'Provide a task name', 'You need *something* to mark as complete in your todo-list.\n'
                                                         f'Use `{await get_server_prefix(self.bot, ctx)}'
                                                         f'complete <task>` to mark a task as complete.')
        else:
            raise error

def setup(bot):
    bot.add_cog(Complete(bot))