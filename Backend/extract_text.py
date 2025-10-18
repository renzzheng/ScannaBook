from flask import Flask, request, jsonify
import boto3
import re
import os
import json
import re
# from aws_utils import textract_client, rekognition_client, s3_client
from PIL import Image
from io import BytesIO
import requests

from dotenv import load_dotenv
load_dotenv()

# defininitions
s3 = boto3.client('s3')
bucket_name = 'book-scanner-lehigh'
image_name = 'books6.png'

textract = boto3.client('textract', region_name='us-east-1')

#--------------------------------------------#
# AWS Rekognition - Detect Labels for Books
#--------------------------------------------#

# create the rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')

# call the rekognition client to detect text in the image
labels_response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': bucket_name,'Name': image_name}}, MaxLabels=100)

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
# PILLOW - Crop Book Spines from Image
#--------------------------------------------#

# TEMP: download S3 bookself into memory
bookshelf = s3.get_object(Bucket=bucket_name, Key=image_name)
img = Image.open(BytesIO(bookshelf['Body'].read())) # full bookshelf image in memory rn

# crop each book spine using bounding boxes from Rekognition
cropped_books = []

# iterate through bounding boxes and crop the image
for i, box in enumerate(books_collected):
    img_width, img_height = img.size
    left = int(box['Left'] * img_width)
    top = int(box['Top'] * img_height)
    width = int(box['Width'] * img_width)
    height = int(box['Height'] * img_height)
    
    # crop the book spine
    cropped_img = img.crop((left, top, left + width, top + height))
    cropped_books.append(cropped_img)
    
    # TEMP: save cropped images locally for testing
    cropped_img.save(f'cropped_book_{i}.png')



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
