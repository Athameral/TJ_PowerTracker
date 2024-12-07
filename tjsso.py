from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.chromium.options import ChromiumOptions
from os import environ
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

TJSSO_URI = (
    environ["TJSSO_URI"]
    if "TJSSO_URI" in environ.keys()
    else "https://iam.tongji.edu.cn/idp/oauth2/authorize"
)

options = ChromiumOptions()
options.browser_version = "131.0.6778.108"  # This can trigger selenium to download the latest release of Chrome.
options.add_argument("--headless=new")

# Prevents chrome from contaminating stdout
options.add_argument("--log-level=3")

options.timeouts = {"implicit": 10000}  # Wait for 10 seconds when finding an element.

# This will be used to extract the log of requests
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})


@dataclass
class TJSSO:
    """A class for the management of SSO"""

    client_id: str
    redirect_uri: str
    username: str
    password: str

    state: str = "profile"
    response_type: str = "code"

    def __post_init__(self) -> None:
        self.driver = ChromiumDriver(options=options)

    def _login(self) -> None:
        """A simple implementation of login to SSO"""
        self.driver.find_element(By.ID, "j_username").send_keys(self.username)
        self.driver.find_element(By.ID, "j_password").send_keys(self.password)
        self.driver.find_element(By.ID, "loginButton").click()
        logger.info(f"TJSSO {self.username} logged in successfully.")

    def get_authorization_code(self, *, client_id: str, redirect_uri: str) -> str:
        raise NotImplementedError
