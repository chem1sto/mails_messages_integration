"""Модель Email."""
from django.db import models

from core.constants import EmailConfig
from core.path_utils import format_attachments_file_path
from mail_recipient.validators import validate_file_does_not_exist


def get_attachment_path(instance, filename: str) -> str:
    """
    Получение сформированного пути для файла из вложений.

    Позволяет избежать циклического импорта.

    Аргументы:
        instance (Email): Экземпляр модели Email.
        filename (str): Имя файла вложения.

    Возвращает:
        str: Сформированный путь для файла вложения.
    """
    return format_attachments_file_path(instance.subject, filename)


class Email(models.Model):
    """
    Модель для хранения информации о полученных электронных письмах.

    Attributes:
        message_id (CharField): Уникальный идентификатор сообщения.
        subject (CharField): Тема письма.
        mail_from (CharField): Отправитель письма.
        date (DateTimeField): Дата отправки письма.
        received (DateTimeField): Дата получения письма.
        text (TextField): Текст письма.
        attachments (FileField): Вложения к письму.
    """

    message_id = models.CharField(
        max_length=EmailConfig.MESSAGE_ID_MAX_LENGTH, unique=True
    )
    subject = models.CharField(
        max_length=EmailConfig.SUBJECT_MAX_LENGTH,
        verbose_name=EmailConfig.SUBJECT_VERBOSE_NAME,
    )
    mail_from = models.CharField(
        max_length=EmailConfig.MAIL_FROM_MAX_LENGTH,
        verbose_name=EmailConfig.MAIL_FROM_VERBOSE_NAME,
        null=True,
        blank=True,
    )
    date = models.DateTimeField(
        verbose_name=EmailConfig.DATE_VERBOSE_NAME,
        null=True,
        blank=True,
    )
    received = models.DateTimeField(
        verbose_name=EmailConfig.RECEIVED_VERBOSE_NAME,
        null=True,
        blank=True,
    )
    text = models.TextField(
        max_length=EmailConfig.TEXT_MAX_LENGTH,
        verbose_name=EmailConfig.TEXT_VERBOSE_NAME,
        null=True,
        blank=True,
    )
    attachments = models.FileField(
        upload_to=get_attachment_path,
        max_length=EmailConfig.ATTACHMENTS_MAX_LENGTH,
        verbose_name=EmailConfig.ATTACHMENTS_VERBOSE_NAME,
        null=True,
        blank=True,
        validators=[validate_file_does_not_exist],
    )

    def __str__(self):
        """
        Возвращает строковое представление объекта Email.

        Returns:
            str: Тема письма, обрезанная до максимальной длины.
        """
        return self.subject[: EmailConfig.ATTACHMENTS_MAX_LENGTH]
