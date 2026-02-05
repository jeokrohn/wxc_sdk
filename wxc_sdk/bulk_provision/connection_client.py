import logging
from dataclasses import dataclass
from typing import Any, Optional

from requests import Response
from tenacity import RetryCallState, Retrying, retry_if_exception, stop_after_attempt, wait_exponential_jitter

from wxc_sdk.rest import RestError, RestSession
from wxc_sdk.tokens import Tokens

log = logging.getLogger(__name__)


def _should_retry(exc: Exception) -> bool:
    if isinstance(exc, RestError):
        status = exc.response.status_code
        return status == 429 or status >= 500
    return True


def _before_sleep(retry_state: RetryCallState) -> None:
    log.warning(
        "retry",
        extra={
            "attempt_number": retry_state.attempt_number,
            "exception": str(retry_state.outcome.exception()),
        },
    )


@dataclass(frozen=True)
class ResponseData:
    response: Response
    data: Any


@dataclass
class ConnectionClient:
    base_url: str
    token: str
    timeout_seconds: int
    max_retries: int
    verify: bool
    proxy_url: Optional[str] = None
    ca_bundle: Optional[str] = None
    session: Optional[RestSession] = None

    def __post_init__(self) -> None:
        session = RestSession(
            tokens=Tokens(access_token=self.token),
            concurrent_requests=1,
            retry_429=False,
            proxy_url=self.proxy_url,
            verify=self.ca_bundle or self.verify,
        )
        session.BASE = self.base_url
        self.session = session

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        ignore_status: Optional[int] = None,
    ) -> ResponseData:
        retrying = Retrying(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential_jitter(multiplier=1, max=10),
            retry=retry_if_exception(_should_retry),
            reraise=True,
            before_sleep=_before_sleep,
        )

        def _do_request() -> ResponseData:
            response, data = self.session._request_w_response(
                method,
                url=self.session.ep(path),
                params=params,
                json=json,
                headers=headers,
                ignore_status=ignore_status,
                timeout=self.timeout_seconds,
            )
            return ResponseData(response=response, data=data)

        return retrying(_do_request)
