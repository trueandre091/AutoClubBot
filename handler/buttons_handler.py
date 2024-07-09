from asyncio import sleep

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from logs.logger import logger
import json

from DB import database as db
from classes.states import *
from classes.upcoming_events_list import UpcomingEventsPanel
from functions import isadmin, ismember, issingleevent
from panels.general import send_general_panel
from panels.set_info import send_set_info_name_panel
from panels.create_event import send_create_event_name_panel
from panels.publish_event import send_publish_event_panel, send_publish_event_confirm_panel
from panels.upcoming_events import send_upcoming_events_panel, edit_upcoming_events_panel, \
    send_delete_event_confirm_panel

with open("view\\start_view.json", encoding="utf-8") as file:
    start_view = json.load(file)
with open("view\\set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)
with open("view\\general_view.json", encoding="utf-8") as file:
    general_view = json.load(file)
with open("view\\publish_event_view.json", encoding="utf-8") as file:
    publish_event_view = json.load(file)
with open("view\\upcoming_events_view.json", encoding="utf-8") as file:
    upcoming_events_view = json.load(file)


async def set_info_button_handler(update: Update, context: CallbackContext):
    await send_set_info_name_panel(update, context)

    return set_info_name_state


async def upcoming_events_button_handler(update: Update, context: CallbackContext):
    user = update.callback_query.from_user
    query = update.callback_query
    chat = update.effective_user
    if query.data == general_view["buttons"]["2"]:
        panel = UpcomingEventsPanel(user.id)
        if not panel.events_list:
            panel.disactivate()
            await chat.send_message(upcoming_events_view["4"])

            return general_state

        await send_upcoming_events_panel(update, context, panel)
        return upcoming_events_state

    else:
        event_id = 0
        for panel in UpcomingEventsPanel.ACTIVE_PANELS:
            if panel.user_id == user.id:
                event_id = panel.get_current_event()[0]

                if query.data == upcoming_events_view["buttons"]["2"]:
                    logger.info("Add / Remove member %s in event %s", user.username, db.get_event_by_id(event_id)[2])

                    db.update_event(event_id, members=user.id)
                    await query.answer()
                    if ismember.ismember(event_id, user.id):
                        await chat.send_message(upcoming_events_view["2"])
                    else:
                        await chat.send_message(upcoming_events_view["3"])

                    return upcoming_events_state

                elif query.data == upcoming_events_view["buttons"]["3"]:
                    pass

                elif query.data == upcoming_events_view["buttons"]["1"]:
                    logger.info("Next event: %s - %s", user.username, db.get_event_by_id(event_id)[2])

                    await edit_upcoming_events_panel(update, context, panel, False)
                    return upcoming_events_state

                elif query.data == upcoming_events_view["buttons"]["4"]:
                    logger.info("Previous event: %s - %s", user.username, db.get_event_by_id(event_id)[2])

                    await edit_upcoming_events_panel(update, context, panel, True)
                    return upcoming_events_state

                elif query.data == upcoming_events_view["buttons"]["5"]:
                    message_id = update.effective_message.id
                    context.user_data["event_id"] = event_id
                    context.user_data["buttons"] = ["Не изменять"]
                    context.user_data["isnew"] = False
                    await update.effective_chat.delete_message(message_id)
                    await send_create_event_name_panel(update, context)

                    return create_event_name_state

                elif query.data == upcoming_events_view["buttons"]["6"]:
                    await send_delete_event_confirm_panel(update, context)
                    return upcoming_events_state

                elif query.data == "Да":
                    logger.info("Delete event: %s - %s", user.username, db.get_event_by_id(event_id)[2])

                    db.delete_event(event_id)

                    await chat.send_message(upcoming_events_view["6"],
                                            reply_markup=ReplyKeyboardRemove())
                    await query.delete_message()
                    return general_state

                elif query.data == "Нет":
                    await query.delete_message()
                    return upcoming_events_state

        if event_id == 0:
            logger.info("Can't find panel: %s", user.username)
            await query.answer()
            return upcoming_events_state


async def create_event_button_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    context.user_data["event_id"] = db.add_event(user.id)
    context.user_data["isnew"] = True

    await send_create_event_name_panel(update, context)
    return create_event_name_state


async def publish_event_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == publish_event_view["buttons"]["1"]:
        await query.answer()
        await send_publish_event_confirm_panel(update, context)

        return publish_event_state

    elif query.data == publish_event_view["buttons"]["2"]:
        message_id = update.effective_message.id
        context.user_data["buttons"] = ["Не изменять"]
        await update.effective_chat.delete_messages([message_id, message_id - 1])
        await send_create_event_name_panel(update, context)

        return create_event_name_state

    elif query.data == "Да":
        logger.info("Publish confirmation: %s", update.effective_user.username)

        message_id = update.effective_message.id
        await update.effective_chat.delete_messages([message_id, message_id - 1])

        users_db = db.get_all_users()
        for user_db in users_db:
            await context.bot.send_message(user_db[0], context.user_data.get("message"), parse_mode="HTML")

        context.user_data.clear()

        chat = update.effective_chat
        await chat.send_message(f"Сообщение отправлено всем пользователям. Количество: {len(users_db)}",
                                reply_markup=ReplyKeyboardRemove())
        await sleep(1)
        await send_general_panel(update, context, isadmin.isadmin(query.from_user.id))
        return general_state

    elif query.data == "Нет":
        await update.effective_message.delete()
        await send_publish_event_panel(update, context)

        return publish_event_state


async def general_buttons_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data in general_view["buttons"].values():
        if query.data == general_view["buttons"]["1"]:
            logger.info("Set info: %s", user.username)
            return await set_info_button_handler(update, context)

        elif query.data == general_view["buttons"]["2"]:
            logger.info("Upcoming events: %s", user.username)
            return await upcoming_events_button_handler(update, context)

        elif query.data == general_view["buttons"]["3"]:
            logger.info("Create event: admin %s", user.username)
            return await create_event_button_handler(update, context)
