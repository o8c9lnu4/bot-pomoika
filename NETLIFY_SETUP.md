# Настройка Netlify для админки

## Быстрая настройка

### 1. Подключение репозитория
1. Войдите в [Netlify](https://netlify.com)
2. Нажмите "New site from Git"
3. Выберите ваш репозиторий
4. Netlify автоматически определит настройки из `netlify.toml`

### 2. Настройки сборки (автоматически из netlify.toml)
- **Base directory**: `frontend`
- **Build command**: `npm install && npm run build`
- **Publish directory**: `frontend/dist`

### 3. Переменные окружения
В настройках сайта добавьте:
- `NODE_ENV=production`

## Ручная настройка (если netlify.toml не работает)

### Build settings:
```
Base directory: frontend
Build command: npm install && npm run build
Publish directory: frontend/dist
```

### Redirects:
```
/admin/*    /index.html    200
/*          /index.html    200
```

## Проверка работы

После деплоя админка будет доступна по адресу:
`https://ваш-домен.netlify.app/#/admin/login`

## Устранение проблем

### Если сборка не проходит:
1. Проверьте, что `package.json` содержит все зависимости
2. Убедитесь, что `vue-toastification` версии 1.7.6 (совместим с Vue 2)
3. Проверьте логи сборки в Netlify

### Если админка не загружается:
1. Проверьте redirects в настройках Netlify
2. Убедитесь, что все файлы загружены в `frontend/dist/`
3. Проверьте консоль браузера на ошибки

### Если API не работает:
1. Убедитесь, что Django бэкенд работает на Render.com
2. Проверьте CORS настройки в Django
3. Проверьте, что `axios.defaults.baseURL` правильно настроен
