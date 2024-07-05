from const import ADMIN


def isadmin(user_id):
    return True if user_id in ADMIN else False
