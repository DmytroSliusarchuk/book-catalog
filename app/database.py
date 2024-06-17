import motor.motor_asyncio

from app.config import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client["book-catalog"]

Books = database["books"]

Reviews = database["reviews"]
