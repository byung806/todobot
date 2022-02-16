import json
import random

from data.config import DEFAULT_COLOR


def get_embed_color(user_id, hex_code=None):
    data = json.load(open('data\\colors.json', 'r'))
    if str(user_id) in data:
        color = data[str(user_id)]
        if color == 'random':
            if hex_code:
                return '#RANDOM'
            color = random.randint(0, 0xFFFFFF)
        if hex_code:
            return '#' + hex(color)[2:].upper()
        else:
            return color
    else:
        if hex_code:
            return '#' + hex(DEFAULT_COLOR).upper()[2:]
        else:
            return DEFAULT_COLOR
