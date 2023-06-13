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

    def insert_row_in_table(self):
        """
        Вставляет список значений в начало таблицы
        """
        data = self._serialazer_for_row()
        self.sheet.insert_row(data)


    def append_row_in_table(self):
        """
        Вставляет список значений в конец таблицы
        """
        data = self._serialazer()
        self.sheet.append_row(data)
    
    def insert_rows_in_table(self):
        data = self._serialiazer_for_rows()
        self.sheet.insert_rows(data)

    def append_rows_in_table(self):
        data = self._serialiazer_for_rows()
        self.sheet.append_rows(data, table_range='A1')
    
    def append_rows_by_cell(self, cell):
        data = self._serialiazer_for_rows()
        self.sheet.append_rows(data, table_range=cell)
    
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

    def _serialazer_for_row(self):
        result = [item.replace('_', ' ') for item in self.data.split()]
        return result
    
    def _serialiazer_for_rows(self):
        result = [[word.replace('_', ' ') for word in row.split()]for row in self.data.split('\n')]
        return result
    
    
