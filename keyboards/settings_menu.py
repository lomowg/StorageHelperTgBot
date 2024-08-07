from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_general import LEXICON


def create_settings_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='✉️ Написать автору', callback_data='to_author')],
                         [InlineKeyboardButton(text=f'{LEXICON['menu']} Меню', callback_data='menu')]]
    )

    return keyboard

