import asyncio
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запускает Telegram-бота (aiogram) в контексте Django проекта.'

    def handle(self, *args, **options):
        from app.bot import main as bot_main

        self.stdout.write(self.style.HTTP_INFO('Запуск Telegram-бота...'))
        try:
            asyncio.run(bot_main())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Остановка бота (Ctrl+C)'))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'Ошибка при работе бота: {exc}'))


