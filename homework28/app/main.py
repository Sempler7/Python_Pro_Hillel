from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="FastAPI CRUD Demo")

app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/")
async def root() -> dict:
    """Кореневий endpoint для перевірки роботи API"""

    return {"message": "Hello, FastAPI CRUD"}


@app.get("/hello/{name}")
async def say_hello(name: str) -> dict:
    return {"message": f"Hello, {name}!"}