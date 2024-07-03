from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from logs.logger import logger
import json

from DB import database as db
from classes.states import *

with open("view\\user\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)


async def set_info_name_handler(update: Update, context: CallbackContext):
    logger.info("Set name %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    db.update_user(update.message.from_user.id, name=message)

    await update.message.chat.send_message(set_info_view["4"])
    return set_info_car_brand_state


async def set_info_car_brand_handler(update: Update, context: CallbackContext):
    logger.info("Set car brand %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    db.update_user(update.message.from_user.id, car_brand=message)

    reply_keyboard = [list(set_info_view["buttons"].values())]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.chat.send_message(set_info_view["5"], reply_markup=reply_markup)
    return set_info_car_drive_state


async def set_info_car_drive_handler(update: Update, context: CallbackContext):
    logger.info("Set car drive %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    match = dict(zip(set_info_view["buttons"].values(), ["FWD", "RWD", "AWD"]))
    db.update_user(update.message.from_user.id, car_drive=match[message])

    await update.message.chat.send_message(set_info_view["6"],
                                           reply_markup=ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True))
    return set_info_car_power_state


def isnum(string):
    try:
        int(string)
    except ValueError:
        return False
    return True


async def set_info_car_power_handler(update: Update, context: CallbackContext):
    logger.info("Set car power %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if not isnum(message):
        await update.message.chat.send_message(set_info_view["6"])
        return set_info_car_power_state

    db.update_user(update.message.from_user.id, car_power=int(message))

    await update.message.chat.send_message(set_info_view["7"])
    return set_info_car_number_state


async def set_info_car_number_handler(update: Update, context: CallbackContext):
    logger.info("Set car number %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if len(message) != 3:
        await update.message.chat.send_message(set_info_view["7"])
        return set_info_car_number_state

    db.update_user(update.message.from_user.id, car_number=message)

    await update.message.chat.send_message(set_info_view["8"])
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("Cancel set info %s: %s", update.message.from_user.username, update.message.text)

    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END
