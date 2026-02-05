import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def _env_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    environment: str
    webex_base_url: str
    webex_token: str
    input_dir: Path
    output_dir: Path
    org_id: Optional[str]
    pipeline_version: str
    batch_size_users: int
    max_rows_users: int
    request_timeout_seconds: int
    max_retries: int
    circuit_breaker_threshold: float
    enable_safe_compensation: bool
    log_level: str
    http_proxy: Optional[str]
    https_proxy: Optional[str]
    no_proxy: Optional[str]
    ssl_verify: bool
    requests_ca_bundle: Optional[str]

    @classmethod
    def from_env(cls) -> "Config":
        environment = os.getenv("ENVIRONMENT")
        webex_base_url = os.getenv("WEBEX_BASE_URL")
        webex_token = os.getenv("WEBEX_TOKEN")
        input_dir = os.getenv("INPUT_DIR")
        output_dir = os.getenv("OUTPUT_DIR")

        assert environment, "ENVIRONMENT is required"
        assert webex_base_url, "WEBEX_BASE_URL is required"
        assert webex_token, "WEBEX_TOKEN is required"
        assert input_dir, "INPUT_DIR is required"
        assert output_dir, "OUTPUT_DIR is required"

        return cls(
            environment=environment,
            webex_base_url=webex_base_url,
            webex_token=webex_token,
            input_dir=Path(input_dir),
            output_dir=Path(output_dir),
            org_id=os.getenv("ORG_ID"),
            pipeline_version=os.getenv("PIPELINE_VERSION", "1"),
            batch_size_users=int(os.getenv("BATCH_SIZE_USERS", "500")),
            max_rows_users=int(os.getenv("MAX_ROWS_USERS", "21000")),
            request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20")),
            max_retries=int(os.getenv("MAX_RETRIES", "5")),
            circuit_breaker_threshold=float(os.getenv("CIRCUIT_BREAKER_THRESHOLD", "0.80")),
            enable_safe_compensation=_env_bool(os.getenv("ENABLE_SAFE_COMPENSATION"), False),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            http_proxy=os.getenv("HTTP_PROXY"),
            https_proxy=os.getenv("HTTPS_PROXY"),
            no_proxy=os.getenv("NO_PROXY"),
            ssl_verify=_env_bool(os.getenv("SSL_VERIFY"), True),
            requests_ca_bundle=os.getenv("REQUESTS_CA_BUNDLE"),
        )
