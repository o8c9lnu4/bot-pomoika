# Инструкция по деплою админки на хостинг

## Подготовка к деплою

### 1. Сборка фронтенда для продакшена

```bash
# Windows
build_production.bat

# Linux/Mac
chmod +x build_production.sh
./build_production.sh
```

Или вручную:
```bash
cd frontend
npm install
npm run build
```

### 2. Настройка Netlify

Для Netlify настройте следующие параметры:

**Build settings:**
- Base directory: `frontend`
- Build command: `npm ci && npm run build`
- Publish directory: `frontend/dist`

**Environment variables:**
- `NODE_ENV=production`

### 2. Настройка переменных окружения на хостинге

Установите следующие переменные окружения на вашем хостинге (Render.com):

```
DEBUG=False
SECRET_KEY=ваш-секретный-ключ-для-продакшена
RENDER_EXTERNAL_HOSTNAME=bot-pomoika.onrender.com
```

### 3. Загрузка файлов

1. Загрузите все файлы проекта на хостинг
2. Убедитесь, что папка `frontend/dist/` содержит собранные файлы
3. Проверьте, что Django может найти статические файлы

## Проверка работы

### После деплоя проверьте:

1. **Основной сайт**: `https://bot-pomoika.onrender.com/`
2. **Админка**: `https://bot-pomoika.onrender.com/#/admin/login`
3. **API**: `https://bot-pomoika.onrender.com/api/posts/`

### Создание суперпользователя

Если нужно создать администратора:

```bash
python manage.py createsuperuser
```

## Настройки для продакшена

### Django настройки уже обновлены:

- ✅ `DEBUG = False` в продакшене
- ✅ `ALLOWED_HOSTS` включает ваш домен
- ✅ `CORS_ALLOWED_ORIGINS` настроен для вашего домена
- ✅ `CSRF_TRUSTED_ORIGINS` включает ваш домен
- ✅ Безопасные cookies в продакшене

### Фронтенд настройки:

- ✅ `axios.defaults.baseURL` автоматически переключается на хостинг
- ✅ Proxy настройки для разработки и продакшена
- ✅ Правильный `publicPath` для статических файлов

## Доступ к админке

После деплоя админка будет доступна по адресу:
**https://bot-pomoika.onrender.com/#/admin/login**

Используйте учетные данные Django суперпользователя для входа.

## Устранение проблем

### Если админка не загружается:

1. Проверьте, что фронтенд собран: `frontend/dist/` содержит файлы
2. Проверьте настройки `STATICFILES_DIRS` в Django
3. Убедитесь, что `publicPath: '/static/'` в vue.config.js

### Если API не работает:

1. Проверьте CORS настройки
2. Убедитесь, что `ALLOWED_HOSTS` включает ваш домен
3. Проверьте переменные окружения

### Если авторизация не работает:

1. Проверьте настройки сессий
2. Убедитесь, что CSRF настройки правильные
3. Проверьте, что пользователь имеет `is_staff=True`
