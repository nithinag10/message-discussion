import base64
from flask import Flask, request
import hashMedia
import database
import json
from twilio.twiml.messaging_response import MessagingResponse
import requests  # request img from web
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET"])
def hello():
    return 'Ok'


def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)


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
    database.insertComment(collection, req_dict['hashValue'], req_dict['comment'])  # inserting comment in dbß
    return "Thanks for the comment"


@app.route("/bot", methods=["POST"])
def bot():
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    print(f'{sender} sent {message}')
    if media_url:
        image_string = requests.get(media_url).content
        hex = hashMedia.getMd5Hexa(image_string)  # getting digest
        return respond(hex)
    else:
        return respond(f'Please send an image!')


@app.route("/panel")
def handlePanelRequest():
    digest = request.args.get('hexValue')
    collection = database.findCollection(database="comments", collection="sub_comments")
    doc = database.findAllComments(collection, digest)
    return doc


@app.route("/reply-comment")
def handleReplyComment():
    parentID = request.args.get("commentID")
    comment = request.args.get("comment")
    digest = request.args.get("hexValue")
    collection = database.findCollection(database="comments", collection="sub_comments")
    database.insertReply(collection, parentID, comment, digest)
    return "Reply inserted"

