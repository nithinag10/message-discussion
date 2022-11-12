from flask_app import settings
from datetime import datetime
import json
from bson import json_util
import json
import bson


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


def insertComment(collection, hex, comment, name):
    now = datetime.now()
    inserting_id = bson.objectid.ObjectId()
    record = {"hashValue": hex, 'comment': comment, 'date': now, 'parentID': None, "name": name, "_id": inserting_id}
    collection.insert_one(record)
    response = {}
    for (key, value) in record.items():
        if key == "_id":
            response['id'] = str(record[key])
        elif key == "date":
            response['date'] = record[key].isoformat()
        else:
            response[key] = record[key]
    return response


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


def insertReply(collection, parentID, comment, digest, name):
    now = datetime.now()
    inserting_id = bson.objectid.ObjectId()
    record = {'parentID': parentID, 'comment': comment, 'date': now, 'hashValue': digest, "_id":inserting_id, 'name':name}
    collection.insert_one(record)
    response = {}
    for (key, value) in record.items():
        if key == "_id":
            response['id'] = str(record[key])
        elif key == "date":
            response['date'] = record[key].isoformat()
        else:
            response[key] = record[key]
    return response
