from flask import Flask, request, jsonify
import boto3
import re
import os
import json
import re
from aws_utils import textract_client, rekognition_client, s3_client
from PIL import Image
import requests

from dotenv import load_dotenv
load_dotenv()

# create the rekognition client
rekognition = boto3.client('rekognition', region='us-east-1')

# define the S3 bucket name + image




app = Flask(__name__)
s3 = boto3.client('s3')
rekog = boto3.client('rekognition')
textract = boto3.client('textract')

BUCKET = 'booksnap-images'

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    s3.upload_fileobj(file, BUCKET, file.filename)

    # Step 1: Detect text
    textract_resp = textract.detect_document_text(
        Document={'S3Object': {'Bucket': BUCKET, 'Name': file.filename}}
    )
    lines = [b['Text'] for b in textract_resp['Blocks'] if b['BlockType'] == 'LINE']

    # Step 2: Filter potential titles
    titles = [line for line in lines if 2 <= len(line.split()) <= 6]

    return jsonify({'titles': titles})