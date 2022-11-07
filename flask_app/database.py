import settings
from datetime import datetime
import json
from bson import json_util


def findCollection(database, collection):
    return settings.setupMongoDB(database, collection)


def findDocument(collection, hex):
    if collection.find_one({'hashvalue': hex}):
        return True
    else:
        return False


def parse_json(data):
    return json.loads(json_util.dumps(data))


def insertDocument(collection, hex):
    record = {"hashvalue": hex}
    collection.insert_one(record)


def insertComment(collection, hex, comment):
    now = datetime.now()
    record = {"hashValue": hex, 'comment': comment, 'date': now, 'parentID': None}
    print(collection.insert_one(record))


def findAllComments(collection, hex):
    search = {"hashValue": hex}
    doc = []
    for comment in collection.find(search):
        record = {}
        for (key, value) in comment.items():
            if key == "_id":
                record['id'] = str(comment[key])
            elif key == "date":
                record['date'] = comment[key].isoformat()
            else:
                record[key] = comment[key]
        doc.append(record)
    return doc


def insertReply(collection, parentID, comment, digest):
    now = datetime.now()
    record = {'parentID': parentID, 'comment': comment, 'date': now, 'hashValue': digest}
    print(collection.insert_one(record))
