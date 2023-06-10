import gspread as gs

client = gs.service_account(filename='auth.json') 

def create(email, name):
    table = client.create(str(name))
    table.share(email_address=email, perm_type='user', role='writer')

    url = 'https://docs.google.com/spreadsheets/d/'+str(table.id)

    return url