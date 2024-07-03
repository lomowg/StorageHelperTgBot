from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_general import LEXICON


def create_dirs_menu(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='📍 Избранное', callback_data='favourites'))

    # for button in sorted(args): Реализовать добавление папок

    kb_builder.row(
        InlineKeyboardButton(
            text='➕ Создать папку',
            callback_data='create_dir'
        ),
        InlineKeyboardButton(
            text=f'{LEXICON['del']} Удалить папку',
            callback_data='delete_dir'
        ),
        width=2
    )

    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON['menu']} Меню', callback_data='menu'))

    return kb_builder.as_markup()

