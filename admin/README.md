# Django Admin для Pomoika Vape Lab

## Установка и запуск

1. Установите зависимости:
```bash
pip install Django djangorestframework Pillow
```

2. Перейдите в папку admin:
```bash
cd admin
```

3. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запустите сервер:
```bash
python manage.py runserver
```

## Доступ к админке

Откройте в браузере: http://127.0.0.1:8000/admin/

## API эндпоинты

- `GET /api/categories/` - список категорий
- `GET /api/items/` - список товаров
- `POST /api/items/` - создать товар
- `GET /api/items/{id}/` - получить товар
- `PUT /api/items/{id}/` - обновить товар
- `DELETE /api/items/{id}/` - удалить товар
- `GET /api/applications/` - список заявок
- `POST /api/applications/` - создать заявку

## Интеграция с фронтендом

Обновите `API_BASE` в вашем фронтенде на:
```
http://127.0.0.1:8000
```

## Структура данных

### Товар (Product)
- title - название
- description - описание
- price - цена
- category - категория
- strength - крепкость
- photo - фото
- is_active - активен ли товар
- flavors - вкусы с наличием

### Заявка (Application)
- customer_name - имя клиента
- contact - контакт
- status - статус (new, processing, completed, cancelled)
- total_amount - сумма заказа
- raw_payload - данные заказа из фронтенда
- notes - заметки администратора
