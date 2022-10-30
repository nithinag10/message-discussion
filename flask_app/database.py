import settings


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
    record = {"hashValue": hex, 'comment': comment}
    print(collection.insert_one(record))
