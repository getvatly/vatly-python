from __future__ import annotations

from vatly import AsyncVatly, Vatly
from vatly._async_resources.rates import AsyncRatesResource
from vatly._async_resources.vat import AsyncVatResource
from vatly._resources.rates import RatesResource
from vatly._resources.vat import VatResource


class TestSyncClient:
    def test_has_vat_resource(self) -> None:
        client = Vatly("vtly_live_key")
        assert isinstance(client.vat, VatResource)
        client.close()

    def test_has_rates_resource(self) -> None:
        client = Vatly("vtly_live_key")
        assert isinstance(client.rates, RatesResource)
        client.close()

    def test_context_manager(self) -> None:
        with Vatly("vtly_live_key") as client:
            assert client.vat is not None
            assert client.rates is not None

    def test_close(self) -> None:
        client = Vatly("vtly_live_key")
        client.close()


class TestAsyncClient:
    def test_has_vat_resource(self) -> None:
        client = AsyncVatly("vtly_live_key")
        assert isinstance(client.vat, AsyncVatResource)

    def test_has_rates_resource(self) -> None:
        client = AsyncVatly("vtly_live_key")
        assert isinstance(client.rates, AsyncRatesResource)

    async def test_async_context_manager(self) -> None:
        async with AsyncVatly("vtly_live_key") as client:
            assert client.vat is not None
            assert client.rates is not None

    async def test_close(self) -> None:
        client = AsyncVatly("vtly_live_key")
        await client.close()
