from flask import Flask, request, jsonify
import boto3
import re
import os
import json
import re
# from aws_utils import textract_client, rekognition_client, s3_client
from PIL import Image
import requests

from dotenv import load_dotenv
load_dotenv()

# define the S3 bucket name + image
bucket_name = 'book-scanner-lehigh'
image_name = 'books6.png'

#--------------------------------------------#
# AWS Rekognition - Detect Labels for Books
#--------------------------------------------#

# create the rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')

# call the rekognition client to detect text in the image
labels_response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': bucket_name,'Name': image_name}}, MaxLabels=50)

# TEST: print detected labels
print("\nDetected labels in the image:")
for label in labels_response['Labels']:
    print(label['Name'], label['Confidence'])

# iterate through the labels to find 'Book' and get bounding boxes
books_collected = []
for label in labels_response['Labels']:
    if label['Name'] == 'Book':         # check if label is 'Book'
        for instance in label['Instances']:
            box = instance['BoundingBox']
            books_collected.append(box)

print(f"Found {len(books_collected)} books in the image")


#--------------------------------------------#
# AWS Textract - Get Text from Book Spines
#--------------------------------------------#
# call the rekognition client to detect text in the image
text_response = rekognition.detect_text(
    Image={'S3Object': {
            'Bucket': bucket_name,
            'Name': image_name
        }
    }
)

# print detected text
print("Detected text in the image:")
for item in text_response['TextDetections']:
    if item['Type'] == 'LINE':
        print(item['DetectedText'])




# app = Flask(__name__)
# s3 = boto3.client('s3')
# rekog = boto3.client('rekognition')
# textract = boto3.client('textract')

# BUCKET = 'booksnap-images'

# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['image']
#     s3.upload_fileobj(file, BUCKET, file.filename)

#     # Step 1: Detect text
#     textract_resp = textract.detect_document_text(
#         Document={'S3Object': {'Bucket': BUCKET, 'Name': file.filename}}
#     )
#     lines = [b['Text'] for b in textract_resp['Blocks'] if b['BlockType'] == 'LINE']

#     # Step 2: Filter potential titles
#     titles = [line for line in lines if 2 <= len(line.split()) <= 6]

#     return jsonify({'titles': titles})
