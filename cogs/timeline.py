'''
Display timeline of future events
'''

from discord.ext import commands

from util.generate_embed import generate_embed


class Timeline(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['today'])
    async def timeline(self, ctx, *, content=None):
        await ctx.send(
            embed=await generate_embed(ctx.message.author, 'Pong!', f'**Ping:** {round(self.bot.latency, 2)}ms'))


def setup(bot):
    bot.add_cog(Timeline(bot))
