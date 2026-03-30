# Changelog

## 0.3.0

Async validation support.

- `client.async_vat.validate()` and `client.async_vat.validate_batch()` on both `Vatly` and `AsyncVatly`
- New types: `AsyncValidateData`, `AsyncMeta`, `AsyncValidateResponse`, `AsyncBatchRejectedItem`, `AsyncBatchData`, `AsyncBatchValidateResponse`
- Async validation requires a Pro or Business plan and a configured webhook URL

## 0.2.0

Type safety, robustness, and test coverage improvements.

- `is_batch_success()` now returns `TypeGuard[BatchResultSuccess]` for proper type narrowing
- `source_status` fields use `Literal["live", "unavailable", "degraded"]` instead of `str`
- `mode` field uses `Literal["test"]` instead of `str`
- New `SourceStatus` type alias exported for type annotations
- `from_dict` methods raise `VatlyError(code="parse_error")` with a descriptive message instead of raw `KeyError` on missing required fields
- Fixed quick start README example to handle `company` being `None`
- Added tests for batch network errors, non-JSON error responses, Content-Type header, async rates errors, forward-compatible deserialization, and missing required fields
- Removed unused test fixtures

## 0.1.0

Initial release.

- Sync client (`Vatly`) and async client (`AsyncVatly`)
- `vatly.vat.validate()` and `vatly.vat.validate_batch()`
- `vatly.rates.list()` and `vatly.rates.get()`
- Typed exception hierarchy: `VatlyError`, `AuthenticationError`, `ValidationError`, `RateLimitError`, `UpstreamError`
- Full type annotations with `py.typed` marker
- API key resolution: explicit arg, `VATLY_API_KEY` env var
