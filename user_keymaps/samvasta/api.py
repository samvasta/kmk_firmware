import wifi
import adafruit_connection_manager
import adafruit_requests
import os
from kmk.scheduler import create_task


radio = wifi.radio
pool = adafruit_connection_manager.get_radio_socketpool(radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)
requests = adafruit_requests.Session(pool, ssl_context)


class Api:

    url = None
    data = {}
    polling_interval_sec = 120
    last_update = 0
    _task = None

    def __init__(self, url: str = None, polling_interval_sec: int = 120):
        self.url = url
        self.data = {}
        self.polling_interval_sec = polling_interval_sec
        self.last_update = 0

    def create_task(self):
        if not self._task:
            self._task = create_task(
                self.poll, period_ms=(self.polling_interval_sec * 1000)
            )

    def poll(self):
        response = requests.get(self.url)
        self.data = response.json()
