# Интеграция почтовых сообщений
## Тестовое задание на позицию "Backend-разработчик"

### Технологии

- Python
- Django
- Channels
- Channels-redis
- Daphne

## Как запустить проект

1. Клонировать репозиторий и перейти в него в командной строке:
    ```bash
    git clone git@github.com:chem1sto/mails_messages_integration.git
    ```
2. Создать и активировать виртуальное окружение:
    ```bash
    cd ./mails_messages_integration/ &&
    python3 -m venv venv
    ```
    * Для Linux/macOS
    ```bash
    source venv/bin/activate
    ```
    * Для Windows
    ```shell
    source venv/scripts/activate
    ```
3. Установить зависимости из файла requirements.txt:
   ```
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Создайте переменные окружения в основной папке проекта "empty_project"
    ```bash
    touch .env
    ```
5. Добавьте ваши данные в файл .env (подробнее в .env.example)
    ```
    SECRET_KEY="Секретный код Django"
    DEBUG="True или False"
    ALLOWED_HOSTS="IP (домен) вашего сервера"
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    ```
6. Добавьте ваши данные в файл .env.db (подробнее в .env.db.example)
    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    ```

### Запуск проекта в dev-режиме

В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
### Автор

[Васильев Владимир](https://github.com/chem1sto)
