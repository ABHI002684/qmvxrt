import json
from typing import Any

import httpx

from app.core.config import settings


class ElexonAPIError(Exception):
    pass


class ElexonClient:
    def __init__(self) -> None:
        self.base_url = settings.elexon_base_url
        self.timeout = settings.request_timeout

    @staticmethod
    def parse_response(response: httpx.Response) -> list[dict[str, Any]]:
        content_type = response.headers.get("content-type", "")

        if "json" in content_type:
            payload = response.json()

            if isinstance(payload, list):
                return payload

            if isinstance(payload, dict):
                records = payload.get("data", payload.get("results", []))
                return records if isinstance(records, list) else []

        records = []

        for line in response.text.splitlines():
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            if isinstance(record, dict):
                records.append(record)

        return records

    async def _get(
        self,
        path: str,
        params: dict[str, str],
    ) -> list[dict[str, Any]]:
        url = f"{self.base_url}{path}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                print(f"Elexon request: {response.request.url}")
                response.raise_for_status()

                records = self.parse_response(response)
                print(f"Elexon records returned: {len(records)}")

                if records:
                    print(f"First record fields: {sorted(records[0].keys())}")

                return records

        except (httpx.HTTPError, ValueError) as exc:
            raise ElexonAPIError(
                f"Elexon request failed for {path}: {exc}"
            ) from exc

    async def get_actuals(
        self,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        return await self._get(
            "/datasets/FUELHH/stream",
            {
                "publishDateTimeFrom": f"{start_date}T00:00:00Z",
                "publishDateTimeTo": f"{end_date}T23:59:59Z",
            },
        )

    async def get_wind_forecasts(
        self,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        return await self._get(
            "/datasets/WINDFOR/stream",
            {
                "publishDateTimeFrom": f"{start_date}T00:00:00Z",
                "publishDateTimeTo": f"{end_date}T23:59:59Z",
            },
        )