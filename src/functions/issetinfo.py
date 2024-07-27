from DB import database as db


def issetinfo(user_id):
    user_db = db.get_user_by_id(user_id)
    if user_db[2] and user_db[3] and user_db[4] and user_db[5] and user_db[6]:
        return True
    return False
