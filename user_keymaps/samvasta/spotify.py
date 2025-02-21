import os

from api import AuthTokenProvider


class CurrentlyPlaying:
    is_playing: bool = False
    track_id: str = None
    track_name: str = None
    popularity: int = None
    track_length_ms: int = None
    track_progress_ms: int = None
    album_id: str = None
    album_name: str = None
    album_art_url: str = None
    artists: list = None


class SpotifyProvider:
    currently_playing: CurrentlyPlaying = None
    thumbnail = None
    polling_interval_sec = 15
    last_update = 0
    _task = None

    def __init__(
        self,
        token_provider: AuthTokenProvider,
        polling_interval_sec: int = 15,
    ):
        self.token_provider = token_provider
        self.currently_playing = None
        self.polling_interval_sec = polling_interval_sec
        self.last_update = 0

    def create_task(self):
        if not self._task:
            self._task = create_task(
                self.poll, period_ms=(self.polling_interval_sec * 1000)
            )

    def poll(self):
        prior_thumbnail_url = self.currently_playing['album_art_url']
        response = requests.get(
            f'{os.getenv("API_BASE_URL")}/api/collections/spotify/currently-playing',
            headers={
                'Authorization': f'Bearer {self.token_provider.token}',
                "Content-Type": "application/json",
            },
        )
        if response.status_code != 200:
            self.currently_playing = None
            return
        self.currently_playing = response.json()
        thumbnail_url = self.currently_playing['album_art_url']
        if thumbnail_url is not None and thumbnail_url != prior_thumbnail_url:
            thumbnail_response = requests.get(
                thumbnail_url,
                headers={
                    'Authorization': f'Bearer {self.token_provider.token}',
                },
            )
            self.thumbnail = thumbnail_response.content
