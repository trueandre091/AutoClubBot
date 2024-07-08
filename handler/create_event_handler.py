from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, filters

from logs.logger import logger
import json

from DB import database as db
from classes.states import *
from panels.general import send_general_panel
from panels.create_event import send_create_event_date_panel, send_create_event_place_panel, \
    send_create_event_info_panel
from panels.publish_event import send_publish_event_panel

with open("view\\create_event_view.json", encoding="utf-8") as file:
    create_event_view = json.load(file)


async def create_event_name_handler(update: Update, context: CallbackContext):
    logger.info("Create event name %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if not message == "Не изменять":
        db.update_event(context.user_data.get("event_id"), name=message)

    await send_create_event_date_panel(update, context)
    return create_event_date_state


async def create_event_date_handler(update: Update, context: CallbackContext):
    logger.info("Create event date %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if not message == "Не изменять":
        chat = update.effective_chat
        try:
            db.update_event(context.user_data.get("event_id"), date=message)
        except ValueError:
            await chat.send_message(create_event_view["8"])
            return create_event_date_state

    await send_create_event_place_panel(update, context)
    return create_event_place_state


async def create_event_place_handler(update: Update, context: CallbackContext):
    logger.info("Create event place %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if not message == "Не изменять":
        db.update_event(context.user_data.get("event_id"), place=message)

    await send_create_event_info_panel(update, context)
    return create_event_info_state


async def create_event_info_handler(update: Update, context: CallbackContext):
    logger.info("Create event info %s: %s", update.message.from_user.username, update.message.text)

    message = update.message.text
    if not message == "Не изменять":
        db.update_event(context.user_data.get("event_id"), info=message)

    await send_publish_event_panel(update, context)
    return publish_event_state


async def skip_create_event_info_handler(update: Update, context: CallbackContext):
    logger.info("Skip create event info %s: %s", update.message.from_user.username, update.message.text)

    await send_publish_event_panel(update, context)
    return publish_event_state


async def cancel_create_event(update: Update, context: CallbackContext) -> int:
    logger.info("Cancel create event %s: %s", update.message.from_user.username, update.message.text)

    db.delete_event(context.user_data.get("event_id"))
    context.user_data.clear()

    await update.message.reply_text(create_event_view["7"],
                                    reply_markup=ReplyKeyboardRemove())

    await send_general_panel(update, context, isadmin=True)
    return general_state


CREATE_EVENT_HANDLERS = [
    create_event_name_handler,
    create_event_date_handler,
    create_event_place_handler,
    create_event_info_handler
]
CREATE_EVENT_HANDLERS_FILTERS = [
    [
        MessageHandler(filters.Regex("^(Отмена)$"), cancel_create_event),
        MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), handler),
    ] for handler in CREATE_EVENT_HANDLERS[:3]
]
CREATE_EVENT_HANDLERS_FILTERS.append(
    [
        MessageHandler(filters.Regex("^(Отмена)$"), cancel_create_event),
        MessageHandler(filters.Regex("^(Пропустить)$"), skip_create_event_info_handler),
        MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$") & ~filters.Regex("^(Пропустить)$"),
                       CREATE_EVENT_HANDLERS[3]),
    ]
)
CREATE_EVENT_HANDLERS_FILTERS.append([MessageHandler(filters.Regex("^(Отмена)$"), cancel_create_event)])
