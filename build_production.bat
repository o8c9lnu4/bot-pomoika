@echo off
echo 🚀 Сборка для продакшена...

REM Переходим в папку фронтенда
cd frontend

REM Устанавливаем зависимости
echo 📦 Установка зависимостей...
npm install

REM Собираем проект для продакшена
echo 🔨 Сборка проекта...
npm run build

echo ✅ Сборка завершена!
echo 📁 Файлы готовы в папке frontend/dist/
echo 🌐 Админка будет доступна по адресу: https://bot-pomoika.onrender.com/#/admin/login
pause
