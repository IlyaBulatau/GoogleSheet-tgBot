from aiogram.fsm.state import State, StatesGroup

class WorkForm(StatesGroup):
    method = State()

class CreateTableForm(StatesGroup):
    email = State()
    name = State()

class ModificationTableForm(StatesGroup):
    table_url = State()