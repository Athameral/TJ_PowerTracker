from tjsso import TJSSO, TJSSO_URI
from urllib.parse import urlencode
from time import sleep
import re


class TJGoudianLoginHelper(TJSSO):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(
            client_id="SYS20230256",
            redirect_uri="https://goudian.tongji.edu.cn/account/oauth2",
            username=username,
            password=password,
        )

    def get_bearer(self) -> str:
        params = dict(
            state=self.state,
            response_type=self.response_type,
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
        )
        driver = self.driver
        url = f"{TJSSO_URI}?{urlencode(params)}"
        driver.get(url)

        sleep(
            2
        )  # if already logged in, the browser should automatically redirect to goudian.
        if "首页" not in driver.title:
            self._login()

        sleep(
            10
        )  # wait for the browser to make a request for the remaining power, so we can get the bearer in log.
        # TODO: intercept the communication and get the bearer directly.
        # TODO: or even better, mock everything with requests after TJSSO.
        logs: list[dict] = driver.get_log("performance")
        bearer = ""
        for log in logs:
            result = re.search(r"Bearer (.*?)\"", repr(log))
            if result:
                bearer = result.group(1)
                break
        else:
            raise Warning("Bearer not found, please try again later.")

        return bearer

    def get_session_id(self) -> str:
        cookie = self.driver.get_cookie("ASP.NET_SessionId")
        return cookie["value"] if cookie else ""
