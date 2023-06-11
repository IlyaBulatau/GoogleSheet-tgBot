from services.client import client
from gspread.exceptions import NoValidUrlKeyFound, APIError

from documents.documents import CONNECT_STATUS

def table_connect(url):
    try:
        table = client.open_by_url(url)
        return url
    except NoValidUrlKeyFound as e:
        return CONNECT_STATUS['Invalid']
    except APIError as e:
        return CONNECT_STATUS['Api Error']