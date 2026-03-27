from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class Company:
    name: str
    address: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Company:
        return cls(name=data["name"], address=data.get("address"))


@dataclass
class VatValidationResult:
    valid: bool
    vat_number: str
    country_code: str
    company: Optional[Company]
    consultation_number: Optional[str]
    requested_at: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VatValidationResult:
        company_data = data.get("company")
        company = Company.from_dict(company_data) if company_data is not None else None
        return cls(
            valid=data["valid"],
            vat_number=data["vat_number"],
            country_code=data["country_code"],
            company=company,
            consultation_number=data.get("consultation_number"),
            requested_at=data["requested_at"],
        )


@dataclass
class ResponseMeta:
    request_id: str
    cached: Optional[bool] = None
    cached_at: Optional[str] = None
    stale: Optional[bool] = None
    source_status: Optional[str] = None
    mode: Optional[str] = None
    request_duration_ms: Optional[int] = None
    count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ResponseMeta:
        return cls(
            request_id=data["request_id"],
            cached=data.get("cached"),
            cached_at=data.get("cached_at"),
            stale=data.get("stale"),
            source_status=data.get("source_status"),
            mode=data.get("mode"),
            request_duration_ms=data.get("request_duration_ms"),
            count=data.get("count"),
        )


@dataclass
class RateLimitInfo:
    limit: Optional[int]
    remaining: Optional[int]
    reset: Optional[str]
    retry_after: Optional[float]
    burst_limit: Optional[int]
    burst_remaining: Optional[int]


@dataclass
class ValidateResponse:
    data: VatValidationResult
    meta: ResponseMeta
    rate_limit: RateLimitInfo


@dataclass
class BatchItemMeta:
    cached: Optional[bool]
    cached_at: Optional[str]
    stale: Optional[bool]
    source_status: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BatchItemMeta:
        return cls(
            cached=data.get("cached"),
            cached_at=data.get("cached_at"),
            stale=data.get("stale"),
            source_status=data.get("source_status"),
        )


@dataclass
class BatchErrorDetail:
    code: str
    message: str


@dataclass
class BatchErrorMeta:
    vat_number: str


@dataclass
class BatchResultSuccess:
    data: VatValidationResult
    meta: BatchItemMeta

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BatchResultSuccess:
        return cls(
            data=VatValidationResult.from_dict(data["data"]),
            meta=BatchItemMeta.from_dict(data["meta"]),
        )


@dataclass
class BatchResultError:
    error: BatchErrorDetail
    meta: BatchErrorMeta

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BatchResultError:
        error_data = data["error"]
        meta_data = data["meta"]
        return cls(
            error=BatchErrorDetail(code=error_data["code"], message=error_data["message"]),
            meta=BatchErrorMeta(vat_number=meta_data["vat_number"]),
        )


BatchResult = Union[BatchResultSuccess, BatchResultError]


def is_batch_success(item: BatchResult) -> bool:
    """Type guard to check if a batch result item is a success."""
    return isinstance(item, BatchResultSuccess)


@dataclass
class BatchSummary:
    total: int
    succeeded: int
    failed: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BatchSummary:
        return cls(total=data["total"], succeeded=data["succeeded"], failed=data["failed"])


@dataclass
class BatchValidateResponse:
    results: List[BatchResult]
    summary: BatchSummary
    meta: ResponseMeta
    rate_limit: RateLimitInfo


@dataclass
class OtherRate:
    rate: float
    type: str


@dataclass
class VatRate:
    country_code: str
    country_name: str
    currency: str
    standard_rate: float
    other_rates: List[OtherRate]
    updated_at: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VatRate:
        other_rates = [OtherRate(rate=r["rate"], type=r["type"]) for r in data["other_rates"]]
        return cls(
            country_code=data["country_code"],
            country_name=data["country_name"],
            currency=data["currency"],
            standard_rate=data["standard_rate"],
            other_rates=other_rates,
            updated_at=data["updated_at"],
        )


@dataclass
class ListRatesResponse:
    data: List[VatRate]
    meta: ResponseMeta
    rate_limit: RateLimitInfo


@dataclass
class GetRateResponse:
    data: VatRate
    meta: ResponseMeta
    rate_limit: RateLimitInfo
