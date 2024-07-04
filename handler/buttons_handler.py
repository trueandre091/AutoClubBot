from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from logs.logger import logger
import json

from DB import database as db
from classes.states import *
from panels.set_info import send_set_info_name_panel

with open("view\\user\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\user\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)
with open("view\\user\\general_view.json", encoding="utf-8") as file:
    general_view = json.load(file)


async def set_info_button_handler(update: Update, context: CallbackContext):
    await send_set_info_name_panel(update, context)

    return set_info_name_state


async def general_buttons_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data in general_view["buttons"].values():
        if query.data == general_view["buttons"]["1"]:
            return await set_info_button_handler(update, context)

        elif query.data == general_view["buttons"]["2"]:
            logger.info("Upcoming events: %s", user.username)


