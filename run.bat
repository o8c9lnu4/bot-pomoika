@echo off
echo Остановка предыдущих процессов Django...
taskkill /F /IM python.exe

echo Очистка статических файлов...
python manage.py collectstatic --no-input --clear

echo Сборка фронтенда...
cd frontend
call npm install
call npm run build
cd ..

echo Копирование файлов фронтенда...
if not exist staticfiles mkdir staticfiles
xcopy /E /I /Y frontend\dist\* staticfiles\

echo Сборка статических файлов...
python manage.py collectstatic --no-input

echo Проверка суперпользователя...
python create_superuser.py

echo Запуск сервера Django...
python manage.py runserver 