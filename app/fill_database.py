import random
import asyncio
from datetime import datetime

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorCollection

from database import Books, Reviews


def generate_books_data(quantity: int = 100) -> list[dict]:
    """
    Generate fake data for books.
    :param quantity: Number of books to generate.
    :return: List of dictionaries with fake data.
    """

    fake = Faker()
    books = []
    for _ in range(quantity):
        book = {
            "title": fake.sentence(
                nb_words=random.randint(2, 6), variable_nb_words=True
            ).title()[:-1],
            "edition": random.randint(1, 10),
            "authors": [
                {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "birth_date": datetime.combine(
                        fake.date_of_birth(minimum_age=16, maximum_age=100),
                        datetime.min.time(),
                    ),
                    "nationality": random.choice(
                        [
                            "American",
                            "British",
                            "French",
                            "German",
                            "Spanish",
                            "Chinese",
                            "Japanese",
                            "Ukrainian",
                            "Italian",
                            "Portuguese",
                        ]
                    ),
                }
                for _ in range(random.randint(1, 3))
            ],
            "published_date": datetime.combine(
                fake.date_between(start_date="-80y", end_date="today"),
                datetime.min.time(),
            ),
            "isbn": fake.isbn13(),
            "pages": random.randint(100, 800),
            "cover_image": fake.image_url(),
            "language": random.choice(
                [
                    "English",
                    "Spanish",
                    "French",
                    "German",
                    "Chinese",
                    "Japanese",
                    "Ukrainian",
                    "Italian",
                    "Portuguese",
                ]
            ),
            "publisher": fake.company(),
            "genres": random.sample(
                [
                    "Fiction",
                    "Non-Fiction",
                    "Mystery",
                    "Science Fiction",
                    "Fantasy",
                    "Romance",
                    "Thriller",
                    "Horror",
                    "Biography",
                    "Self-Help",
                    "History",
                    "Poetry",
                ],
                random.randint(1, 5),
            ),
            "summary": fake.paragraph(nb_sentences=5),
        }
        books.append(book)
    return books


def generate_reviews_data(book_ids: list, quantity: int = 1000) -> list[dict]:
    """
    Generate fake data for reviews.
    :param book_ids: List of books ids.
    :param quantity: Number of reviews to generate.
    :return: List of dictionaries with fake data.
    """

    fake = Faker()
    reviews = []
    for _ in range(quantity):
        review = {
            "book_id": random.choice(book_ids),
            "reviewer": {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            },
            "rating": random.randint(1, 10),
            "comment": fake.paragraph(nb_sentences=3),
            "review_date": fake.date_time_this_year(),
        }
        reviews.append(review)
    return reviews


async def load_data_to_database(
    data: list[dict], collection: AsyncIOMotorCollection
) -> None:
    """
    Load data to MongoDB database.
    :param data: List of dictionaries with data to load.
    :param collection: Collection to load data to.
    """
    try:
        result = await collection.insert_many(data)
    except Exception as e:
        print(f"Error occurred while loading data to database: {e}")
        return

    print(f"Data loaded to database. Inserted {len(result.inserted_ids)} documents.")


async def get_all_books_ids() -> list:
    """
    Get all books ids from the database.
    :return: List of books ids.
    """

    books_ids = []
    async for book in Books.find({}, {"_id": 1}):
        books_ids.append(book["_id"])

    return books_ids


async def fill_database(book_quantity: int = 100, review_quantity: int = 10000) -> None:
    """
    Fill database with fake data.
    :param book_quantity: Number of books to generate.
    :param review_quantity: Number of reviews to generate.
    """

    books_data = generate_books_data(quantity=book_quantity)

    await load_data_to_database(books_data, Books)

    books_ids = await get_all_books_ids()

    reviews_data = generate_reviews_data(books_ids, quantity=review_quantity)

    await load_data_to_database(reviews_data, Reviews)

    print("Database filled with fake data.")


if __name__ == "__main__":
    asyncio.run(fill_database())


"""
{
  "title": "Test Book 1",
  "authors": [
    {
      "first_name": "Test Author Name",
      "last_name": "Test Author Last Name",
      "birth_date": "2024-06-13",
      "nationality": "Ukrainian"
    }
  ],
  "published_date": "2024-06-13",
  "language": "Ukrainian",
  "genres": [
    "Science Fiction",
    "History"
  ],
  "edition":1,
  "isbn": "000-0-00-000000-0",
  "pages": 100,
  "cover_image": "https://placekitten.com/692/818",
  "publisher": "Test Company",
  "summary": "Summary"
}
"""
