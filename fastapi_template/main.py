from typing import List, Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Author(BaseModel):
    id: int
    name: str


AUTHORS = {1: Author(id=1, name="John Doe")}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/authors", response_model=List[Author])
async def list_authors():
    return AUTHORS


@app.get("/authors/{author_id}", response_model=Author)
async def read_author(author_id: int):
    return AUTHORS[author_id]


@app.post("/authors", response_model=Author)
async def create_author(author: Author):
    AUTHORS[author.id] = author
    return author


def start():
    uvicorn.run("fastapi_template.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
