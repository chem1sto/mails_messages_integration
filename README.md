# Интеграция почтовых сообщений
## Тестовое задание на позицию "Backend-разработчик"

## О проекте
&ensp; &nbsp; В данном проекте реализован интерфейс для получения всех
электронных писем с вложениями с самых популярных почтовых сервисов gmail.com,
yandex.ru, mail.ru. Для подключения к почтовому сервису нужно создать
специальный пароль почтового приложения от аккаунта, на котором настроена
двухэтапная авторизация.

&ensp; &nbsp; С инструкциями по созданию специального пароля для приложения
почты можно ознакомиться по следующим ссылкам:
- Mail.ru: https://help.mail.ru/mail/security/protection/external/
- Yandex.ru: https://yandex.ru/support/id/authorization/app-passwords.html
- Gmail.com: https://support.google.com/mail/answer/185833?hl=ru

Получить пароль приложения для своего аккаунта можно по ссылкам:
- Mail.ru: https://account.mail.ru/user/2-step-auth/passwords/
- Yandex.ru: https://id.yandex.ru/security/app-passwords
- Gmail.com: https://myaccount.google.com/apppasswords

## Технологии
- Python
- Django
- Channels
- Channels-redis
- Daphne

## Как запустить проект
1. Клонировать репозиторий и перейти в него в командной строке:
    ```bash
    git clone git@github.com:chem1sto/test_mails_messages_integration.git
    ```
2. Создать и активировать виртуальное окружение:
    ```bash
    cd ./test_mails_messages_integration/ &&
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
    REDIS_HOSTS = "IP (домен) вашего сервера, порт 6379"
    DB_NAME="Название базы данных"
    POSTGRES_USER="Пользователь базы данных"
    POSTGRES_PASSWORD="Пароль пользователя"
    DB_HOST="Хост базы данных"
    ```
6. Добавьте ваши данные в файл .env.db (подробнее в .env.db.example)
    ```
    DB_ENGINE="backend django для работы с PostgreSQL"
    DB_NAME="Название базы данных"
    POSTGRES_USER="Пользователь базы данных"
    POSTGRES_PASSWORD="Пароль пользователя"
    DB_HOST="Хост базы данных"
    DB_PORT="Порт хоста базы данных"
    ```

### Запуск проекта в dev-режиме
1. Убедитесь, что docker установлен:
    ```bash
   docker --version
    ```
    Инструмент Docker engine можно установить с [этого официального сайта](https://docs.docker.com/engine/install/)
2. Скачайте образ Redis и запустите контейнер:
   ```bash
   docker pull redis:latest
   docker run -d --name redis -p 6379:6379 redis:latest
   ```
3. Для запуска проекта перейдите в папку с файлом manage.py и выполните команды:
   ```bash
   cd ../test_mails_messages_integration/src/ &&
   python manage.py makemigrations &&
   python manage.py migrate &&
   python manage.py collectstatic --noinput
   python manage.py runserver
   ```

## Автор
[Васильев Владимир](https://github.com/chem1sto)

## Лицензия
Пожалуйста, ознакомьтесь с [MIT license](https://github.com/chem1sto/test_mails_messages_integration?tab=MIT-1-ov-file)
