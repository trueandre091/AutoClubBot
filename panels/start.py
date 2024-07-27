from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from logs.logger import logger
import json

from DB import database as db
from classes.states import *
from functions import isadmin, issetinfo, isnum
from handler.buttons_handler import set_info_button_handler
from panels.general import send_general_panel

with open("view\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("</start> command: %s %s", update.message.from_user.id, update.message.from_user.username)

    user = update.message.from_user
    chat = update.message.chat

    if db.get_user_by_id(user.id) == 1:
        print("Необходимо создать базу данных. Введите команды ниже\nНажмите Ctrl + C\nВведите python DB\\database.py")

        return ConversationHandler.END

    if not db.get_user_by_id(user.id):
        logger.info("New user: %s %s", update.message.from_user.id, update.message.from_user.username)
        db.add_user(user.id, user.username if user.username else " ")

        buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in
                   [list(start_view["buttons"].values())[0]]]
        reply_markup = InlineKeyboardMarkup.from_row(buttons)

        await chat.send_message(start_view["2"], reply_markup=reply_markup)
        return set_info_state

    if not issetinfo.issetinfo(user.id):
        await chat.send_message(set_info_view["10"], reply_markup=ReplyKeyboardRemove())

        return await set_info_button_handler(update, context)

    await send_general_panel(update, context, isadmin.isadmin(user.id))
    return general_state


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("</delete_user> command: %s %s - %s", update.message.from_user.id, update.message.from_user.username,
                update.message.text.split()[-1])

    chat = update.message.chat
    delete_user_id = update.message.text.split()[-1]
    if not isnum.isnum(delete_user_id):
        await chat.send_message("Нужно ввести id пользователя!")
    if not db.delete_user(delete_user_id):
        await chat.send_message("Пользователь не найден")

    return
