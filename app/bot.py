import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from .config import load_config
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
            "🛍️ <b>Добро пожаловать в наш магазин!</b>\n\n"
            "Здесь вы можете посмотреть каталог товаров и оформить заказ.\n\n"
            "Нажмите кнопку ниже, чтобы открыть каталог:"
        )
        
        # Используем тот же URL, что настроен в BotFather
        # Замените на ваш реальный Netlify URL
        webapp_url = config.webapp_url or "https://pomoika-miniapp-frontend.netlify.app/"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Открыть каталог", web_app=WebAppInfo(url=webapp_url))]
        ])
            
        await message.answer(text, reply_markup=kb)

    @dp.message(F.text)
    async def on_text(message: Message) -> None:
        await message.answer(
            "Для просмотра каталога используйте кнопку \"🛒 Открыть каталог\" или команду /start"
        )

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


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
