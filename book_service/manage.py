import random
from faker import Faker
import requests
import typer

from book_service.main import AuthorCreate, AuthorRead, BookCreate, BookRead

host = 'http://localhost:8000'

app = typer.Typer()
fake = Faker()
random.seed()

def _make_author() -> AuthorCreate:
    return AuthorCreate(
        name=fake.name()
    )

def _make_book(author_id: int) -> BookCreate:
    book = BookCreate(
        isbn=int(fake.isbn13(separator='')),
        title=fake.sentence(nb_words=4),
        author_id=author_id,
    )
    return book

def _post_author(author: AuthorCreate) -> AuthorRead:
    post_data = author.json()
    r = requests.post(f"{host}/authors", data=post_data)
    r.raise_for_status()
    data = r.json()
    return AuthorRead(**data)

def _post_book(book: BookCreate) -> BookRead:
    post_data = book.json()
    r = requests.post(f"{host}/books", data=post_data)
    r.raise_for_status()
    data = r.json()
    return BookRead(**data)

@app.command()
def generate_books(n: int = 1):
    author = False
    for _ in range(n):
        if not author or bool(random.getrandbits(1)):
            author = _make_author()
            typer.echo(f"Making new author {author.name}")
            data = _post_author(author)
            author_id = data.id
        book = _make_book(author_id)
        data = _post_book(book)
        typer.echo(f"{book.title} by {author.name}")

@app.command()
def generate_authors(n: int = 1):
    for _ in range(n):
        author = _make_author()
        data = _post_author(author)
        typer.echo(data)

if __name__ == "__main__":
    app()
