"""FastAPI application with automated review setup."""

from fastapi import FastAPI

app = FastAPI(title="FastAPI Project")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> dict[str, int]:
    return {"item_id": item_id}
