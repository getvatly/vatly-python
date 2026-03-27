# vatly

Official Python SDK for the [Vatly](https://vatly.dev) VAT validation API. Validate EU, UK, Swiss, Norwegian, and Australian VAT/GST numbers and look up VAT rates by country. See the full [API reference](https://docs.vatly.dev/api-reference).

## Installation

```bash
pip install vatly
```

## Quick Start

```python
from vatly import Vatly

vatly = Vatly("vtly_live_...")

result = vatly.vat.validate("NL123456789B01")
print(result.data.valid)  # True
if result.data.company:
    print(result.data.company.name)
```

## Usage

### `vatly.vat.validate()`

Validate a single VAT number.

```python
result = vatly.vat.validate(
    "NL123456789B01",
    requester_vat_number="DE987654321",  # optional, for consultation number
    cache=False,                          # optional, bypass 30-day cache
    request_id="my-trace-id",            # optional, for request tracing
)

print(result.data.valid)              # True
print(result.data.vat_number)         # "NL123456789B01"
print(result.data.country_code)       # "NL"
print(result.data.company.name)       # "Example BV"
print(result.data.company.address)    # "Amsterdam, Netherlands" or None
print(result.data.consultation_number)  # None or string (EU/UK only)
print(result.data.requested_at)       # "2026-03-18T12:00:00Z"

print(result.meta.request_id)         # "req_abc123"
print(result.meta.cached)             # True/False/None
print(result.meta.stale)              # True/False/None
print(result.meta.source_status)      # "live", "unavailable", "degraded", or None

print(result.rate_limit.remaining)    # 99
print(result.rate_limit.burst_limit)  # int or None
```

### `vatly.vat.validate_batch()`

Validate up to 50 VAT numbers in a single request.

```python
from vatly import is_batch_success

result = vatly.vat.validate_batch(
    ["NL123456789B01", "DE987654321", "XX000"],
    requester_vat_number="DE987654321",  # optional
    cache=False,                          # optional
    request_id="my-trace-id",            # optional
)

print(result.summary.total)      # 3
print(result.summary.succeeded)  # 2
print(result.summary.failed)     # 1

for item in result.results:
    if is_batch_success(item):
        print(f"{item.data.vat_number} is {'valid' if item.data.valid else 'invalid'}")
    else:
        print(f"{item.meta.vat_number} failed: {item.error.message}")
```

### `vatly.rates.list()`

List VAT rates for all supported countries.

```python
result = vatly.rates.list()

for rate in result.data:
    print(f"{rate.country_name}: {rate.standard_rate}%")
```

### `vatly.rates.get(country_code)`

Get VAT rates for a specific country.

```python
result = vatly.rates.get("NL")

print(result.data.standard_rate)  # 21
print(result.data.other_rates)    # [OtherRate(rate=9, type="reduced"), ...]
```

## Async Usage

```python
from vatly import AsyncVatly

async with AsyncVatly("vtly_live_...") as vatly:
    result = await vatly.vat.validate("NL123456789B01")
    print(result.data.valid)

    rates = await vatly.rates.list()
    for rate in rates.data:
        print(f"{rate.country_name}: {rate.standard_rate}%")
```

## Error Handling

The SDK raises typed exceptions for all error conditions. Use `try`/`except` with specific exception classes:

```python
from vatly import (
    Vatly,
    VatlyError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    UpstreamError,
)

vatly = Vatly("vtly_live_...")

try:
    result = vatly.vat.validate("INVALID")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except UpstreamError as e:
    print(f"Tax authority unavailable. Retry after {e.retry_after}s")
except AuthenticationError as e:
    print("Invalid API key or insufficient plan")
except ValidationError as e:
    print(f"Invalid input: {e.message}")
    if e.details:
        for d in e.details:
            print(f"  {d['field']}: {d['message']}")
except VatlyError as e:
    print(e.message, e.code, e.status_code)
```

### Error Classes

| Class | Trigger Codes |
|-------|---------------|
| `AuthenticationError` | `unauthorized`, `tier_insufficient`, `forbidden`, `key_revoked` |
| `ValidationError` | `invalid_vat_format`, `missing_parameter`, `validation_error`, `invalid_json` |
| `RateLimitError` | `rate_limit_exceeded`, `burst_limit_exceeded` |
| `UpstreamError` | `upstream_unavailable`, `upstream_member_state_unavailable` |
| `VatlyError` | Base class for all errors, including `timeout`, `network_error`, `parse_error`, `internal_error`, `key_limit_reached` |

### Error Properties

```python
e.message      # Human-readable message
e.code         # Machine-readable code (e.g. "unauthorized", "rate_limit_exceeded")
e.status_code  # HTTP status (0 for network/timeout errors)
e.request_id   # Request ID (string or None)
e.docs_url     # Link to error documentation (string, empty if not provided)
e.details      # Validation error details (list of dicts or None)
```

### Retries

The SDK does not retry automatically. `RateLimitError` and `UpstreamError` include a `retry_after` property (seconds) when the server provides one.

## Test Mode

Use test API keys (`vtly_test_*`) to validate without hitting real tax authorities.

```python
vatly = Vatly("vtly_test_...")
result = vatly.vat.validate("NL123456789B01")
print(result.meta.mode)  # "test"
```

| Magic VAT Number | Result |
|-----------------|--------|
| `NL123456789B01` | Valid, with company info |
| `XX000000000` | Invalid format error |

## Configuration

```python
# String API key
vatly = Vatly("vtly_live_...")

# Keyword arguments
vatly = Vatly(
    api_key="vtly_live_...",
    base_url="https://api.vatly.dev",  # default
    timeout=30.0,                       # seconds, default
)

# Environment variable fallback
# Set VATLY_API_KEY=vtly_live_... and omit the key:
vatly = Vatly()
```

The client also supports context managers for proper resource cleanup:

```python
with Vatly("vtly_live_...") as vatly:
    result = vatly.vat.validate("NL123456789B01")
```

## Type Hints

The package includes a `py.typed` marker (PEP 561) for full type checking support.

```python
from vatly import (
    Vatly,
    AsyncVatly,
    ValidateResponse,
    BatchValidateResponse,
    BatchResultSuccess,
    BatchResultError,
    Company,
    VatValidationResult,
    ResponseMeta,
    RateLimitInfo,
    VatRate,
    OtherRate,
    ListRatesResponse,
    GetRateResponse,
    BatchSummary,
    is_batch_success,
)
```

## Requirements

- Python >= 3.9
- [httpx](https://www.python-httpx.org/) >= 0.27 (sole runtime dependency)

## License

MIT
