from datetime import datetime


async def log(user_id: int, event_type, event):
    data = {
        "measurement": "bot_commands",
        "time": datetime.utcnow(),
        "fields": {"event": 1},
        "tags": {
            "user": str(user_id),
            "event": event_type + ': ' + event,
        },
    }
    print(data)
