import json


async def get_user_tasks(user_id) -> dict:
    """
    :param user_id: Discord ID of user
    :return: Dictionary of user tasks  {"task": [boolean completed, int priority]}
    """
    data = json.load(open('data\\tasks.json', 'r'))
    if str(user_id) in data:
        return data[str(user_id)]
    else:
        return {}
