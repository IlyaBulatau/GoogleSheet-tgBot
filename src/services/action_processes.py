from gspread import Worksheet, client as cl
from gspread.client import Spreadsheet
from gspread.exceptions import IncorrectCellLabel

from services.client import client

class ActionTable:
    """
    Обьект действий с таблицей
    """
    
    def __init__(self, url: str, data: str = None):
        self.client: cl = client # обьект клиента google
        self.table: Spreadsheet = client.open_by_url(url) # обьект таблицы
        self.data: str = data # данные
        self.sheet: Worksheet = self.table.sheet1 # обьект первого листа

    def insert_ro_in_table(self):
        """
        Вставляет список значений в начало таблицы
        """
        data = self._serialazer()
        self.sheet.insert_row(data)


    def append_row_in_table(self):
        """
        Вставляет список значений в конец таблицы
        """
        data = self._serialazer()
        self.sheet.append_row(data)

    def set_value_in_cell(self, cell, value):
        """
        Вставляет значения в ячейку

        Если номер ячейки не валиден обрабатывает исключение и возвращает False 
        """
        try:
            self.sheet.update_acell(cell, value)
            return True
        except IncorrectCellLabel as e:
            return False

    def rename_table(self, name):
        """
        Менет имя паблицы
        """
        self.table.update_title(name)

    def _serialazer(self):
        result = []
        for item in self.data.split():
            item = item.replace('_', ' ')
            result.append(item)
        return result
    
    
