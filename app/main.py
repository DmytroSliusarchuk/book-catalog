from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.books.router import router as books_router
from app.config import app_config

app = FastAPI(**app_config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
