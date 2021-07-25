'''
Set a reminder for the future (ex: todo rm 1d4h do the dishes)
'''
import asyncio
import json
import time

import discord
from discord.ext import commands
from discord.ext import tasks

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def parse_time(self, time):
        seconds = 0
        multi = 1
        positions = {'d': 3600 * 24, 'h': 3600, 'm': 60, 's': 1}
        i = 0
        while i < len(time):
            if time[i] in positions:
                multi = positions[time[i]]
                i += 1
            elif time[i] in '1234567890':
                num = []
                try:
                    while i < len(time):
                        num.insert(0, int(time[i]))
                        i += 1
                    seconds += multi * int(''.join(map(str, num)))
                except ValueError:
                    if num:
                        seconds += multi * int(''.join(map(str, num)))
            else:
                return -1
        return seconds

    @commands.command(aliases=['remind', 'rm', 'notify', 'notifyme', 'timer', 'remindme'])
    async def reminder(self, ctx, time: str, *, reminder: str):
        if not reminder:
            reminder = ''
        time = time.lower()[::-1]
        seconds = int(await self.parse_time(time))
        if seconds == -1:
            raise Exception
        temp = seconds
        days = int(temp/(3600*24))
        temp -= days*3600*24
        hours = int(temp/(3600))
        temp -= hours*3600
        minutes = int(temp/(60))
        temp -= minutes*60
        secs = temp
        time_list = []
        if days != 0:
            if days == 1:
                time_list.append(f'{days} day')
            else:
                time_list.append(f'{days} days')
        if hours != 0:
            if hours == 1:
                time_list.append(f'{hours} hour')
            else:
                time_list.append(f'{hours} hours')
        if minutes != 0:
            if minutes == 1:
                time_list.append(f'{minutes} minute')
            else:
                time_list.append(f'{minutes} minutes')
        if secs != 0:
            if secs == 1:
                time_list.append(f'{secs} second')
            else:
                time_list.append(f'{secs} seconds')
        time_string = ' '.join(time_list)
        msg = await send_embed(ctx, 'Set a reminder', f'<@!{ctx.author.id}>, I\'ll remind you about **{reminder}** in **{time_string}**.')
        await asyncio.sleep(seconds)
        embed = await send_embed(ctx, 'Reminder', f'<@!{ctx.author.id}>, **{time_string}** ago you asked to be reminded about **{reminder}**.'
                                          f'\n[Jump to message]({ctx.message.jump_url})', send=False)
        await ctx.author.send(embed=embed)
        await msg.add_reaction('<:check:867760636980756500>')

    @reminder.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await send_embed(ctx, 'Provide a reminder', 'You need *something* for me to remind you about.\n'
                                                         f'Use `{await get_server_prefix(self.bot, ctx)}remind <time> <reminder>` so I know what to remind you about.')
        else:
            raise error

def setup(bot):
    bot.add_cog(Reminder(bot))