from dotenv import load_dotenv
import os
import pymongo

load_dotenv()  # take environment variables from .env.


def setupMongoDB(database , collection):
    """

    :rtype: object
    """
    client = pymongo.MongoClient("mongodb+srv://"+os.environ['USER_NAME']+":" + os.environ[
        'SECRET_KEY'] + "@cluster0.2vscuym.mongodb.net/?retryWrites=true&w=majority")
    database = client[database]
    collection = database[collection]
    return collection

