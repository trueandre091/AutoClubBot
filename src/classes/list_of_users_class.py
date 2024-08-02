import json

from DB import database as db


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


class ListOfUsersPanel:
    ACTIVE_PANELS = []

    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.page_id = 0
        self.users = sorted(db.get_all_users(), key=lambda x: (x[4], -x[5]))
        self.pages = split(self.users, 15)
        self.ACTIVE_PANELS.append(self)

    def next_page(self):
        self.page_id += 1
        if self.page_id > len(self.pages) - 1:
            self.page_id = 0

        return self.pages[self.page_id]

    def disactivate(self):
        self.ACTIVE_PANELS.remove(self)

    def get_current_page(self):
        return self.pages[self.page_id]