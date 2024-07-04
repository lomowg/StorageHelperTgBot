from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import add_new_user, get_user
from lexicon.lexicon_general import LEXICON

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.settings_menu import create_settings_menu, create_language_menu
from keyboards.main_menu import create_main_menu
from keyboards.storage_menu import create_dirs_menu
from database.connection_pool import DataBaseClass


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, database: DataBaseClass):

    text = LEXICON_RU[message.text]

    if not await get_user(connector=database, user_id=message.from_user.id):
        await add_new_user(connector=database, user_id=message.from_user.id, username=message.from_user.username)

    await message.answer(
        text=text,
        reply_markup=create_main_menu()
    )


@router.callback_query(F.data == 'storage')
async def process_storage_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_dirs_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'settings')
async def process_settings_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_settings_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'language')
async def process_language_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_language_menu()
    )

    await callback.answer()


@router.callback_query(F.data.in_(['lan_RU', 'lan_EN']))
async def process_language_choice_command(callback: CallbackQuery):
    # Реализовать смену языка

    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_language_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'menu')
async def process_menu_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_main_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'create_dir')
async def process_create_dir_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_dirs_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'delete_dir')
async def process_delete_dir_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    # Реализовать удаление папок

    await callback.message.edit_text(
        text=text,
        reply_markup=create_dirs_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'help')
async def process_help_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON['menu']} Меню', callback_data='menu'))

    await callback.message.edit_text(
        text=text,
        reply_markup=kb_builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data == 'to_author')
async def process_create_dir_command(callback: CallbackQuery):
    text = LEXICON_RU[callback.data]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='settings'))

    await callback.message.edit_text(
        text=text,
        reply_markup=kb_builder.as_markup()
    )

    await callback.answer()
