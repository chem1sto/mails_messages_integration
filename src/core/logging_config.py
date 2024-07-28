import logging
from django.conf import settings


def setup_fetch_emails_logging():
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
