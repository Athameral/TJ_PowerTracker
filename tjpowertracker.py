import requests
from dataclasses import dataclass
from tjgoudian import TJGoudianLoginHelper
import logging

logger = logging.getLogger(__name__)

TJ_REMAINING_API_URI = "https://goudian.tongji.edu.cn/api/Room/Remaining"


@dataclass
class TJPowerTracker:
    username: str
    password: str

    bearer: str = ""
    session_id: str = ""
    max_retry: int = 5

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

    def get_remaining(self, **kwargs) -> float:
        response = self._try_get_remaining(**kwargs)
        for retrial in range(self.max_retry):
            if response.status_code != 200:
                logger.info("Did not get code 200, trying getting a new bearer...")
                self.bearer = self.loginhelper.get_bearer()
                logger.info(f"Got bearer: {self.bearer}")
                self.session_id = self.loginhelper.get_session_id()
                response = self._try_get_remaining(**kwargs)
            else:
                break

        else:
            raise RuntimeError(
                f"Failed to get remaining power after {self.max_retry} retrials."
            )

        # {
        #     "result": {"next": "提示:每天早上9点更新", "remaining": 7.22},
        #     "targetUrl": None,
        #     "success": True,
        #     "error": None,
        #     "unAuthorizedRequest": False,
        #     "__abp": True,
        # }
        content: dict = response.json()
        if "result" in content.keys():
            result: dict = content["result"]
            if "remaining" in result.keys():
                remaining = float(result["remaining"])
                logger.info(f"Got remaining={remaining} successfully.")
                return remaining

        raise RuntimeError("Failed to parse remaining power from response.")
