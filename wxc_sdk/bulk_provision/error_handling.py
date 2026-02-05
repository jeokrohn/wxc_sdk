import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from requests import HTTPError

from wxc_sdk.rest import RestError

log = logging.getLogger(__name__)


class ReasonCode(str, Enum):
    invalid_input_schema = "invalid_input_schema"
    duplicate_key = "duplicate_key"
    out_of_scope = "out_of_scope"
    auth_invalid = "auth_invalid"
    permission_denied = "permission_denied"
    non_retryable_external = "non_retryable_external"
    retry_exhausted = "retry_exhausted"
    invalid_response_schema = "invalid_response_schema"
    ambiguous_match = "ambiguous_match"
    half_applied = "half_applied"


class ErrorClass(str, Enum):
    retryable_external = "retryable_external"
    non_retryable_external = "non_retryable_external"
    assertion_failure = "assertion_failure"


@dataclass(frozen=True)
class ErrorInfo:
    reason_code: ReasonCode
    reason_message: str
    http_status: Optional[int] = None
    error_class: Optional[ErrorClass] = None


def classify_http_status(status_code: int) -> ErrorInfo:
    if status_code == 401:
        return ErrorInfo(
            reason_code=ReasonCode.auth_invalid,
            reason_message="Unauthorized",
            http_status=status_code,
            error_class=ErrorClass.non_retryable_external,
        )
    if status_code == 403:
        return ErrorInfo(
            reason_code=ReasonCode.permission_denied,
            reason_message="Forbidden",
            http_status=status_code,
            error_class=ErrorClass.non_retryable_external,
        )
    if 400 <= status_code < 500:
        return ErrorInfo(
            reason_code=ReasonCode.non_retryable_external,
            reason_message=f"HTTP {status_code}",
            http_status=status_code,
            error_class=ErrorClass.non_retryable_external,
        )
    return ErrorInfo(
        reason_code=ReasonCode.retry_exhausted,
        reason_message=f"HTTP {status_code}",
        http_status=status_code,
        error_class=ErrorClass.retryable_external,
    )


def map_exception(exc: Exception) -> ErrorInfo:
    if isinstance(exc, RestError):
        status_code = exc.response.status_code
        info = classify_http_status(status_code)
        return ErrorInfo(
            reason_code=info.reason_code,
            reason_message=str(exc),
            http_status=status_code,
            error_class=info.error_class,
        )
    if isinstance(exc, HTTPError):
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code is not None:
            return classify_http_status(status_code)
    return ErrorInfo(
        reason_code=ReasonCode.non_retryable_external,
        reason_message=str(exc),
    )
