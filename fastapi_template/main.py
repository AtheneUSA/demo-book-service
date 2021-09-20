from typing import List, Optional
from sqlalchemy.engine import result
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

app = FastAPI()


class AuthorBase(SQLModel):
    name: str
class Author(AuthorBase, table=True):
    __tablename__ = "authors"
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="author")

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

class AuthorReadWithBooks(AuthorBase):
    id: int
    books: List["BookBase"]

class BookBase(SQLModel):
    isbn: int = Field(primary_key=True)
    title: str

class Book(BookBase, table=True):
    __tablename__ = "books"
    author_id: int = Field(foreign_key="authors.id")
    author: Author = Relationship(back_populates="books")

class BookCreate(BookBase):
    author_id: int = Field(foreign_key="authors.id")

class BookRead(BookBase):
    author: AuthorRead

AuthorReadWithBooks.update_forward_refs()

sqlite_file_name = (
    "/Users/e72816/workspace/AtheneUSA/templates/fastapi-template/database.db"
)
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_db_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/authors", response_model=List[AuthorRead])
async def list_authors(session: Session = Depends(get_db_session)):
    authors = session.exec(select(Author)).all()
    return authors


@app.post("/authors", response_model=AuthorRead)
async def create_author(author: AuthorCreate, session: Session = Depends(get_db_session)):
    db_author = Author.from_orm(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@app.get("/authors/{author_id}", response_model=AuthorReadWithBooks)
async def read_author(author_id: int, session: Session = Depends(get_db_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    print(author.books)
    return author


@app.delete("/authors/{author_id}")
async def delete_author(author_id: int, session: Session = Depends(get_db_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}


@app.get("/books", response_model=List[BookRead])
async def list_books(session: Session = Depends(get_db_session)):
    books = session.exec(select(Book)).all()
    return books


@app.post("/books", response_model=BookRead)
async def create_book(book: BookCreate, session: Session = Depends(get_db_session)):
    db_book = Book.from_orm(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.get("/books/{isbn}", response_model=BookRead)
async def read_book(isbn: int, session: Session = Depends(get_db_session)):
    book = session.get(Book, isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{isbn}")
async def delete_book(isbn: int, session: Session = Depends(get_db_session)):
    book = session.get(Book, isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}


def start():
    uvicorn.run("fastapi_template.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
