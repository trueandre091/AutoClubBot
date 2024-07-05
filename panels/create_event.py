from asyncio import sleep

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import json

with open("view\\create_event_view.json", encoding="utf-8") as file:
    create_event_view = json.load(file)


async def send_create_event_name_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat

    await chat.send_message(create_event_view["2"])
    await chat.send_message(create_event_view["3"],
                            reply_markup=ReplyKeyboardMarkup([[create_event_view["buttons"]["2"]]], resize_keyboard=True))


async def send_create_event_date_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat

    await chat.send_message(create_event_view["4"])


async def send_create_event_place_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat

    await chat.send_message(create_event_view["5"])


async def send_create_event_info_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    reply_keyboard = [list(create_event_view["buttons"].values())[:2]]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await chat.send_message(create_event_view["6"], reply_markup=reply_markup)


async def send_publish_event_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [InlineKeyboardButton(text=name, callback_data=name) for name in create_event_view["buttons"]["3"]]
    reply_markup = InlineKeyboardMarkup.from_column(buttons)

    await chat.send_message(create_event_view["7"], reply_markup=ReplyKeyboardRemove())
