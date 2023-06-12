from services.client import client
from gspread.exceptions import NoValidUrlKeyFound, APIError

from documents.documents import CONNECT_STATUS
from logger.logger import logger

def table_connect(url):
    """
    Используется для проверки url от пользователя
    """
    try:
        table = client.open_by_url(url)
        table_name = str(table.title)
        return (url, table_name)
    except NoValidUrlKeyFound as e:
        logger.info(str(e))
        return (CONNECT_STATUS['Invalid'], 0) # для того что бы возвращать кортеж
    except APIError as e:
        logger.info(str(e))
        return (CONNECT_STATUS['Api Error'], 0)