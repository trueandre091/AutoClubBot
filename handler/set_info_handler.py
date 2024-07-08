from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, filters

from logs.logger import logger
import json
from asyncio import sleep

from DB import database as db
from classes.states import *
from handler.buttons_handler import set_info_button_handler
from functions import isnum, issetinfo, isadmin
from panels.general import send_general_panel
from panels.set_info import send_set_info_car_brand_panel, send_set_info_car_drive_panel, \
    send_set_info_car_power_panel, send_set_info_car_number_panel

with open("view\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)


async def set_info_name_handler(update: Update, context: CallbackContext):
    logger.info("Set name %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    db.update_user(update.message.from_user.id, name=message)

    await send_set_info_car_brand_panel(update, context)
    return set_info_car_brand_state


async def set_info_car_brand_handler(update: Update, context: CallbackContext):
    logger.info("Set car brand %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    db.update_user(update.message.from_user.id, car_brand=message)

    await send_set_info_car_drive_panel(update, context)
    return set_info_car_drive_state


async def set_info_car_drive_handler(update: Update, context: CallbackContext):
    logger.info("Set car drive %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    match = dict(zip(set_info_view["buttons"].values(), ["FWD", "RWD", "AWD"]))
    db.update_user(update.message.from_user.id, car_drive=match[message])

    await send_set_info_car_power_panel(update, context)
    return set_info_car_power_state


async def set_info_car_power_handler(update: Update, context: CallbackContext):
    logger.info("Set car power %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if not isnum.isnum(message):
        await send_set_info_car_power_panel(update, context)
        return set_info_car_power_state

    db.update_user(update.message.from_user.id, car_power=int(message))

    await send_set_info_car_number_panel(update, context)
    return set_info_car_number_state


async def set_info_car_number_handler(update: Update, context: CallbackContext):
    logger.info("Set car number %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    user = update.message.from_user
    chat = update.message.chat
    if len(message) != 3:
        await send_set_info_car_number_panel(update, context)
        return set_info_car_number_state

    db.update_user(update.message.from_user.id, car_number=message)

    if not issetinfo.issetinfo(user.id):
        await sleep(1)
        await chat.send_message(set_info_view["10"])
        return await set_info_button_handler(update, context)

    await chat.send_message(set_info_view["8"])
    await sleep(1)
    await send_general_panel(update, context, isadmin.isadmin(user.id))
    return general_state


async def cancel_set_info(update: Update, context: CallbackContext) -> int:
    logger.info("Cancel set info %s: %s", update.message.from_user.username, update.message.text)

    await update.message.reply_text(set_info_view["9"], reply_markup=ReplyKeyboardRemove())

    user = update.message.from_user
    chat = update.message.chat
    if not issetinfo.issetinfo(user.id):
        await sleep(1)
        await chat.send_message(set_info_view["10"], reply_markup=ReplyKeyboardRemove())
        return await set_info_button_handler(update, context)

    await send_general_panel(update, context, isadmin.isadmin(user.id))
    return general_state


SET_INFO_HANDLERS = [
    set_info_name_handler,
    set_info_car_brand_handler,
    set_info_car_drive_handler,
    set_info_car_power_handler,
    set_info_car_number_handler,
]
SET_INFO_HANDLERS_FILTERS = [
    [
        MessageHandler(filters.Regex("^(Отмена)$"), cancel_set_info),
        MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), handler),
    ] for handler in SET_INFO_HANDLERS
]
