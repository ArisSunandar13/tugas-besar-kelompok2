import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
db_log_history = os.getenv('DB_LOG_HISTORY')


def get(db):
    try:
        with open(db, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return ['error']


def post(db, data):
    with open(db, 'w') as file:
        json.dump(data, file, indent=4)

    return get(db).pop()


def get_last_log_history():
    return get(db_log_history).pop()


def post_log_history(user, action):
    data_log_history = get(db_log_history)

    data_log_history.append({
        'username': user['username'],
        'role': user['role'],
        'action': action,
        'date': datetime.now().strftime("%d-%m-%Y"),
        'time': datetime.now().strftime("%H:%M:%S")
    })

    post(db_log_history, data_log_history)
