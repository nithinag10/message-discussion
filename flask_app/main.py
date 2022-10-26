import base64
from flask import Flask, request
import hashMedia
import settings

app = Flask(__name__)


@app.route('/')
def hello():
    client = settings.setupMongoDB()
    print(client)
    return 'Ok'


@app.route("/upload", methods=["POST"])
def handleVideo():
    image = request.files["file"]
    image_string = base64.b64encode(image.read())  # encoding image to base64
    hexa = hashMedia.getMd5Hexa(image_string)
    return "DONE boy"


if __name__ == "__main__":
    app.run(debug=True)
