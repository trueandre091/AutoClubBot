from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from logs.logger import logger
import json

from DB import database as db

with open("view\\user\\general_view.json", encoding="utf-8") as file:
    general_view = json.load(file)


def general_reply_markup():
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in general_view["buttons"].values()]
    return InlineKeyboardMarkup.from_row(buttons)


async def send_general_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("General: %s", update.message.from_user.username)

    user = update.message.from_user
    user_db = db.get_user_by_id(user.id)
    message = f"{general_view["2"]}\n{general_view["3"]}"
    message = f"{message}\n\n{general_view["4"] + " " + str(user_db[6])}"
    message = f"{message}\n{general_view["5"] + " " + str(user_db[4])}"
    message = f"{message}\n{general_view["6"] + " " + str(user_db[3])}"
    message = f"{message}\n{general_view["7"] + " " + str(user_db[5])}"
    message = f"{message}\n\n{general_view["8"]}"

    await update.message.chat.send_message(message, parse_mode='HTML',
                                           reply_markup=general_reply_markup())
