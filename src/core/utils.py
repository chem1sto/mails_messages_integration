import os
from email import policy
from email.parser import BytesParser
from typing import Any

import aioimaplib

from core.constants import ERROR_MESSAGES
from core.logging_config import setup_aioimaplib_logging
from email_account.models import EmailAccount

aioimaplib_logger = setup_aioimaplib_logging()


def email_file_path(instance, filename):
    """Формирование пути загрузки файла, включая оригинальное название."""
    return os.path.join("email_files", instance.subject[:50], filename)


async def fetch_emails(
    email_account: EmailAccount,
) -> dict[str, str] | list[dict[str, Any]]:
    """Подключение к почтовому серверу и получение электронных писем."""
    imap_server = "imap.gmail.com"
    imap = aioimaplib.IMAP4_SSL(host=imap_server)
    try:
        await imap.wait_hello_from_server()
        login_result = await imap.login(
            email_account.email, email_account.password
        )
        if login_result[0] != "OK":
            aioimaplib_logger.error(
                f"Ошибка аутентификации: {login_result[1]}"
            )
            return {"error": ERROR_MESSAGES.get("auth_failed")}
        await imap.select("INBOX")
        status, messages = await imap.search("ALL")
        if status != "OK":
            aioimaplib_logger.error(f"Ошибка при поиске писем: {messages[0]}")
            return {"error": "Ошибка при поиске писем"}
        email_list = []
        for msg_id in messages[0].split()[:10]:
            status, msg_data = await imap.fetch(msg_id.decode(), "(RFC822)")
            if messages[0] == b"":
                aioimaplib_logger.info("Нет сообщений для обработки")
                return email_list
            if status == "BAD":
                aioimaplib_logger.error(
                    f"Ошибка при получении письма {msg_id}: {msg_data[1]}"
                )
                continue
            try:
                if len(msg_data) < 2:
                    aioimaplib_logger.error(
                        f"Неожиданная ошибка при получении письма {msg_id}: "
                        f"Недостаточно данных"
                    )
                    continue
                msg = BytesParser(policy=policy.default).parsebytes(
                    msg_data[1]
                )
                subject = msg["Subject"]
                email_list.append({"subject": subject, "from": msg["From"]})
            except IndexError as e:
                aioimaplib_logger.error(
                    f"Ошибка при парсинге письма {msg_id}: {str(e)}"
                )
                continue
        await imap.logout()
        return email_list
    except aioimaplib.Error as e:
        aioimaplib_logger.error(f"Ошибка при работе с IMAP: {str(e)}")
        return {"error": "Ошибка при работе с IMAP"}
    except Exception as e:
        aioimaplib_logger.error(f"Неожиданная ошибка: {str(e)}")
        return {"error": "Неожиданная ошибка"}
