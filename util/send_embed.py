import discord


async def send_embed(ctx, title, description, avatar_url=None, send=True, color=None):
    if not color:
        color = discord.Color.blue()
    if not avatar_url:
        avatar_url = ctx.author.avatar_url
    embed = discord.Embed(
        description=description,
        color=color
    ).set_author(name=title, icon_url=avatar_url)
    if send:
        return await ctx.send(embed=embed)
    else:
        return embed
