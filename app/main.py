from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.books.router import router as books_router
from app.reviews.router import router as reviews_router
from app.config import app_configs, settings

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        {"message": exc.detail, "status_code": exc.status_code},
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        {"message": exc.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.get(
    "/",
    tags=["root"],
    description="Root endpoint.",
    summary="Root endpoint to check if the API is running.",
    status_code=status.HTTP_200_OK,
)
async def root() -> dict[str, str]:
    return {"message": "Book Catalog API is running."}


app.include_router(books_router)
app.include_router(reviews_router)
