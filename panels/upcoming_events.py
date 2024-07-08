from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext

import json

from classes.upcoming_events_list import UpcomingEventsPanel
from functions import isadmin

with open("view\\publish_event_view.json", encoding="utf-8") as file:
    publish_event_view = json.load(file)
with open("view\\upcoming_events_view.json", encoding="utf-8") as file:
    upcoming_events_view = json.load(file)


def create_upcoming_events_message(event):
    message = f"<b>{event[2]}</b>"
    message = f"{message}\n{event[5]}" if event[5] else message
    message = f"{message}\n\n{publish_event_view["4"] + ' ' + event[3]}"
    message = f"{message}\n{publish_event_view["5"] + ' ' + event[4]}"
    return message


async def send_upcoming_events_panel(update: Update, context: CallbackContext, panel: UpcomingEventsPanel, direction: bool):
    user = update.effective_user
    chat = update.effective_chat
    event = panel.get_event(direction)
    message = create_upcoming_events_message(event)
    photo = event[6]
    if isadmin.isadmin(user.id):
        buttons = list(upcoming_events_view["buttons"].values())
    else:
        buttons = list(upcoming_events_view["buttons"].values())[:3]

    reply_keyboard = [[]]
    for i in range(len(buttons)):
        if i == 3:
            reply_keyboard.append([])
        reply_keyboard[-1].append(InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]))

    print(reply_keyboard)
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    if event[6]:
        await chat.send_photo(InputMediaPhoto(event[6]), caption=message, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await chat.send_message(message, parse_mode="HTML", reply_markup=reply_markup)









