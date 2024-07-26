class EmailConfig:
    """
    Настройки для модели Email.
    """

    SUBJECT_MAX_LENGTH = 255,
    SUBJECT_VERBOSE_NAME = "Тема сообщения"
    DATE_OF_RECEIPT_VERBOSE_NAME = "Дата получения письма"
    DATE_OF_DISPATCH_VERBOSE_NAME = "Дата отправки письма"
    BODY_MAX_LENGTH = 5000
    BODY_VERBOSE_NAME = "Описание или текст письма"
    INCLUDED_FILES_VERBOSE_NAME = "Прикреплённые файлы"
