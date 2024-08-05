"""Модель Email."""

from core.constants import ATTACHMENTS, AttachmentConfig, EmailConfig
from django.db import models

# from mail_recipient.custom_storage import CustomStorage


class Email(models.Model):
    """
    Модель для хранения текстовой информации о полученных электронных письмах.

    Атрибуты:
        message_id (CharField): Уникальный идентификатор сообщения.
        subject (CharField): Тема письма.
        mail_from (CharField): Отправитель письма.
        date (DateTimeField): Дата отправки письма.
        received (DateTimeField): Дата получения письма.
        text (TextField): Текст письма.
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

    def __str__(self):
        """
        Возвращает строковое представление объекта Email.

        Возвращает:
            str: Тема письма, обрезанная до максимальной длины.
        """
        return self.subject[: EmailConfig.SUBJECT_MAX_LENGTH]


class Attachment(models.Model):
    """
    Модель для хранения информации о вложениях электронных писем.

    Атрибуты:
        email (ForeignKey): Внешний ключ, связывающий вложение с электронным
    письмом.
        file (FileField): Поле для хранения файла вложения.
        filename (CharField): Имя файла вложения.
        url (URLField): URL-адрес для доступа к файлу вложения.
    """

    email = models.ForeignKey(
        Email, related_name=ATTACHMENTS, on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=ATTACHMENTS,
        max_length=AttachmentConfig.ATTACHMENT_PATH_MAX_LENGTH,
        verbose_name=AttachmentConfig.ATTACHMENT_VERBOSE_NAME,
    )
    filename = models.CharField(
        max_length=AttachmentConfig.ATTACHMENT_FILENAME_MAX_LENGTH
    )
    url = models.URLField()

    def __str__(self):
        """
        Возвращает строковое представление объекта Attachment.

        Возвращает:
            str: Имя файла вложения, обрезанное до максимальной длины.
        """
        return self.filename[: AttachmentConfig.ATTACHMENT_FILENAME_MAX_LENGTH]
