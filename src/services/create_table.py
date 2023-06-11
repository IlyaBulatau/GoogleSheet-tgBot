from gspread.exceptions import APIError
from services.client import client


def create(email, name):
    try:
        table = client.create(str(name))
        table.share(email_address=email, perm_type='user', role='writer')
        url = 'https://docs.google.com/spreadsheets/d/'+str(table.id)
        return table
    except APIError as e:
        return None