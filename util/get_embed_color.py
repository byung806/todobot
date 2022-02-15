import json


def get_embed_color(user_id, hex_code=None):
    data = json.load(open('data\\colors.json', 'r'))
    if str(user_id) in data:
        if not hex_code:
            sixteenIntegerHex = int(data[str(user_id)].replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)
            return readableHex
        else:
            return data[str(user_id)]
    else:
        if not hex_code:
            return 0  # black color
        else:
            return '#000000'
