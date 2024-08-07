from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_general import LEXICON


def create_settings_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='💾 Сохранение истории сообщений', callback_data='keep_history_setting')],
                         [InlineKeyboardButton(text='⤴️ Указание пересылки', callback_data='forward_setting')],
                         [InlineKeyboardButton(text='✉️ Написать автору', callback_data='to_author')],
                         [InlineKeyboardButton(text=f'{LEXICON['menu']} Меню', callback_data='menu')]]
    )

    return keyboard


def create_forward_setting_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='✅ Включить', callback_data='forward_on')],
                         [InlineKeyboardButton(text='❌ Отключить', callback_data='forward_off')],
                         [InlineKeyboardButton(text='⬅️ Назад', callback_data='settings')]]
    )

    return keyboard


def create_history_setting_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='✅ Включить', callback_data='keep_history_on')],
                         [InlineKeyboardButton(text='❌ Отключить', callback_data='keep_history_off')],
                         [InlineKeyboardButton(text='⬅️ Назад', callback_data='settings')]]
    )

    return keyboard
