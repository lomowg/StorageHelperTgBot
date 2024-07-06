from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot
from aiogram.types import BotCommand


def create_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🗃️ Хранилище', callback_data='storage')],
                         [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings')],
                         [InlineKeyboardButton(text='⁉️ Помощь', callback_data='help')]]
    )

    return keyboard


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/menu',
                   description='Вызов главного меню'),
    ]

    await bot.set_my_commands(main_menu_commands)
