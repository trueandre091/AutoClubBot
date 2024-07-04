from telegram import Update
from telegram.ext import CallbackContext

from logs.logger import logger
import json
from asyncio import sleep

from DB import database as db
from classes.states import *
from handler.buttons_handler import set_info_button_handler
from functions import isnum, issetinfo
from panels.general import send_general_panel
from panels.create_event import send_create_event_name_panel, send_create_event_date_panel, \
    send_create_event_place_panel, send_create_event_info_panel

with open("view\\create_event_view.json", encoding="utf-8") as file:
    create_event_view = json.load(file)


async def create_event_name_handler(update: Update, context: CallbackContext):
    logger.info("Create event name %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    db.update_user(update.message.from_user.id, name=message)

    await send_create_event_name_panel(update, context)
    return create_event_date_state


async def create_event_date_handler(update: Update, context: CallbackContext):
    logger.info("Create event date %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    db.update_user(update.message.from_user.id, name=message)

    await send_create_event_name_panel(update, context)
    return create_event_date_state
