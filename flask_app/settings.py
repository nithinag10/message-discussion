from dotenv import load_dotenv
import os
import pymongo

load_dotenv()  # take environment variables from .env.


def setupMongoDB():
    client = pymongo.MongoClient("mongodb+srv://discussmadro:" + os.environ[
        'SECRET_KEY'] + "@cluster0.2vscuym.mongodb.net/?retryWrites=true&w=majority")
    return client
