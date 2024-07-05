from aiogram.filters.state import StatesGroup, State


class FSMStorageManipulating(StatesGroup):
    in_menu = State()
    in_folder = State()
    write_folder_name = State()
    