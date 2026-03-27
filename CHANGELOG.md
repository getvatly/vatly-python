# Changelog

## 0.1.0

Initial release.

- Sync client (`Vatly`) and async client (`AsyncVatly`)
- `vatly.vat.validate()` and `vatly.vat.validate_batch()`
- `vatly.rates.list()` and `vatly.rates.get()`
- Typed exception hierarchy: `VatlyError`, `AuthenticationError`, `ValidationError`, `RateLimitError`, `UpstreamError`
- Full type annotations with `py.typed` marker
- API key resolution: explicit arg, `VATLY_API_KEY` env var
