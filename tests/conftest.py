from __future__ import annotations

from typing import Generator

import pytest
import respx

from vatly import AsyncVatly, Vatly

MOCK_API_KEY = "vtly_live_test123"
BASE_URL = "https://api.vatly.dev"

VALID_RESPONSE = {
    "data": {
        "valid": True,
        "vat_number": "NL123456789B01",
        "country_code": "NL",
        "company": {"name": "Test BV", "address": "Amsterdam, Netherlands"},
        "consultation_number": None,
        "requested_at": "2026-03-18T12:00:00Z",
    },
    "meta": {
        "request_id": "req_abc123",
        "cached": None,
        "cached_at": None,
        "stale": None,
        "mode": None,
        "request_duration_ms": 150,
        "source_status": None,
    },
}

RATE_LIMIT_HEADERS = {
    "x-ratelimit-limit": "100",
    "x-ratelimit-remaining": "99",
    "x-ratelimit-reset": "2026-04-01T00:00:00Z",
}

BATCH_RESPONSE = {
    "data": {
        "results": [
            {
                "data": {
                    "valid": True,
                    "vat_number": "NL123456789B01",
                    "country_code": "NL",
                    "company": {"name": "Test BV", "address": "Amsterdam"},
                    "consultation_number": None,
                    "requested_at": "2026-03-18T12:00:00Z",
                },
                "meta": {
                    "cached": None,
                    "cached_at": None,
                    "stale": None,
                    "source_status": None,
                },
            },
            {
                "data": {
                    "valid": True,
                    "vat_number": "DE987654321",
                    "country_code": "DE",
                    "company": {"name": "Test GmbH", "address": "Berlin"},
                    "consultation_number": None,
                    "requested_at": "2026-03-18T12:00:01Z",
                },
                "meta": {
                    "cached": None,
                    "cached_at": None,
                    "stale": None,
                    "source_status": None,
                },
            },
        ],
        "summary": {"total": 2, "succeeded": 2, "failed": 0},
    },
    "meta": {
        "request_id": "req_batch1",
        "mode": None,
        "request_duration_ms": 300,
    },
}

LIST_RATES_RESPONSE = {
    "data": [
        {
            "country_code": "NL",
            "country_name": "Netherlands",
            "currency": "EUR",
            "standard_rate": 21,
            "other_rates": [{"rate": 9, "type": "reduced"}, {"rate": 0, "type": "zero"}],
            "updated_at": "2026-01-01T00:00:00Z",
        },
        {
            "country_code": "DE",
            "country_name": "Germany",
            "currency": "EUR",
            "standard_rate": 19,
            "other_rates": [{"rate": 7, "type": "reduced"}],
            "updated_at": "2026-01-01T00:00:00Z",
        },
    ],
    "meta": {"request_id": "req_rates1", "count": 2},
}

GET_RATE_RESPONSE = {
    "data": {
        "country_code": "NL",
        "country_name": "Netherlands",
        "currency": "EUR",
        "standard_rate": 21,
        "other_rates": [{"rate": 9, "type": "reduced"}, {"rate": 0, "type": "zero"}],
        "updated_at": "2026-01-01T00:00:00Z",
    },
    "meta": {"request_id": "req_rate_nl"},
}


@pytest.fixture()
def mock_api() -> Generator[respx.MockRouter, None, None]:
    with respx.mock(base_url=BASE_URL) as router:
        yield router


@pytest.fixture()
def client() -> Generator[Vatly, None, None]:
    c = Vatly(MOCK_API_KEY)
    yield c
    c.close()


@pytest.fixture()
def async_client() -> Generator[AsyncVatly, None, None]:
    c = AsyncVatly(MOCK_API_KEY)
    yield c
