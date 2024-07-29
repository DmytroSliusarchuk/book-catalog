from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, status, Path, HTTPException, Query

from app.database import Reviews
from app.reviews.schemas import ReviewBaseSchema
from app.config import settings

router = APIRouter(prefix="/books/{book_id}/reviews", tags=["reviews"])


@router.get(
    "/",
    description="Get all reviews for a book",
    summary="Get all reviews for a book from the database",
    response_description="List of reviews",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewBaseSchema],
)
async def get_all_reviews(
    book_id: Annotated[str, Path(title="Book ID")],
    page: Annotated[int, Query(ge=1, title="Page number")] = 1,
    limit: Annotated[
        int,
        Query(ge=1, le=500, title="Page size"),
    ] = settings.DEFAULT_PAGE_SIZE,
) -> list[ReviewBaseSchema]:
    """
    Get all reviews for a book from the database
    :param book_id: Book ID
    :param page: Page number
    :param limit: Page size
    :return: List of reviews
    """

    try:
        book_id = ObjectId(book_id)

        reviews = (
            await Reviews.find({"book_id": book_id})
            .sort("_id")
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list(length=None)
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return reviews


@router.get(
    "/{review_id}",
    description="Get a review by id",
    summary="Get a review by id from the database",
    response_description="Review data",
    status_code=status.HTTP_200_OK,
    response_model=ReviewBaseSchema,
)
async def get_review_by_id(
    book_id: Annotated[str, Path(title="Book ID")],
    review_id: Annotated[str, Path(title="Review ID")],
) -> ReviewBaseSchema:
    """
    Get a review by id from the database
    :param book_id: Book ID
    :param review_id: Review ID
    :return: Review data
    """

    try:
        book_id = ObjectId(book_id)
        review_id = ObjectId(review_id)

        review = await Reviews.find_one({"_id": review_id, "book_id": book_id})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


@router.delete(
    "/{review_id}",
    description="Delete a review by id",
    summary="Delete a review by id from the database",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review_by_id(
    book_id: Annotated[str, Path(title="Book ID")],
    review_id: Annotated[str, Path(title="Review ID")],
) -> None:
    """
    Delete a review by id from the database
    :param book_id: Book ID
    :param review_id: Review ID
    """

    try:
        book_id = ObjectId(book_id)
        review_id = ObjectId(review_id)

        result = await Reviews.delete_one({"_id": review_id, "book_id": book_id})
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")


@router.post(
    "/",
    description="Create a review",
    summary="Create a review for a book in the database",
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    book_id: Annotated[str, Path(title="Book ID")], review: ReviewBaseSchema
) -> dict[str, str]:
    """
    Create a review for a book in the database
    :param book_id: Book ID
    :param review: Review data
    :return: Created review ID
    """

    try:
        book_id = ObjectId(book_id)

        review_data = review.dict(exclude_unset=True, by_alias=True)
        review_data["book_id"] = book_id

        if "_id" in review_data:
            review_data["_id"] = ObjectId(review_data["_id"])

        result = await Reviews.insert_one(review_data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not result.inserted_id:
        raise HTTPException(
            status_code=400, detail="Error occurred while creating a review"
        )

    return {"review_id": str(result.inserted_id)}

@router.put(
    "/{review_id}",
    description="Update a review",
    summary="Update a review for a book in the database",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_review(
    book_id: Annotated[str, Path(title="Book ID")],
    review_id: Annotated[str, Path(title="Review ID")],
    review: ReviewBaseSchema,
) -> None:
    """
    Update a review for a book in the database
    :param book_id: Book ID
    :param review_id: Review ID
    :param review: Review data
    """

    try:
        book_id = ObjectId(book_id)
        review_id = ObjectId(review_id)

        review_data = review.dict(exclude_unset=True, by_alias=True)

        if "_id" in review_data:
            del review_data["_id"]
        if "book_id" in review_data:
            del review_data["book_id"]

        result = await Reviews.update_one(
            {"_id": review_id, "book_id": book_id}, {"$set": review_data}
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
