from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from logs.logger import logger
import json
from datetime import datetime

from DB import database as db
from classes.states import *

with open("view\\user\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\user\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)


async def set_info_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = query.message.chat
    await query.answer()
    await chat.send_message(set_info_view["2"])
    await chat.send_message(set_info_view["3"],
                            reply_markup=ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True))

    return set_info_name_state


async def general_buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    db.update_user(query.from_user.id, last_timestamp=datetime.now())
