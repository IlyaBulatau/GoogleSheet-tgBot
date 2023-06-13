from aiogram.fsm.state import State, StatesGroup

class WorkForm(StatesGroup):
    method = State()

class CreateTableForm(StatesGroup):
    email = State()
    name = State()

class ModificationTableForm(StatesGroup):
    table_url = State()

class ActionTableForm(StatesGroup):
    action = State()
    table_name = State()
    values = State()
    cell = State()
    index = State()
    table_url = State()

