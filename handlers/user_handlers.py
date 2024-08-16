from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMedia, InputMediaVideo, InputMediaAnimation
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


from aiogram import types

from database.database import add_new_user, get_user, get_user_folder, add_new_folder, get_user_all_folders, \
    delete_folder, get_user_folder_id, get_messages_from_folder, add_message, delete_message, update_forward_info, \
    get_user_forward_info, get_user_keep_history, update_keep_history, rename_folder
from lexicon.lexicon_general import LEXICON

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.settings_menu import create_settings_menu, create_forward_setting_menu, create_history_setting_menu
from keyboards.main_menu import create_main_menu
from keyboards.storage_menu import create_dirs_menu, create_edit_keyboard, create_rename_keyboard
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
async def process_main_menu_command(message: Message, state: FSMContext, bot: Bot, database: DataBaseClass):
    text = LEXICON_RU['menu']
    keep_history_status = await get_user_keep_history(connector=database, user_id=message.from_user.id)

    await message.answer(
        text=text,
        reply_markup=create_main_menu()
    )

    if not keep_history_status:
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


@router.callback_query(F.data == 'forward_setting')
async def process_forward_settings_command(callback: CallbackQuery, database: DataBaseClass):
    status = await get_user_forward_info(connector=database, user_id=callback.from_user.id)
    text = (f'{LEXICON_RU[callback.data]}\n\n'
            f'Сейчас: {['❌ Откл.', '✅ Вкл.'][status]}')

    await callback.message.edit_text(
        text=text,
        reply_markup=create_forward_setting_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'forward_on')
async def process_forward_settings_on(callback: CallbackQuery, database: DataBaseClass):
    status = await get_user_forward_info(connector=database, user_id=callback.from_user.id)
    text = (f'{LEXICON_RU[callback.data]}\n\n'
            f'Сейчас: ✅ Вкл.')

    await update_forward_info(connector=database, user_id=callback.from_user.id, forward_info=True)

    if callback.message.text != text:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_forward_setting_menu()
        )

    await callback.answer()


@router.callback_query(F.data == 'forward_off')
async def process_forward_settings_off(callback: CallbackQuery, database: DataBaseClass):
    status = await get_user_forward_info(connector=database, user_id=callback.from_user.id)
    text = (f'{LEXICON_RU[callback.data]}\n\n'
            f'Сейчас: ❌ Откл.')

    await update_forward_info(connector=database, user_id=callback.from_user.id, forward_info=False)

    if callback.message.text != text:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_forward_setting_menu()
        )

    await callback.answer()


@router.callback_query(F.data == 'keep_history_setting')
async def process_keep_history_setting_command(callback: CallbackQuery, database: DataBaseClass):
    status = await get_user_keep_history(connector=database, user_id=callback.from_user.id)
    text = (f'{LEXICON_RU[callback.data]}\n\n'
            f'Сейчас: {['❌ Откл.', '✅ Вкл.'][status]}')

    await callback.message.edit_text(
        text=text,
        reply_markup=create_history_setting_menu()
    )

    await callback.answer()


@router.callback_query(F.data == 'keep_history_on')
async def process_keep_history_on(callback: CallbackQuery, database: DataBaseClass):
    status = await get_user_keep_history(connector=database, user_id=callback.from_user.id)
    text = (f'{LEXICON_RU[callback.data]}\n\n'
            f'Сейчас: ✅ Вкл.')

    await update_keep_history(connector=database, user_id=callback.from_user.id, keep_history=True)

    if callback.message.text != text:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_history_setting_menu()
        )

    await callback.answer()


@router.callback_query(F.data == 'keep_history_off')
async def process_keep_history_off(callback: CallbackQuery, database: DataBaseClass):
    status = await get_user_keep_history(connector=database, user_id=callback.from_user.id)
    text = (f'{LEXICON_RU[callback.data]}\n\n'
            f'Сейчас: ❌ Откл.')

    await update_keep_history(connector=database, user_id=callback.from_user.id, keep_history=False)

    if callback.message.text != text:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_history_setting_menu()
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
    user_forward_info = await get_user_forward_info(connector=database, user_id=user_id)

    await callback.message.edit_text(f"❗️🗂 Ваши сообщения из папки {folder_name}:")

    messages = await get_messages_from_folder(connector=database, folder_id=folder_id)

    for message in messages:
        message_type = message['message_type']
        content = message['content']
        caption = message['caption']
        forward_info = message['forward_info']

        if forward_info and user_forward_info:
            caption = f"{forward_info}\n\n{caption}"

        if message_type == 'text':
            await callback.message.answer(caption)
        elif message_type == 'photo':
            await callback.message.answer_photo(content[0], caption=caption)
        elif message_type == 'video':
            await callback.message.answer_video(content[0], caption=caption)
        elif message_type == 'document':
            await callback.message.answer_document(content[0], caption=caption)
        elif message_type == 'audio':
            await callback.message.answer_audio(content[0], caption=caption)
        elif message_type == 'voice':
            await callback.message.answer_voice(content[0], caption=caption)
        elif message_type == 'animation':
            await callback.message.answer_animation(content[0], caption=caption)
        elif message_type == 'album':
            first_data = eval(content[0])
            first_data.caption = caption
            media_group = [first_data] + list(map(eval, content[1:]))

            if len(caption) > 1024:
                caption = caption[:1024]

            first_data.caption = caption
            await callback.message.answer_media_group(media_group)

    await state.set_state(FSMStorageManipulating.in_folder)
    await state.update_data(folder_id=folder_id)
    await callback.answer()


@router.message(lambda message: message.reply_to_message is not None
                                and 'del' in message.text
                                and message.reply_to_message.media_group_id
                                and (message.reply_to_message.photo or message.reply_to_message.video or message.reply_to_message.animation),
                StateFilter(FSMStorageManipulating.in_folder))
async def process_delete_albums(message: types.Message, database: DataBaseClass, state: FSMContext):
    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')
    caption = message.reply_to_message.caption if message.reply_to_message.caption else ''
    file_id = []

    if message.reply_to_message.photo:
        file_id = [f'InputMediaPhoto(media=\"{message.reply_to_message.photo[-1].file_unique_id}\")']
    elif message.reply_to_message.video:
        file_id = [f'InputMediaVideo(media=\"{message.reply_to_message.video.file_unique_id}\")']
    elif message.reply_to_message.animation:
        file_id = [f'InputMediaAnimation(media=\"{message.reply_to_message.animation.file_unique_id}\")']

    await delete_message(connector=database, folder_id=folder_id, caption=caption, file_id=file_id)
    await message.answer(text='Сообщение удалено!', reply_to_message_id=message.reply_to_message.message_id)


@router.message(lambda message: message.reply_to_message is not None and 'del' in message.text,
                StateFilter(FSMStorageManipulating.in_folder))
async def process_delete_message_command(message: types.Message, database: DataBaseClass, state: FSMContext):
    content = None
    file_id = None
    caption = message.reply_to_message.caption if message.reply_to_message.caption else ''

    if message.reply_to_message.text:
        caption = message.reply_to_message.text
    elif message.reply_to_message.photo:
        content = [message.reply_to_message.photo[-1].file_id]
        file_id = [message.reply_to_message.photo[-1].file_unique_id]
    elif message.reply_to_message.video:
        content = [message.reply_to_message.video.file_id]
        file_id = [message.reply_to_message.video.file_unique_id]
    elif message.reply_to_message.document:
        content = [message.reply_to_message.document.file_id]
        file_id = [message.reply_to_message.document.file_unique_id]
    elif message.reply_to_message.audio:
        content = [message.reply_to_message.audio.file_id]
        file_id = [message.reply_to_message.audio.file_unique_id]
    elif message.reply_to_message.voice:
        content = [message.reply_to_message.voice.file_id]
        file_id = [message.reply_to_message.voice.file_unique_id]
    elif message.reply_to_message.animation:
        content = [message.reply_to_message.animation.file_id]
        file_id = [message.reply_to_message.animation.file_unique_id]

    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')

    await delete_message(connector=database, folder_id=folder_id, caption=caption, file_id=file_id)
    await message.answer(text='Сообщение удалено!', reply_to_message_id=message.reply_to_message.message_id)


# @router.message(lambda message: message.media_group_id,
#                 StateFilter(FSMStorageManipulating.in_folder))
# async def process_new_albums(message: Message, album: list[Message]):
#     media_group = []
#     for msg in album:
#         if msg.photo:
#             file_id = msg.photo[-1].file_id
#             media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption))
#         else:
#             obj_dict = msg.dict()
#             file_id = obj_dict[msg.content_type]['file_id']
#             media_group.append(InputMedia(media=file_id))
#     print(media_group)
#     await message.answer_media_group(media_group)


@router.message(lambda message: message.media_group_id and (message.photo or message.video or message.animation),
                StateFilter(FSMStorageManipulating.in_folder))
async def process_new_albums(message: types.Message, database: DataBaseClass, state: FSMContext, album: list[Message]):
    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')

    content_group = []
    file_id_group = []
    caption = album[0].caption if album[0].caption else ''
    message_type = 'album'
    forward_tag = album[0].forward_from.username if album[0].forward_from else album[0].forward_from_chat.username
    forward_info = f"➡️ Переслано от {album[0].forward_from.full_name if album[0].forward_from else album[0].forward_from_chat.title} (@{forward_tag})"

    for n, msg in enumerate(album):
        if msg.photo:
            content_group.append(f'InputMediaPhoto(media=\"{msg.photo[-1].file_id}\")')
            file_id_group.append(f'InputMediaPhoto(media=\"{msg.photo[-1].file_unique_id}\")')
        elif msg.video:
            content_group.append(f'InputMediaVideo(media=\"{msg.video.file_id}\")')
            file_id_group.append(f'InputMediaVideo(media=\"{msg.video.file_unique_id}\")')
        elif msg.animation:
            content_group.append(f'InputMediaAnimation(media=\"{msg.animation.file_id}\")')
            file_id_group.append(f'InputMediaAnimation(media=\"{msg.animation.file_unique_id}\")')

    await add_message(connector=database,
                      folder_id=folder_id,
                      message_type=message_type,
                      content=content_group,
                      caption=caption,
                      forward_info=forward_info,
                      file_id=file_id_group)


@router.message(StateFilter(FSMStorageManipulating.in_folder))
async def process_new_message(message: types.Message, database: DataBaseClass, state: FSMContext):
    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')

    message_type = None
    content = None
    caption = message.caption if message.caption else ''
    file_id = None

    if message.forward_from or message.forward_from_chat:
        forward_tag = message.forward_from.username if message.forward_from else message.forward_from_chat.username
        forward_info = rf"➡️ Переслано от {message.forward_from.full_name if message.forward_from else message.forward_from_chat.title} (@{forward_tag})"
    else:
        forward_info = ''
    if message.text:
        message_type = 'text'
        caption = message.text
    elif message.photo:
        message_type = 'photo'
        content = [message.photo[-1].file_id]
        file_id = [message.photo[-1].file_unique_id]
    elif message.video:
        message_type = 'video'
        content = [message.video.file_id]
        file_id = [message.video.file_unique_id]
    elif message.document:
        message_type = 'document'
        content = [message.document.file_id]
        file_id = [message.document.file_unique_id]
    elif message.audio:
        message_type = 'audio'
        content = [message.audio.file_id]
        file_id = [message.audio.file_unique_id]
    elif message.voice:
        message_type = 'voice'
        content = [message.voice.file_id]
        file_id = [message.voice.file_unique_id]
    elif message.animation:
        message_type = 'animation'
        content = [message.animation.file_id]
        file_id = [message.animation.file_unique_id]
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


@router.callback_query(F.data == 'rename_dir')
async def process_rename_dir_command(callback: CallbackQuery, database: DataBaseClass):
    text = LEXICON_RU[callback.data]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_rename_keyboard(*await get_user_all_folders(connector=database,
                                                                        user_id=callback.from_user.id))
    )

    await callback.answer()


@router.callback_query(lambda x: x.data.endswith('rename'))
async def process_rename_folder_press(callback: CallbackQuery, database: DataBaseClass, state: FSMContext):
    user_id = callback.from_user.id
    folder_name = callback.data[:-6]
    folder_id = await get_user_folder_id(connector=database, user_id=user_id, folder_name=folder_name)

    await callback.message.edit_text(
        text=f"Введите новое название для папки \"{folder_name}\":",
    )

    await state.set_state(FSMStorageManipulating.rename_folder)
    await state.update_data(folder_id=folder_id)

    await callback.answer()


@router.message(StateFilter(FSMStorageManipulating.rename_folder))
async def process_rename_folder(message: types.Message, database: DataBaseClass, state: FSMContext):
    new_folder_name = message.text
    user_id = message.from_user.id

    state_data = await state.get_data()
    folder_id = state_data.get('folder_id')

    if await get_user_folder(database, user_id, new_folder_name):
        await message.answer("Папка с таким названием уже существует. Попробуйте другое название.")
    else:
        await rename_folder(database, user_id, folder_id, new_folder_name)
        await message.answer(f"Папка успешно переименована.",
                             reply_markup=create_dirs_menu(* await get_user_all_folders(connector=database,
                                                                                        user_id=message.from_user.id)))
        await state.set_state(default_state)
