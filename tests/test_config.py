from __future__ import annotations

import warnings

import pytest

from vatly import Vatly, VatlyError


class TestConfigResolution:
    def test_accepts_string_api_key(self) -> None:
        client = Vatly("vtly_live_mykey")
        assert client.vat is not None
        assert client.rates is not None
        client.close()

    def test_accepts_kwarg_api_key(self) -> None:
        client = Vatly(api_key="vtly_live_mykey")
        assert client.vat is not None
        client.close()

    def test_falls_back_to_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("VATLY_API_KEY", "vtly_live_envkey")
        client = Vatly()
        assert client.vat is not None
        client.close()

    def test_raises_when_no_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("VATLY_API_KEY", raising=False)
        with pytest.raises(VatlyError, match="No API key provided"):
            Vatly()

    def test_raises_when_empty_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("VATLY_API_KEY", raising=False)
        with pytest.raises(VatlyError):
            Vatly("")

    def test_custom_base_url(self) -> None:
        client = Vatly("vtly_live_key", base_url="https://custom.api.vatly.dev")
        assert client._config.base_url == "https://custom.api.vatly.dev"
        client.close()

    def test_custom_timeout(self) -> None:
        client = Vatly("vtly_live_key", timeout=5.0)
        assert client._config.timeout == 5.0
        client.close()

    def test_default_base_url(self) -> None:
        client = Vatly("vtly_live_key")
        assert client._config.base_url == "https://api.vatly.dev"
        client.close()

    def test_default_timeout(self) -> None:
        client = Vatly("vtly_live_key")
        assert client._config.timeout == 30.0
        client.close()

    def test_warns_on_invalid_key_prefix(self) -> None:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            client = Vatly("invalid_prefix_key")
            assert len(w) == 1
            assert "vtly_live_" in str(w[0].message)
            client.close()

    def test_no_warning_for_live_key(self) -> None:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            client = Vatly("vtly_live_key")
            assert len(w) == 0
            client.close()

    def test_no_warning_for_test_key(self) -> None:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            client = Vatly("vtly_test_key")
            assert len(w) == 0
            client.close()

    def test_env_var_used_when_arg_is_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("VATLY_API_KEY", "vtly_live_from_env")
        client = Vatly()
        assert client._config.api_key == "vtly_live_from_env"
        client.close()

    def test_explicit_key_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("VATLY_API_KEY", "vtly_live_from_env")
        client = Vatly("vtly_live_explicit")
        assert client._config.api_key == "vtly_live_explicit"
        client.close()
