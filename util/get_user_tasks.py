import json

def get_user_tasks(user_id):
    data = json.load(open('data\\tasks.json', 'r'))
    if str(user_id) in data:
        return data[str(user_id)]
    else:
        return []