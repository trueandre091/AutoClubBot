from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from logs.logger import logger
import json

with open("/src/view/set_info_view.json", encoding="utf-8") as file:
    set_info_view = json.load(file)


async def send_set_info_name_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [[set_info_view["buttons"]["4"]]]
    extra_buttons = context.user_data.get("buttons")
    if extra_buttons:
        buttons = [extra_buttons]

    await chat.send_message(set_info_view["2"])
    await chat.send_message(set_info_view["3"],
                            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


async def send_set_info_car_brand_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [[set_info_view["buttons"]["4"]]]
    extra_buttons = context.user_data.get("buttons")
    if extra_buttons:
        buttons = [extra_buttons]

    await chat.send_message(set_info_view["4"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


async def send_set_info_car_drive_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    reply_keyboard = [list(set_info_view["buttons"].values())[:3], [list(set_info_view["buttons"].values())[3]]]
    extra_buttons = context.user_data.get("buttons")
    if extra_buttons:
        reply_keyboard = [list(set_info_view["buttons"].values())[:3], extra_buttons]

    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await chat.send_message(set_info_view["5"], reply_markup=reply_markup)


async def send_set_info_car_power_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [[set_info_view["buttons"]["4"]]]
    extra_buttons = context.user_data.get("buttons")
    if extra_buttons:
        buttons = [extra_buttons]

    await chat.send_message(set_info_view["6"],
                            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


async def send_set_info_car_number_panel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    buttons = [[]]
    extra_buttons = context.user_data.get("buttons")
    if extra_buttons:
        buttons = [extra_buttons]
    await chat.send_message(set_info_view["7"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))

