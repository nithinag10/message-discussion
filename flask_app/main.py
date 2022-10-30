import base64
from flask import Flask, request
import hashMedia
import database
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Ok'


@app.route("/upload", methods=["POST"])
def handleVideo():
    image = request.files["file"]
    image_string = base64.b64encode(image.read())  # encoding image to base64
    hex = hashMedia.getMd5Hexa(image_string)  # getting digest
    collection = database.findCollection(database="comments", collection="comments")  # finding collection
    if not database.findDocument(collection, hex):  # checking if the media already exist
        database.insertDocument(collection, hex)
    return "I got your message"


@app.route("/comment", methods=["POST"])
def postComment():
    req = request.data
    req_string = req.decode()
    req_dict = json.loads(req_string)
    collection = database.findCollection(database="comments", collection="sub_comments")  # finding collection
    database.insertComment(collection, req_dict['hashValue'],req_dict['comment']) # inserting comment in dbß
    return "Thanks for the comment"


if __name__ == "__main__":
    app.run(debug=True)
