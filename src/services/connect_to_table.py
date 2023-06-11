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
        return url
    except NoValidUrlKeyFound as e:
        logger.info(str(e))
        return CONNECT_STATUS['Invalid']
    except APIError as e:
        logger.info(str(e))
        return CONNECT_STATUS['Api Error']