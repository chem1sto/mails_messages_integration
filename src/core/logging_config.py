import logging
from django.conf import settings


def setup_aioimaplib_logging():
    aioimaplib_logger = logging.getLogger("aioimaplib")
    aioimaplib_logger.setLevel(logging.DEBUG)
    if "console" in settings.LOGGING["handlers"]:
        aioimaplib_logger.addHandler(settings.LOGGING["handlers"]["console"])
    else:
        aioimaplib_handler = logging.StreamHandler()
        aioimaplib_handler.setLevel(logging.DEBUG)
        aioimaplib_formatter = logging.Formatter(
            "{levelname} {asctime} {message}", style="{"
        )
        aioimaplib_handler.setFormatter(aioimaplib_formatter)
        aioimaplib_logger.addHandler(aioimaplib_handler)
    return aioimaplib_logger
