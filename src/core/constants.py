ACTION = "action"
ALL = "ALL"
ATTACHMENTS = "attachments"
BAD = "BAD"
AUTH_FAILED_ERROR_MESSAGE = "Введены некорректные данные пользователя"
AUTH_FAILED_LOGGER_ERROR_MESSAGE = "Ошибка аутентификации: %s"
DATE = "date"
EMAIL = "email"
EMAIL_LIST = "email_list"
EMAIL_NOT_FOUND = "Электронная почта не найдена"
EMAIL_REQUIRED = "Требуется электронная почта"
EMAILS = "emails"
ERROR = "error"
FETCH_EMAILS = "fetch_emails"
FROM = "from"
INBOX = "INBOX"
INDEX = "index"
NO_MESSAGES_TO_PROCESS_LOGGER_INFO = "Нет сообщений для обработки"
NO_DATA_IN_MAIL_LOGGER_ERROR_MESSAGE = (
    "Неожиданная ошибка при получении письма %s: Недостаточно данных"
)
MESSAGE = "message"
OK = "OK"
PARSING_MAIL_LOGGER_ERROR_MESSAGE = "Ошибка при парсинге письма %s: %s"
RFC822_FORMAT = "(RFC822)"
RECEIVE_MAIL_ERROR_MESSAGE = "Ошибка при получении письма %s: %s"
RECEIVED = "received"
RESPONSE_TIMED_OUT = "Превышено время ожидания ответа"
SEARCH_MAILS_ERROR_MESSAGE = "Ошибка при поиске писем"
SEARCH_MAILS_LOGGER_ERROR_MESSAGE = "Ошибка при поиске писем: %s"
SELECT_INBOX_ERROR_MESSAGE = "Ошибка при выборе почтового ящика"
SELECT_INBOX_LOGGER_ERROR_MESSAGE = "Ошибка при выборе почтового ящика: %s"
SUBJECT = "subject"
TEXT = "text"
TYPE = "type"
UNSUPPORTED_ACTION = "Неподдерживаемое действие: %s"


class EmailConfig:
    """
    Настройки для модели Email.
    """

    SUBJECT_MAX_LENGTH = 255
    SUBJECT_VERBOSE_NAME = "Тема сообщения"
    DATE_OF_RECEIPT_VERBOSE_NAME = "Дата получения письма"
    DATE_OF_DISPATCH_VERBOSE_NAME = "Дата отправки письма"
    BODY_MAX_LENGTH = 5000
    BODY_VERBOSE_NAME = "Описание или текст письма"
    INCLUDED_FILES_VERBOSE_NAME = "Прикреплённые файлы"


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
