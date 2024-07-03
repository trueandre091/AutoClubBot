from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from logs.logger import logger
import json
from asyncio import sleep

from DB import database as db
from classes.states import *
from handler.buttons_handler import set_info_button_handler
from functions import isnum, issetinfo

with open("view\\user\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\user\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)
with open("view\\user\\general_view.json", encoding="utf-8") as file:
    general_view = json.load(file)


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
                                           reply_markup=ReplyKeyboardMarkup([["Отмена"]], resize_keyboard=True))
    return set_info_car_power_state


async def set_info_car_power_handler(update: Update, context: CallbackContext):
    logger.info("Set car power %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    chat = update.message.chat
    if not isnum.isnum(message):
        await chat.send_message(set_info_view["6"])
        return set_info_car_power_state

    db.update_user(update.message.from_user.id, car_power=int(message))

    await chat.send_message(set_info_view["7"])
    return set_info_car_number_state


async def set_info_car_number_handler(update: Update, context: CallbackContext):
    logger.info("Set car number %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    user = update.message.from_user
    chat = update.message.chat
    if len(message) != 3:
        await chat.send_message(set_info_view["7"])
        return set_info_car_number_state

    db.update_user(update.message.from_user.id, car_number=message)

    if not issetinfo.issetinfo(user.id):
        await sleep(1)
        await chat.send_message(start_view["3"])
        return await set_info_button_handler(update, context)

    await chat.send_message(set_info_view["8"])
    await sleep(1)
    await chat.send_message(general_view["2"], reply_markup=general_reply_markup(general_view["buttons"].values()))
    return general_state


async def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("Cancel set info %s: %s", update.message.from_user.username, update.message.text)

    await update.message.reply_text("Операция отменена.")

    user = update.message.from_user
    chat = update.message.chat
    if not issetinfo.issetinfo(user.id):
        await sleep(1)
        await chat.send_message(start_view["3"])
        return await set_info_button_handler(update, context)

    await chat.send_message(general_view["2"], reply_markup=general_reply_markup(general_view["buttons"].values()))
    return general_state
