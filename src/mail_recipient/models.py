from django.db import models


class Email(models.Model):
    id = models.AutoField()
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема сообщения"
    )
    date_of_receipt = models.DateTimeField(
        verbose_name="Дата получения письма",
        null=True, blank=True
    )
    date_of_dispatch = models.DateTimeField(
        verbose_name="Дата отправки письма",
        null=True, blank=True
    )
    body = models.TextField(
        max_length=5000,
        verbose_name="Описание или текст письма",
        null=True, blank=True
    )
    included_files = models.FileField(
        upload_to="email_files",
        verbose_name="Прикреплённые файлы",
        null=True, blank=True
    )

    def __str__(self):
        return self.subject[:50]
