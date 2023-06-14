from gspread import Worksheet, client as cl
from gspread.client import Spreadsheet
from gspread.exceptions import IncorrectCellLabel, APIError
import gspread_formatting as gf
from string import ascii_letters

from services.client import client

class BaseTable:
    """
    Базовый класс таблиц
    """

    def __init__(self, url: str, data: str = None):
        self.client: cl = client # обьект клиента google
        self.table: Spreadsheet = client.open_by_url(url) # обьект таблицы
        self.data: str = data # данные
        self.sheet: Worksheet = self.table.sheet1 # обьект первого листа


class ActionTable(BaseTable):
    """
    Обьект действий с таблицей
    """
    
    def __init__(self, url: str, data: str = None):
        super().__init__(url, data)

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
        data = self._serialazer_for_row()
        self.sheet.append_row(data)
    
    def insert_row_by_index(self, index):
        data = self._serialazer_for_row()
        try:
            self.sheet.insert_row(data, int(index))
            return True
        except ValueError as e:
            return False
            
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

    def delete_rows(self, index):
        index = self._serializer_index(index)
        if isinstance(index, int):
            self.sheet.delete_rows(index)
            return True
        if isinstance(index, tuple):
            start, end = index
            self.sheet.delete_rows(start, end)
            return True
        return False

    def _serialazer_for_row(self):
        result = [item.replace('_', ' ') for item in self.data.split()]
        return result
    
    def _serialiazer_for_rows(self):
        result = [[word.replace('_', ' ') for word in row.split()]for row in self.data.split('\n')]
        return result
    
    def _serializer_index(self, index):
        if str(index).isdigit():
            return int(index)
        try:
            start, end = index.split(':')
            return (int(start), int(end))
        except:
            return ValueError
    

class ColorFormattingTable(BaseTable):

    def __init__(self, url: str, data: str = None):
        super().__init__(url, data)

    def set_color(self, values, color):
        color = self._get_color(color)
        if values in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\
                        АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ': # если указаны русские симолы не пропускать
            return False
        
        format_ = gf.CellFormat(backgroundColor=gf.Color(*color)) # форматирование по цвету
        try:
            gf.format_cell_range(self.sheet, values, format_)
            return True
        except APIError as e:
            return False
        except ValueError as e:
            return False
    
    def _get_color(self, color: str):
        """
        Достает цвет из коллбека
        """
        color = color.split('_')[1]

        if color == 'blue':
            return (0, 0.25, 1)

        elif color == 'red':
            return (1, 0.25, 0)

        elif color == 'green':
            return (0.25, 1, 0)        
        