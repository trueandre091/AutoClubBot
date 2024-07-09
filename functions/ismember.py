from DB import database as db


def ismember(event_id, user_id):
    event_db = db.get_event_by_id(event_id)
    if str(user_id) in event_db[7].split():
        return True
    return False