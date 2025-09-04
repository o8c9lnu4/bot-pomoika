import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from .catalog import PAGE_SIZE, paginate
from .config import load_config
from .keyboards import categories_kb, items_kb
from .storage import CatalogStorage


async def main() -> None:
    config = load_config()
    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    storage = CatalogStorage(Path(__file__).resolve().parent.parent / "data" / "catalog.json")
    storage.load()

    @dp.message(CommandStart())
    async def on_start(message: Message) -> None:
        text = (
            "Добро пожаловать! Это каталог.\n"
            "- Введите текст для поиска\n"
            "- Или выберите категорию"
        )
        kb = categories_kb(storage.categories())
        if config.webapp_url:
            open_app = InlineKeyboardButton(text="Открыть Mini App", web_app=WebAppInfo(url=config.webapp_url))
            rows = list(kb.inline_keyboard)
            rows.insert(0, [open_app])
            kb = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.answer(text, reply_markup=kb)

    @dp.message(F.text)
    async def on_search(message: Message) -> None:
        query = (message.text or "").strip()
        results = storage.search(query)
        if not results:
            await message.answer("Ничего не найдено. Попробуйте другой запрос.")
            return
        page = paginate(results, 1, PAGE_SIZE)
        for item in page.items:
            caption = f"<b>{item.title}</b>\nЦена: {item.price:.2f}\n{item.description}"
            if item.photo_url:
                await message.answer_photo(item.photo_url, caption=caption)
            else:
                await message.answer(caption)

    def is_admin(user_id: int) -> bool:
        return user_id in config.admin_ids

    @dp.message(Command("admin"))
    async def admin_help(message: Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Админ-команды:\n"
            "/list — список товаров (id, название, цена)\n"
            "/add <категория> | <название> | <цена> | <описание> | [photo_url]\n"
            "/del <id> — удалить товар\n"
            "/price <id> <новая_цена> — изменить цену\n"
            "/reload — перечитать data/catalog.json"
        )

    @dp.message(Command("list"))
    async def admin_list(message: Message) -> None:
        if not is_admin(message.from_user.id):
            return
        items = storage.all_items()
        if not items:
            await message.answer("Каталог пуст.")
            return
        lines = [
            f"{i.id}. {i.title} — {i.price:.2f} ({i.category})" for i in items
        ]
        await message.answer("\n".join(lines)[:4000])

    @dp.message(Command("add"))
    async def admin_add(message: Message) -> None:
        if not is_admin(message.from_user.id):
            return
        text = (message.text or "").split(" ", 1)
        if len(text) < 2:
            await message.answer("Формат: /add Категория | Название | 123.45 | Описание | [photo_url]")
            return
        payload = text[1]
        parts = [p.strip() for p in payload.split("|")]
        if len(parts) < 4:
            await message.answer("Нужно минимум 4 поля через |: категория, название, цена, описание")
            return
        category, title, price_str, description = parts[:4]
        photo_url = parts[4] if len(parts) >= 5 else None
        try:
            price = float(price_str.replace(",", "."))
        except ValueError:
            await message.answer("Цена должна быть числом")
            return
        item = storage.add_item(title=title, description=description, price=price, category=category, photo_url=photo_url)
        await message.answer(f"Добавлено: {item.id}. {item.title} — {item.price:.2f}")

    @dp.message(Command("del"))
    async def admin_del(message: Message) -> None:
        if not is_admin(message.from_user.id):
            return
        text = (message.text or "").split()
        if len(text) != 2:
            await message.answer("Формат: /del <id>")
            return
        ok = storage.delete_item(text[1])
        await message.answer("Удалено" if ok else "Товар не найден")

    @dp.message(Command("price"))
    async def admin_price(message: Message) -> None:
        if not is_admin(message.from_user.id):
            return
        text = (message.text or "").split()
        if len(text) != 3:
            await message.answer("Формат: /price <id> <цена>")
            return
        item_id, price_str = text[1], text[2]
        try:
            price = float(price_str.replace(",", "."))
        except ValueError:
            await message.answer("Цена должна быть числом")
            return
        ok = storage.update_price(item_id, price)
        await message.answer("Обновлено" if ok else "Товар не найден")

    @dp.message(Command("reload"))
    async def admin_reload(message: Message) -> None:
        if not is_admin(message.from_user.id):
            return
        storage.reload()
        await message.answer("Каталог перечитан из файла.")

    @dp.message(F.web_app_data)
    async def on_webapp_data(message: Message) -> None:
        if not message.web_app_data or not message.web_app_data.data:
            return
        data = message.web_app_data.data
        try:
            import json as _json
            order = _json.loads(data)
        except Exception:
            await message.answer("Не удалось разобрать заказ")
            return
        total = order.get("total", 0)
        items = order.get("items", [])
        lines = ["Новый заказ из Mini App:"]
        for it in items:
            lines.append(f"- {it.get('title')} — {it.get('price')}")
        lines.append(f"Итого: {total}")
        text = "\n".join(lines)
        await message.answer("Спасибо! Заказ отправлен администратору.")
        for admin_id in config.admin_ids:
            try:
                await bot.send_message(chat_id=admin_id, text=text)
            except Exception:
                pass

    @dp.callback_query(F.data.startswith("cat:"))
    async def on_category(call: CallbackQuery) -> None:
        await call.answer()
        category = call.data.split(":", 1)[1]
        items = storage.items_by_category(category)
        page = paginate(items, 1)
        if not items:
            await call.message.edit_text("В категории пока пусто.")
            return
        await render_category(call, category, page.page, page.total_pages, page.items)

    @dp.callback_query(F.data.startswith("page:"))
    async def on_page(call: CallbackQuery) -> None:
        await call.answer()
        _, category, page_str = call.data.split(":", 2)
        page_num = int(page_str)
        items = storage.items_by_category(category)
        page = paginate(items, page_num)
        await render_category(call, category, page.page, page.total_pages, page.items)

    @dp.callback_query(F.data == "back:cats")
    async def on_back(call: CallbackQuery) -> None:
        await call.answer()
        await call.message.edit_text(
            "Выберите категорию:", reply_markup=categories_kb(storage.categories())
        )

    async def render_category(
        call: CallbackQuery,
        category: str,
        page_num: int,
        total_pages: int,
        items,
    ) -> None:
        text_lines = [f"Категория: <b>{category}</b>"]
        for item in items:
            text_lines.append(f"\n<b>{item.title}</b> — {item.price:.2f}\n{item.description}")
        await call.message.edit_text(
            "\n".join(text_lines),
            reply_markup=items_kb(category, page_num, total_pages),
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
