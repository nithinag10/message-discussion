import base64
from flask import Flask, request
from flask_app import hashMedia
from flask_app import database
import json
from twilio.twiml.messaging_response import MessagingResponse
import requests  # request img from web
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/', methods=["GET"])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def postComment():
    req = request.data
    req_string = req.decode()
    req_dict = json.loads(req_string)
    collection = database.findCollection(database="comments", collection="sub_comments")  # finding collection
    response = database.insertComment(collection, req_dict['hashValue'], req_dict['comment'], name=req_dict['name'])  # inserting comment in dbß
    return response


@app.route("/bot", methods=["POST"])
def bot():
    load_dotenv()
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    print(message)
    print(f'{sender} sent {message}')
    if media_url:
        image_string = requests.get(media_url).content
        hex = hashMedia.getMd5Hexa(image_string)  # getting digest
    else:
        hex = hashMedia.getMd5Hexa(message.encode('utf-8')) # getting digest from text message
    collection = database.findCollection(database="comments", collection="comments")  # finding collection
    if not database.findDocument(collection, hex):  # checking if the media already exist
        database.insertDocument(collection, hex)
    return respond("Enter forum here:"+os.environ['FRONT_END_HOST']+"/panel/"+str(hex))

@app.route("/panel")
@cross_origin(supports_credentials=True)
def handlePanelRequest():
    digest = request.args.get('hexValue')
    collection = database.findCollection(database="comments", collection="sub_comments")
    doc = database.findAllComments(collection, digest)
    return doc


@app.route("/reply-comment", methods=["POST"])
@cross_origin(supports_credentials=True)
def handleReplyComment():
    req = request.data
    req_string = req.decode()
    req_dict = json.loads(req_string)
    parentID = req_dict.get("commentID")
    comment = req_dict.get("comment")
    digest = req_dict.get("hexValue")
    name = req_dict.get("name")
    collection = database.findCollection(database="comments", collection="sub_comments")
    res = database.insertReply(collection, parentID, comment, digest, name)
    return res
