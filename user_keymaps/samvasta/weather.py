import os

from api import Api, AuthTokenProvider


class AirQuality(Api):
    def __init__(self, token_provider: AuthTokenProvider):
        super().__init__(
            token_provider,
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={os.getenv("LATITUDE")}&longitude={os.getenv("LONGITUDE")}&current=us_aqi,dust,uv_index&format=json&timeformat=unixtime",
            3600,  # api refreshes every hour
        )

    def get_metric(self, metric):
        return f"{self.data['current'][metric]}{self.data['current_units'][metric]}"

    def aqi(self):
        return self.get_metric("us_aqi")

    def dust(self):
        return self.get_metric("dust")

    def uv(self):
        return self.get_metric("uv_index")


class Weather(Api):
    weather_metrics = [
        "time",
        "interval",
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "is_day",
        "precipitation",
        "rain",
        "showers",
        "snowfall",
        "weather_code",
        "cloud_cover",
        "surface_pressure",
        "wind_speed_10m",
        "wind_direction_10m",
    ]

    weather_codes = {
        0: "Clear",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",  # Deposition rime fog
        51: "Light Drizzle",
        53: "Drizzle",
        55: "Heavy Drizzle",
        56: "Light Freezing Drizzle",
        57: "Freezing Drizzle",
        61: "Light Rain",
        63: "Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Freezing Rain",
        71: "Light Snow",
        73: "Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Light Rain Showers",
        81: "Rain Showers",
        82: "Heavy Rain Showers",
        85: "Light Snow Showers",
        86: "Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Slight Hail",
        99: "Thunderstorm with Heavy Hail",
    }

    def __init__(self, token_provider: AuthTokenProvider):
        super().__init__(
            token_provider,
            f"https://api.open-meteo.com/v1/forecast?latitude={os.getenv("LATITUDE")}&longitude={os.getenv("LONGITUDE")}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&format=json&timeformat=unixtime",
            120,
        )

    def get_metric(self, metric):
        return f"{self.data['current'][metric]}{self.data['current_units'][metric]}"

    def describe_weather(self):
        return self.weather_codes[self.data["current"]["weather_code"]]

    def weather_code(self):
        return self.data["current"]["weather_code"]

    def temperature(self):
        return self.get_metric("temperature_2m")

    def humidity(self):
        return self.get_metric("relative_humidity_2m")

    def apparent_temperature(self):
        return self.get_metric("apparent_temperature")

    def day_or_night(self):
        return "Night" if self.data["current"]["is_day"] == 0 else "Day"

    def precipitation(self):
        return self.get_metric("precipitation")

    def rain(self):
        return self.get_metric("rain")

    def showers(self):
        return self.get_metric("showers")

    def snowfall(self):
        return self.get_metric("snowfall")

    def cloud_cover(self):
        return self.get_metric("cloud_cover")

    def pressure(self):
        return self.get_metric("surface_pressure")

    def wind_speed(self):
        return self.get_metric("wind_speed_10m")

    def wind_direction(self):
        return self.get_metric("wind_direction_10m")
