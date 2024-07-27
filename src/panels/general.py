from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from logs.logger import logger
import json

from DB import database as db

with open("/src/view/general_view.json", encoding="utf-8") as file:
    general_view = json.load(file)


def create_general_message(user_id):
    user_db = db.get_user_by_id(user_id)
    message = f"{general_view['2'] + ', ' + user_db[2] + '!'}\n{general_view['3']}"
    message = f"{message}\n\n{general_view['4'] + ' ' + str(user_db[6])}"
    message = f"{message}\n{general_view['5'] + ' ' + str(user_db[4])}"
    message = f"{message}\n{general_view['6'] + ' ' + str(user_db[3])}"
    message = f"{message}\n{general_view['7'] + ' ' + str(user_db[5])}"
    message = f"{message}\n\n{general_view['8']}"
    return message


def general_reply_markup(isadmin: bool):
    names = general_view["buttons"].values() if isadmin else list(general_view["buttons"].values())[:-1]
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in names]
    return InlineKeyboardMarkup.from_column(buttons)


async def send_general_panel(update: Update, context: ContextTypes.DEFAULT_TYPE, isadmin: bool = False):
    logger.info("General: %s %s", update.effective_user.id, update.effective_user.username)

    user = update.effective_user
    chat = update.effective_chat
    message = create_general_message(user.id)

    await chat.send_message(message, parse_mode='HTML',
                            reply_markup=general_reply_markup(isadmin))
