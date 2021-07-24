import discord

from util.get_embed_color import get_embed_color


async def send_embed(ctx, title, description, avatar_url=None, send=True):
    if not avatar_url:
        avatar_url = ctx.author.avatar_url
    embed = discord.Embed(
        description=description,
        color=get_embed_color(ctx.author.id)
    ).set_author(name=title, icon_url=avatar_url)
    if send:
        return await ctx.channel.send(embed=embed)
    else:
        return embed