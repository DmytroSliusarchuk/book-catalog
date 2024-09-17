from pydantic import Field, BaseModel, PastDatetime

from app.books.schemas import PyObjectId


class ReviewerBaseSchema(BaseModel):
    first_name: str = Field(title="Reviewer first name")
    last_name: str = Field(title="Reviewer last name")


class ReviewBaseSchema(BaseModel):
    id: PyObjectId | None = Field(
        alias="_id", title="Review ID", exclude_none=True, default=None
    )
    book_id: PyObjectId = Field(title="Book ID")
    rating: int = Field(title="Review rating", ge=1, le=10)
    comment: str = Field(title="Review comment")
    reviewer: ReviewerBaseSchema = Field(title="Reviewer data")
    review_date: PastDatetime = Field(title="Review date")
