#!/usr/bin/env bash

# Остановка всех предыдущих процессов Django
echo "Остановка предыдущих процессов Django..."
pkill -f runserver

# Очистка старых статических файлов
echo "Очистка статических файлов..."
python manage.py collectstatic --no-input --clear

# Сборка фронтенда
echo "Сборка фронтенда..."
cd frontend
npm install
npm run build
cd ..

# Копирование собранных файлов фронтенда
echo "Копирование файлов фронтенда..."
mkdir -p staticfiles
cp -r frontend/dist/* staticfiles/

# Сборка статических файлов
echo "Сборка статических файлов..."
python manage.py collectstatic --no-input

# Создание суперпользователя, если его нет
echo "Проверка суперпользователя..."
python create_superuser.py

# Запуск сервера Django
echo "Запуск сервера Django..."
python manage.py runserver 