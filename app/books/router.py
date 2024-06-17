from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Query, Path

from app.database import Books
from app.books.schemas import BookBaseSchema, BookDetailSchema
from app.config import DEFAULT_PAGE_SIZE

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    "/",
    description="Get all books",
    summary="Get all books from the database",
    response_description="List of books",
    status_code=status.HTTP_200_OK,
    response_model=list[BookBaseSchema],
)
async def get_all_books(
    page: Annotated[int, Query(ge=1, title="Page number")] = 1,
    limit: Annotated[
        int,
        Query(ge=1, le=500, title="Page size"),
    ] = DEFAULT_PAGE_SIZE,
) -> list[BookBaseSchema]:
    """
    Get all books from the database
    :return: List of books
    """
    try:
        books = (
            await Books.find(
                {},
                {
                    "title": 1,
                    "authors.first_name": 1,
                    "authors.last_name": 1,
                    "published_date": 1,
                    "language": 1,
                    "genres": 1,
                },
            )
            .sort("_id")
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list(length=None)
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return books


@router.get(
    "/{book_id}",
    description="Get a book by id",
    summary="Get a book from the database by id",
    response_description="Book data",
    status_code=status.HTTP_200_OK,
    response_model=BookDetailSchema,
)
async def get_book_by_id(
    book_id: Annotated[str, Path(title="Book id")],
) -> BookDetailSchema:
    """
    Get a book from the database by id
    :param book_id: Book id
    :return: Book data
    """
    try:
        book_id = ObjectId(book_id)

        book = await Books.find_one({"_id": book_id})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.delete(
    "/{book_id}",
    description="Delete a book by id",
    summary="Delete a book from the database by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book_by_id(book_id: Annotated[str, Path(title="Book id")]) -> None:
    """
    Delete a book from the database by id
    :param book_id: Book id
    """
    try:
        book_id = ObjectId(book_id)

        result = await Books.delete_one({"_id": book_id})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")


@router.post(
    "/",
    description="Create a new book",
    summary="Create a new book in the database",
    status_code=status.HTTP_201_CREATED,
)
async def create_book(book: BookDetailSchema) -> dict[str, str]:
    """
    Create a new book in the database
    :param book: Book data
    """
    try:
        book_dict = book.dict(by_alias=True, exclude_unset=True)
        if "_id" in book_dict:
            book_dict["_id"] = ObjectId(book_dict["_id"])

        result = await Books.insert_one(book_dict)

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not result.inserted_id:
        raise HTTPException(
            status_code=400, detail="Error occurred while creating a book"
        )

    return {"book_id": str(result.inserted_id)}


@router.put(
    "/{book_id}",
    description="Update a book by id",
    summary="Update a book in the database by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_book_by_id(
    book_id: Annotated[str, Path(title="Book id")], book: BookDetailSchema
) -> None:
    """
    Update a book in the database by id
    :param book_id: Book id
    :param book: Book data
    """
    try:
        book_id = ObjectId(book_id)
        book_dict = book.dict(by_alias=True, exclude_unset=True)

        result = await Books.update_one({"_id": book_id}, {"$set": book_dict})

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")


# Will be properly implemented soon
@router.get(
    "/search",
    description="Search books",
    summary="Search books in the database",
    response_description="List of books",
    status_code=status.HTTP_200_OK,
    response_model=list[BookBaseSchema],
)
async def search_books(
    title: Annotated[str, Query(title="Book title")],
) -> list[BookBaseSchema]:
    """
    Search books in the database
    :param title: Book title
    """
    try:
        books = await Books.find(
            {
                "title": 1,
                "authors.first_name": 1,
                "authors.last_name": 1,
                "published_date": 1,
                "language": 1,
                "genres": 1,
            },
        ).to_list(length=None)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return books
