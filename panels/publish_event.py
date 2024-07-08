from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
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

    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in publish_event_view["buttons"].values()]
    reply_markup = InlineKeyboardMarkup.from_column(buttons)

    await chat.send_message(publish_event_view["6"], reply_markup=ReplyKeyboardMarkup([[create_event_view["buttons"]["2"]]], resize_keyboard=True))
    await chat.send_message(message, parse_mode="HTML", reply_markup=reply_markup)


async def send_publish_event_confirm_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in ["Да", "Нет"]]
    reply_markup = InlineKeyboardMarkup.from_row(buttons)

    await chat.send_message("Вы уверены?\nСообщение будет отправлено всем пользователям, зарегистрированным в боте",
                            reply_markup=reply_markup)

