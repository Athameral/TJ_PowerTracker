from smtplib import SMTP_SSL
from email.message import EmailMessage
from time import localtime
from config import config
import logging

logger = logging.getLogger(__name__)

def send_remaining(From: str, To: str, remaining: float, password: str):
    with SMTP_SSL(config.smtp["server"], config.smtp["port"]) as server:
        msg = EmailMessage()
        msg["From"] = From
        msg["To"] = To
        time = localtime()
        msg["Subject"] = f"{time.tm_year}-{time.tm_mon}-{time.tm_mday} {time.tm_hour}:{time.tm_min}:{time.tm_sec}，剩余{remaining}度"
        server.login(From, password)
        logger.info(f"SMTP {From} logged in successfully.")
        server.send_message(msg)
        logger.info(f"SMTP {From} sent successfully.")
