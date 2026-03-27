from __future__ import annotations

import os
import warnings
from dataclasses import dataclass
from typing import Optional

from vatly._errors import VatlyError

_DEFAULT_BASE_URL = "https://api.vatly.dev"
_DEFAULT_TIMEOUT = 30.0


@dataclass
class VatlyConfig:
    api_key: str
    base_url: str
    timeout: float

    @classmethod
    def resolve(
        cls,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> VatlyConfig:
        resolved_key = api_key or os.environ.get("VATLY_API_KEY", "")

        if not resolved_key:
            raise VatlyError(
                "No API key provided. Pass it to the constructor or set the "
                "VATLY_API_KEY environment variable.",
                code="missing_api_key",
                status_code=0,
            )

        if not resolved_key.startswith(("vtly_live_", "vtly_test_")):
            warnings.warn(
                "The API key does not start with 'vtly_live_' or 'vtly_test_'. "
                "This may indicate an invalid key.",
                stacklevel=3,
            )

        return cls(
            api_key=resolved_key,
            base_url=base_url or _DEFAULT_BASE_URL,
            timeout=timeout if timeout is not None else _DEFAULT_TIMEOUT,
        )
