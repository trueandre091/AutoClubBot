from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from logs.logger import logger
import json

from DB import database as db
from classes.states import *

with open("view\\user\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\user\\general_view.json", encoding="utf-8") as file:
    general_view = json.load(file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("</start> command: %s", update.message.from_user.username)

    user = update.message.from_user
    db.add_event(user.id, start_view["1"])

    if not db.get_user_by_id(user.id):
        logger.info("New user: %s", update.message.from_user.username)
        db.add_user(user.id, user.username)

        buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in start_view["buttons"].values()]
        reply_markup = InlineKeyboardMarkup.from_row(buttons)

        await update.message.reply_text(start_view["2"], reply_markup=reply_markup)
        return set_info_name_state

    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in general_view["buttons"].values()]
    reply_markup = InlineKeyboardMarkup.from_row(buttons)
    await update.message.reply_text(general_view["2"], reply_markup=reply_markup)
    return general_state
