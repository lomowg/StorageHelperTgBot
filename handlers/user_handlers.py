from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram import types

from database.database import add_new_user, get_user, get_user_folder, add_new_folder, get_user_all_folders, \
    delete_folder, get_user_folder_id, get_messages_from_folder, add_message, delete_message
from lexicon.lexicon_general import LEXICON

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.settings_menu import create_settings_menu, create_language_menu
from keyboards.main_menu import create_main_menu
from keyboards.storage_menu import create_dirs_menu, create_edit_keyboard
from database.connection_pool import DataBaseClass
from services.delete_messages import cmd_clear

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


@router.message(Command(commands=['menu']))
async def process_main_menu_command(message: Message, state: FSMContext, bot: Bot):
    text = LEXICON_RU['menu']

    await message.answer(
        text=text,
        reply_markup=create_main_menu()
    )

    await cmd_clear(message=message, bot=bot)
    await state.set_state(default_state)


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

    await callback.message.edit_text(
        text=text,
        reply_markup=create_edit_keyboard(*await get_user_all_folders(connector=database,
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


@router.callback_query(lambda x: x.data.endswith('del'))
async def process_del_bookmark_press(callback: CallbackQuery, database: DataBaseClass):
    await delete_folder(connector=database, user_id=callback.from_user.id, folder_name=callback.data[:-3])
    await callback.message.edit_text(
        text=LEXICON_RU['storage'],
        reply_markup=create_dirs_menu(*await get_user_all_folders(connector=database, user_id=callback.from_user.id))
    )

    await callback.answer()


@router.callback_query(lambda x: x.data.endswith('_fldBtn'))
async def process_folder_press(callback: CallbackQuery, database: DataBaseClass, state: FSMContext):
    folder_name = callback.data.replace('_fldBtn', '')
    user_id = callback.from_user.id
    folder_id = await get_user_folder_id(connector=database, user_id=user_id, folder_name=folder_name)

    await callback.message.edit_text(f"❗️🗂 Ваши сообщения из папки {folder_name}:")

    messages = await get_messages_from_folder(connector=database, folder_id=folder_id)

    for message in messages:
        message_type = message['message_type']
        content = message['content']
        caption = message['caption']
        forward_info = message['forward_info']

        if forward_info:
            if caption:
                caption = f"⤴️{forward_info}\n\n{caption}"
            else:
                caption = f'⤴️{forward_info}\n\n'

        if message_type == 'text':
            await callback.message.answer(f'{caption}{content}')
        elif message_type == 'photo':
            await callback.message.answer_photo(content, caption=caption)
        elif message_type == 'video':
            await callback.message.answer_video(content, caption=caption)
        elif message_type == 'document':
            await callback.message.answer_document(content, caption=caption)
        elif message_type == 'audio':
            await callback.message.answer_audio(content, caption=caption)
        elif message_type == 'voice':
            await callback.message.answer_voice(content, caption=caption)
        elif message_type == 'animation':
            await callback.message.answer_animation(content, caption=caption)

    await state.set_state(FSMStorageManipulating.in_folder)
    await state.update_data(folder_id=folder_id)
    await callback.answer()


@router.message(lambda message: message.reply_to_message is not None and 'del' in message.text,
                StateFilter(FSMStorageManipulating.in_folder))
async def process_delete_message_command(message: types.Message, database: DataBaseClass, state: FSMContext):
    content = None
    file_id = None

    if message.reply_to_message.text:
        content = message.reply_to_message.text
    elif message.reply_to_message.photo:
        content = message.reply_to_message.photo[-1].file_id
        file_id = message.reply_to_message.photo[-1].file_unique_id
    elif message.reply_to_message.video:
        content = message.reply_to_message.video.file_id
        file_id = message.reply_to_message.video.file_unique_id
    elif message.reply_to_message.document:
        content = message.reply_to_message.document.file_id
        file_id = message.reply_to_message.document.file_unique_id
    elif message.reply_to_message.audio:
        content = message.reply_to_message.audio.file_id
        file_id = message.reply_to_message.audio.file_unique_id
    elif message.reply_to_message.voice:
        content = message.reply_to_message.voice.file_id
        file_id = message.reply_to_message.voice.file_unique_id
    elif message.reply_to_message.animation:
        content = message.reply_to_message.animation.file_id
        file_id = message.reply_to_message.animation.file_unique_id

    caption = message.reply_to_message.caption if message.reply_to_message.caption else ''
    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')

    await delete_message(connector=database, folder_id=folder_id, content=content, caption=caption, file_id=file_id)
    await message.answer(text='Сообщение удалено!', reply_to_message_id=message.reply_to_message.message_id)


@router.message(StateFilter(FSMStorageManipulating.in_folder))
async def process_new_message(message: types.Message, database: DataBaseClass, state: FSMContext):
    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')

    message_type = None
    content = None
    caption = message.caption if message.caption else ''
    file_id = None

    if message.forward_from or message.forward_from_chat:
        forward_info = f"Переслано от {message.forward_from.full_name if message.forward_from else message.forward_from_chat.title}"
    else:
        forward_info = ''

    if message.text:
        message_type = 'text'
        content = message.text
    elif message.photo:
        message_type = 'photo'
        content = message.photo[-1].file_id
        file_id = message.photo[-1].file_unique_id
    elif message.video:
        message_type = 'video'
        content = message.video.file_id
        file_id = message.video.file_unique_id
    elif message.document:
        message_type = 'document'
        content = message.document.file_id
        file_id = message.document.file_unique_id
    elif message.audio:
        message_type = 'audio'
        content = message.audio.file_id
        file_id = message.audio.file_unique_id
    elif message.voice:
        message_type = 'voice'
        content = message.voice.file_id
        file_id = message.voice.file_unique_id
    elif message.animation:
        message_type = 'animation'
        content = message.animation.file_id
        file_id = message.animation.file_unique_id
    else:
        await message.answer("Этот тип сообщения не поддерживается.")
        return

    await add_message(connector=database,
                      folder_id=folder_id,
                      message_type=message_type,
                      content=content,
                      caption=caption,
                      forward_info=forward_info,
                      file_id=file_id)



