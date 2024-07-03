from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🗃️ Хранилище', callback_data='storage')],
                         [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings')],
                         [InlineKeyboardButton(text='⁉️ Помощь', callback_data='help')]]
    )

    return keyboard


