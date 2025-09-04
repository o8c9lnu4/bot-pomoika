Телеграм бот-каталог (Python, Aiogram 3)

Возможности:
- Просмотр категорий
- Пагинация списка товаров
- Поиск по названию/описанию

Структура:
- `app/bot.py` — точка входа бота
- `app/config.py` — загрузка конфигурации из `.env`
- `app/storage.py` — чтение каталога из `data/catalog.json`
- `app/catalog.py` — пагинация
- `app/keyboards.py` — инлайн-клавиатуры
- `data/catalog.json` — пример данных

Установка (Windows PowerShell):
1) Перейдите в папку проекта:
```
cd "C:\Users\Admin\Desktop\pomoika vape lab"
```
2) Создайте виртуальное окружение и установите зависимости:
```
py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```
3) Создайте файл `.env` рядом с `requirements.txt` со своим токеном бота:
```
BOT_TOKEN=123456:ABC-DEF-your-token
ADMIN_IDS=
```

Запуск:
```
.\.venv\Scripts\python -m app.bot
```

Mini App (веб-приложение):
- Запуск API/веб-сервера:
```
.\.venv\Scripts\python -m uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```
- Откройте `http://127.0.0.1:8000/` — это Mini App (темная фиолетово-чёрная тема), данные берутся из `data/catalog.json`.
- Чтобы показать кнопку Mini App в боте, добавьте в `.env`:
```
WEBAPP_URL=http://127.0.0.1:8000/
```
- Перезапустите бота и используйте `/start` — появится кнопка "Открыть Mini App".

Публикация Mini App:
- **Netlify**: Base directory пустой, Publish directory: `web`, Build command: пустой
- **Backend API**: деплой FastAPI на Railway/Render/VPS, получите HTTPS URL
- В `web/config.js` укажите: `API_BASE: 'https://ваш-backend-домен'`
- В `@BotFather` → Menu Button → Web App URL: `https://ваш-netlify-домен.netlify.app/`
- В `.env`: `WEBAPP_URL=https://ваш-netlify-домен.netlify.app/`

Где взять токен:
- В `@BotFather` создайте бота и получите `BOT_TOKEN`.

Как изменить каталог:
- Отредактируйте `data/catalog.json` (поля: `id`, `title`, `description`, `price`, `category`, `photo_url`).

Примечания:
- Aiogram v3 использует `Dispatcher().start_polling(...)`.
- Поиск: отправьте любое сообщение с текстом — бот покажет найденные позиции.

Админка:
- В `.env` укажите `ADMIN_IDS` через запятую. Только эти пользователи могут использовать команды ниже.
- Команды:
  - `/admin` — помощь по админ-командам
  - `/list` — список товаров (id, название, цена, категория)
  - `/add <категория> | <название> | <цена> | <описание> | [photo_url]` — добавить товар
  - `/del <id>` — удалить товар
  - `/price <id> <новая_цена>` — изменить цену
  - `/reload` — перечитать файл `data/catalog.json`

