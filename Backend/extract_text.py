from flask import Flask, request, jsonify
import boto3
import re
import os
import json
import re
# from aws_utils import textract_client, rekognition_client, s3_client
from PIL import Image, ImageDraw
from io import BytesIO
import requests

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# defininitions
s3 = boto3.client('s3')
bucket_name = 'book-scanner-lehigh'
image_name = 'bookshelves/books7.png'

# create the rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')

#--------------------------------------------#
# AWS Rekognition - Detect Labels for Books
#--------------------------------------------#
def detect_books(image_name):
    # call the rekognition client to detect text in the image
    labels_response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket_name,'Name': image_name}}, MaxLabels=100)

    # iterate through the labels to find 'Book' and get bounding boxes
    books_collected = []
    for label in labels_response['Labels']:
        if label['Name'] == 'Book':         # check if label is 'Book'
            for instance in label['Instances']:
                box = instance['BoundingBox']
                books_collected.append(box)

    print(f"Found {len(books_collected)} books in the image")
    return books_collected

books_collected = detect_books(image_name)

#--------------------------------------------#
# PILLOW - Crop Book Spines from Image
#--------------------------------------------#
def crop_books(books_collected):
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
        
        # # TEMP: save cropped images locally for testing
        # cropped_img.save(f'cropped_book_{i}.png')

    # upload cropped book spines back to S3
    for i, cropped in enumerate(cropped_books):
        buffer = BytesIO()
        cropped.save(buffer, 'PNG') # better for text clarity
        buffer.seek(0)
        
        # store into S3
        Key = f'cropped_books/book_{i}.png'  # goes into s3://book-scanner-lehigh/cropped_books/
        s3.put_object(Bucket=bucket_name, Key = f'cropped_books/book_{i}.png', Body=buffer, ContentType='image/png')
        print(f"Uploaded {Key} to S3 Bucket")
    
    return cropped_books

cropped_books = crop_books(books_collected)


#--------------------------------------------#
# AWS Rekognition - Get Text from Individual Book Spines
#--------------------------------------------#

def get_text_from_books(cropped_books):
    book_texts = {}
    for i in range(len(cropped_books)):
        book_key = f'cropped_books/book_{i}.png'
        text_response = rekognition.detect_text(
        Image={'S3Object': {'Bucket': bucket_name,'Name': book_key}}
        )

        print(f"\nText for book {i}: ")
        detected_texts = []
        for item in text_response['TextDetections']:
            if item['Type'] == 'LINE':
                detected_texts.append(item['DetectedText'])
                print(item['DetectedText'])
        book_texts[book_key] = detected_texts
    return book_texts

book_texts = get_text_from_books(cropped_books)


#--------------------------------------------#
# Clean and Prepare Titles for Google Books API
#--------------------------------------------#




#--------------------------------------------#
# Google Books API - Search for Book Info
#--------------------------------------------#
def query_google_books(title: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if "items" in data:
            info = data["items"][0]["volumeInfo"]
            return {
                "title": info.get("title"),
                "authors": info.get("authors"),
                "averageRating": info.get("averageRating"),
                "ratingsCount": info.get("ratingsCount"),
                "description": info.get("description"),
                "thumbnail": info.get("imageLinks", {}).get("thumbnail")
            }
    return None




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
