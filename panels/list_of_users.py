from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

import json

from classes.list_of_users_class import ListOfUsersPanel

with open("view\\list_of_users_view.json", encoding="utf-8") as file:
    list_of_users_view = json.load(file)


def create_list_of_users_message(panel):
    page = panel.next_page()
    page_id = panel.page_id
    message = f"{list_of_users_view["2"]}\n"

    place = int(str(page_id) + "1")
    for user in page:
        message = f"{message}\n<code><b>{place}</b> - {user[6]} {user[4]} {user[3]} {user[5]} ЛС</code>"
        place += 1
    return message


def create_list_of_users_reply_markup(panel: ListOfUsersPanel):
    if len(panel.pages) == 1:
        return ReplyKeyboardMarkup([[list_of_users_view["buttons"]["2"]]], resize_keyboard=True, one_time_keyboard=True)
    return InlineKeyboardMarkup.from_column(
        InlineKeyboardButton(text=name, callback_data=name) for name in [list_of_users_view["buttons"]["1"]])


async def send_list_of_users_panel(update: Update, context: CallbackContext, panel: ListOfUsersPanel):
    chat = update.effective_chat
    message = create_list_of_users_message(panel)

    await chat.send_message(message, parse_mode="HTML", reply_markup=create_list_of_users_reply_markup(panel))


async def edit_list_of_users_panel(update: Update, context: CallbackContext, panel: ListOfUsersPanel):
    chat = update.effective_chat
    query = update.callback_query
    message = create_list_of_users_message(panel)

    await query.edit_message_text(message, parse_mode="HTML",
                                  reply_markup=create_list_of_users_reply_markup(panel))
