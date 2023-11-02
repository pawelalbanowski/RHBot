import gspread
from dotenv import load_dotenv
import os
import pymongo
from pprint import pprint



def next_available_row(worksheet):
  str_list = list(filter(None, worksheet.col_values(1)))
  return len(str_list) + 1


def update_gsheet(driverlist, mongo, wks_num):
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
    wks = sh.get_worksheet(wks_num)
    next_row = next_available_row(wks)

    try:
        wks.batch_clear([f"A2:H{next_row}"])
        wks.batch_update([{
          'range': f'A2:H{str(2 + len(driverlist))}',
          'values': driverlist
        }])
    except gspread.exceptions.APIError as er:
        pprint(er)


def update_rc(wks_num, clips):
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
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/17p5B6Wr5jFBVtWq1H0EGTDEnDWa7xupn6Q-blWLzdow/edit#gid=1494087773")
    wks = sh.get_worksheet(wks_num)
    next_row = next_available_row(wks)

    try:
        # wks.batch_clear([f"A2:K{next_row}"])
        wks.batch_update([{
          'range': f"B4:D{str(4 + len(clips['S1']))}",
          'values': clips['S1']
        }])
        wks.batch_update([{
            'range': f"B56:D{str(56 + len(clips['S2']))}",
            'values': clips['S2']
        }])
        wks.batch_update([{
            'range': f"B108:D{str(108 + len(clips['S3']))}",
            'values': clips['S3']
        }])
        wks.batch_update([{
            'range': f"B160:D105{str(160 + len(clips['S4']))}",
            'values': clips['S4']
        }])
    except gspread.exceptions.APIError as er:
        pprint(er)




