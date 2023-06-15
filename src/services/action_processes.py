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

    def set_color(self, cell, color):
        
        color = self._get_color(color)
        if cell in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\
                        АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ': # если указаны русские симолы не пропускать
            return False
        
        format_ = gf.CellFormat(backgroundColor=gf.Color(*color)) # форматирование по цвету
        try:
            gf.format_cell_range(self.sheet, cell, format_)
            return 'Suc'
        except APIError as e:
            return False
        except ValueError as e:
            return False
        
    def set_color_rgb(self, cell, rgb):
        if not self._is_valid_rgb(rgb):
            return 'error rgb'
        
        if cell in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\
                        АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ': # если указаны русские симолы не пропускать
            return 'error cell'

        r, g, b = rgb.split()
        rgb = self._rgb_serializer((int(r), int(g), int(b)))

        format_ = gf.CellFormat(backgroundColor=gf.Color(*rgb)) # форматирование по цвету
        try:
            gf.format_cell_range(self.sheet, cell, format_)
            return True
        except APIError as e:
            return 'error cell'
        except ValueError as e:
            return 'error cell'

            
    def _get_color(self, color: str):
        """
        Достает цвет из коллбека
        """
        color = color.split('_')[1]

        if color == 'blue':
            return self._rgb_serializer((0, 0, 255))

        elif color == 'red':
            return self._rgb_serializer((255, 0, 0))

        elif color == 'green':
            return self._rgb_serializer((0, 255, 0))

        elif color == 'white':
            return self._rgb_serializer((255, 255, 255))

        elif color == 'black':
            return self._rgb_serializer((0, 0, 0))

        elif color == 'yellow':
            return self._rgb_serializer((255, 255, 0))

        elif color == 'grey':
            return self._rgb_serializer((128, 128, 128))

        elif color == 'brown':
            return self._rgb_serializer((139, 69, 19))      
        
    
    def _rgb_serializer(self, rgb):
        """
        Сериализует входящий rgb в значени от 0 до 1
        """
        r, g, b = rgb
        return(round(r/255, 2), round(g/255, 2), round(b/255, 2))
        
        
    def _is_valid_rgb(self, color):   
        """
        Проверяет валидность введенных данных rgb
        """     
        try:
            r, g, b = color.split()
        except:
            return False

        if not all((
            str(r).isdigit(),
            str(g).isdigit(),
            str(b).isdigit())):
            return False

        if not all((
            0 <= int(r) <= 255,
            0 <= int(g) <= 255,
            0 <= int(b) <= 255)):
            return False
        
        return True
    
class FontFormattingTable(BaseTable):

    def __init__(self, url: str, data: str = None):
        super().__init__(url, data)

    def set_font_style(self, cell, style):
        if cell in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\
                        АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ': # если указаны русские симолы не пропускать
            return False

        style = self._style_serialier(style)

        if style == 'italic':
            format_ = gf.CellFormat(textFormat=gf.TextFormat(italic=True))
        
        elif style == 'bold':
            format_ = gf.CellFormat(textFormat=gf.TextFormat(bold=True))

        elif style == 'georgia':
            format_ = gf.CellFormat(textFormat=gf.TextFormat(fontFamily=style))

        elif style == 'verdana':
            format_ = gf.CellFormat(textFormat=gf.TextFormat(fontFamily=style))

        elif style == 'strikethrough':
            format_ = gf.CellFormat(textFormat=gf.TextFormat(strikethrough=True))

        elif style == 'underline':
            format_ = gf.CellFormat(textFormat=gf.TextFormat(underline=True))

        try:
            gf.format_cell_range(self.sheet, cell, format_)  
            return True
        except APIError as e:
            return False
        except ValueError as e:
            return False


    def set_font_size(self, cell, size):
        if cell in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\
                        АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ': # если указаны русские симолы не пропускать
            return 'error cell'
        
        if not self._is_valid_size(size):
            return 'error size'

        format_ = gf.CellFormat(textFormat=gf.TextFormat(fontSize=int(size)))

        try:
            gf.format_cell_range(self.sheet, cell, format_)
            return True
        except APIError as e:
            return 'error cell'
        except ValueError as e:
            return 'error cell'



    def _is_valid_size(self, size):
        if str(size).isdigit():
            return True
        return False


    def _style_serialier(self, style):
        style = style.split('_')[1]

        return style