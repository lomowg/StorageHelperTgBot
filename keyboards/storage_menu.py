from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_general import LEXICON


def create_dirs_menu(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text='📍 Избранное', callback_data='Избранное_fldBtn'))

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=str(button).replace('_fldBtn', ''),
            callback_data=str(button)
        ))

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

    kb_builder.row(InlineKeyboardButton(text='✏️ Переименовать папку', callback_data='rename_dir'))

    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON['menu']} Меню', callback_data='menu'))

    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {str(button).replace('_fldBtn', '')}',
            callback_data=f'{str(button).replace('_fldBtn', '')}del'
        ))

    kb_builder.row(
        InlineKeyboardButton(
            text='⬅️ Отменить',
            callback_data='storage'
        )
    )
    return kb_builder.as_markup()


def create_rename_keyboard(*args: int) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'✏️ {str(button).replace('_fldBtn', '')}',
            callback_data=f'{str(button).replace('_fldBtn', '')}rename'
        ))

    kb_builder.row(
        InlineKeyboardButton(
            text='⬅️ Отменить',
            callback_data='storage'
        )
    )
    return kb_builder.as_markup()
