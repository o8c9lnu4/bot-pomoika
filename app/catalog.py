from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .storage import CatalogItem


PAGE_SIZE = 6


@dataclass
class Page:
    items: Sequence[CatalogItem]
    page: int
    total_pages: int


def paginate(items: Sequence[CatalogItem], page: int, page_size: int = PAGE_SIZE) -> Page:
    if page < 1:
        page = 1
    total = len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = min(page, total_pages)
    start = (page - 1) * page_size
    end = start + page_size
    return Page(items=items[start:end], page=page, total_pages=total_pages)
