# Деплой Telegram Bot + Mini App

## 1. Backend API (Railway)

1) Зайдите на [railway.app](https://railway.app) и войдите через GitHub
2) Создайте новый проект "Deploy from GitHub repo"
3) Выберите ваш репозиторий
4) Railway автоматически определит Python и установит зависимости
5) В настройках проекта добавьте переменные окружения:
   ```
   BOT_TOKEN=ваш_токен_от_BotFather
   ADMIN_IDS=ваш_telegram_id
   ```
6) Получите URL вашего приложения (например: `https://pomoika-api-production.up.railway.app`)

## 2. Frontend Mini App (Netlify)

1) Зайдите на [netlify.com](https://netlify.com) и войдите через GitHub
2) "New site from Git" → выберите ваш репозиторий
3) Настройки:
   - **Base directory**: пустой
   - **Publish directory**: `web`
   - **Build command**: пустой
4) После деплоя получите URL (например: `https://pomoika-miniapp.netlify.app`)

## 3. Обновите конфиги

1) В `web/config.js` замените:
   ```js
   API_BASE: 'https://ВАШ-RAILWAY-ДОМЕН.up.railway.app'
   ```

2) В `.env` (для локального бота):
   ```env
   BOT_TOKEN=ваш_токен
   ADMIN_IDS=ваш_id
   WEBAPP_URL=https://pomoika-miniapp.netlify.app/
   ```

## 4. Настройте бота

1) В [@BotFather](https://t.me/BotFather):
   - `/setmenubutton`
   - Выберите вашего бота
   - **Button text**: `Каталог`
   - **Web App URL**: `https://pomoika-miniapp.netlify.app/`

2) Запустите бота локально:
   ```bash
   .\.venv\Scripts\python -m app.bot
   ```

## 5. Проверка

- Откройте бота в Telegram → /start → "Открыть Mini App"
- Mini App должен загрузить каталог и позволить добавлять в корзину
- При оформлении заказа → уведомление админам

## Структура проекта

```
├── app/           # Python код (бот + API)
├── web/           # Mini App (HTML/CSS/JS)
├── data/          # catalog.json
├── requirements.txt
├── railway.json   # Railway конфиг
├── Procfile       # Heroku/Railway
└── runtime.txt    # Python версия
```
