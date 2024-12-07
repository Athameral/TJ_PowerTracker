from dataclasses import dataclass
from typing import TypedDict
import re
import json
import logging

logger = logging.getLogger(__name__)

class SMTPConfig(TypedDict):
    server: str
    port: int
    username: str
    password: str

@dataclass
class Config:
    username: str
    password: str
    email_list: list[str]
    smtp: SMTPConfig
    check_interval_normal: float
    check_interval_urgent: float

    def __post_init__(self) -> None:
        for email in self.email_list:
            if not self._validate_email(email):
                raise ValueError(f"Invalid email address: {email}")

    @staticmethod
    def _validate_email(email: str) -> bool:
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(pattern, email) is not None


with open("./cfg.json", encoding="UTF-8") as f:
    config = Config(**json.load(f))
    logger.info(f"Config loaded successfully: username={config.username}")
