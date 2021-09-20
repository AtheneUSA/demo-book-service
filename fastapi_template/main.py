import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


def start():
    uvicorn.run("fastapi_template.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
