# Исправление ошибки Netlify

## Проблема
```
sh: 1: vue-cli-service: not found
```

## Решение

### 1. Обновлен package.json
Переместил необходимые пакеты из `devDependencies` в `dependencies`:
- `@vue/cli-service`
- `vue-template-compiler`
- `sass`
- `sass-loader`
- `vuetify-loader`

### 2. Обновлен netlify.toml
Изменил команду сборки с `npm ci` на `npm install`:
```toml
command = "npm install && npm run build"
```

### 3. Проверка
Сборка теперь проходит успешно локально и должна работать на Netlify.

## Что делать дальше

1. Зафиксируйте изменения в git
2. Запустите новый деплой на Netlify
3. Админка будет доступна по адресу: `https://ваш-домен.netlify.app/#/admin/login`

## Если проблема повторится

Проверьте в настройках Netlify:
- Base directory: `frontend`
- Build command: `npm install && npm run build`
- Publish directory: `frontend/dist`
