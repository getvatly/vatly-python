from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

import httpx

from vatly._config import VatlyConfig
from vatly._resources.rates import RatesResource
from vatly._resources.vat import VatResource


class Vatly:
    """Synchronous client for the Vatly VAT validation API."""

    vat: VatResource
    rates: RatesResource

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self._config = VatlyConfig.resolve(api_key, base_url, timeout)
        self._http = httpx.Client(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
        )
        self.vat = VatResource(self._http, self._config)
        self.rates = RatesResource(self._http, self._config)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Vatly:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()
