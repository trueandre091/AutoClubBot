from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from logs.logger import logger
import json
from asyncio import sleep

from classes.states import *
from handler.buttons_handler import set_info_button_handler
from functions import issetinfo
from panels.general import send_general_panel

with open("view\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)


async def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("Cancel set info %s: %s", update.message.from_user.username, update.message.text)

    await update.message.reply_text("Операция отменена.", reply_markup=ReplyKeyboardRemove())

    user = update.message.from_user
    chat = update.message.chat
    if not issetinfo.issetinfo(user.id):
        await sleep(1)
        await chat.send_message(start_view["3"], reply_markup=ReplyKeyboardRemove())
        return await set_info_button_handler(update, context)

    await send_general_panel(update, context)
    return general_state
