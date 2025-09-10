#!/bin/bash

echo "🚀 Сборка для продакшена..."

# Переходим в папку фронтенда
cd frontend

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
npm install

# Собираем проект для продакшена
echo "🔨 Сборка проекта..."
npm run build

echo "✅ Сборка завершена!"
echo "📁 Файлы готовы в папке frontend/dist/"
echo "🌐 Админка будет доступна по адресу: https://bot-pomoika.onrender.com/#/admin/login"
