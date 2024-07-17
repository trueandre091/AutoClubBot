from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext

import json

from DB import database as db

with open("view\\publish_event_view.json", encoding="utf-8") as file:
    publish_event_view = json.load(file)
with open("view\\create_event_view.json", encoding="utf-8") as file:
    create_event_view = json.load(file)


def create_publish_message(event_id):
    event_db = db.get_event_by_id(event_id)
    message = f"{publish_event_view["2"]}\n{publish_event_view["3"]}"
    message = f"{message}\n\n<b>{event_db[2]}</b>"
    message = f"{message}\n{event_db[5]}" if event_db[5] else message
    message = f"{message}\n{publish_event_view["4"] + ' ' + event_db[3]}"
    message = f"{message}\n{publish_event_view["5"] + ' ' + event_db[4]}"
    return message


async def send_publish_event_panel(update: Update, context: CallbackContext, isnew: bool = True):
    chat = update.effective_chat
    message = create_publish_message(context.user_data.get("event_id"))
    context.user_data["message"] = message

    buttons = list(publish_event_view["buttons"].values())
    if not context.user_data.get("buttons"):
        buttons = [buttons[:-1]]
    reply_keyboard = [InlineKeyboardButton(text=name, callback_data=name) for name in buttons]
    reply_markup = InlineKeyboardMarkup.from_column(reply_keyboard)

    await chat.send_message(
        publish_event_view["6"],
        reply_markup=ReplyKeyboardMarkup(keyboard=[[create_event_view["buttons"]["2"]]],
                                         resize_keyboard=True) if context.user_data.get("isnew") else ReplyKeyboardRemove())
    await chat.send_message(message, parse_mode="HTML", reply_markup=reply_markup)


async def send_publish_event_confirm_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in ["Да", "Нет"]]
    reply_markup = InlineKeyboardMarkup.from_row(buttons)

    await chat.send_message(publish_event_view["7"],
                            reply_markup=reply_markup)
