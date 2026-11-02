"""FastAPI application with automated review setup."""

from fastapi import FastAPI

app = FastAPI(title="FastAPI Project")


@app.get("/health")  # type: ignore[untyped-decorator]
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items/{item_id}")  # type: ignore[untyped-decorator]
def read_item(item_id: int) -> dict[str, int]:
    return {"item_id": item_id}
