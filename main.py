from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ConversationHandler
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from const import TOKEN

from handler.buttons_handler import *
from handler.cancel_handler import cancel
from handler.set_info_handler import SET_INFO_HANDLERS_FILTERS
from panels.start import *
from classes.states import *

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    general_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            set_info_state: [CallbackQueryHandler(set_info_button_handler)],
            set_info_name_state: SET_INFO_HANDLERS_FILTERS[0],
            set_info_car_brand_state: SET_INFO_HANDLERS_FILTERS[1],
            set_info_car_drive_state: SET_INFO_HANDLERS_FILTERS[2],
            set_info_car_power_state: SET_INFO_HANDLERS_FILTERS[3],
            set_info_car_number_state: SET_INFO_HANDLERS_FILTERS[4],
            general_state: [CallbackQueryHandler(general_buttons_handler)],
            upcoming_events_state: [],
            create_event_state: [CallbackQueryHandler(create_event_button_handler)],
            create_event_name_state: []
        },
        fallbacks=[MessageHandler(filters.Regex("^(Отмена)$"), cancel)]
    )

    application.add_handler(general_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
