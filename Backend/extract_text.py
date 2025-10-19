# from flask import Flask, request, jsonify
import boto3
import re
import os
import json
import re
from PIL import Image, ImageDraw
from io import BytesIO
import requests

from dotenv import load_dotenv
load_dotenv()

# defininitions
s3 = boto3.client('s3')
bucket_name = 'book-scanner-lehigh'
image_name = 'bookshelves/books7.png'

# create the rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')

# creates bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

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

    # print(f"Found {len(books_collected)} books in the image")
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
        # print(f"Uploaded {Key} to S3 Bucket")
    
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

        # print(f"\nText for book {i}: ")
        detected_texts = []
        for item in text_response['TextDetections']:
            if item['Type'] == 'LINE':
                detected_texts.append(item['DetectedText'])
                print(item['DetectedText'])
        book_texts[book_key] = detected_texts
    print(f"TEST: {book_texts}")
    return book_texts

book_texts = get_text_from_books(cropped_books)


#--------------------------------------------#
# Clean and Prepare Titles for Google Books API
#--------------------------------------------#
def clean_title(book_texts):
    # basic cleaning: remove special characters, extra spaces
    cleaned_titles = {}
    for book_key, texts in book_texts.items():
        filtered_lines = [line for line in texts if re.search('[A-Za-z0-9]', line)]
        query_title = " ".join(filtered_lines)
        cleaned_titles[book_key] = query_title

    # print result
    for book_key, title in cleaned_titles.items():
        print(f"{book_key}: {title}")

    return cleaned_titles
clean_titles = clean_title(book_texts)


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


# list to hold book infos
book_infos = {}

for book_key, title in clean_titles.items():
    if title.strip():  # skip empty titles
        info = query_google_books(title)
        book_infos[book_key] = info
        print(f"\nBook: {book_key}")
        print(f"Query Title: {title}")
        if info:
            print("Google Books Result:")
            print(f"Title: {info['title']}")
            print(f"Authors: {info['authors']}")
            print(f"Rating: {info.get('averageRating')}")
            print(f"Description: {info.get('description')}")
        else:
            print("No results found.")

#for book_key, texts in book_texts.items():
#    if texts:
#        title_query = texts[0]  # assume first detected line is the title
#        book_info = query_google_books(title_query)
#        book_infos.append((book_key, book_info))

#for book_key, info in book_infos:
#    print(f"\nBook Key: {book_key}")
#    print(f"Book Info: {info}")
#



#--------------------------------------------#
# Lambda Handler for Iniital Image Upload
#--------------------------------------------#
def lambda_handler(event, context):
    # extract image info from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    image_key = event['Records'][0]['s3']['object']['key']
    
    # detect books in the image
    books_collected = detect_books(image_key)
    
    # crop book spines
    cropped_books = crop_books(books_collected)
    
    # get text from cropped book spines
    book_texts = get_text_from_books(cropped_books)
    
    # prepare titles and query Google Books API
    book_infos = {}
    for book_key, texts in book_texts.items():
        if texts:
            title = texts[0]  # assume first detected line is the title
            clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)  # basic cleaning
            book_info = query_google_books(clean_title)
            book_infos[book_key] = book_info
    
    return {
        'statusCode': 200,
        'body': json.dumps(book_infos)
    }
