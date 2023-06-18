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

class FormattingTableForm(StatesGroup):
    formatting = State()
    table_url = State()

class ColorFormattingTableForm(StatesGroup):
    formatting = State()
    cell = State()
    values = State()
    rgb = State()
    table_url = State()


class FontFormattingTableForm(StatesGroup):
    formatting = State()
    font = State()
    style = State()
    cell = State()
    size = State()
    color = State()
    rgb = State()
    table_url = State()

class PaymentForm(StatesGroup):
    label = State()
    days = State()