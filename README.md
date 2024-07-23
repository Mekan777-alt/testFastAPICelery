## Установка и запуск

### Зависимости

- Python 3.10
- PostgreSQL
- Redis (для очередей задач Celery)
- Docker и Docker Compose

### Шаги установки и запуска с Docker Compose

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Mekan777-alt/testFastAPICelery.git
   cd testFastAPICelery
2. Создайте файл .env в корне проекта и добавьте следующие переменные:
    ```bash
   DB_USER=ваш_пользователь
   DB_PASSWORD=ваш_пароль
   DB_HOST=db
   DB_NAME=ваша_база_данных
   REDIS_HOST=redis
   REDIS_PORT=6379
3. Запустите приложение с помощью Docker Compose:
    ```bash
   docker-compose up -d

