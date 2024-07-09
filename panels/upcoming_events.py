from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext

import json

from classes.upcoming_events_list import UpcomingEventsPanel
from functions import isadmin, issingleevent

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


def create_upcoming_events_reply_markup(user_id, panel):
    if isadmin.isadmin(user_id):
        buttons = list(upcoming_events_view["buttons"].values())
    else:
        buttons = list(upcoming_events_view["buttons"].values())[:3]

    reply_keyboard = [[]]
    for i in range(len(buttons)):
        if i == 3:
            reply_keyboard.append([])
        reply_keyboard[-1].append(InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]))

    if issingleevent.issingleevent(panel):
        reply_keyboard[0].pop(0)
        reply_keyboard[0].pop(1)

    return InlineKeyboardMarkup(reply_keyboard)


async def send_upcoming_events_panel(update: Update, context: CallbackContext, panel: UpcomingEventsPanel):
    user = update.effective_user
    chat = update.effective_chat
    event = panel.next_event(True)
    message = create_upcoming_events_message(event)
    photo = event[6]

    if photo:
        await chat.send_photo(InputMediaPhoto(event[6]), caption=message, parse_mode="HTML",
                              reply_markup=create_upcoming_events_reply_markup(user.id, panel))
    else:
        await chat.send_message(message, parse_mode="HTML",
                                reply_markup=create_upcoming_events_reply_markup(user.id, panel))


async def edit_upcoming_events_panel(update: Update, context: CallbackContext, panel: UpcomingEventsPanel,
                                     direction: bool):
    user = update.effective_user
    query = update.callback_query
    event = panel.next_event(direction)
    message = create_upcoming_events_message(event)
    photo = event[6]

    if photo:
        await query.edit_message_media(InputMediaPhoto(event[6]),
                                       reply_markup=create_upcoming_events_reply_markup(user.id, panel))
        await query.edit_message_caption(caption=message, parse_mode="HTML")
    else:
        await query.edit_message_text(message, parse_mode="HTML",
                                      reply_markup=create_upcoming_events_reply_markup(user.id, panel))


async def send_delete_event_confirm_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in ["Да", "Нет"]]
    reply_markup = InlineKeyboardMarkup.from_row(buttons)

    await chat.send_message(upcoming_events_view["5"],
                            reply_markup=reply_markup)
