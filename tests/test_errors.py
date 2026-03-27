from __future__ import annotations

from vatly import (
    AuthenticationError,
    RateLimitError,
    UpstreamError,
    ValidationError,
    VatlyError,
)


class TestVatlyError:
    def test_has_correct_properties(self) -> None:
        err = VatlyError(
            "test message",
            code="test_code",
            status_code=400,
            request_id="req_123",
            docs_url="https://docs.vatly.dev",
        )
        assert err.message == "test message"
        assert err.code == "test_code"
        assert err.status_code == 400
        assert err.request_id == "req_123"
        assert err.docs_url == "https://docs.vatly.dev"

    def test_str_returns_message(self) -> None:
        err = VatlyError("human readable message")
        assert str(err) == "human readable message"

    def test_is_instance_of_exception(self) -> None:
        err = VatlyError("msg")
        assert isinstance(err, Exception)

    def test_request_id_defaults_to_none(self) -> None:
        err = VatlyError("msg")
        assert err.request_id is None

    def test_docs_url_defaults_to_empty(self) -> None:
        err = VatlyError("msg")
        assert err.docs_url == ""

    def test_details_defaults_to_none(self) -> None:
        err = VatlyError("msg")
        assert err.details is None

    def test_details_carries_array(self) -> None:
        details = [{"field": "vat_number", "message": "is required"}]
        err = VatlyError("msg", details=details)
        assert err.details == [{"field": "vat_number", "message": "is required"}]


class TestErrorHierarchy:
    def test_authentication_error_isinstance(self) -> None:
        err = AuthenticationError("msg", code="unauthorized", status_code=401)
        assert isinstance(err, VatlyError)
        assert isinstance(err, AuthenticationError)

    def test_validation_error_isinstance(self) -> None:
        err = ValidationError("msg", code="invalid_vat_format", status_code=422)
        assert isinstance(err, VatlyError)
        assert isinstance(err, ValidationError)

    def test_rate_limit_error_isinstance(self) -> None:
        err = RateLimitError("msg", code="rate_limit_exceeded", status_code=429, retry_after=30.0)
        assert isinstance(err, VatlyError)
        assert isinstance(err, RateLimitError)
        assert err.retry_after == 30.0

    def test_upstream_error_isinstance(self) -> None:
        err = UpstreamError("msg", code="upstream_unavailable", status_code=503, retry_after=60.0)
        assert isinstance(err, VatlyError)
        assert isinstance(err, UpstreamError)
        assert err.retry_after == 60.0

    def test_authentication_error_has_no_details(self) -> None:
        err = AuthenticationError("msg", code="unauthorized", status_code=401)
        assert err.details is None

    def test_rate_limit_error_retry_after_none(self) -> None:
        err = RateLimitError("msg", code="rate_limit_exceeded", status_code=429)
        assert err.retry_after is None

    def test_upstream_error_retry_after_none(self) -> None:
        err = UpstreamError("msg", code="upstream_unavailable", status_code=503)
        assert err.retry_after is None
