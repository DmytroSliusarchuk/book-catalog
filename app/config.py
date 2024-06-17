import os

from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.environ.get("MONGODB_URL")

tags_metadata = [
    {"name": "root", "description": "Root endpoint."},
    {"name": "books", "description": "Operations with books."},
    {"name": "reviews", "description": "Operations with reviews."},
]

app_config = {
    "title": "Book Catalog API",
    "description": "API for books and reviews.",
    "version": "0.0.2",
    "openapi_tags": tags_metadata,
}

DEFAULT_PAGE_SIZE = 15
