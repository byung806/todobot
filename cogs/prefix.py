import json
import re

import discord
from discord.ext import commands

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pf', 'changeprefix', 'newprefix'])
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, new_prefix=None):
        '''
        Change the server-wide prefix!
        '''
        old_prefix = await get_server_prefix(self.bot, ctx)
        if not new_prefix:
            await send_embed(ctx, 'Server prefix', f'**{ctx.guild.name}**\'s current prefix is `{old_prefix}`.')
            return
        found = re.findall(r'".+"', new_prefix)
        if found:
            new_prefix = found[0][1:-1]
        else:
            raise Exception
        data = json.load(open('data\\prefixes.json', 'r'))
        if new_prefix == 'todo ' and str(ctx.guild.id) in data:
            data.pop(str(ctx.guild.id))
        else:
            data[str(ctx.guild.id)] = new_prefix
        json_data = json.dumps(data)
        f = open('data\\prefixes.json', 'w')
        f.write(json_data)
        f.close()
        await send_embed(ctx, 'Server prefix set', f'Prefix set to: `{new_prefix}`\nOld prefix: `{old_prefix}`',
                         color=discord.Color.green())

    @prefix.error
    async def prefix_error(self, ctx, error):
        await send_embed(ctx, 'Could not set prefix', 'Surround your new prefix in double quotes.'
                                                      f' (ex: {await get_server_prefix(self.bot, ctx)}prefix "todo "')


def setup(bot):
    bot.add_cog(Prefix(bot))
