import requests
from dataclasses import dataclass
from tjgoudian import TJGoudianLoginHelper

TJ_REMAINING_API_URI = "https://goudian.tongji.edu.cn/api/Room/Remaining"


@dataclass
class TJPowerTracker:
    username: str
    password: str

    bearer: str = ""
    session_id: str = ""

    def __post_init__(self):
        self.loginhelper = TJGoudianLoginHelper(
            username=self.username, password=self.password
        )

    def _try_get_remaining(self, spoofing_browser=False) -> requests.Response:
        cookies = {
            "ASP.NET_SessionId": self.session_id,
        }

        headers = {
            "Authorization": f"Bearer {self.bearer}",
        }

        if spoofing_browser:
            pass  # headers balabala...

        response = requests.get(
            TJ_REMAINING_API_URI,
            cookies=cookies,
            headers=headers,
        )

        return response

    def get_remaining(self, **kwargs):
        response = self._try_get_remaining(**kwargs)
        if response.status_code != 200:
            self.bearer = self.loginhelper.get_bearer()
            self.session_id = self.loginhelper.get_session_id()
            response = self._try_get_remaining(**kwargs)

        return response.json()