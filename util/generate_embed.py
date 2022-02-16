import discord

from util.get_embed_color import get_embed_color


async def generate_embed(author, title, description, color=None):
    if not color:
        color = get_embed_color(author.id)
    embed = discord.Embed(
        description=description,
        color=color
    ).set_author(name=title, icon_url=author.avatar_url)
    return embed
