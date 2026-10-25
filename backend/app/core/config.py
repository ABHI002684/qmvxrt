import os


class Settings:
    app_name: str = "Wind Forecast Analytics API"
    api_prefix: str = "/api"
    elexon_base_url: str = "https://data.elexon.co.uk/bmrs/api/v1"
    request_timeout: float = 30.0


settings = Settings()