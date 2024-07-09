import datetime
import json

from DB import database as db

with open("view\\upcoming_events_view.json", encoding="utf-8") as file:
    upcoming_events_view = json.load(file)


class EventsList:
    def __init__(self):
        self.events = db.get_all_events_after(datetime.datetime.today().date())

    def refresh(self):
        self.events = db.get_all_events_after(datetime.datetime.today().date())


class UpcomingEventsPanel:
    ACTIVE_PANELS = []

    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.index = -1
        self.events_list = db.get_all_events_after(datetime.datetime.today().date())
        self.ACTIVE_PANELS.append(self)

    def next_event(self, direction: bool):
        if direction:
            self.index += 1
            if self.index > len(self.events_list) - 1:
                self.index = 0
        else:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.events_list) - 1

        return self.events_list[self.index]

    def disactivate(self):
        self.ACTIVE_PANELS.remove(self)

    def get_current_event(self):
        return self.events_list[self.index]


