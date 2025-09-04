from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import json


@dataclass
class CatalogItem:
    id: str
    title: str
    description: str
    price: float
    category: str
    photo_url: Optional[str] = None


class CatalogStorage:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._items: List[CatalogItem] = []
        self._categories: List[str] = []

    def load(self) -> None:
        if not self.file_path.exists():
            self._items = []
            self._categories = []
            return
        data: List[Dict[str, Any]] = json.loads(self.file_path.read_text(encoding="utf-8"))
        self._items = [CatalogItem(**row) for row in data]
        self._categories = sorted({item.category for item in self._items})

    def categories(self) -> List[str]:
        return list(self._categories)

    def items_by_category(self, category: str) -> List[CatalogItem]:
        return [i for i in self._items if i.category == category]

    def search(self, query: str) -> List[CatalogItem]:
        q = query.lower().strip()
        if not q:
            return []
        return [
            i
            for i in self._items
            if q in i.title.lower() or q in i.description.lower()
        ]

    # --- Admin write operations ---
    def save(self) -> None:
        data = [
            {
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "price": i.price,
                "category": i.category,
                "photo_url": i.photo_url,
            }
            for i in self._items
        ]
        self.file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self._categories = sorted({item.category for item in self._items})

    def reload(self) -> None:
        self.load()

    def next_id(self) -> str:
        max_num = 0
        for item in self._items:
            try:
                max_num = max(max_num, int(item.id))
            except ValueError:
                continue
        return str(max_num + 1)

    def add_item(
        self,
        title: str,
        description: str,
        price: float,
        category: str,
        photo_url: Optional[str] = None,
    ) -> CatalogItem:
        new_item = CatalogItem(
            id=self.next_id(),
            title=title,
            description=description,
            price=price,
            category=category,
            photo_url=photo_url,
        )
        self._items.append(new_item)
        self.save()
        return new_item

    def delete_item(self, item_id: str) -> bool:
        before = len(self._items)
        self._items = [i for i in self._items if i.id != item_id]
        changed = len(self._items) != before
        if changed:
            self.save()
        return changed

    def update_price(self, item_id: str, price: float) -> bool:
        for i in self._items:
            if i.id == item_id:
                i.price = price
                self.save()
                return True
        return False

    def all_items(self) -> List[CatalogItem]:
        return list(self._items)
