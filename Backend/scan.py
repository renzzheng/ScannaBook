import boto3
import json
import re
from PIL import Image
from io import BytesIO
import requests
import base64
import openai
import os

# Load env variables
from dotenv import load_dotenv
load_dotenv()

# AWS clients
rekognition = boto3.client('rekognition', region_name='us-east-1')
s3 = boto3.client('s3')

# API keys
GOOGLE_KEY = os.getenv('GOOGLEBOOKS_API_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")
BUCKET_NAME = 'book-scanner-lehigh'

# -----------------------------
# Detect books using Rekognition
# -----------------------------
def detect_books_from_image(image_bytes):
    labels_response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=100
    )
    books_collected = []
    for label in labels_response['Labels']:
        if label['Name'] == 'Book':
            for instance in label['Instances']:
                books_collected.append(instance['BoundingBox'])
    return books_collected

# -----------------------------
# Crop book spines
# -----------------------------
def crop_books_from_image(image_bytes, books_collected):
    img = Image.open(BytesIO(image_bytes))
    cropped_books = []

    for i, box in enumerate(books_collected):
        img_width, img_height = img.size
        left = int(box['Left'] * img_width)
        top = int(box['Top'] * img_height)
        width = int(box['Width'] * img_width)
        height = int(box['Height'] * img_height)

        cropped_img = img.crop((left, top, left + width, top + height))
        cropped_books.append(cropped_img)

        # Optional: upload cropped book to S3
        buffer = BytesIO()
        cropped_img.save(buffer, 'PNG')
        buffer.seek(0)
        s3.put_object(Bucket=BUCKET_NAME, Key=f'cropped_books/book_{i}.png', Body=buffer, ContentType='image/png')

    return cropped_books

# -----------------------------
# Detect text from cropped books
# -----------------------------
def get_text_from_cropped_books(cropped_books):
    book_texts = {}
    for i in range(len(cropped_books)):
        buffer = BytesIO()
        cropped_books[i].save(buffer, 'PNG')
        buffer.seek(0)

        text_response = rekognition.detect_text(
            Image={'Bytes': buffer.getvalue()}
        )
        lines = [item['DetectedText'] for item in text_response['TextDetections'] if item['Type'] == 'LINE']
        book_texts[f'book_{i}'] = lines
    return book_texts

# -----------------------------
# Clean title
# -----------------------------
def clean_title(book_texts):
    cleaned_titles = {}
    for key, lines in book_texts.items():
        filtered_lines = [line for line in lines if re.search('[A-Za-z0-9]', line)]
        cleaned_titles[key] = " ".join(filtered_lines)
    return cleaned_titles

# -----------------------------
# Query Google Books
# -----------------------------
def query_google_books(title, author=None):
    query = f"intitle:{title}"
    if author:
        query += f"+inauthor:{author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
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

# -----------------------------
# Lambda handler
# -----------------------------
def lambda_handler(event, context):
    # Frontend should send image as base64 in event['image_base64']
    image_data = event['image_base64']
    image_bytes = base64.b64decode(image_data)

    # Detect books
    books_collected = detect_books_from_image(image_bytes)
    cropped_books = crop_books_from_image(image_bytes, books_collected)
    book_texts = get_text_from_cropped_books(cropped_books)
    clean_titles = clean_title(book_texts)

    all_books = []
    for key, title in clean_titles.items():
        if title.strip():
            info = query_google_books(title)
            book_entry = {
                "id": key,
                "title": title,
                "authors": info.get("authors", []) if info else [],
                "rating": info.get("averageRating") if info else None,
                "description": info.get("description") if info else "No description available",
                "thumbnail": info.get("thumbnail") if info else None
            }
            all_books.append(book_entry)

    response = {
        "message": "Bookshelf processed successfully!",
        "books": all_books
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
