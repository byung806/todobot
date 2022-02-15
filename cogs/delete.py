'''
Delete a task from the todolist.
'''

import json

import discord
from discord.ext import commands

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['remove', 'del'])
    async def delete(self, ctx, *, task):
        data = json.load(open('data\\tasks.json', 'r'))
        if str(ctx.message.author.id) in data:
            if task == 'all' or task == 'everything':
                data[str(ctx.message.author.id)] = []
                popped = 'all'
            else:
                found = []
                for t in data[str(ctx.message.author.id)].keys():  # finding matching tasks with diff capitalization
                    if t.lower() == task.lower() and not data[str(ctx.message.author.id)][t]:
                        found.append(t)

                if len(found) >= 2:  # found 2 or more matching tasks to delete
                    if task not in found:
                        await send_embed(ctx, 'Multiple tasks found',
                                         f'Which task would you like to remove? ({", ".join(found)})')
                        choice = (
                            await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content
                        while choice not in found:
                            await send_embed(ctx,
                                             'Choose a task from the list',
                                             f'Which task would you like to remove? ({", ".join(found)})\n(Case sensitive)')
                            choice = (
                                await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content
                        data[str(ctx.message.author.id)].pop(choice)  # valid choice inside found
                        popped = choice
                    else:  # if exact same capitalization is found
                        data[str(ctx.message.author.id)].pop(task)
                        popped = task

                elif len(found) == 1:  # only 1 is found
                    data[str(ctx.message.author.id)].pop(found[0])
                    popped = found[0]

                else:  # no matches are found
                    await send_embed(ctx, 'Couldn\'t find any tasks with that name',
                                     'No matches were found. Use the `list` command to check your todo-list.',
                                     color=discord.Color.red())
                    return
        else:  # no todo-list found
            await send_embed(ctx, 'Empty todo-list', 'Your todo-list is empty. Add a task using the `add` command.',
                             color=discord.Color.red())
            return

        if popped != 'all':
            await send_embed(ctx, 'Task deleted', f'Removed **{popped}**.', color=discord.Color.green())
            json_data = json.dumps(data)
            f = open('data\\tasks.json', 'w')
            f.write(json_data)
            f.close()
        else:
            await send_embed(ctx, 'Confirmation',
                             'Are you sure you want to clear your todo-list? This is **irreversible**.')
            if (await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)).content.lower() in [
                'yes', 'y', 'yup', 'sure', 'ok', 'okay', 'yeah', 'ofc', 'of course']:
                data[str(ctx.message.author.id)] = {}
                json_data = json.dumps(data)
                f = open('data\\tasks.json', 'w')
                f.write(json_data)
                f.close()
                await send_embed(ctx, 'Todo-list cleared', 'Deleted all tasks on your todo-list!',
                                 color=discord.Color.green())
            else:
                await send_embed(ctx, 'Not cleared', 'Okay, didn\'t delete all tasks on your todo-list.')

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await send_embed(ctx, 'Provide a task name', 'You need *something* to delete from your todo-list.\n'
                                                         f'Use `{await get_server_prefix(self.bot, ctx)}'
                                                         f'delete <task>` to delete a task.',
                             color=discord.Color.red())
        else:
            raise error


def setup(bot):
    bot.add_cog(Delete(bot))
