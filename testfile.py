import pymongo
import os

mongodb_uri = os.getenv('MONGODB_URI')
mongo = pymongo.MongoClient(mongodb_uri)


db = mongo['Season3']
drivers_col = db['Drivers']

drivers_col.update_many({}, {"$set": {"placement": {
    "string": "",
    "ms": 100000
}}})