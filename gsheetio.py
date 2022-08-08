import gspread
from dotenv import load_dotenv
import os
import pymongo
from pprint import pprint

def update_sheet(msg, roles, mongo):
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

  wks1.batch_update([{
    'range': 'A2:B3',
    'values': [['first', 'second'], ['third', 'fourth']]
  }])


  mongodb_uri = os.getenv('MONGODB_URI')

  mongo = pymongo.MongoClient(mongodb_uri)

  db = mongo['Season2']
  drivers_col = db['Drivers']
  cars_col = db['Cars']

  result = drivers_col.update_one({"gt": "Albannt8960"}, {"$set": {"dcname": "albannt"}})

  pprint(result)


