from gspread import Worksheet, client as cl
from gspread.client import Spreadsheet

from services.client import client

class ActionTable:
    """
    Обьект действий с таблицей
    """
    
    def __init__(self, url: str, data: str):
        self.client: cl = client
        self.table: Spreadsheet = client.open_by_url(url)
        self.data: str = data
        self.sheet: Worksheet = self.table.sheet1

    def insert_ro_in_table(self):
        data = self._serialazer()
        self.sheet.insert_row(data)


    def append_row_in_table(self):
        data = self._serialazer()
        self.sheet.append_row(data)

    def _serialazer(self):
        result = []
        for item in self.data.split():
            item = item.replace('_', ' ')
            result.append(item)
        return result

