from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_general import LEXICON


def create_settings_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🌏 Язык', callback_data='language')],
                         [InlineKeyboardButton(text='✉️ Написать автору', callback_data='to_author')],
                         [InlineKeyboardButton(text=f'{LEXICON['menu']} Меню', callback_data='menu')]]
    )

    return keyboard


def create_language_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🇷🇺 RU', callback_data='lan_RU')],
                         [InlineKeyboardButton(text='🇺🇸 EN', callback_data='lan_EN')],
                         [InlineKeyboardButton(text='⬅️ Назад', callback_data='settings')]]
    )

    return keyboard
