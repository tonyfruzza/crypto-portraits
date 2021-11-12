import os
import requests
import json
from flask import Flask, render_template, request, redirect, send_file, send_from_directory
from s3_functions import list_files, upload_file, show_image
import boto3
import urllib.request

app = Flask(__name__)

LAST_MEME_GEN = ""
BUCKET = os.environ.get('BUCKET_NAME')
SQS_NAME = os.environ.get('SQS_NAME')
# AWS_REGION = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/placement/region').read().decode()
AWS_REGION = 'us-east-1'

@app.route("/")
def home():
    global LAST_MEME_GEN
    return render_template('index.html', last_meme_gen=LAST_MEME_GEN)

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)

@app.route("/mint_nft", methods=['POST'])
def queue_meme():
    global AWS_REGION

    sqs = boto3.resource('sqs', region_name=AWS_REGION)
    queue = sqs.get_queue_by_name(QueueName=SQS_NAME)
    response = queue.send_message(MessageBody=json.dumps(request.form))

    return redirect("/")

@app.route("/pics")
def list():
    contents = show_image(BUCKET)
    return render_template('collection.html', contents=contents)

if __name__ == '__main__':
    app.run(debug=True)
