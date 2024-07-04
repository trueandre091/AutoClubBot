from const import admin


def isadmin(user_id):
    return True if user_id in admin else False
