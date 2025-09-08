# 1. Сборка фронтенда
FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# 2. Сборка бэкенда
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Системные зависимости для psycopg2 и других пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
# Копируем собранный фронт в Django staticfiles
COPY --from=frontend /app/frontend/dist /app/frontend/dist

# Собираем статику
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# RUN python create_superuser.py
# Запуск gunicorn
CMD gunicorn blog_project.wsgi:application --bind 0.0.0.0:8000 