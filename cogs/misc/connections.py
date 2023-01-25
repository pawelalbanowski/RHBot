import pymongo
import os

mongodb_uri = os.getenv('MONGODB_URI')
mongo = pymongo.MongoClient(mongodb_uri)