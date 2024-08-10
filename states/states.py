from aiogram.filters.state import StatesGroup, State


class FSMStorageManipulating(StatesGroup):
    in_folder = State()
    write_folder_name = State()
    rename_folder = State()
