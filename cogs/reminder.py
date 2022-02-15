import json
import re
import time
from datetime import datetime

import discord
from discord.ext import commands, tasks

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel()

    async def parse_time(self, time):
        if re.fullmatch(r'((2[0-4]|1[3-9]):(5[0-9]|4[0-9]|3[0-9]|2[0-9]|1[0-9]|0[0-9]))|'
                        r'((1[0-2]|0?[1-9]):(5[0-9]|4[0-9]|3[0-9]|2[0-9]|1[0-9]|0[0-9])[pa]m?)', time):
            now_time = datetime.now().hour * 3600 + datetime.now().minute * 60
            time = time.replace('m', '')
            if time.endswith('p') or time.endswith('a'):
                times = [int(x) for x in time[:-1].split(':')]
                if time.endswith('p'):
                    times[0] += 12
            else:
                times = [int(x) for x in time.split(':')]
            time = times[0] * 3600 + times[1] * 60
            if now_time > time:
                seconds = time + 86400 - now_time
            else:
                seconds = time - now_time
        else:
            time = time.lower()[::-1]
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
    async def reminder(self, ctx, t: str, *, reminder: str):
        '''
        Set a reminder for the future (ex: todo rm 1d4h do the dishes)
        '''
        if not reminder:
            reminder = ''
        seconds = int(await self.parse_time(t))
        if seconds == -1:
            raise Exception
        temp = seconds
        days = int(temp / (3600 * 24))
        temp -= days * 3600 * 24
        hours = int(temp / 3600)
        temp -= hours * 3600
        minutes = int(temp / 60)
        temp -= minutes * 60
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
        msg = await send_embed(ctx, 'Set a reminder',
                               f'<@!{ctx.author.id}>, I\'ll remind you about **{reminder}** in **{time_string}**.',
                               color=discord.Color.green())
        data = json.load(open('data\\reminders.json', 'r'))
        seconds += time.time()
        data[seconds] = [ctx.author.id, ctx.channel.id, reminder, time_string, msg.id]
        json_data = json.dumps(data)
        f = open('data\\reminders.json', 'w')
        f.write(json_data)
        f.close()

    @reminder.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await send_embed(ctx, 'Provide a reminder', 'You need *something* for me to remind you about.\n'
                                                        f'Use `{await get_server_prefix(self.bot, ctx)}remind <time> <reminder>`.',
                             color=discord.Color.red())
        else:
            await send_embed(ctx, 'Provide a valid time', 'You need to specify a valid time.\n'
                                                          f'Use `{await get_server_prefix(self.bot, ctx)}remind <time> <reminder>`'
                                                          f' where `<time>` is a time like `11:59p`, `9:00am`, `4:44pm`, `23:29` or in relative format like'
                                                          f' `4h40s` or `1d30m10s`.',
                             color=discord.Color.red())

    @tasks.loop(seconds=5.0)
    async def reminder_loop(self):
        # [time since epoch: [userid, channelid, messagecontent, timestring, originalmessageid]]
        data = json.load(open('data\\reminders.json', 'r'))
        current_time = time.time()
        for t, reminder_specifics in dict(data).items():
            if float(t) <= current_time:
                user_id, channel_id, reminder, time_string, message_id = reminder_specifics
                author = await self.bot.fetch_user(user_id)
                channel = await self.bot.fetch_channel(channel_id)
                message = await channel.fetch_message(message_id)
                embed = await send_embed(channel, 'Reminder',
                                         f'<@!{author.id}>, **{time_string}** ago you asked to be reminded about **{reminder}**. '
                                         f'\n[Jump to reminder]({message.jump_url})', avatar_url=author.avatar_url,
                                         send=False)
                await author.send(embed=embed)
                await message.add_reaction('<:check:867760636980756500>')

                data.pop(t)
                json_data = json.dumps(data)
                f = open('data\\reminders.json', 'w')
                f.write(json_data)
                f.close()

    @reminder_loop.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Reminder(bot))
