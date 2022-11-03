import settings
from datetime import datetime



def findCollection(database, collection):
    return settings.setupMongoDB(database, collection)


def findDocument(collection, hex):
    if collection.find_one({'hashvalue': hex}):
        return True
    else:
        return False


def insertDocument(collection, hex):
    record = {"hashvalue": hex}
    collection.insert_one(record)


def insertComment(collection, hex, comment):
    now = datetime.now()
    record = {"hashValue": hex, 'comment': comment, 'date':now}
    print(collection.insert_one(record))


def findAllComments(collection , hex):
    search = { "hashValue" : hex}
    doc = []
    for comment in collection.find(search):
        doc.append({'date':comment.get('date') , 'coment':comment.get('comment')})
    return doc



