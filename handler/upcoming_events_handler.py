from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

import json

from functions import isadmin
from classes.states import *
from panels.general import send_general_panel

with open("view\\upcoming_events_view.json", encoding="utf-8") as file:
    upcoming_events_view = json.load(file)
with open("view\\upcoming_event_members_view.json", encoding="utf-8") as file:
    upcoming_event_members_view = json.load(file)


async def cancel_upcoming_events(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()

    await update.message.reply_text(upcoming_events_view["7"],
                                    reply_markup=ReplyKeyboardRemove())

    await send_general_panel(update, context, isadmin.isadmin(update.message.from_user.id))
    return general_state
