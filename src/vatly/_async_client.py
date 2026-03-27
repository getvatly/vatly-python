from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

import httpx

from vatly._async_resources.rates import AsyncRatesResource
from vatly._async_resources.vat import AsyncVatResource
from vatly._config import VatlyConfig


class AsyncVatly:
    """Asynchronous client for the Vatly VAT validation API."""

    vat: AsyncVatResource
    rates: AsyncRatesResource

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self._config = VatlyConfig.resolve(api_key, base_url, timeout)
        self._http = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
        )
        self.vat = AsyncVatResource(self._http, self._config)
        self.rates = AsyncRatesResource(self._http, self._config)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncVatly:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()
