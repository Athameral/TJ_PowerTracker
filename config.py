from dataclasses import dataclass
import re


@dataclass
class Config:
    username: str
    password: str
    email_list: list[str]
    smtp_username: str
    smtp_password: str
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
