from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def categories_kb(categories: list[str]) -> InlineKeyboardMarkup:
    rows = []
    for cat in categories:
        rows.append([InlineKeyboardButton(text=cat, callback_data=f"cat:{cat}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def items_kb(category: str, page: int, total_pages: int) -> InlineKeyboardMarkup:
    buttons = []
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"page:{category}:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"page:{category}:{page+1}"))
    buttons.append(nav)
    buttons.append([InlineKeyboardButton(text="⬅️ Категории", callback_data="back:cats")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
