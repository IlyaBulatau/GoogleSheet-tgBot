import gspread as gs
from gspread.exceptions import APIError

from database.models import User

client = gs.service_account(filename='auth.json') 

def create(email, name):
    try:
        table = client.create(str(name))
        table.share(email_address=email, perm_type='user', role='writer')
        url = 'https://docs.google.com/spreadsheets/d/'+str(table.id)
        return url
    except APIError as e:
        return None