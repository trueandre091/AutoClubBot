from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

import json

from DB import database as db
from classes.upcoming_events_panel import UpcomingEventsPanel
from functions import isadmin, issingleevent

with open("view\\publish_event_view.json", encoding="utf-8") as file:
    publish_event_view = json.load(file)
with open("view\\upcoming_events_view.json", encoding="utf-8") as file:
    upcoming_events_view = json.load(file)
with open("view\\upcoming_event_members_view.json", encoding="utf-8") as file:
    upcoming_event_members_view = json.load(file)


def create_upcoming_events_message(event):
    message = f"<b>{event[2]}</b>"
    message = f"{message}\n{event[5]}" if event[5] else message
    message = f"{message}\n\n{publish_event_view["4"] + ' ' + event[3]}"
    message = f"{message}\n{publish_event_view["5"] + ' ' + event[4]}"
    return message


def create_upcoming_events_reply_markup(user_id, panel):
    if isadmin.isadmin(user_id):
        buttons = list(upcoming_events_view["buttons"].values())[:-1]
    else:
        buttons = list(upcoming_events_view["buttons"].values())[:3]

    reply_keyboard = [[]]
    for i in range(len(buttons)):
        if i == 3:
            reply_keyboard.append([])
        reply_keyboard[-1].append(InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]))

    return InlineKeyboardMarkup(reply_keyboard)


async def send_upcoming_events_panel(update: Update, context: CallbackContext, panel: UpcomingEventsPanel):
    user = update.effective_user
    chat = update.effective_chat
    event = panel.next_event()
    message = create_upcoming_events_message(event)

    await chat.send_message(message, parse_mode="HTML",
                            reply_markup=create_upcoming_events_reply_markup(user.id, panel))


async def edit_upcoming_events_panel(update: Update, context: CallbackContext, panel: UpcomingEventsPanel,
                                     direction: bool):
    user = update.effective_user
    query = update.callback_query
    event = panel.next_event()
    message = create_upcoming_events_message(event)

    if issingleevent.issingleevent(panel):
        return

    await query.edit_message_text(message, parse_mode="HTML",
                                  reply_markup=create_upcoming_events_reply_markup(user.id, panel))


async def send_delete_event_confirm_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in ["Да", "Нет"]]
    reply_markup = InlineKeyboardMarkup.from_row(buttons)

    await chat.send_message(upcoming_events_view["5"],
                            reply_markup=reply_markup)


def create_upcoming_event_members_message(update: Update, context: CallbackContext, event_id):
    users = db.get_event_users(event_id)
    message = f"{upcoming_event_members_view['2']} <b><i>{db.get_event_by_id(event_id)[2]}</i></b>:\n"
    place = 1
    for user in users:
        message = f"{message}\n<code><b>{place}</b> - {user[6]} {user[4]} {user[3]} {user[5]} ЛС</code>"
        place += 1
    return message if len(users) > 0 else upcoming_event_members_view["4"]


async def send_upcoming_event_members_panel(update: Update, context: CallbackContext, event_id):
    chat = update.effective_chat
    message = create_upcoming_event_members_message(update, context, event_id)

    await chat.send_message(message, parse_mode="HTML",
                            reply_markup=ReplyKeyboardMarkup([[upcoming_events_view["buttons"]["6"]]],
                                                             resize_keyboard=True))
