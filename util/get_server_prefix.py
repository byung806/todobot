import json

from data.config import PREFIX


async def get_server_prefix(bot, message) -> str:
    data = json.load(open('data\\prefixes.json', 'r'))
    if str(message.guild.id) in data:
        return data[str(message.guild.id)]
    else:
        return PREFIX
