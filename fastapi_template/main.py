from typing import List, Optional
from sqlalchemy.engine import result
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


class Author(SQLModel, table=True):
    __tablename__ = "authors"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Book(SQLModel, table=True):
    __tablename__ = "books"
    isbn: int = Field(primary_key=True)
    title: str
    author_id: int


sqlite_file_name = "/Users/e72816/workspace/AtheneUSA/templates/fastapi-template/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/authors", response_model=List[Author])
async def list_authors():
    with Session(engine) as session:
        authors = session.exec(select(Author)).all()
        return authors


@app.post("/authors", response_model=Author)
async def create_author(author: Author):
    with Session(engine) as session:
        session.add(author)
        session.commit()
        session.refresh(author)
        return author


@app.get("/authors/{author_id}", response_model=Author)
async def read_author(author_id: int):
    with Session(engine) as session:
        statement = select(Author).where(Author.id == author_id)
        result = session.exec(statement).one()
        return result


@app.get("/books", response_model=List[Book])
async def list_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        return books


@app.post("/books", response_model=Book)
async def create_book(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book


@app.get("/books/{isbn}", response_model=Book)
async def read_book(isbn: int):
    with Session(engine) as session:
        statement = select(Book).where(Book.isbn == isbn)
        result = session.exec(statement).one()
        return result


def start():
    uvicorn.run("fastapi_template.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
