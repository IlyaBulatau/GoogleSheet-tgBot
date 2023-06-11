from gspread.exceptions import APIError
from services.client import client

from logger.logger import logger


def create(email, name):
    """
    Используется для проверки email от пользователя
    """
    try:
        table = client.create(str(name))
        table.share(email_address=email, perm_type='user', role='writer')
        url = 'https://docs.google.com/spreadsheets/d/'+str(table.id)
        return url
    except APIError as e:
        logger.info(str(e))
        return None