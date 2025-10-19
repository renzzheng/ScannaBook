import boto3
import re
import os
import json
import re
from PIL import Image, ImageDraw
from io import BytesIO
import requests
import openai

from dotenv import load_dotenv
load_dotenv()


# defininitions
s3 = boto3.client('s3')
bucket_name = 'book-scanner-lehigh'
image_name = 'bookshelves/books9.png'

# create the rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')
# creates bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

GOOGLE_KEY = os.getenv('GOOGLEBOOKS_API_KEY')
AWS_BEARER_TOKEN_BEDROCK = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

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
    # print(f"TEST: {book_texts}")
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
# AWS Bedrock - Sort Book Text
#--------------------------------------------#
# def clean_with_bedrock(clean_titles):
#     bedrock_cleaned = {}

#     for book_key, title_text in clean_titles.items():
#         prompt = f"""
#         Clean the following book title text by removing gibberish.
#         Extract the book's correct title and author.
#         Return ONLY a JSON object with 'title' and 'author'.

#         Example:
#         Input: 'ROWLING YEAR 3 AND THE PRISONER OF AZKABAN HARRY POTTER S'
#         Output: {{ "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling" }}

#         Now do the same for this input: "{title_text}"
#         """

#         # call Bedrock GPT-OSS 20B model
#         response = bedrock.invoke_model(
#             modelId="gpt-3.3-mini",
#             body=json.dumps({
#                 "text": {"prompt": prompt},   # <-- wrap prompt inside an object
#                 "max_tokens": 150
#             }),
#             contentType="application/json",
#             accept="application/json"
#         )


#         # parse response
#         result = json.loads(response["body"].read())
#         output_text = result.get("text", "").strip()

#         try:
#             # attempt to parse JSON returned by the model
#             bedrock_cleaned[book_key] = json.loads(output_text)
#         except json.JSONDecodeError:
#             # fallback if model output is not valid JSON
#             bedrock_cleaned[book_key] = {"title": None, "author": None}

#     return bedrock_cleaned

# clean_bedrock = clean_with_bedrock(clean_titles)


#--------------------------------------------#
# Sort Book Text using OPENAI
#--------------------------------------------#
def clean_with_openai(clean_titles):
    cleaned = {}

    for book_key, title_text in clean_titles.items():
        prompt = f"""
        Clean the following book title text by removing gibberish.
        Extract the book's correct title and author.
        Return ONLY a JSON object with 'title' and 'author'.

        Example:
        Input: 'ROWLING YEAR 3 AND THE PRISONER OF AZKABAN HARRY POTTER S'
        Output: {{ "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling" }}

        Now do the same for this input: "{title_text}"
        """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )

        output_text = response.choices[0].message.content.strip()

        try:
            cleaned[book_key] = json.loads(output_text)
        except json.JSONDecodeError:
            cleaned[book_key] = {"title": None, "author": None}

    return cleaned

cleaned_with_openai = clean_with_openai(clean_titles)


#--------------------------------------------#
# Google Books API - Search for Book Info
#--------------------------------------------#
def query_google_books(title: str, author: str = None):
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

#--------------------------------------------#
# Main Processing Loop (Cleaning + Querying Books)
#--------------------------------------------#
# list to hold book info
book_infos = {}

for book_key, raw_title in clean_titles.items():
    if raw_title.strip():
        # pass a dict with one book
        cleaned = clean_with_bedrock({book_key: raw_title})
        title = cleaned[book_key]["title"]
        author = cleaned[book_key]["author"]

        info = query_google_books(title, author)
        book_infos[book_key] = info

        print(f"\nBook: {book_key}")
        print(f"Query Title: {title}")
        print(f"Author: {author}")
        if info:
            print("Google Books Result:")
            print(f"Title: {info['title']}")
            print(f"Authors: {info['authors']}")
            print(f"Rating: {info.get('averageRating')}")
            print(f"Description: {info.get('description')}")
            print(f"Thumbnail: {info.get('thumbnail')}")
        else:
            print("No results found.")




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
