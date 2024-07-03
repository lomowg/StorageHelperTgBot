from aiogram import Router
from aiogram.types import Message
from keyboards.main_menu import create_main_menu

router = Router()

@router.message()
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}', reply_markup=create_main_menu())