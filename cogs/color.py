import json
import re

from discord.ext import commands

from util.generate_embed import generate_embed
from util.get_embed_color import get_embed_color


class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['changecolor', 'colors'])
    async def color(self, ctx, *, color=None):
        data = json.load(open('data\\colors.json', 'r'))
        if not color:
            color = get_embed_color(ctx.message.author.id, True)
            description = f'Your color is **{color}**.'
        else:
            preset_colors = json.load(open('data\\preset_colors.json', 'r'))
            if color in preset_colors:
                color = preset_colors[color]
            regex = "^#*([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            p = re.compile(regex)
            if re.search(p, color) or color == 'random':
                if color != 'random':
                    color = color.replace('#', '')
                    if (len(color) == 3):
                        color *= 2
                    data[str(ctx.message.author.id)] = int(color, 16)
                else:
                    data[str(ctx.message.author.id)] = color
                json_data = json.dumps(data)
                f = open('data\\colors.json', 'w')
                f.write(json_data)
                f.close()
                description = f'Set your color to **#{color.upper()}**.'
            else:
                raise Exception

        await ctx.send(
            embed=await generate_embed(ctx.message.author, f'{ctx.message.author.name}\'s color', description))

    @color.error
    async def color_error(self, ctx, error):
        await ctx.send(embed=await generate_embed(ctx.message.author, 'Invalid color',
                                                  'Enter a valid hex value (ex: #FFF or #121B24)'))


def setup(bot):
    bot.add_cog(Color(bot))
