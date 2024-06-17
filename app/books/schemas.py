from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator, PositiveInt, PastDatetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class AuthorBaseSchema(BaseModel):
    first_name: str = Field(title="Author first name")
    last_name: str = Field(title="Author last name")


class AuthorDetailSchema(AuthorBaseSchema):
    birth_date: PastDatetime = Field(title="Author birth date")
    nationality: str = Field(title="Author nationality")


class BookBaseSchema(BaseModel):
    id: PyObjectId | None = Field(
        alias="_id", title="Book ID", exclude_none=True, default=None
    )
    title: str = Field(title="Book title")
    authors: list[AuthorBaseSchema] = Field(title="List of book authors")
    published_date: PastDatetime = Field(title="Book published date")
    language: str = Field(title="Book language")
    genres: list[str] = Field(title="List of book genres")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BookDetailSchema(BookBaseSchema):
    edition: PositiveInt | None = Field(title="Book edition", default=None)
    isbn: str = Field(title="Book ISBN")
    pages: PositiveInt = Field(title="Book pages")
    cover_image: str | None = Field(title="Book cover image", default=None)
    publisher: str = Field(title="Book publisher")
    summary: str | None = Field(title="Book summary", default=None)
