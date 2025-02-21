import wifi
import adafruit_connection_manager
import adafruit_requests
import os
from kmk.scheduler import create_task


radio = wifi.radio
pool = adafruit_connection_manager.get_radio_socketpool(radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)
requests = adafruit_requests.Session(pool, ssl_context)

wifi_valid = False
try:
    wifi.radio.connect(
        os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
    )
    wifi_valid = True
except OSError as e:
    print(f"❌ OSError: {e}")


class AuthTokenProvider:
    token = None

    def __init__(self):
        self.refresh_token()

    def refresh_token(self):
        if not wifi_valid:
            return
        response = requests.post(
            f'{os.getenv("API_BASE_URL")}/api/collections/users/auth-with-password',
            json={
                "identity": os.getenv("API_USERNAME"),
                "password": os.getenv("API_PASSWORD"),
            },
            headers={
                "Content-Type": "application/json",
            },
        )

        self.token = response.json()['token']


class Api:

    url = None
    data = {}
    polling_interval_sec = 120
    last_update = 0
    _task = None

    def __init__(
        self,
        token_provider: AuthTokenProvider,
        url: str = None,
        polling_interval_sec: int = 120,
    ):
        self.token_provider = token_provider
        self.url = url
        self.data = {}
        self.polling_interval_sec = polling_interval_sec
        self.last_update = 0

    def create_task(self):
        if not self._task and wifi_valid:
            self._task = create_task(
                self.poll, period_ms=(self.polling_interval_sec * 1000)
            )

    def poll(self):
        if not wifi_valid:
            return
        response = requests.get(
            self.url,
            headers={
                'Authorization': f'Bearer {self.token_provider.token}',
                "Content-Type": "application/json",
            },
        )
        self.data = response.json()
