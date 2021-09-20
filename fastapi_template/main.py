from typing import List, Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Author(BaseModel):
    id: int
    name: str


class Book(BaseModel):
    isbn: int
    title: str
    author_id: int


AUTHORS = {
    1: Author(id=1, name="John Doe"),
}

BOOKS = {
    123456789012: Book(isbn=123456789012, title="Foo Bar", author_id=1),
}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/authors", response_model=List[Author])
async def list_authors():
    return list(AUTHORS.values())


@app.post("/authors", response_model=Author)
async def create_author(author: Author):
    AUTHORS[author.id] = author
    return author


@app.get("/authors/{author_id}", response_model=Author)
async def read_author(author_id: int):
    return list(AUTHORS[author_id])


@app.get("/books", response_model=List[Book])
async def list_books():
    return list(BOOKS.values())


@app.post("/books", response_model=Book)
async def create_book(book: Book):
    BOOKS[book.isbn] = book
    return book


@app.get("/books/{isbn}", response_model=Book)
async def read_book(isbn: int):
    return BOOKS[isbn]


def start():
    uvicorn.run("fastapi_template.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
