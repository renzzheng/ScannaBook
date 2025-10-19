from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import re
import os
import json
import re
from PIL import Image
from io import BytesIO
import requests
import openai
import base64
import uuid
from google import genai

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# remove proxy environment variables that might interfere with OpenAI client
if "http_proxy" in os.environ:
    del os.environ["http_proxy"]
if "https_proxy" in os.environ:
    del os.environ["https_proxy"]

# defininitions
s3 = boto3.client("s3")
bucket_name = "book-scanner-lehigh"
image_name = "bookshelves/books9.png"

# create the rekognition client
rekognition = boto3.client("rekognition", region_name="us-east-1")
# creates bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# API keys
GOOGLE_KEY = os.getenv("GOOGLEBOOKS_API_KEY")
AWS_BEARER_TOKEN_BEDROCK = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
openai.api_key = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


# --------------------------------------------#
# AWS Rekognition - Detect Labels for Books
# --------------------------------------------#
def detect_books(bucket_name, image_name):
    # call the rekognition client to detect text in the image
    labels_response = rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}}, MaxLabels=100
    )

    # iterate through the labels to find 'Book' and get bounding boxes
    books_collected = []
    for label in labels_response["Labels"]:
        if label["Name"] == "Book":  # check if label is 'Book'
            for instance in label["Instances"]:
                box = instance["BoundingBox"]
                books_collected.append(box)

    # print(f"Found {len(books_collected)} books in the image")
    return books_collected


# --------------------------------------------#
# PILLOW - Crop Book Spines from Image
# --------------------------------------------#
def crop_books(bucket_name, image_name, books_collected):
    # TEMP: download S3 bookself into memory
    bookshelf = s3.get_object(Bucket=bucket_name, Key=image_name)
    img = Image.open(
        BytesIO(bookshelf["Body"].read())
    )  # full bookshelf image in memory rn

    # crop each book spine using bounding boxes from Rekognition
    cropped_books = []

    # iterate through bounding boxes and crop the image
    for i, box in enumerate(books_collected):
        img_width, img_height = img.size
        left = int(box["Left"] * img_width)
        top = int(box["Top"] * img_height)
        width = int(box["Width"] * img_width)
        height = int(box["Height"] * img_height)

        # crop the book spine
        cropped_img = img.crop((left, top, left + width, top + height))
        cropped_books.append(cropped_img)

        # # TEMP: save cropped images locally for testing
        # cropped_img.save(f'cropped_book_{i}.png')

    # upload cropped book spines back to S3
    for i, cropped in enumerate(cropped_books):
        buffer = BytesIO()
        cropped.save(buffer, "PNG")  # better for text clarity
        buffer.seek(0)

        # store into S3
        Key = f"cropped_books/book_{i}.png"  # goes into s3://book-scanner-lehigh/cropped_books/
        s3.put_object(
            Bucket=bucket_name,
            Key=f"cropped_books/book_{i}.png",
            Body=buffer,
            ContentType="image/png",
        )
        # print(f"Uploaded {Key} to S3 Bucket")

    return cropped_books


# --------------------------------------------#
# AWS Rekognition - Get Text from Individual Book Spines
# --------------------------------------------#
def get_text_from_books(bucket_name, cropped_books):
    book_texts = {}
    for i in range(len(cropped_books)):
        book_key = f"cropped_books/book_{i}.png"
        text_response = rekognition.detect_text(
            Image={"S3Object": {"Bucket": bucket_name, "Name": book_key}}
        )

        # print(f"\nText for book {i}: ")
        detected_texts = []
        for item in text_response["TextDetections"]:
            if item["Type"] == "LINE":
                detected_texts.append(item["DetectedText"])
                print(item["DetectedText"])
        book_texts[book_key] = detected_texts
    # print(f"TEST: {book_texts}")
    return book_texts


# --------------------------------------------#
# Clean and Prepare Titles for Google Books API
# --------------------------------------------#
def clean_title(book_texts):
    # basic cleaning: remove special characters, extra spaces
    cleaned_titles = {}
    for book_key, texts in book_texts.items():
        filtered_lines = [line for line in texts if re.search("[A-Za-z0-9]", line)]
        query_title = " ".join(filtered_lines)
        cleaned_titles[book_key] = query_title

    # print result
    for book_key, title in cleaned_titles.items():
        print(f"{book_key}: {title}")

    return cleaned_titles


# --------------------------------------------#
# Sort Book Text using GEMINI AI
# --------------------------------------------#
def clean_with_gemini(clean_titles):
    cleaned = {}

    # create client with API key
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    client = genai.Client(api_key=GEMINI_API_KEY)

    for book_key, title_text in clean_titles.items():
        prompt = f"""
        You are a book title cleaner.

        Given a noisy OCR text of a book cover, your task is to:
        1. Identify the real book title and author.
        2. Output only valid JSON with keys "title" and "author".
        3. If the author is J.K. Rowling or another famous author, include the correct spelling.
        4. Do not echo my instructions, just output JSON.

        Example:
        Input: ROWLING YEAR 3 AND THE PRISONER OF AZKABAN HARRY POTTER S
        Output:
        {{ "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling" }}

        Now clean this text: "{title_text}"
        """

        sort_response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        output_text = sort_response.candidates[0].content.parts[0].text.strip()

        # remove code fences if Gemini includes them
        output_text = re.sub(
            r"^```(?:json)?|```$", "", output_text.strip(), flags=re.MULTILINE
        ).strip()
        # Print the raw output from Gemini
        print(f"\n--- Gemini raw output for {book_key} ---")
        print(output_text)
        print("--- end raw output ---\n")

        # TODO
        try:
            book_info = json.loads(output_text)
            cleaned[book_key] = {
                "title": book_info.get("title", "").strip(),
                "author": book_info.get("author", "").strip(),
            }
        except json.JSONDecodeError:
            print(f"Error decoding JSON for book {book_key}. Output was: {output_text}")
            cleaned[book_key] = {"title": title_text, "author": ""}
    return cleaned


# --------------------------------------------#
# Google Books API - Search for Book Info
# --------------------------------------------#
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
                "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
            }
    return None


# -----------------------------
# Flask endpoint for file upload
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]

    # generate unique S3 key
    key = f"bookshelves/{uuid.uuid4()}_{file.filename}"

    # upload original image to S3
    s3.upload_fileobj(file, bucket_name, key)

    # process the uploaded image
    books_collected = detect_books(bucket_name, key)
    cropped_books = crop_books(bucket_name, key, books_collected)
    book_texts = get_text_from_books(bucket_name, cropped_books)
    clean_titles_dict = clean_title(book_texts)
    cleaned = clean_with_gemini(clean_titles_dict)

    all_books = []
    for (
        k,
        book_data,
    ) in cleaned.items():  # book_data is a dict with 'title' and 'author'
        print("DEBUG:", k, book_data)  # <--- add this
        title = book_data.get("title") or ""
        author = book_data.get("author") or None

        if title.strip():  # now safe
            info = query_google_books(title, author)
            all_books.append(
                {
                    "id": k,
                    "title": title,
                    "author": author,
                    "authors": info.get("authors") if info else [],
                    "rating": info.get("averageRating") if info else None,
                    "description": info.get("description")
                    if info
                    else "No description available",
                    "thumbnail": info.get("thumbnail") if info else None,
                }
            )

    # pretty-print like for pedro
    response = {"message": "Bookshelf processed successfully!", "books": all_books}

    # save to JSON file locally
    with open("bookshelf_response.json", "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)

    return jsonify(response), 200


if __name__ == "__main__":
    # import json
    # with open("event.json") as f:
    #     event = json.load(f)
    # print(lambda_handler(event, None))

    app.run(debug=True)
