import pymongo
import settings
from bson.json_util import dumps, loads


def findCollection():
    return settings.setupMongoDB(database="comments", collection="comments")


def findDocument(collection, hex):
    if collection.find_one({'hashvalue': hex}):
        return True
    else :
        return False




def insertDocument(collection , hex):
    record = {"hashvalue": hex}
    print(collection.insert_one(record))

