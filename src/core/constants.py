ACTION = "action"
ALL = "ALL"
ATTACHMENTS = "attachments"
ATTACHMENTS_MAX_LENGTH = 150
BAD = "BAD"
AUTH_FAILED_ERROR_MESSAGE = "Введены некорректные данные пользователя"
AUTH_FAILED_LOGGER_ERROR_MESSAGE = "Ошибка аутентификации: %s"
CONTENT = "content"
CONTENT_DISPOSITION = "Content-Disposition"
DATE = "date"
EMAIL = "email"
EMAIL_ACCOUNT_NOT_FOUND_ERROR_MESSAGE = "Электронная почта не найдена"
EMAIL_ACCOUNT_NOT_FOUND_LOGGER_ERROR_MESSAGE = (
    "Электронная почта в не найдена: %s"
)
EMAIL_LOGGER_ERROR_MESSAGE = "Ошибка при получении письма: %s"
EMAIL_LIST = "email_list"
EMAIL_REQUIRED_ERROR_MESSAGE = "Требуется электронная почта"
EMAIL_REQUIRED_LOGGER_ERROR_MESSAGE = (
    "Нет электронной почты в text_data_json: %s"
)
EMAILS = "emails"
ERROR = "error"
FETCH_EMAILS = "fetch_emails"
FILENAME = "filename"
FROM = "from"
INBOX = "INBOX"
INDEX = "index"
NO_MESSAGES_TO_PROCESS_LOGGER_INFO = "Нет сообщений для обработки"
NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE = (
    "Неожиданная ошибка при получении письма %s: Недостаточно данных"
)
MESSAGE = "message"
MULTIPART = "multipart"
NO_EMAIL_ERROR_MESSAGE = "Требуется электронная почта"
OK = "OK"
PARSING_MAIL_LOGGER_ERROR_MESSAGE = "Ошибка при парсинге письма %s: %s"
RFC822_FORMAT = "(RFC822)"
RECEIVE_MAIL_ERROR_MESSAGE = "Ошибка при получении письма %s: %s"
RECEIVED = "received"
SEARCH_MAILS_ERROR_MESSAGE = "Ошибка при поиске писем"
SEARCH_MAILS_LOGGER_ERROR_MESSAGE = "Ошибка при поиске писем: %s"
SELECT_INBOX_ERROR_MESSAGE = "Ошибка при выборе почтового ящика"
SELECT_INBOX_LOGGER_ERROR_MESSAGE = "Ошибка при выборе почтового ящика: %s"
SERIALIZE_DATETIME_ERROR_MESSAGE = "Переданные данные нельзя сериализовать."
SUBJECT = "subject"
TEXT = "text"
TEXT_PLANE = "text/plain"
TEXT_HTML = "text/html"
TIMEOUT_ERROR_MESSAGE = "Превышено время ожидания ответа"
TIMEOUT_LOGGER_ERROR_MESSAGE = (
    "Превышено время ожидания ответа от imap-сервера"
)
TYPE = "type"
UNEXPECTED_ERROR_MESSAGE = "Произошла неожиданная ошибка: %s"
UNEXPECTED_LOGGER_ERROR_MESSAGE = "Произошла неожиданная ошибка: %s"
UNSUPPORTED_ACTION_ERROR_MESSAGE = "Неподдерживаемое действие: %s"
UNSUPPORTED_ACTION_LOGGER_ERROR_MESSAGE = (
    "Передано неподдерживаемое действие: %s"
)


class EmailConfig:
    """
    Настройки для модели Email.
    """

    MESSAGE_ID_MAX_LENGTH = 255
    SUBJECT_MAX_LENGTH = 255
    SUBJECT_VERBOSE_NAME = "Тема сообщения"
    MAIL_FROM_MAX_LENGTH = 255
    MAIL_FROM_VERBOSE_NAME = "Отправитель"
    DATE_VERBOSE_NAME = "Дата получения письма"
    RECEIVED_VERBOSE_NAME = "Дата отправки письма"
    TEXT_MAX_LENGTH = 100
    TEXT_VERBOSE_NAME = "Описание или текст письма"
    ATTACHMENTS_MAX_LENGTH = 150
    ATTACHMENTS_VERBOSE_NAME = "Вложения"


class EmailAccountConfig:
    """
    Настройки для модели EmailAccount.
    """

    EMAIL = "email"
    EMAIL_VERBOSE_NAME = "Электронная почта"
    EMAIL_HELP_TEXT = "Введите адрес электронной почты"
    PASSWORD = "password"
    PASSWORD_MAX_LENGTH = 128
    PASSWORD_VERBOSE_NAME = "Пароль"
    PASSWORD_HELP_TEXT = "Введите пароль от электронной почты"
    UNIQUE_EMAIL_PASSWORD_NAME = "unique_email_password"
