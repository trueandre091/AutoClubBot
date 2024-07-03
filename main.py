from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ConversationHandler
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from const import TOKEN

from handler.buttons_handler import *
from handler.messages_handler import *
from panels.user.start import *
from classes.states import *

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    general_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            set_info_state: [CallbackQueryHandler(set_info_button_handler)],
            set_info_name_state: [MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), set_info_name_handler)],
            set_info_car_brand_state: [MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), set_info_car_brand_handler)],
            set_info_car_drive_state: [MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), set_info_car_drive_handler)],
            set_info_car_power_state: [MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), set_info_car_power_handler)],
            set_info_car_number_state: [MessageHandler(filters.TEXT & ~filters.Regex("^(Отмена)$"), set_info_car_number_handler)],
            general_state: [CallbackQueryHandler(general_buttons_handler)],
            upcoming_events_state: []
        },
        fallbacks=[MessageHandler(filters.Regex("^(Отмена)$"), cancel)]
    )

    application.add_handler(general_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
