import pymongo
import os
import certifi


ca = certifi.where()
mongodb_uri = os.getenv('MONGODB_URI')
mongo = pymongo.MongoClient(mongodb_uri, tlsCAFile=ca)