from django.db import models

from core.constants import EmailConfig
from core.utils import email_file_path


class Email(models.Model):
    subject = models.CharField(
        max_length=EmailConfig.SUBJECT_MAX_LENGTH,
        verbose_name=EmailConfig.SUBJECT_VERBOSE_NAME
    )
    date_of_receipt = models.DateTimeField(
        verbose_name=EmailConfig.DATE_OF_RECEIPT_VERBOSE_NAME,
        null=True, blank=True
    )
    date_of_dispatch = models.DateTimeField(
        verbose_name=EmailConfig.DATE_OF_DISPATCH_VERBOSE_NAME,
        null=True, blank=True
    )
    body = models.TextField(
        max_length=EmailConfig.BODY_MAX_LENGTH,
        verbose_name=EmailConfig.BODY_VERBOSE_NAME,
        null=True, blank=True
    )
    included_files = models.FileField(
        upload_to=email_file_path,
        verbose_name=EmailConfig.INCLUDED_FILES_VERBOSE_NAME,
        null=True, blank=True
    )

    def __str__(self):
        return self.subject[:50]
