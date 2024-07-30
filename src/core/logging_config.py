"""Настройка логирования для модулей fetch_emails и consumer."""

import logging

from django.conf import settings


def setup_fetch_emails_logging():
    """Настройка логирования для fetch_emails."""
    aioimaplib_logger = logging.getLogger("fetch_emails")
    aioimaplib_handler = logging.StreamHandler()
    aioimaplib_handler.setLevel(logging.DEBUG)
    aioimaplib_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s"
        )
    )
    aioimaplib_logger.addHandler(aioimaplib_handler)
    aioimaplib_logger.addHandler(settings.LOGGING["handlers"]["console"])
    return aioimaplib_logger


def setup_consumer_logging():
    """Настройка логирования для consumer."""
    consumer_logger = logging.getLogger("consumer")
    consumer_handler = logging.StreamHandler()
    consumer_handler.setLevel(logging.DEBUG)
    consumer_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s"
        )
    )
    consumer_logger.addHandler(consumer_handler)
    consumer_logger.addHandler(settings.LOGGING["handlers"]["console"])
    return consumer_logger
