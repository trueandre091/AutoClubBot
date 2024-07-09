from classes.upcoming_events_list import UpcomingEventsPanel


def issingleevent(panel: UpcomingEventsPanel):
    if len(panel.events_list) == 1:
        return True
    return False
