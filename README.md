# Интеграция почтовых сообщений
## Тестовое задание на позицию "Junior Python Developer"

### Технологии

- Python
- Django
- Django Rest Framework

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

### Запуск проекта в dev-режиме

В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
### Автор

[Васильев Владимир](https://github.com/chem1sto)
