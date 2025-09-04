from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .storage import CatalogItem, CatalogStorage


class ItemIn(BaseModel):
    title: str
    description: str
    price: float
    category: str
    photo_url: str | None = None


def build_app() -> FastAPI:
    app = FastAPI(title="Pomoika Vape Lab Catalog API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    data_path = Path(__file__).resolve().parent.parent / "data" / "catalog.json"
    storage = CatalogStorage(data_path)
    storage.load()

    @app.get("/api/categories", response_model=List[str])
    def get_categories() -> List[str]:
        return storage.categories()

    @app.get("/api/items", response_model=list[CatalogItem])
    def get_items(category: str | None = None, q: str | None = None):
        if category:
            return storage.items_by_category(category)
        if q:
            return storage.search(q)
        return storage.all_items()

    @app.post("/api/items", response_model=CatalogItem)
    def add_item(item: ItemIn):
        return storage.add_item(
            title=item.title,
            description=item.description,
            price=item.price,
            category=item.category,
            photo_url=item.photo_url,
        )

    @app.delete("/api/items/{item_id}")
    def delete_item(item_id: str):
        if not storage.delete_item(item_id):
            raise HTTPException(status_code=404, detail="Not found")
        return {"ok": True}

    # Serve static Mini App
    static_dir = Path(__file__).resolve().parent.parent / "web"
    static_dir.mkdir(exist_ok=True)
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="web")

    return app


app = build_app()
