from aiogram import Router
from aiogram.types import Message
from keyboards.main_menu import create_main_menu

router = Router()


@router.message()
async def any_message(message: Message):
    await message.answer(f'Я работаю только через меню:', reply_markup=create_main_menu())