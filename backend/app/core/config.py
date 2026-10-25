
import os


class Settings:
    app_name: str = "Wind Forecast Analytics API"
    api_prefix: str = "/api"
    elexon_base_url: str = "https://data.elexon.co.uk/bmrs/api/v1"
    request_timeout: float = 30.0

    @property
    def cors_origins(self) -> list[str]:
        origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
        return [
            origin.strip().rstrip("/")
            for origin in origins.split(",")
            if origin.strip()
        ]


settings = Settings()
