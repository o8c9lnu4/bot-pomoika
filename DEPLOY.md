# Деплой Telegram Bot + Mini App + Django Admin

## 1. Backend API + Django Admin (Render)

1) Зайдите на [render.com](https://render.com) и войдите через GitHub
2) Нажмите "New +" → "Web Service"
3) Подключите ваш GitHub репозиторий
4) Настройки:
   - **Name**: `pomoika-api`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     cd admin && python manage.py migrate
     cd admin && python manage.py collectstatic --noinput
     ```
   - **Start Command**: `cd admin && python manage.py runserver 0.0.0.0:$PORT`
5) В разделе "Environment Variables" добавьте:
   ```
   BOT_TOKEN=ваш_токен_от_BotFather
   ADMIN_IDS=ваш_telegram_id
   DJANGO_SECRET_KEY=сгенерируйте_секретный_ключ
   DJANGO_DEBUG=False
   ```
6) Нажмите "Create Web Service"
7) Получите URL вашего приложения (например: `https://pomoika-api.onrender.com`)
8) **Django Admin будет доступен по адресу**: `https://pomoika-api.onrender.com/admin/`

## 2. Frontend Mini App (Netlify)

1) Зайдите на [netlify.com](https://netlify.com) и войдите через GitHub
2) "New site from Git" → выберите ваш репозиторий
3) Настройки:
   - **Base directory**: `frontend-only`
   - **Publish directory**: `frontend-only` (или оставьте пустым)
   - **Build command**: `echo 'Static site - no build needed'`
4) После деплоя получите URL (например: `https://pomoika-miniapp.netlify.app`)

**Альтернативно**: Netlify автоматически определит настройки из `frontend-only/netlify.toml`

**Если все еще ошибка**: В настройках Netlify отключите "Auto-install dependencies"

## 3. Обновите конфиги

1) В `frontend-only/config.js` замените:
   ```js
   API_BASE: 'https://ВАШ-RENDER-ДОМЕН.onrender.com'
   ```

2) В `.env` (для локального бота):
   ```env
   BOT_TOKEN=ваш_токен
   ADMIN_IDS=ваш_id
   WEBAPP_URL=https://pomoika-miniapp.netlify.app/
   ```

3) **Создайте суперпользователя для Django Admin**:
   - После деплоя на Render, подключитесь к консоли
   - Выполните: `cd admin && python manage.py createsuperuser`

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

- **Django Admin**: `https://ВАШ-RENDER-ДОМЕН.onrender.com/admin/`
  - Войдите с учетными данными суперпользователя
  - Добавьте категории, товары с вкусами
  - Просматривайте заявки от клиентов

- **Mini App**: Откройте бота в Telegram → /start → "Открыть Mini App"
  - Mini App должен загрузить каталог и позволить добавлять в корзину
  - При оформлении заказа → уведомление админам
  - Заявки появятся в Django Admin

## Структура проекта

```
├── app/           # Python код (бот + API)
├── admin/         # Django Admin панель
│   ├── manage.py
│   ├── admin_project/
│   └── shop/      # Django приложение
├── frontend-only/ # Mini App для Netlify
├── web/           # Mini App (HTML/CSS/JS)
├── data/          # catalog.json
├── requirements.txt
├── render.yaml    # Render конфиг
├── Procfile       # Heroku/Render
└── netlify.toml   # Netlify конфиг
```

## 6. Генерация секретного ключа Django

Для продакшена сгенерируйте новый секретный ключ:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Используйте этот ключ в переменной окружения `DJANGO_SECRET_KEY` на Render.
