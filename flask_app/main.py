import base64

from flask import Flask, request
import hashMedia

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Ok'


@app.route("/upload", methods=["POST"])
def handleVideo():
    image = request.files["file"]
    image_string = base64.b64encode(image.read())
    hexa = hashMedia.getMd5Hexa(image_string)
    print(hexa)
    return "DONE boy"
