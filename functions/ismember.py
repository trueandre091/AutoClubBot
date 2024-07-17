from DB import database as db


def ismember(event_id, user_id):
    events = db.get_user_events(user_id)
    if event_id in [event[0] for event in events]:
        return True
    return False
