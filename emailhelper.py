from smtplib import SMTP_SSL
from email.message import EmailMessage
from time import localtime


def send_remaining(From: str, To: str, remaining: float, password: str):
    with SMTP_SSL("smtp.tongji.edu.cn") as server:
        msg = EmailMessage()
        msg["From"] = From
        msg["To"] = To
        time = localtime()
        msg["Subject"] = f"{time.tm_year}-{time.tm_mon}-{time.tm_mday} {time.tm_hour}时，剩余{remaining}度"
        server.login(From, password)
        server.send_message(msg)