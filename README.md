# Pomoika Vape Lab Bot

Простой Telegram бот для Pomoika Vape Lab.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` с токеном бота:
```env
BOT_TOKEN=ваш_токен_от_BotFather
```

3. Запустите бота:
```bash
python -m app.bot
```

## Команды бота

- `/start` - начать работу с ботом
- `/help` - показать справку
- `/info` - информация о Pomoika Vape Lab
- `/contact` - контактная информация

## Структура проекта

```
├── app/
│   ├── __init__.py
│   ├── bot.py          # Основной код бота
│   └── config.py       # Конфигурация
├── requirements.txt    # Зависимости
└── README.md          # Этот файл
```