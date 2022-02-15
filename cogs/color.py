import json
import re

from discord.ext import commands

from util.get_embed_color import get_embed_color
from util.send_embed import send_embed


class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['changecolor', 'colors'])
    async def color(self, ctx, *, color=None):
        data = json.load(open('data\\colors.json', 'r'))
        if not color:
            color = get_embed_color(ctx.message.author.id, True)
            description = f'Your color is {color}.'
        else:
            regex = "^#*([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            p = re.compile(regex)
            if re.search(p, color):
                if len(color) == 4:
                    color = '#' + ''.join(map(lambda x: x + x, color[1:].split('')))
                data[str(ctx.message.author.id)] = color
                json_data = json.dumps(data)
                f = open('data\\colors.json', 'w')
                f.write(json_data)
                f.close()
                description = f'Set your color to {color}.'
            else:
                raise Exception

        await send_embed(ctx, f'{ctx.message.author.name}\'s color', description)

    @color.error
    async def color_error(self, ctx, error):
        await send_embed(ctx, 'Invalid color', 'Enter a valid hex value (ex: #FFF or #121B24)')


def setup(bot):
    bot.add_cog(Color(bot))
