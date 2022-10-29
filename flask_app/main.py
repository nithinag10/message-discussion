import base64
from flask import Flask, request
import hashMedia
import database

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Ok'


@app.route("/upload", methods=["POST"])
def handleVideo():
    image = request.files["file"]
    image_string = base64.b64encode(image.read())  # encoding image to base64
    hex = hashMedia.getMd5Hexa(image_string) # getting digest
    collection = database.findCollection() # finding collection
    if not database.findDocument(collection, hex): # checking if the media already exist
        database.insertDocument(collection, hex)
    return "DONE boy"


if __name__ == "__main__":
    app.run(debug=True)
