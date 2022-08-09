import gspread
from dotenv import load_dotenv
import os
import pymongo
from pprint import pprint


def next_available_row(worksheet):
  str_list = list(filter(None, worksheet.col_values(1)))
  return len(str_list) + 1


def update_sheet(driverlist, mongo):
    load_dotenv()

    creds = {
      "type": "service_account",
      "project_id": os.getenv("G_PROJECT_ID"),
      "private_key_id": os.getenv("G_PRIVATE_KEY_ID"),
      "private_key": os.getenv("G_PRIVATE_KEY").replace(r'\n', '\n'),
      "client_email": os.getenv("G_CLIENT_EMAIL"),
      "client_id": os.getenv("G_CLIENT_ID"),
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": os.getenv("G_CERT_URI")
    }

    gc = gspread.service_account_from_dict(creds)
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/10aTiW9Y-DLus_FmJO6ZK6XCPW1cLhBwiyUKam7SW7F0/edit#gid=0")
    wks1 = sh.get_worksheet(0)
    next_row = next_available_row(wks1)

    db = mongo['Season2']
    drivers_col = db['Drivers']
    cars_col = db['Cars']

    # res = drivers_col.find_one({"id": id})

    try:
        wks1.batch_update([{
          'range': f'A{"2"}:F{str(2 + len(driverlist))}',
          'values': driverlist
        }])
    except gspread.exceptions.APIError as er:
        pprint(er)




