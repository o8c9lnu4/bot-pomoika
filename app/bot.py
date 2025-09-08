import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from django.conf import settings
from django.utils import timezone

import django
import os

# Ensure Django is setup when running bot directly (e.g., via asyncio.run)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog.models import Post

from .config import load_config


async def main() -> None:
    config = load_config()
    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def on_start(message: Message) -> None:
        text = (
            "🤖 <b>Привет! Я бот Pomoika Vape Lab</b>\n\n"
            "Я помогу вам с информацией о наших товарах.\n\n"
            "Используйте команды:\n"
            "/help - помощь\n"
            "/info - информация о нас"
        )
        await message.answer(text)

    @dp.message(Command("help"))
    async def on_help(message: Message) -> None:
        text = (
            "📋 <b>Доступные команды:</b>\n\n"
            "/start - начать работу с ботом\n"
            "/help - показать это сообщение\n"
            "/info - информация о Pomoika Vape Lab\n"
            "/contact - контактная информация"
        )
        await message.answer(text)

    @dp.message(Command("info"))
    async def on_info(message: Message) -> None:
        text = (
            "🏪 <b>Pomoika Vape Lab</b>\n\n"
            "Мы специализируемся на качественных вейп-товарах:\n"
            "• Электронные сигареты\n"
            "• Жидкости для вейпа\n"
            "• Аксессуары\n"
            "• Запчасти\n\n"
            "Все товары сертифицированы и имеют гарантию качества."
            f"Сайт: {config.base_url}\n"
        )
        await message.answer(text)

    @dp.message(Command("contact"))
    async def on_contact(message: Message) -> None:
        text = (
            "📞 <b>Контактная информация</b>\n\n"
            "Для заказа и консультаций обращайтесь:\n"
            "• Telegram: @pmkvl_admin\n"
        )
        await message.answer(text)

    @dp.message(Command("posts"))
    async def on_posts(message: Message) -> None:
        posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')[:5]
        if not posts:
            await message.answer("Пока нет опубликованных постов.")
            return
        items = []
        for p in posts:
            url = f"{config.base_url}/post/{p.id}/"
            title = p.title
            items.append(f"• <a href=\"{url}\">{title}</a>")
        text = "\n".join(["📰 <b>Последние посты</b>", *items])
        await message.answer(text, disable_web_page_preview=True)

    @dp.message()
    async def on_any_message(message: Message) -> None:
        text = (
            "Не понимаю эту команду. Используйте /help для просмотра доступных команд."
        )
        await message.answer(text)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
