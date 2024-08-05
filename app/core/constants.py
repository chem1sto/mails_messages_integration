"""Константы и настройки для моделей проекта."""

ACTION = "action"
ADD_EMAIL_ACCOUNT_HTML = "add_email_account.html"
ALL = "ALL"
ALL_EMAILS_ID_RECEIVED_LOGGER_INFO = (
    "Получены идентификаторы всех электронных писем и обновлен прогресс-бар"
)
AT = "@"
ATTACHMENTS = "attachments"
BAD = "BAD"
BS4_PARSER = "html.parser"
AUTH_FAILED_ERROR_MESSAGE = "Введены некорректные данные пользователя"
AUTH_FAILED_LOGGER_ERROR_MESSAGE = "Ошибка аутентификации: %s"
CHECKED = "checked"
CHECKED_EMAIL_LOGGER_INFO_MESSAGE = "Проверено письмо с id %s"
CLOSE_CONNECTION = "close_connection"
CONTENT = "content"
CONTENT_DISPOSITION = "Content-Disposition"
CURRENT_GMT = 3
DATE = "date"
DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
EMAIL = "email"
EMAIL_ACCOUNT_NOT_FOUND_ERROR_MESSAGE = "Электронная почта не найдена"
EMAIL_ACCOUNT_NOT_FOUND_LOGGER_ERROR_MESSAGE = (
    "Электронная почта в не найдена: %s"
)
EMAIL_DATA = "email_data"
EMAIL_DATA_SEND_LOGGER_MESSAGE = (
    "Данные письма с message_id %s отправлены на страницу"
)
EMAIL_LIST_HTML = "email_list.html"
EMAIL_LIST_REDIRECT = "/email_list/?email={email}"
EMAIL_REQUIRED_ERROR_MESSAGE = "Требуется электронная почта"
EMAIL_REQUIRED_LOGGER_ERROR_MESSAGE = (
    "Нет электронной почты в text_data_json: %s"
)
ENCODING = "encoding"
ERROR = "error"
FETCH_EMAILS = "fetch_emails"
FETCH_EMAILS_CANCELLED_LOGGER_MESSAGE = "Обработка писем отменена"
FETCH_EMAILS_COMPLETE_LOGGER_MESSAGE = (
    "Проверка и обработка писем закончены %s"
)
FILE_NOT_FOUND = "Файл {filename} не найден"
FILENAME = "filename"
FORM = "form"
FROM = "from"
HASHED_SUBJECT_MAX_LENGTH = 16
IMAP_DOMAIN_SERVER = {
    "gmail.com": "imap.gmail.com",
    "yandex.ru": "imap.yandex.ru",
    "mail.ru": "imap.mail.ru",
    "inbox.ru": "imap.mail.ru",
    "bk.ru": "imap.mail.ru",
    "list.ru": "imap.mail.ru",
}
INBOX = "INBOX"
INDEX = "index"
MAIL_FROM = "mail_from"
MESSAGE = "message"
MESSAGE_ID = "Message-ID"
NEW_EMAIL = "new_email"
REQUEST_METHOD = "POST"
MULTIPART = "multipart"
NEW_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S"
NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE = (
    "Неожиданная ошибка при получении письма %s: Недостаточно данных"
)
NO_SUBJECT = "Без темы"
NO_MESSAGE_TO_PROCESS_ERROR_MESSAGE = "Нет письма для обработки"
NO_MESSAGE_TO_PROCESS_LOGGER_ERROR_MESSAGE = "Нет письма для обработки: %s"
OK = "OK"
PARSING_MAIL_LOGGER_ERROR_MESSAGE = "Ошибка при парсинге письма %s: %s"
PASSWORD = "password"
PROGRESS = "progress"
RFC822_FORMAT = "(RFC822)"
RECEIVE_MAIL_LOGGER_ERROR_MESSAGE = "Ошибка при получении письма %s: %s"
RECEIVED = "received"
SAVE_EMAIL_TO_DB = "save_email_to_db"
SAVE_EMAIL_ATTACHMENTS_TO_DB_SUCCESS = (
    "Вложение %s для письма с message_id %s успешно сохранено."
)
SAVE_EMAIL_TO_DB_SUCCESS = (
    "Электронное письмо с message_id %s успешно сохранено."
)
SEARCH_MAILS_ERROR_MESSAGE = "Ошибка при поиске писем"
SEARCH_MAILS_LOGGER_ERROR_MESSAGE = "Ошибка при поиске писем: %s"
SELECT_INBOX_ERROR_MESSAGE = "Ошибка при выборе почтового ящика"
SELECT_INBOX_LOGGER_ERROR_MESSAGE = "Ошибка при выборе почтового ящика: %s"
SUBJECT = "subject"
TEXT = "text"
TEXT_HTML = "text/html"
TEXT_PLANE = "text/plain"
TIMEOUT_ERROR_MESSAGE = "Превышено время ожидания ответа"
TIMEOUT_LOGGER_ERROR_MESSAGE = (
    "Превышено время ожидания ответа от imap-сервера"
)
TOTAL_EMAILS = "total_emails"
TOTAL = "total"
TYPE = "type"
UNEXPECTED_LOGGER_ERROR_MESSAGE = "Произошла неожиданная ошибка: %s"
UNSUPPORTED_ACTION_ERROR_MESSAGE = "Неподдерживаемое действие: %s"
UNSUPPORTED_ACTION_LOGGER_ERROR_MESSAGE = (
    "Передано неподдерживаемое действие: %s"
)
URL = "url"


class AttachmentConfig:
    """Настройки для модели Attachments."""

    ATTACHMENT_FILENAME_MAX_LENGTH = 255
    ATTACHMENT_PATH_MAX_LENGTH = 150
    ATTACHMENT_VERBOSE_NAME = "Вложение"


class EmailConfig:
    """Настройки для модели Email."""

    MESSAGE_ID_MAX_LENGTH = 255
    SUBJECT_MAX_LENGTH = 255
    SUBJECT_VERBOSE_NAME = "Тема сообщения"
    MAIL_FROM_MAX_LENGTH = 255
    MAIL_FROM_VERBOSE_NAME = "Отправитель"
    DATE_VERBOSE_NAME = "Дата получения письма"
    RECEIVED_VERBOSE_NAME = "Дата отправки письма"
    TEXT_MAX_LENGTH = 100
    TEXT_VERBOSE_NAME = "Описание или текст письма"


class EmailAccountConfig:
    """Настройки для модели EmailAccount."""

    EMAIL = "email"
    EMAIL_VERBOSE_NAME = "Электронная почта"
    EMAIL_HELP_TEXT = "Введите адрес электронной почты"
    PASSWORD = "password"
    PASSWORD_MAX_LENGTH = 128
    PASSWORD_VERBOSE_NAME = "Пароль"
    PASSWORD_HELP_TEXT = "Введите пароль от электронной почты"
    UNIQUE_EMAIL_PASSWORD_NAME = "unique_email_password"


class EmailAccountFormConfig:
    """Настройки для формы EmailAccount."""

    PASSWORD_LABEL = "Пароль приложения от почты"
    PASSWORD_HELP_TEXT = "Введите пароль приложения от почты"
    PASSWORD_VALIDATOR_MESSAGE = "Пароль должен быть не менее 8 символов"
