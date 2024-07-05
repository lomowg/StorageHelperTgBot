from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram import types

from database.database import add_new_user, get_user, get_user_folder, add_new_folder, get_user_all_folders
from lexicon.lexicon_general import LEXICON

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.settings_menu import create_settings_menu, create_language_menu
from keyboards.main_menu import create_main_menu
from keyboards.storage_menu import create_dirs_menu
from database.connection_pool import DataBaseClass

from states.states import FSMStorageManipulating


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
async def process_storage_command(callback: CallbackQuery, database: DataBaseClass):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_dirs_menu(* await get_user_all_folders(connector=database, user_id=callback.from_user.id))
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
async def process_create_dir_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Введите название новой папки:",
    )

    await state.set_state(FSMStorageManipulating.write_folder_name)
    await callback.answer()


@router.message(StateFilter(FSMStorageManipulating.write_folder_name))
async def process_folder_name(message: types.Message, database: DataBaseClass, state: FSMContext):
    folder_name = message.text
    user_id = message.from_user.id

    if await get_user_folder(database, user_id, folder_name):
        await message.answer("Папка с таким названием уже существует. Попробуйте другое название.")
    else:
        await add_new_folder(database, user_id, folder_name)
        await message.answer(f"Папка '{folder_name}' успешно создана.",
                             reply_markup=create_dirs_menu(* await get_user_all_folders(connector=database,
                                                                                        user_id=message.from_user.id)))
        await state.set_state(default_state)


@router.callback_query(F.data == 'delete_dir')
async def process_delete_dir_command(callback: CallbackQuery, database: DataBaseClass):
    text = LEXICON_RU[callback.data]

    # Реализовать удаление папок

    await callback.message.edit_text(
        text=text,
        reply_markup=create_dirs_menu(*await get_user_all_folders(connector=database,
                                                                  user_id=callback.from_user.id))
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
