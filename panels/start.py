from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from logs.logger import logger
import json

from DB import database as db
from classes.states import *
from functions import isadmin, issetinfo
from handler.buttons_handler import set_info_button_handler
from panels.general import send_general_panel

with open("view\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("</start> command: %s", update.message.from_user.username)

    user = update.message.from_user
    chat = update.message.chat
    db.add_log(user.id, start_view["1"])

    if not db.get_user_by_id(user.id):
        logger.info("New user: %s", update.message.from_user.username)
        db.add_user(user.id, user.username)

        buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in start_view["buttons"].values()]
        reply_markup = InlineKeyboardMarkup.from_row(buttons)

        await chat.send_message(start_view["2"], reply_markup=reply_markup)
        return set_info_state

    if not issetinfo.issetinfo(user.id):
        await chat.send_message(set_info_view["10"], reply_markup=ReplyKeyboardRemove())

        return await set_info_button_handler(update, context)

    await send_general_panel(update, context, isadmin.isadmin(user.id))
    return general_state
