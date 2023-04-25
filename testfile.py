import pymongo
import os
from pprint import pprint

# mongodb_uri = os.getenv('MONGODB_URI')
# mongo = pymongo.MongoClient(mongodb_uri)
#
#
# db = mongo['RH']
# drivers_col = db['drivers']
#
# drivers_col.update_many({}, {"$set": {"placement": {
#     "lap_string": "",
#     "lap_ms": 100000,
#     "finish_string": "",
#     "finish_ms": 1000000
# }}})


test = [
    {'id': 1, 't': 't'},
    {'id': 2, 'd': 'd'},
]

pprint((list(filter(lambda d: d['id'] == 2, test)))[0])



