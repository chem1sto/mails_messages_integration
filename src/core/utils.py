import os
from email import policy
from email.parser import BytesParser
from typing import Any, Coroutine

import aioimaplib


def email_file_path(instance, filename):
    """Формирование пути загрузки файла, включая оригинальное название."""
    return os.path.join("email_files", instance.subject[:50], filename)


async def fetch_emails(
    email_account: Any,
) -> Coroutine[Any, Any, list[dict[str, Any]]]:
    """Подключение к почтовому серверу и получение электронных писем."""
    imap_server = "imap.gmail.com"
    imap = aioimaplib.IMAP4_SSL(host=imap_server)
    try:
        await imap.wait_hello_from_server()
        await imap.login(email_account.email, email_account.password)
    except aioimaplib.Error as e:
        return {"error": str(e)}
    await imap.select("INBOX")
    status, messages = await imap.search("ALL")
    email_list = []
    for msg_id in messages[1].split():
        status, msg_data = await imap.fetch(msg_id, "(RFC822)")
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[1])
        subject = msg["Subject"]
        email_list.append({"subject": subject, "from": msg["From"]})
    await imap.logout()
    return email_list
